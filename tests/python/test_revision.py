"""Exercise the bounded runner with local scripts, never model calls."""
import hashlib
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / "tests" / ".revision-tmp"


class RevisionTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.base = Path(self.temp.name)
        self.target = self.base / "draft, with spaces.md"
        self.target.write_text("A bounded draft.\n", encoding="utf-8")
        self.source = self.base / "evidence, with spaces.txt"
        self.source.write_text("Source evidence.\n", encoding="utf-8")
        self.run = self.base / "new run"
        self.mark = self.base / "called.txt"
        self.fixture = self.base / "provider fixture.py"
        self.fixture.write_text('''import json, pathlib, subprocess, sys, time
mode, mark = sys.argv[1:]
request = json.load(sys.stdin)
with pathlib.Path(mark).open("a", encoding="utf-8") as handle:
    handle.write(mode + "\\n")
if mode == "timeout":
    time.sleep(5)
if mode == "descendant":
    child_code = "import pathlib,sys,time; p=pathlib.Path(sys.argv[1]); p.with_suffix('.ready').write_text('ready'); time.sleep(3); p.with_suffix('.late').write_text('late write')"
    subprocess.Popen([sys.executable, "-c", child_code, mark], stdin=subprocess.DEVNULL, stdout=sys.stdout, stderr=sys.stderr)
    time.sleep(5)
if mode == "malformed":
    print("{broken")
elif mode == "badaccept":
    print(json.dumps({"decision":"accept", "issues":[{"id":"x", "severity":"major", "location":"intro", "comment":"wrong"}]}))
elif mode == "duplicate":
    issue = {"id":"x", "severity":"minor", "location":"intro", "comment":"wording"}
    print(json.dumps({"decision":"revise", "issues":[issue,issue]}))
elif mode == "stop":
    print(json.dumps({"decision":"stop", "issues":[{"id":"unsupported", "severity":"major", "location":"claim", "comment":"No supplied evidence supports the requested claim."}]}))
elif mode == "revise":
    pathlib.Path(request["target"]["path"]).write_text("Revised using supplied evidence.\\n", encoding="utf-8")
    print(json.dumps({"changes":["Reworded the draft."], "unresolved":[]}))
elif mode == "noop":
    print(json.dumps({"changes":["I changed everything."], "unresolved":[]}))
elif mode == "mutatingreview":
    pathlib.Path(request["target"]["path"]).write_text("Unauthorized reviewer edit.", encoding="utf-8")
    print(json.dumps({"decision":"accept", "issues":[]}))
elif mode == "needsrevision" or (mode == "conditional" and "Revised" not in request["target"]["text"]):
    print(json.dumps({"decision":"revise", "issues":[{"id":"specificity", "severity":"minor", "location":"paragraph 1", "comment":"Use the supplied evidence."}]}))
elif mode == "checkfail":
    print("fixture check failure", file=sys.stderr)
    sys.exit(7)
else:
    print(json.dumps({"decision":"accept", "issues":[]}))
''', encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def command(self, mode):
        return json.dumps([sys.executable, "-X", "utf8", "-B", str(self.fixture), mode, str(self.mark)])

    def invoke(self, modes=("accept", "accept"), reviser="revise", execute=True, extra=()):
        args = [sys.executable, "-X", "utf8", "-B", str(ROOT / "tools" / "revise.py"), str(self.target),
                "--reviewer", self.command(modes[0]), "--reviewer", self.command(modes[1]),
                "--reviser", self.command(reviser), "--out", str(self.run), "--source", str(self.source), *extra]
        if execute:
            args.append("--execute")
        return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", timeout=20)

    def manifest(self):
        return json.loads((self.run / "manifest.json").read_text(encoding="utf-8"))

    def test_preflight_has_no_calls_no_output_folder(self):
        result = self.invoke(execute=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.mark.exists())
        self.assertFalse(self.run.exists())
        self.assertEqual(json.loads(result.stdout)["status"], "preflight")

    def test_acceptance_preserves_evidence_sidecars_and_stderr_receipts(self):
        sidecar = self.base / "references.bib"
        sidecar.write_text("@misc{synthetic,title={Fixture}}", encoding="utf-8")
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = self.manifest()
        self.assertEqual(receipt["status"], "accepted")
        self.assertEqual(len(receipt["rounds"]), 1)
        material = receipt["material"]
        self.assertTrue(any(item["original"] == str(sidecar) for item in material))
        for item in material:
            actual = (self.run / item["snapshot"]).read_bytes()
            self.assertEqual(hashlib.sha256(actual).hexdigest(), item["sha256"])
        self.assertEqual(len(list((self.run / "receipts").glob("*.stderr.txt"))), 2)

    def test_actual_revision_and_followup_acceptance(self):
        result = self.invoke(modes=("conditional", "conditional"))
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = self.manifest()
        revision = receipt["rounds"][0]["revision"]
        self.assertNotEqual(revision["before_sha256"], revision["after_sha256"])
        self.assertTrue(revision["content_changed"])
        self.assertTrue(all(item["status"] == "accepted_by_followup_reviewer" for item in revision["dispositions"]))
        self.assertEqual(len(receipt["rounds"]), 2)
        self.assertEqual(self.source.read_text(), "Source evidence.\n")

    def test_claimed_edits_are_not_actual_proof_and_budget_exhausts(self):
        result = self.invoke(modes=("needsrevision", "accept"), reviser="noop", extra=("--rounds", "2"))
        self.assertEqual(result.returncode, 3, result.stderr)
        receipt = self.manifest()
        self.assertEqual(receipt["status"], "exhausted")
        self.assertFalse(receipt["rounds"][0]["revision"]["content_changed"])
        self.assertEqual(self.mark.read_text().splitlines().count("noop"), 1)

    def test_scientific_stop(self):
        result = self.invoke(modes=("stop", "accept"))
        self.assertEqual(result.returncode, 4, result.stderr)
        self.assertEqual(self.manifest()["status"], "scientific_stop")
        self.assertNotIn("revise", self.mark.read_text().splitlines())

    def test_invalid_review_schema_and_json(self):
        for mode in ("malformed", "badaccept", "duplicate"):
            with self.subTest(mode=mode):
                self.run = self.base / ("run-" + mode)
                result = self.invoke(modes=(mode, "accept"))
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(self.manifest()["status"], "operational_failure")

    def test_timeout(self):
        result = self.invoke(modes=("timeout", "accept"), extra=("--timeout", "0.2"))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("timed out", self.manifest()["error"])

    def test_timeout_terminates_descendant_and_does_not_wait_for_inherited_pipes(self):
        start = time.monotonic()
        result = self.invoke(modes=("descendant", "accept"), extra=("--timeout", "0.8"))
        elapsed = time.monotonic() - start
        # Give an escaped child time to perform its delayed write. This checks
        # process lifetime, not only a misleading fast parent return.
        time.sleep(3.5)
        self.assertTrue(self.mark.with_suffix(".ready").exists(), "fixture descendant never started")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertLess(elapsed, 2.5, f"timeout blocked for {elapsed:.2f}s on inherited capture pipes")
        self.assertFalse(self.mark.with_suffix(".late").exists(), "descendant wrote after timeout")

    def test_check_failure_does_not_claim_acceptance(self):
        result = self.invoke(extra=("--check", self.command("checkfail")))
        self.assertEqual(result.returncode, 2, result.stderr)
        receipt = self.manifest()
        self.assertEqual(receipt["status"], "operational_failure")
        self.assertIn("check", receipt["error"])
        self.assertEqual(receipt["command_receipts"][-1]["returncode"], 7)

    def test_configured_successful_check_runs_before_acceptance(self):
        result = self.invoke(extra=("--check", self.command("checksuccess")))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.mark.read_text().splitlines()[-1], "checksuccess")
        self.assertEqual(len(self.manifest()["checks"]), 1)

    def test_reviewer_edits_are_detected(self):
        result = self.invoke(modes=("mutatingreview", "accept"))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("only the reviser", self.manifest()["error"])

    def test_binary_evidence_is_preserved_without_extraction_claim(self):
        binary = self.base / "evidence.pdf"
        binary.write_bytes(b"%PDF-fixture\x00not-real-pdf")
        result = self.invoke(extra=("--source", str(binary)))
        self.assertEqual(result.returncode, 0, result.stderr)
        prompt = json.loads(next((self.run / "receipts").glob("*.prompt.json")).read_text())
        source = next(item for item in prompt["sources"] if item["path"] == str(binary))
        self.assertIsNone(source["text"])
        self.assertIn("no extraction", source["interpretation"])

    def test_existing_output_and_missing_command_rejected_without_calls(self):
        self.run.mkdir()
        result = self.invoke(execute=False)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.mark.exists())
        self.run = self.base / "another run"
        result = self.invoke(execute=False, extra=("--check", '["definitely-missing-binary-fixture-xyz"]'))
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.run.exists())


if __name__ == "__main__":
    unittest.main()
