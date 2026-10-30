import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[2] / 'tools' / 'pipeline_checkpoint.py'


class CheckpointTests(unittest.TestCase):
    def run_checkpoint(self, root, phases):
        checkpoint = root / 'checkpoint.json'
        checkpoint.write_text(json.dumps({'phases': phases}), encoding='utf-8')
        return subprocess.run([sys.executable, str(TOOL), str(checkpoint)], capture_output=True, text=True)

    def test_changed_artifact_invalidates_completed_dependents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'data.txt').write_bytes(b'changed')
            phases = [
                {'id': 'data', 'state': 'completed', 'depends_on': [], 'checks': [{'passed': True, 'evidence': 'log'}],
                 'artifacts': [{'path': 'data.txt', 'sha256': hashlib.sha256(b'original').hexdigest()}]},
                {'id': 'analysis', 'state': 'completed', 'depends_on': ['data'], 'checks': [{'passed': True, 'evidence': 'run log'}]},
                {'id': 'report', 'state': 'pending', 'depends_on': ['analysis']},
            ]
            result = self.run_checkpoint(root, phases)
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual([p['effective_state'] for p in report['phases']], ['needs_recheck', 'needs_recheck', 'blocked'])
            self.assertEqual((root / 'data.txt').read_bytes(), b'changed')

    def test_completed_requires_recorded_successful_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_checkpoint(Path(tmp), [{'id': 'design', 'state': 'completed', 'depends_on': [], 'checks': []}])
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)['phases'][0]['effective_state'], 'needs_recheck')

    def test_valid_checkpoint_and_missing_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'input').write_bytes(b'abc')
            phase = {'id': 'one', 'state': 'completed', 'depends_on': [], 'checks': [{'passed': True, 'evidence': 'reviewed'}],
                     'artifacts': [{'path': 'input', 'sha256': hashlib.sha256(b'abc').hexdigest()}]}
            self.assertEqual(self.run_checkpoint(root, [phase]).returncode, 0)
            (root / 'input').unlink()
            self.assertEqual(self.run_checkpoint(root, [phase]).returncode, 1)

    def test_unknown_dependency_and_cycle_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for phases in ([{'id': 'a', 'state': 'pending', 'depends_on': ['missing']}],
                           [{'id': 'a', 'state': 'pending', 'depends_on': ['b']}, {'id': 'b', 'state': 'pending', 'depends_on': ['a']}]):
                result = self.run_checkpoint(root, phases)
                self.assertEqual(result.returncode, 2)

    def test_unsafe_artifact_paths_and_malformed_checks_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = {'id': 'a', 'state': 'completed', 'depends_on': [],
                    'checks': [{'passed': True, 'evidence': 'reviewed'}]}
            for artifact in ({'path': '../outside', 'sha256': 'a' * 64},
                             {'path': str(root / 'absolute'), 'sha256': 'a' * 64},
                             {'path': 'data', 'sha256': 'not-a-hash'},
                             {'path': 'bad\ud800name', 'sha256': 'a' * 64}):
                result = self.run_checkpoint(root, [{**base, 'artifacts': [artifact]}])
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertNotIn('Traceback', result.stderr)
            result = self.run_checkpoint(root, [{**base, 'checks': [{'passed': 'yes', 'evidence': 'log'}]}])
            self.assertEqual(result.returncode, 2, result.stderr)

    def test_invalid_state_is_a_bounded_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_checkpoint(Path(tmp), [{'id': 'a', 'state': [], 'depends_on': []}])
            self.assertEqual(result.returncode, 2)
            self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
