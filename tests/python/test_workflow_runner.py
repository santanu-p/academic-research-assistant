"""Behavior tests for the opt-in local research workflow runner."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "workflow_runner.py"


def phase(identifier, code, *, depends_on=None, outputs=None, timeout_seconds=10):
    return {
        "id": identifier,
        "command": [sys.executable, "-c", code],
        "depends_on": depends_on or [],
        "outputs": outputs or [],
        "timeout_seconds": timeout_seconds,
    }


def workflow(phases):
    return {"version": 1, "title": "Synthetic workflow test", "phases": phases}


class WorkflowRunnerTests(unittest.TestCase):
    def run_manifest(self, root, data, *flags):
        manifest = root / "workflow.json"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-B", str(TOOL), str(manifest), *flags],
            cwd=root, capture_output=True, text=True, encoding="utf-8", timeout=20,
        )

    def test_default_plan_orders_dependencies_without_running_commands(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            root = Path(directory)
            data = workflow([
                phase("report", "from pathlib import Path; Path('report.txt').write_text('done')",
                      depends_on=["prepare"], outputs=["report.txt"]),
                phase("prepare", "from pathlib import Path; Path('input.txt').write_text('ready')",
                      outputs=["input.txt"]),
            ])

            result = self.run_manifest(root, data)

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual([item["id"] for item in report["phases"]], ["prepare", "report"])
            self.assertEqual([item["status"] for item in report["phases"]], ["planned", "planned"])
            self.assertFalse((root / "input.txt").exists())
            self.assertFalse((root / "report.txt").exists())

    def test_execute_runs_dependencies_and_records_output_hashes(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            root = Path(directory)
            data = workflow([
                phase("summary", "from pathlib import Path; Path('summary.txt').write_bytes(Path('prepared.txt').read_bytes().upper())",
                      depends_on=["prepare"], outputs=["summary.txt"]),
                phase("prepare", "from pathlib import Path; Path('prepared.txt').write_bytes(b'raw')",
                      outputs=["prepared.txt"]),
            ])

            result = self.run_manifest(root, data, "--execute")

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual([item["id"] for item in report["phases"]], ["prepare", "summary"])
            self.assertEqual([item["status"] for item in report["phases"]], ["completed", "completed"])
            self.assertEqual(report["phases"][1]["outputs"][0]["sha256"], hashlib.sha256(b"RAW").hexdigest())
            self.assertEqual((root / "summary.txt").read_bytes(), b"RAW")

    def test_root_option_places_outputs_in_the_selected_project_directory(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            base = Path(directory)
            manifest_dir = base / "manifests"
            project_dir = base / "project"
            manifest_dir.mkdir()
            project_dir.mkdir()
            data = workflow([phase(
                "produce", "from pathlib import Path; Path('result.txt').write_text('result')",
                outputs=["result.txt"],
            )])

            result = self.run_manifest(manifest_dir, data, "--execute", "--root", str(project_dir))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project_dir / "result.txt").is_file())
            self.assertFalse((manifest_dir / "result.txt").exists())

    def test_failed_phase_blocks_dependents_but_runs_independent_phase(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            root = Path(directory)
            data = workflow([
                phase("dependent", "from pathlib import Path; Path('dependent.txt').write_text('wrong')",
                      depends_on=["fail"], outputs=["dependent.txt"]),
                phase("independent", "from pathlib import Path; Path('independent.txt').write_text('ran')",
                      outputs=["independent.txt"]),
                phase("fail", "raise SystemExit(7)"),
            ])

            result = self.run_manifest(root, data, "--execute")

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            states = {item["id"]: item["status"] for item in report["phases"]}
            self.assertEqual(states, {"fail": "failed", "dependent": "blocked", "independent": "completed"})
            self.assertEqual(next(item["exit_code"] for item in report["phases"] if item["id"] == "fail"), 7)
            self.assertFalse((root / "dependent.txt").exists())
            self.assertTrue((root / "independent.txt").is_file())

    def test_timeout_is_reported_and_blocks_dependents(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            root = Path(directory)
            data = workflow([
                phase("slow", "import time; time.sleep(5)", timeout_seconds=1),
                phase("after", "from pathlib import Path; Path('after.txt').write_text('wrong')",
                      depends_on=["slow"], outputs=["after.txt"]),
            ])

            result = self.run_manifest(root, data, "--execute")

            self.assertEqual(result.returncode, 1)
            records = {item["id"]: item for item in json.loads(result.stdout)["phases"]}
            self.assertEqual(records["slow"]["status"], "timed_out")
            self.assertEqual(records["after"]["status"], "blocked")
            self.assertFalse((root / "after.txt").exists())

    def test_successful_command_without_declared_output_is_failed(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            root = Path(directory)
            data = workflow([phase("produce", "pass", outputs=["missing.txt"])])

            result = self.run_manifest(root, data, "--execute")

            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["phases"][0]["status"], "failed")
            self.assertIn("missing.txt", json.loads(result.stdout)["phases"][0]["reason"])

    def test_declared_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            root = Path(directory)
            output = root / "result.txt"
            output.write_text("keep", encoding="utf-8")
            data = workflow([phase(
                "produce", "from pathlib import Path; Path('result.txt').write_text('replace')",
                outputs=["result.txt"],
            )])

            result = self.run_manifest(root, data, "--execute")

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertEqual(report["phases"][0]["status"], "failed")
            self.assertIn("already exists", report["phases"][0]["reason"])
            self.assertEqual(output.read_text(encoding="utf-8"), "keep")

    def test_string_command_is_rejected_instead_of_treated_as_shell(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            root = Path(directory)
            data = workflow([{"id": "unsafe", "command": "echo should-not-run"}])

            result = self.run_manifest(root, data, "--execute")

            self.assertEqual(result.returncode, 2)
            self.assertIn("command must be a list", result.stderr)

    def test_output_traversal_is_rejected_before_commands_run(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            base = Path(directory)
            root = base / "project"
            root.mkdir()
            outside = base / "outside.txt"
            data = workflow([phase(
                "unsafe", "from pathlib import Path; Path('marker.txt').write_text('ran')",
                outputs=["../outside.txt"],
            )])

            result = self.run_manifest(root, data, "--execute")

            self.assertEqual(result.returncode, 2)
            self.assertIn("safe relative path", result.stderr)
            self.assertFalse(outside.exists())
            self.assertFalse((root / "marker.txt").exists())

    def test_report_collision_is_rejected_before_commands_run(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            root = Path(directory)
            report = root / "receipt.json"
            report.write_text("keep", encoding="utf-8")
            data = workflow([phase("write", "from pathlib import Path; Path('marker').write_text('ran')")])

            result = self.run_manifest(root, data, "--execute", "--report", str(report))

            self.assertEqual(result.returncode, 2)
            self.assertIn("already exists", result.stderr)
            self.assertEqual(report.read_text(encoding="utf-8"), "keep")
            self.assertFalse((root / "marker").exists())

    def test_report_path_cannot_overlap_a_phase_output(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            root = Path(directory)
            report = root / "receipt.json"
            data = workflow([phase(
                "write", "from pathlib import Path; Path('receipt.json').write_text('phase output')",
                outputs=["receipt.json"],
            )])

            result = self.run_manifest(root, data, "--execute", "--report", str(report))

            self.assertEqual(result.returncode, 2)
            self.assertIn("conflicts with a declared phase output", result.stderr)
            self.assertFalse(report.exists())

    def test_dependency_cycle_is_rejected_before_commands_run(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            root = Path(directory)
            data = workflow([
                phase("one", "pass", depends_on=["two"]),
                phase("two", "pass", depends_on=["one"]),
            ])

            result = self.run_manifest(root, data, "--execute")

            self.assertEqual(result.returncode, 2)
            self.assertIn("cycle", result.stderr)


if __name__ == "__main__":
    unittest.main()
