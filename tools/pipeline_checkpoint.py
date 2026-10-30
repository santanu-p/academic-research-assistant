"""Check a local research workflow checkpoint without executing its steps.

The report evaluates recorded states, declared dependencies and file hashes.
Recorded checks are assertions by the author, not independent validation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

MAX_CHECKPOINT_BYTES = 1_000_000
MAX_ARTIFACT_BYTES = 256 * 1024 * 1024
STATES = {'pending', 'in_progress', 'completed', 'failed', 'blocked'}


def evaluate(data, root):
    if not isinstance(data, dict) or not isinstance(data.get('phases'), list) or not 1 <= len(data['phases']) <= 500:
        raise ValueError('checkpoint must contain 1 to 500 phases')
    phases = data['phases']
    by_id = {}
    for phase in phases:
        if not isinstance(phase, dict):
            raise ValueError('each phase must be an object')
        name, state = phase.get('id'), phase.get('state')
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,99}', name) or name in by_id:
            raise ValueError('phase IDs must be unique letters, digits, hyphens or underscores')
        if not isinstance(state, str) or state not in STATES:
            raise ValueError(f'{name}: invalid state')
        deps, checks, artifacts = phase.get('depends_on', []), phase.get('checks', []), phase.get('artifacts', [])
        if not isinstance(deps, list) or not all(isinstance(x, str) for x in deps) or len(set(deps)) != len(deps):
            raise ValueError(f'{name}: dependencies must be distinct phase IDs')
        if not isinstance(checks, list) or not all(isinstance(x, dict) and type(x.get('passed')) is bool and
                isinstance(x.get('evidence'), str) and bool(x['evidence'].strip()) for x in checks):
            raise ValueError(f'{name}: checks need a boolean passed and nonempty evidence description')
        if not isinstance(artifacts, list):
            raise ValueError(f'{name}: artifacts must be a list')
        for item in artifacts:
            if not isinstance(item, dict):
                raise ValueError(f'{name}: artifact must be an object')
            relative, digest = item.get('path'), item.get('sha256')
            if (not isinstance(relative, str) or not relative or len(relative) > 1024 or '\\' in relative or ':' in relative or
                    any(0xD800 <= ord(char) <= 0xDFFF for char in relative) or
                    Path(relative).is_absolute() or any(part in ('..', '') for part in relative.split('/')) or
                    not isinstance(digest, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', digest)):
                raise ValueError(f'{name}: artifact requires a safe relative path and SHA-256')
        by_id[name] = phase
    for phase in phases:
        if any(dep not in by_id for dep in phase.get('depends_on', [])):
            raise ValueError(f"{phase['id']}: unknown dependency")

    root = Path(root).resolve()
    states, visiting = {}, set()
    def visit(name):
        if name in states:
            return states[name]
        if name in visiting:
            raise ValueError('phase dependencies contain a cycle')
        visiting.add(name)
        phase = by_id[name]
        dep_states = [visit(dep)['effective_state'] for dep in phase.get('depends_on', [])]
        state, reasons = phase['state'], []
        if state == 'completed':
            checks = phase.get('checks', [])
            if not checks or not all(check['passed'] for check in checks):
                reasons.append('successful recorded checks are missing or failed')
            if any(dep != 'completed' for dep in dep_states):
                reasons.append('a dependency is not currently completed')
            for artifact in phase.get('artifacts', []):
                try:
                    target = (root / artifact['path']).resolve(strict=True)
                    target.relative_to(root)
                    if not target.is_file() or target.stat().st_size > MAX_ARTIFACT_BYTES:
                        raise OSError('not a regular file or exceeds size limit')
                    digest = hashlib.sha256()
                    with target.open('rb') as stream:
                        count = 0
                        for block in iter(lambda: stream.read(1024 * 1024), b''):
                            count += len(block)
                            if count > MAX_ARTIFACT_BYTES:
                                raise OSError('artifact exceeds size limit')
                            digest.update(block)
                    if digest.hexdigest() != artifact['sha256'].lower():
                        reasons.append(f"artifact changed: {artifact['path']}")
                except (OSError, ValueError, RuntimeError):
                    reasons.append(f"artifact unavailable or outside checkpoint directory: {artifact['path']}")
            effective = 'needs_recheck' if reasons else 'completed'
        elif state in ('pending', 'in_progress') and any(dep != 'completed' for dep in dep_states):
            effective = 'blocked'
            reasons.append('a dependency is not currently completed')
        else:
            effective = state
        visiting.remove(name)
        states[name] = {'id': name, 'recorded_state': state, 'effective_state': effective, 'reasons': reasons}
        return states[name]

    for phase in phases:
        visit(phase['id'])
    result = [states[phase['id']] for phase in phases]
    return {'phases': result, 'note': 'Read-only consistency check of recorded claims and hashes; no workflow or scientific validation was executed.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint', type=Path, help='JSON checkpoint; artifact paths are relative to its directory')
    args = parser.parse_args()
    try:
        with args.checkpoint.open('rb') as stream:
            raw = stream.read(MAX_CHECKPOINT_BYTES + 1)
        if len(raw) > MAX_CHECKPOINT_BYTES:
            raise ValueError('checkpoint exceeds size limit')
        result = evaluate(json.loads(raw.decode('utf-8-sig')), args.checkpoint.parent)
    except (OSError, ValueError, RecursionError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return int(any(phase['effective_state'] in ('needs_recheck', 'blocked', 'failed') for phase in result['phases']))


if __name__ == '__main__':
    raise SystemExit(main())
