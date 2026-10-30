"""Exercise the offline comparison through its public command line."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "text_revision_report.py"
SCRATCH = ROOT / "tests" / ".text-report-tmp"


class ReportTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.base = Path(self.temp.name)
        self.old = self.base / "old & draft.txt"
        self.new = self.base / "new.txt"
        self.out = self.base / "comparison.html"

    def tearDown(self):
        self.temp.cleanup()
        try:
            SCRATCH.rmdir()
        except OSError:
            pass  # Another test or an existing file still uses the directory.

    def run_report(self, output=None):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), str(self.old),
                               str(self.new), str(output or self.out)], capture_output=True,
                              text=True, encoding="utf-8", timeout=10)

    def test_changes_escape_markup_and_preserve_original_bytes(self):
        old = "A claim is strong.\n<script>alert(1)</script>\n".encode()
        new = "A claim is tentative.\n<script>alert(1)</script>\n".encode()
        self.old.write_bytes(old)
        self.new.write_bytes(new)
        result = self.run_report()
        self.assertEqual(result.returncode, 0, result.stderr)
        page = self.out.read_text(encoding="utf-8")
        self.assertIn('<del title="Deleted">strong.</del>', page)
        self.assertIn('<ins title="Added">tentative.</ins>', page)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', page)
        self.assertNotIn('<script>', page)
        self.assertNotIn(str(self.base), page)
        self.assertIn('old &amp; draft.txt', page)
        self.assertEqual(self.old.read_bytes(), old)
        self.assertEqual(self.new.read_bytes(), new)

    def test_existing_output_and_source_path_are_never_overwritten(self):
        self.old.write_text("old", encoding="utf-8")
        self.new.write_text("new", encoding="utf-8")
        self.out.write_text("existing", encoding="utf-8")
        self.assertEqual(self.run_report().returncode, 2)
        self.assertEqual(self.out.read_text(), "existing")
        self.assertEqual(self.run_report(self.old).returncode, 2)
        self.assertEqual(self.old.read_text(), "old")

    def test_invalid_and_oversize_inputs_do_not_create_report(self):
        self.new.write_text("new", encoding="utf-8")
        for data in (b"\xff", b"hello\x00world", b"x" * 1_000_001):
            with self.subTest(length=len(data)):
                self.old.write_bytes(data)
                self.assertEqual(self.run_report().returncode, 2)
                self.assertFalse(self.out.exists())

    def test_identical_unicode_is_unmarked(self):
        self.old.write_text("α β\n", encoding="utf-8")
        self.new.write_text("α β\n", encoding="utf-8")
        self.assertEqual(self.run_report().returncode, 0)
        page = self.out.read_text(encoding="utf-8")
        self.assertIn("<pre>α β\n</pre>", page)
        self.assertNotIn("<del ", page)
        self.assertNotIn("<ins ", page)


if __name__ == "__main__":
    unittest.main()
