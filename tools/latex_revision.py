"""Build clean and marked LaTeX PDFs using separately installed tools.

The updated project is copied to a temporary work directory. The original
inputs are read only, and the requested output directory must be new and
outside both input project directories. Requires latexdiff and Tectonic.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile

REPARSE_POINT = getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400)


def command(value: str, label: str) -> list[str]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f'{label} must be a JSON array of command arguments') from exc
    if not isinstance(parsed, list) or not parsed or any(
        not isinstance(item, str) or not item or '\0' in item for item in parsed
    ):
        raise ValueError(f'{label} must be a nonempty JSON array of nonempty strings')
    if not shutil.which(parsed[0]):
        raise ValueError(f'{label} executable was not found: {parsed[0]}')
    return parsed


def inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def check_project_tree(root: Path) -> None:
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [item for item in dirs if item != '.git']
        for item in (*dirs, *files):
            candidate = Path(current) / item
            info = candidate.lstat()
            if candidate.is_symlink() or getattr(info, 'st_file_attributes', 0) & REPARSE_POINT:
                raise ValueError(f'Project links are not supported: {candidate}')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: list[str], cwd: Path, log: Path, timeout: int, output=None) -> None:
    try:
        completed = subprocess.run(args, cwd=cwd, stdout=output or subprocess.PIPE,
                                   stderr=subprocess.PIPE, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        log.write_bytes((exc.stdout or b'') + (exc.stderr or b''))
        raise ValueError(f'{log.stem} timed out after {timeout} seconds') from exc
    except OSError as exc:
        raise ValueError(f'Could not run {log.stem}: {exc}') from exc
    message = (completed.stdout or b'') + completed.stderr
    log.write_bytes(message)
    if completed.returncode:
        raise ValueError(f'{log.stem} failed with exit code {completed.returncode}; see {log.name}')


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path, help='Earlier main LaTeX file')
    parser.add_argument('after', type=Path, help='Updated main LaTeX file')
    parser.add_argument('--out', type=Path, required=True, help='New output directory outside the input projects')
    parser.add_argument('--project-root', type=Path, help='Updated project root; defaults to the updated file directory')
    parser.add_argument('--latexdiff-command', default='["latexdiff"]', help='JSON command array for latexdiff')
    parser.add_argument('--tectonic-command', default='["tectonic"]', help='JSON command array for Tectonic')
    parser.add_argument('--timeout', type=int, default=180, help='Maximum seconds per external command')
    args = parser.parse_args(argv)
    try:
        old = args.before.resolve(strict=True)
        new = args.after.resolve(strict=True)
        root = (args.project_root or new.parent).resolve(strict=True)
        if not old.is_file() or not new.is_file() or old.suffix.lower() != '.tex' or new.suffix.lower() != '.tex':
            raise ValueError('Both inputs must be existing .tex files')
        if not root.is_dir() or root == root.parent or not inside(new, root):
            raise ValueError('The updated file must be inside a specific project directory')
        if args.timeout < 1 or args.timeout > 3600:
            raise ValueError('Timeout must be between 1 and 3600 seconds')
        out = args.out.parent.resolve(strict=True) / args.out.name
        if out.exists() or out.is_symlink():
            raise ValueError('Output directory already exists')
        if inside(out, root) or inside(out, old.parent):
            raise ValueError('Output directory must be outside the input projects')
        diff = command(args.latexdiff_command, 'latexdiff command')
        compiler = command(args.tectonic_command, 'Tectonic command')
        check_project_tree(root)
        old_sha, new_sha = digest(old), digest(new)
        out.mkdir()
        with tempfile.TemporaryDirectory(prefix='.ara-tex-', dir=out) as temporary:
            work = Path(temporary).resolve(strict=True)
            if not inside(work, out.resolve(strict=True)) or work == out.resolve(strict=True):
                raise ValueError('Temporary directory is outside the requested output directory')
            snapshot = work / 'project'
            shutil.copytree(root, snapshot, ignore=shutil.ignore_patterns('.git'))
            copied_main = snapshot / new.relative_to(root)
            with tempfile.NamedTemporaryFile(prefix='ara-marked-', suffix='.tex',
                                             dir=copied_main.parent, delete=False) as marked:
                marked_source = Path(marked.name)
                run([*diff, '--flatten', str(old), str(copied_main)], copied_main.parent,
                    out / 'latexdiff.log', args.timeout, output=marked)
            build = work / 'build'
            build.mkdir()
            for source, log, tex_log in ((copied_main, 'clean.log', 'clean-tex.log'),
                                         (marked_source, 'marked.log', 'marked-tex.log')):
                try:
                    run([*compiler, '--untrusted', '--keep-logs', '--outdir', str(build), str(source)],
                        copied_main.parent, out / log, args.timeout)
                finally:
                    generated_log = build / (source.stem + '.log')
                    if generated_log.is_file():
                        shutil.copyfile(generated_log, out / tex_log)
                pdf = build / (source.stem + '.pdf')
                if not pdf.is_file() or not pdf.read_bytes().startswith(b'%PDF-'):
                    raise ValueError(f'{log} completed without producing a PDF')
            if digest(old) != old_sha or digest(new) != new_sha:
                raise ValueError('An input file changed during the build; outputs were not published')
            files = ((build / (copied_main.stem + '.pdf'), out / 'clean.pdf'),
                     (build / (marked_source.stem + '.pdf'), out / 'marked.pdf'),
                     (marked_source, out / 'marked.tex'))
            for source, target in files:
                with source.open('rb') as src, target.open('xb') as dst:
                    shutil.copyfileobj(src, dst)
            report = {'before_sha256': old_sha, 'after_sha256': new_sha,
                      'clean_pdf_sha256': digest(out / 'clean.pdf'),
                      'marked_pdf_sha256': digest(out / 'marked.pdf'),
                      'comparison': 'latexdiff --flatten', 'compiler': 'Tectonic',
                      'scope': ('Input hashes cover the main files only. The marked build uses updated project '
                                'resources; changes to images or bibliography files are not compared. '
                                'Inspect both PDFs and the logs; hashes do not validate scientific content.')}
            (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print(f'Created clean.pdf, marked.pdf and marked.tex in {out}. Inspect both PDFs and the logs.')
        return 0
    except (OSError, ValueError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
