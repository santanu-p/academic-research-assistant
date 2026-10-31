"""Small external-command fixtures for the LaTeX revision CLI tests."""
from pathlib import Path
import sys
import time

mode, *args = sys.argv[1:]
if mode == 'diff':
    if args[0] != '--flatten' or len(args) != 3:
        raise SystemExit('expected flattened comparison of two files')
    old, new = (Path(value) for value in args[1:])
    old_text, new_text = old.read_text(encoding='utf-8'), new.read_text(encoding='utf-8')
    if 'FAIL-DIFF' in old_text:
        raise SystemExit('synthetic comparison failure')
    if 'SLEEP-DIFF' in old_text:
        print('synthetic comparison is waiting', file=sys.stderr, flush=True)
        time.sleep(3)
    print('% comparison of old and updated sources')
    print('% removed: ' + old_text.strip())
    print('% added: ' + new_text.strip())
    print(new_text)
elif mode == 'tectonic':
    if args[:3] != ['--untrusted', '--keep-logs', '--outdir'] or len(args) != 5:
        raise SystemExit('expected restricted compiler arguments')
    out, source = Path(args[3]), Path(args[4])
    text = source.read_text(encoding='utf-8')
    if 'FAIL-COMPILE' in text:
        raise SystemExit('synthetic compiler failure')
    if 'FAIL-MARKED' in text and source.name.startswith('ara-marked-'):
        raise SystemExit('synthetic marked build failure')
    if not (source.parent / 'figure.dat').is_file() or not (source.parent / 'chapter.tex').is_file():
        raise SystemExit('project resources were not copied alongside the manuscript')
    if 'USE-PARENT-ASSET' in text and not (source.parent.parent / 'shared' / 'shared.tex').is_file():
        raise SystemExit('parent project resource was not copied')
    out.mkdir(parents=True, exist_ok=True)
    (out / (source.stem + '.pdf')).write_bytes(b'%PDF-1.4\nfixture:' + source.name.encode() + b'\n%%EOF\n')
    (out / (source.stem + '.log')).write_text('synthetic compiler log\n', encoding='utf-8')
else:
    raise SystemExit('unknown fixture mode')
