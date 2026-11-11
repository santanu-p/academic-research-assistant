"""Reconstruct a fresh authoring workspace from a distributed plugin.

Run the copy at plugin/dev/reconstruct.py --out <new-empty-workspace>.
Requires requirements-dev.txt; optional scientific dependencies enable more tests.
"""
from pathlib import Path
import argparse, shutil, subprocess, sys

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    dev=Path(__file__).resolve().parent
    package=dev.parent
    if not (package/'resources/originals').is_dir() or not (dev/'integration').is_dir():
        parser.error('Run the distributed copy at <plugin>/dev/reconstruct.py')
    destination=args.out.resolve()
    if destination.exists() and any(destination.iterdir()):
        parser.error('Output must be new or empty; existing work is never overwritten')
    if destination==package or destination.is_relative_to(package):
        parser.error('Output must be outside the installed plugin')
    destination.mkdir(parents=True,exist_ok=True)
    for name in ['build_tools','tests','docs','integration']:
        shutil.copytree(dev/name,destination/name)
    shutil.copy2(dev/'requirements-dev.txt',destination/'requirements-dev.txt')
    for source in (package/'resources/originals').iterdir():
        target=destination/source.name
        shutil.copytree(source,target) if source.is_dir() else shutil.copy2(source,target)
    shutil.copytree(dev/'schemas',destination/'work/schemas')
    for script in ['inspect_sources.py','build_plugin.py','validate_package.py']:
        subprocess.run([sys.executable,'-X','utf8','-B',str(destination/'build_tools'/script)],cwd=destination,check=True)
    print('Reconstructed and validated:',destination/'academic-research-assistant')

if __name__=='__main__':
    main()
