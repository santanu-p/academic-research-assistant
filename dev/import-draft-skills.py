"""Import independently authored skill drafts without replacing existing skills."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
source = Path(sys.argv[1]).resolve(strict=True)
renames = {'methodology-design': 'independent-methodology-design',
           'research-planning': 'independent-research-planning'}
out = ROOT / 'docs' / 'independent-skill-import.json'
records = json.loads(out.read_text(encoding='utf-8')) if out.exists() else []
existing = {item['source_name']: item for item in records}
for folder in sorted(path for path in source.iterdir() if path.is_dir()):
    target_name = renames.get(folder.name, folder.name)
    target = ROOT / 'skills' / target_name
    source_entry = folder / 'SKILL.md'
    if folder.name in existing:
        item = existing[folder.name]
        if (item['target_name'] != target_name or
                hashlib.sha256(source_entry.read_bytes()).hexdigest() != item['source_sha256'] or
                hashlib.sha256((target / 'SKILL.md').read_bytes()).hexdigest() != item['target_sha256']):
            raise ValueError(f'Existing import differs: {folder.name}')
        continue
    if target.exists():
        raise FileExistsError(f'Refusing to overwrite {target}')
    shutil.copytree(folder, target)
    entry = target / 'SKILL.md'
    if target_name != folder.name:
        text = entry.read_text(encoding='utf-8')
        old = 'name: ' + folder.name + '\n'
        if text.count(old) != 1:
            raise ValueError(f'Cannot safely rename {folder.name}')
        entry.write_text(text.replace(old, 'name: ' + target_name + '\n', 1), encoding='utf-8', newline='\n')
    records.append({'source_name': folder.name, 'target_name': target_name,
                    'source_sha256': hashlib.sha256(source_entry.read_bytes()).hexdigest(),
                    'target_sha256': hashlib.sha256(entry.read_bytes()).hexdigest(),
                    'note': 'Frontmatter name changed to avoid a collision.' if target_name != folder.name else 'Copied unchanged.'})
out.write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
print(f'Accounted for {len(records)} independently authored skills; mapping: {out}')
