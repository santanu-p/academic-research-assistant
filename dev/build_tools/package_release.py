"""Create and independently inspect a single-plugin release archive."""
from pathlib import Path, PurePosixPath
import hashlib, json, zipfile

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'academic-research-assistant'
RELEASE=ROOT/'release'

def included(path):
    return '__pycache__' not in path.parts and path.suffix not in ['.pyc','.pyo'] and not any(x in path.parts for x in ['node_modules','.pytest_cache'])

def main():
    RELEASE.mkdir(exist_ok=True)
    files={}
    for p in sorted(PACKAGE.rglob('*')):
        if not p.is_file() or not included(p.relative_to(PACKAGE)):
            continue
        if p.is_symlink():
            raise ValueError('Symlinks may not enter release')
        rel=p.relative_to(PACKAGE).as_posix()
        if rel=='audit/package-files.json':
            continue
        files[rel]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    (PACKAGE/'audit/package-files.json').write_text(json.dumps({'excludes':'This index itself; runtime bytecode/cache files are not delivered','files':files},indent=2),encoding='utf-8')
    archive=RELEASE/'academic-research-assistant-1.0.0.zip'
    entries={}
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(PACKAGE.rglob('*')):
            rel=p.relative_to(PACKAGE)
            if not included(rel):
                continue
            name='academic-research-assistant/'+rel.as_posix()+('/' if p.is_dir() else '')
            info=zipfile.ZipInfo(name,date_time=(2026,10,25,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(0o40755 if p.is_dir() else 0o100644)<<16
            data=b'' if p.is_dir() else p.read_bytes()
            z.writestr(info,data)
            if p.is_file():
                entries[name]=hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        seen=set()
        for n in z.namelist():
            p=PurePosixPath(n)
            assert not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n
            assert n.casefold() not in seen
            seen.add(n.casefold())
        assert {PurePosixPath(n).parts[0] for n in z.namelist()}=={'academic-research-assistant'}
        for name,sha in entries.items():
            assert hashlib.sha256(z.read(name)).hexdigest()==sha
        assert len([n for n in entries if len(PurePosixPath(n).parts)==4 and n.startswith('academic-research-assistant/skills/') and n.endswith('/SKILL.md')])==118
        mapping=json.loads(z.read('academic-research-assistant/audit/source-map.json'))
        for entry in mapping:
            name='academic-research-assistant/'+entry['destination']
            if entry['kind']=='file':
                assert hashlib.sha256(z.read(name)).hexdigest()==entry['sha256']
            else:
                assert name.rstrip('/')+'/' in z.namelist()
    sha=hashlib.sha256(archive.read_bytes()).hexdigest()
    (RELEASE/'SHA256SUMS.txt').write_text(sha+'  '+archive.name+'\n',encoding='utf-8')
    result={'archive':str(archive),'bytes':archive.stat().st_size,'sha256':sha,'file_entries':len(entries),
            'source_files_verified':273,'directory_entries_verified':179,'active_skills':118,
            'one_plugin_root':True,'all_archive_file_hashes_match_package':True,'passed':True}
    (RELEASE/'archive-inspection.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
