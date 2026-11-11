"""Include authored integration sources and an isolated reconstruction entrypoint."""
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'academic-research-assistant'

def snapshot():
    integration=ROOT/'integration'
    for relative in ['README.md','THIRD_PARTY_NOTICES.md','requirements-optional.txt',
                     'docs','server','workflows','agents','skills/research-assistant','audit']:
        source=OUT/relative
        dest=integration/relative
        if source.is_dir():
            shutil.copytree(source,dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,dest)
    dev=OUT/'dev'
    for name in ['build_tools','tests','docs','integration']:
        shutil.copytree(ROOT/name,dev/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    shutil.copy2(ROOT/'requirements-dev.txt',dev/'requirements-dev.txt')
    shutil.copytree(ROOT/'work/schemas',dev/'schemas',dirs_exist_ok=True)
    shutil.copy2(ROOT/'build_tools/reconstruct.py',dev/'reconstruct.py')
    print('Authored sources, tests, requirements and official schemas included under dev/')

if __name__=='__main__':
    snapshot()
