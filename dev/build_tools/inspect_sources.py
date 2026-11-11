"""Freeze, inspect, and safely expand the complete supplied collection."""
from pathlib import Path, PurePosixPath
import ast, csv, hashlib, io, json, re, shutil, stat, zipfile, sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'work'
ORIGINALS = BUILD / 'originals'
EXPANDED = BUILD / 'expanded'
INPUTS = ['latexdocumentmaker', 'research-writing-guardrails', 'researchevidencefinder',
          'scholarresearch', 'scientific-visual-table-style', 'academic-humanizer-main.zip',
          'academic-pptx-skill-main.zip', 'ARMS-main.zip', 'humanizer-main.zip']

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    BUILD.mkdir(exist_ok=True)
    original_entries = []
    for name in INPUTS:
        src = ROOT / name
        for p in ([src] if src.is_file() else [src, *sorted(src.rglob('*'))]):
            rel = p.relative_to(ROOT)
            dst = ORIGINALS / rel
            if p.is_symlink():
                raise ValueError(f'Symlink requires explicit handling: {p}')
            if p.is_dir():
                dst.mkdir(parents=True, exist_ok=True)
                original_entries.append({'source': rel.as_posix(), 'kind': 'directory'})
            else:
                data = p.read_bytes()
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists() and dst.read_bytes() != data:
                    raise ValueError(f'Source changed since snapshot: {p}')
                dst.write_bytes(data)
                original_entries.append({'source': rel.as_posix(), 'kind': 'file',
                                         'bytes': len(data), 'sha256': digest(data)})
    expanded_entries = []
    for archive in sorted(ORIGINALS.glob('*.zip')):
        with zipfile.ZipFile(archive) as z:
            if z.testzip():
                raise ValueError(f'Invalid ZIP: {archive}')
            seen = set()
            for i in z.infolist():
                rel = PurePosixPath(i.filename)
                if rel.is_absolute() or '..' in rel.parts or '\\' in i.filename or ':' in i.filename:
                    raise ValueError(f'Unsafe ZIP entry: {i.filename}')
                if stat.S_ISLNK(i.external_attr >> 16):
                    raise ValueError(f'ZIP symlink: {i.filename}')
                if i.filename.casefold() in seen:
                    raise ValueError(f'ZIP collision: {i.filename}')
                seen.add(i.filename.casefold())
                dst = EXPANDED / rel
                entry = {'archive': archive.name, 'source': i.filename,
                         'kind': 'directory' if i.is_dir() else 'file'}
                if i.is_dir():
                    dst.mkdir(parents=True, exist_ok=True)
                else:
                    data = z.read(i)
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_bytes(data)
                    entry.update(bytes=len(data), sha256=digest(data))
                expanded_entries.append(entry)
    inspection = []
    for base in [ORIGINALS, EXPANDED]:
        for p in sorted(base.rglob('*')):
            if not p.is_file():
                continue
            data = p.read_bytes()
            row = {'tree': base.name, 'path': p.relative_to(base).as_posix(),
                   'bytes': len(data), 'sha256': digest(data)}
            try:
                s = data.decode('utf-8-sig')
                if '\x00' in s:
                    raise UnicodeError('NUL')
                row.update(type='text', lines=len(s.splitlines()),
                           headings=re.findall(r'^#{1,6} .+$', s, re.M),
                           urls=sorted(set(re.findall(r'https?://[^\s<>\)\]"`]+', s))),
                           references=re.findall(r'\[[^\]]*\]\(([^)]+)\)', s),
                           dependencies=[l.strip() for l in s.splitlines() if re.search(
                               r'(?i)require|depend|\bmcp\b|pip install|npm |npx |python|codex |claude |affiliate|license|api.key|token|credential', l)])
                if p.name == 'SKILL.md':
                    if not s.startswith('---'):
                        row['frontmatter_error'] = 'missing frontmatter'
                    else:
                        try:
                            row['frontmatter'] = yaml.safe_load(s.split('---', 2)[1])
                        except yaml.YAMLError as e:
                            row['frontmatter_error'] = str(e)
                if p.suffix == '.json':
                    try:
                        row['json'] = json.loads(s)
                    except ValueError as e:
                        row['parse_error'] = str(e)
                if p.suffix in ['.yaml', '.yml']:
                    try:
                        row['yaml'] = yaml.safe_load(s)
                    except yaml.YAMLError as e:
                        row['parse_error'] = str(e)
                if p.suffix == '.py':
                    try:
                        tree = ast.parse(s)
                        row['imports'] = sorted(set(n.module or '' for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)) |
                                                {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names})
                    except SyntaxError as e:
                        row['parse_error'] = str(e)
                if p.suffix == '.csv':
                    rows = list(csv.reader(io.StringIO(s)))
                    row.update(csv_header=rows[0] if rows else [], csv_rows=max(0, len(rows)-1))
            except UnicodeError:
                row['type'] = 'binary'
                if p.suffix == '.png':
                    from PIL import Image
                    with Image.open(p) as im:
                        row.update(image_size=list(im.size), image_mode=im.mode)
                        im.verify()
                elif p.suffix == '.pdf':
                    from pypdf import PdfReader
                    pdf = PdfReader(p)
                    row.update(pdf_pages=len(pdf.pages), pdf_text='\n'.join(pg.extract_text() or '' for pg in pdf.pages))
                elif p.suffix == '.zip':
                    row['zip_members'] = zipfile.ZipFile(p).namelist()
            inspection.append(row)
    for name, value in [('original-inventory.json', original_entries), ('archive-inventory.json', expanded_entries),
                        ('inspection.json', inspection)]:
        (BUILD / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    skills = [x for x in inspection if x['path'].endswith('SKILL.md')]
    print(json.dumps({'original_files': sum(x['kind']=='file' for x in original_entries),
                      'original_directories': sum(x['kind']=='directory' for x in original_entries),
                      'archive_files': sum(x['kind']=='file' for x in expanded_entries),
                      'skills': len(skills), 'inspection_records': len(inspection)}, indent=2))
    if '--verbose' in sys.argv:
        for s in skills:
            fm = s.get('frontmatter', {})
            print(s['tree']+'/'+s['path'], json.dumps(fm, ensure_ascii=False))
    print('PARSE ERRORS', [(x['path'],x.get('parse_error') or x.get('frontmatter_error')) for x in inspection if x.get('parse_error') or x.get('frontmatter_error')])

if __name__ == '__main__':
    main()
