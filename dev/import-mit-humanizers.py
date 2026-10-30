"""Preserve the supplied MIT Humanizer sources and expose their complete methods."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
sources = Path(sys.argv[1]).resolve(strict=True)
descriptions = {
    'humanizer': 'Edit general prose for a natural author voice while preserving the facts and intended meaning.',
    'academic-humanizer': 'Edit academic and proposal prose for author voice while preserving evidence, citations, uncertainty and technical meaning.',
}
records = []
for name, description in descriptions.items():
    source = sources / (name + '-main')
    archived = ROOT / 'resources' / 'upstream' / (name + '-main')
    skill = ROOT / 'skills' / name
    if archived.exists() or skill.exists():
        raise FileExistsError(f'Refusing to replace existing material for {name}')
    for item in sorted(path for path in source.rglob('*') if path.is_file()):
        rel = item.relative_to(source)
        target_rel = Path('gitignore.original.txt') if rel.as_posix() == '.gitignore' else rel
        target = archived / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(item, target)
        records.append({'source': (Path(name + '-main') / rel).as_posix(),
                        'destination': target.relative_to(ROOT).as_posix(),
                        'sha256': hashlib.sha256(item.read_bytes()).hexdigest()})
    skill.mkdir(parents=True)
    shutil.copyfile(source / 'LICENSE', skill / 'LICENSE')
    original = (source / 'SKILL.md').read_bytes()
    match = re.match(rb'\A---\r?\n.*?\r?\n---\r?\n', original, re.S)
    if not match:
        raise ValueError(f'Cannot parse original frontmatter for {name}')
    header = ('---\nname: ' + name + '\ndescription: ' + json.dumps(description) + '\n---\n\n').encode('utf-8')
    (skill / 'SKILL.md').write_bytes(header + original[match.end():])
out = ROOT / 'docs' / 'humanizer-source-map.json'
out.write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
print(f'Preserved {len(records)} upstream files; adapted only active frontmatter.')
