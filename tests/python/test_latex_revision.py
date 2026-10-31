"""Test the revision CLI's file-preservation and external-tool boundaries."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / 'tools' / 'latex_revision.py'
FIXTURE = ROOT / 'tests' / 'fixtures' / 'latex_revision_tools.py'
SCRATCH = ROOT / 'tests' / '.latex-revision-tmp'


class LatexRevisionTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.base = Path(self.temp.name)
        self.old = self.base / 'old project' / 'main.tex'
        self.new = self.base / 'new project' / 'main.tex'
        self.old.parent.mkdir()
        self.new.parent.mkdir()
        self.old.write_text('Old manuscript.\n', encoding='utf-8')
        self.new.write_text('Updated manuscript.\n', encoding='utf-8')
        (self.new.parent / 'chapter.tex').write_text('Included section.\n', encoding='utf-8')
        (self.new.parent / 'figure.dat').write_bytes(b'synthetic figure')
        self.out = self.base / 'deliverables'

    def tearDown(self):
        self.temp.cleanup()
        try:
            SCRATCH.rmdir()
        except OSError:
            pass

    def run_tool(self, output=None, extra=()):
        diff = json.dumps([sys.executable, '-B', str(FIXTURE), 'diff'])
        tex = json.dumps([sys.executable, '-B', str(FIXTURE), 'tectonic'])
        return subprocess.run([sys.executable, '-B', str(TOOL), str(self.old), str(self.new),
                               '--out', str(output or self.out), '--latexdiff-command', diff,
                               '--tectonic-command', tex, *extra], capture_output=True, text=True,
                              encoding='utf-8', timeout=30)

    def test_builds_both_outputs_without_changing_source_projects(self):
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.out / 'clean.pdf').read_bytes().startswith(b'%PDF-'))
        self.assertTrue((self.out / 'marked.pdf').read_bytes().startswith(b'%PDF-'))
        comparison = (self.out / 'marked.tex').read_text(encoding='utf-8')
        self.assertIn('Old manuscript.', comparison)
        self.assertIn('Updated manuscript.', comparison)
        for name in ('clean-tex.log', 'marked-tex.log'):
            self.assertTrue((self.out / name).is_file(), name)
            self.assertIn('synthetic compiler log', (self.out / name).read_text(encoding='utf-8'))
        self.assertEqual(self.old.read_text(encoding='utf-8'), 'Old manuscript.\n')
        self.assertEqual(self.new.read_text(encoding='utf-8'), 'Updated manuscript.\n')
        self.assertEqual((self.new.parent / 'figure.dat').read_bytes(), b'synthetic figure')

    def test_existing_output_is_not_modified(self):
        self.out.mkdir()
        sentinel = self.out / 'clean.pdf'
        sentinel.write_bytes(b'existing data')
        result = self.run_tool()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(sentinel.read_bytes(), b'existing data')

    def test_failed_comparison_does_not_publish_pdfs(self):
        self.old.write_text('FAIL-DIFF\n', encoding='utf-8')
        result = self.run_tool()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.out / 'clean.pdf').exists())
        self.assertFalse((self.out / 'marked.pdf').exists())
        self.assertEqual(self.new.read_text(encoding='utf-8'), 'Updated manuscript.\n')

    def test_failed_marked_build_keeps_logs_but_publishes_no_pdfs(self):
        self.new.write_text('FAIL-MARKED\n', encoding='utf-8')
        result = self.run_tool()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.out / 'clean.pdf').exists())
        self.assertFalse((self.out / 'marked.pdf').exists())
        self.assertIn('synthetic marked build failure', (self.out / 'marked.log').read_text(encoding='utf-8'))

    def test_timeout_keeps_diagnostics_and_publishes_no_pdfs(self):
        self.old.write_text('SLEEP-DIFF\n', encoding='utf-8')
        result = self.run_tool(extra=('--timeout', '1'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('timed out', result.stderr)
        self.assertTrue((self.out / 'latexdiff.log').is_file())
        self.assertIn('synthetic comparison is waiting', (self.out / 'latexdiff.log').read_text(encoding='utf-8'))
        self.assertFalse((self.out / 'clean.pdf').exists())

    def test_project_root_includes_resources_above_main_file(self):
        root = self.new.parent
        paper, shared = root / 'paper', root / 'shared'
        paper.mkdir()
        shared.mkdir()
        self.new = paper / 'main.tex'
        self.new.write_text('USE-PARENT-ASSET\n', encoding='utf-8')
        (paper / 'chapter.tex').write_text('Included material.\n', encoding='utf-8')
        (paper / 'figure.dat').write_bytes(b'figure')
        (shared / 'shared.tex').write_text('Shared material.\n', encoding='utf-8')
        result = self.run_tool(extra=('--project-root', str(root)))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.out / 'marked.pdf').is_file())
        self.assertEqual((shared / 'shared.tex').read_text(encoding='utf-8'), 'Shared material.\n')

    def test_linked_project_resource_is_rejected_before_output(self):
        link = self.new.parent / 'linked.tex'
        try:
            link.symlink_to(self.old)
        except OSError as exc:
            self.skipTest(f'Creating symlinks is unavailable: {exc}')
        result = self.run_tool()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.out.exists())
        self.assertEqual(self.old.read_text(encoding='utf-8'), 'Old manuscript.\n')

    def test_output_inside_input_project_is_rejected(self):
        output = self.new.parent / 'deliverables'
        result = self.run_tool(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
