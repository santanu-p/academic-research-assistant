"""ARMS adapter boundary tests; never invoke a real model or experiment."""
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/expanded/ARMS-main"
ADAPTER = ROOT / "build_tools/adapt_arms.py"
BASH = shutil.which("bash")
GIT = shutil.which("git") or r"C:\Program Files\Git\cmd\git.exe"


def hashes(base):
    return {p.relative_to(base).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in base.rglob("*") if p.is_file()}


class ArmsAdapterTests(unittest.TestCase):
    def setUp(self):
        # Break caught: a missing adapter cannot silently produce an unadapted package.
        self.assertTrue(ADAPTER.is_file(), "The ARMS adapter module must be implemented")
        spec = importlib.util.spec_from_file_location("adapt_arms", ADAPTER)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / "work")
        self.addCleanup(self.temp.cleanup)
        self.package = Path(self.temp.name) / "plugin"
        shutil.copytree(SOURCE, self.package / "resources/upstream/ARMS-main")
        for src in (SOURCE / "skills").iterdir():
            shutil.copytree(src, self.package / "skills" / ("arms-" + src.name))
        self.original_hashes = hashes(self.package / "resources")
        (self.package / "untouched.txt").write_text("unrelated", encoding="utf-8")

    def adapt(self):
        return self.module.adapt_arms(self.package)

    def test_adapter_resolves_shipped_resources_and_retains_missing_dependency_status(self):
        # Break caught: paths must resolve from an active skill after namespacing.
        changes = self.adapt()
        self.assertTrue(changes)
        brief = self.package / "skills/arms-brief-expander/SKILL.md"
        text = brief.read_text(encoding="utf-8")
        targets = re.findall(r"`([^`]*research_brief_template\.md)`", text)
        self.assertTrue(targets)
        self.assertTrue(all((brief.parent / target).is_file() for target in targets))
        for skill in (self.package / "skills").glob("arms-*/SKILL.md"):
            body = skill.read_text(encoding="utf-8")
            self.assertNotIn("~/.claude", body)
            self.assertNotIn(".claude/skills/", body)
            for target in re.findall(r"`(\.\./arms-[^`\s]+\.(?:md|py|sh))`", body):
                self.assertTrue((skill.parent / target).is_file(), (skill, target))
            for target in re.findall(r"`((?:\.\./arms-house-style/)?examples/(?:abstract-reader-first|dense-results-paragraph)\.md)`", body):
                self.assertTrue((skill.parent / target).is_file(), (skill, target))
        critic = (self.package / "skills/arms-paper-critic/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("UNAVAILABLE_UPSTREAM_SCORING_RUBRIC", critic)
        self.assertFalse((self.package / "skills/_shared/scoring_rubric.md").exists())
        pipeline = (self.package / "skills/arms-research-pipeline/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("../../agents/consistency-auditor.md", pipeline)
        self.assertNotIn('prompt: "/consistency-auditor ', pipeline)

    def test_adapter_is_idempotent_and_never_modifies_preserved_sources(self):
        # Break caught: repeat builds must neither accumulate prose nor mutate provenance.
        self.adapt()
        first = hashes(self.package)
        self.assertEqual(self.adapt(), [])
        self.assertEqual(first, hashes(self.package))
        self.assertEqual(self.original_hashes, hashes(self.package / "resources"))
        self.assertEqual((self.package / "untouched.txt").read_text(), "unrelated")

    def _shell(self, script, args=(), env=None, cwd=None):
        if not BASH:
            self.skipTest("Bash is not installed")
        return subprocess.run([BASH, str(script), *map(str, args)],
                              cwd=cwd, env=env, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=30)

    def _stub_env(self):
        # CLIs are checked for availability only; a preflight invoking one would fail.
        bin_dir = self.package / "bin"
        bin_dir.mkdir(exist_ok=True)
        for name in ["claude", "codex", "latexmk", "latexdiff"]:
            path = bin_dir / name
            path.write_text("#!/bin/sh\nprintf 'CLI MUST NOT RUN\\n' >&2\nexit 97\n", encoding="utf-8")
            path.chmod(0o755)
        env = dict(os.environ)
        env["PATH"] = str(bin_dir) + os.pathsep + env["PATH"]
        env.pop("ARMS_ENABLE_GIT_SNAPSHOT", None)
        return env

    def _manuscript(self):
        work = self.package / "project"
        work.mkdir(exist_ok=True)
        manuscript = work / "manuscript.tex"
        manuscript.write_text("original manuscript\n", encoding="utf-8")
        return manuscript

    def test_preflight_checks_tools_before_outputs_or_model_invocations(self):
        # Break caught: missing dependencies must fail before logs, edits or paid calls.
        self.adapt()
        manuscript = self._manuscript()
        script = self.package / "skills/arms-critic-revisor/run_loop.sh"
        env = self._stub_env()
        (self.package / "bin/latexdiff").unlink()
        result = self._shell(script, [manuscript, "--preflight"], env)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("latexdiff", result.stderr)
        self.assertNotIn("CLI MUST NOT RUN", result.stderr)
        self.assertFalse((manuscript.parent / "critic_revisor_logs").exists())
        self.assertEqual(manuscript.read_text(), "original manuscript\n")

    def test_complete_preflight_and_syntax_pass_without_outputs(self):
        # Break caught: successful preflight must stop without starting the loop.
        self.adapt()
        manuscript = self._manuscript()
        script = self.package / "skills/arms-critic-revisor/run_loop.sh"
        syntax = subprocess.run([BASH, "-n", str(script)], capture_output=True, text=True) if BASH else None
        if syntax is not None:
            self.assertEqual(syntax.returncode, 0, syntax.stderr)
        result = self._shell(script, [manuscript, "--preflight"], self._stub_env())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("CLI MUST NOT RUN", result.stderr)
        self.assertFalse((manuscript.parent / "critic_revisor_logs").exists())

    def _git(self, work, *args):
        result = subprocess.run([GIT, "-C", str(work), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def _repository(self):
        if not Path(GIT).exists() and not shutil.which(GIT):
            self.skipTest("Git is not installed")
        manuscript = self._manuscript()
        work = manuscript.parent
        self._git(work, "init", "-q")
        self._git(work, "config", "user.name", "ARMS adapter test")
        self._git(work, "config", "user.email", "arms-adapter-test@example.invalid")
        (work / "unrelated.txt").write_text("baseline\n")
        self._git(work, "add", "--", "manuscript.tex", "unrelated.txt")
        self._git(work, "commit", "-qm", "baseline")
        return manuscript, work

    def test_git_opt_in_preflight_rejects_an_existing_index(self):
        # Break caught: snapshot opt-in must not absorb pre-existing staged changes.
        self.adapt()
        manuscript, work = self._repository()
        (work / "unrelated.txt").write_text("user staged edit\n")
        self._git(work, "add", "--", "unrelated.txt")
        before = self._git(work, "diff", "--cached")
        env = self._stub_env()
        env["ARMS_ENABLE_GIT_SNAPSHOT"] = "1"
        script = self.package / "skills/arms-critic-revisor/run_loop.sh"
        result = self._shell(script, [manuscript, "--preflight"], env)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("index", result.stderr.lower())
        self.assertEqual(before, self._git(work, "diff", "--cached"))
        self.assertFalse((work / "critic_revisor_logs").exists())
        env.pop("ARMS_ENABLE_GIT_SNAPSHOT")
        result = self._shell(script, [manuscript, "--preflight"], env)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_snapshot_helper_commits_only_manuscript_and_current_run(self):
        # Break caught: a snapshot must never stage or commit unrelated user edits.
        self.adapt()
        manuscript, work = self._repository()
        manuscript.write_text("revised manuscript\n")
        (work / "unrelated.txt").write_text("user unstaged edit\n")
        run_dir = work / "critic_revisor_logs/run_test"
        run_dir.mkdir(parents=True)
        (run_dir / "review.md").write_text("review\n")
        text = (self.package / "skills/arms-critic-revisor/run_loop.sh").read_text(encoding="utf-8")
        helper = re.search(r"(?ms)^git_snapshot_round\(\) \{.*?^\}\n", text)
        self.assertIsNotNone(helper, "Snapshot helper must be callable independently of models")
        env = self._stub_env()
        env.update(WORK_DIR=str(work), MANU_FILE=manuscript.name, RUN_DIR=str(run_dir), USE_GIT="1")
        env["ARMS_ENABLE_GIT_SNAPSHOT"] = "1"
        if not BASH:
            self.skipTest("Bash is not installed")
        result = subprocess.run([BASH, "-c", helper.group(0) + "\ngit_snapshot_round 1\n"],
                                env=env, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        names = set(self._git(work, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines())
        self.assertEqual(names, {"manuscript.tex", "critic_revisor_logs/run_test/review.md"})
        self.assertEqual(self._git(work, "diff", "--name-only"), "unrelated.txt")
        self.assertEqual(self._git(work, "diff", "--cached", "--name-only"), "")


if __name__ == "__main__":
    unittest.main()
