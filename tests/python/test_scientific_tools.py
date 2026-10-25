"""Regression tests use synthetic values and temporary files; no network calls."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import prose_metrics as prose, table_qa as table, visual_qa as visual

PLOTTING = importlib.util.find_spec("numpy") is not None and importlib.util.find_spec("matplotlib") is not None


class ProseTests(unittest.TestCase):
    def test_protected_markup_and_short_paragraphs(self):
        text = "A brief paragraph.\n\n```python\nnot prose 100\n```\n\nA longer paragraph has $hidden math 42$ words. <!-- hidden -->"
        result = prose.analyze_text(text, "markdown", 4)
        self.assertEqual(result["words"], 8)
        self.assertEqual(result["numeric_expressions"], 0)
        self.assertEqual(result["short_paragraphs"]["paragraphs"], [1])

    def test_latex_comments_math_and_decimal(self):
        result = prose.analyze_text(r"\section{Results}" + "\nA value is 3.14. Another result holds. % ignored 500\n" + r"\[x=999\]", "latex")
        self.assertEqual(result["numeric_expressions"], 1)
        self.assertEqual(result["sentences"]["count"], 2)
        self.assertIn("includes", " ".join(result["limits"]))

    def test_invalid_utf8_json_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.md"
            path.write_bytes(b"\xff")
            result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(ROOT / "tools/prose_metrics.py"), str(path), "--json"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("error", json.loads(result.stderr))


class TableTests(unittest.TestCase):
    def test_numbers_uncertainty_locale_missing(self):
        self.assertEqual(table.parse_number("−1,234.50e-2 ± 0.1 kg")["value"], "-12.3450")
        self.assertEqual(table.parse_number("1.23(4)")["uncertainty"], "0.04")
        self.assertEqual(table.parse_number("1.234,50", decimal=",", grouping=".")["value"], "1234.50")
        self.assertTrue(table.parse_number("N/A")["missing"])
        self.assertIsNone(table.parse_number("1,23.5"))
        self.assertIsNone(table.parse_number("1 ± -2"))

    def test_precision_units_and_missingness(self):
        report = table.analyze_text('sample,value\na,"1,200.50 kg"\nb,2.0\nc,NA\n')
        column = report["columns"][1]
        self.assertEqual(column["missing_rows"], [4])
        self.assertEqual(column["decimal_places"], [1, 2])
        self.assertEqual(len(column["notes"]), 2)

    def test_malformed_tables_rejected(self):
        for text in ['a,b\n"unclosed,1', 'a,b\n1,2,3']:
            with self.assertRaises(ValueError):
                table.analyze_text(text)


class VisualTests(unittest.TestCase):
    def test_svg_physical_scale_font_and_resources(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg" width="100mm" height="50mm" viewBox="0 0 200 100"><g font-size="5"><text x="1" y="10">small</text></g><image href="https://example.invalid/a.png"/><image href="data:image/png;base64,AA=="/></svg>'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.svg"
            path.write_text(svg, encoding="utf-8")
            report = visual.analyze_file(path)
            self.assertEqual(report["physical_mm"], [100, 50])
            self.assertEqual(len(report["small_text"]), 1)
            self.assertEqual(report["embedded_resources"], 1)
            self.assertEqual(len(report["external_references"]), 1)

    def test_missing_pdf_backend_is_incomplete(self):
        with patch.object(visual.importlib, "import_module", side_effect=ImportError):
            self.assertEqual(visual.inspect_pdf("unused.pdf")["status"], "incomplete")

    @unittest.skipUnless(importlib.util.find_spec("PIL"), "Pillow unavailable")
    def test_raster_dimensions_and_dpi(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.png"
            Image.new("RGB", (100, 80)).save(path, dpi=(300, 300))
            result = visual.analyze_file(path)
            self.assertEqual(result["pixels"], [100, 80])
            self.assertAlmostEqual(result["dpi"][0], 300, places=1)


@unittest.skipUnless(PLOTTING, "NumPy/Matplotlib unavailable")
class PlotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tools import scientific_visuals
        cls.plot = scientific_visuals

    def tearDown(self):
        import matplotlib.pyplot as plt
        plt.close("all")

    def test_pareto_directions_duplicates_and_nonfinite(self):
        points = [[1, 2], [1, 2], [2, 1], [2, 3]]
        self.assertEqual(self.plot.pareto_frontier(points), [0, 1, 3])
        self.assertEqual(self.plot.pareto_frontier(points, ("higher", "lower")), [2])
        for data, directions in [([[float("nan"), 1]], ("lower", "higher")), (points, ("bad", "higher"))]:
            with self.assertRaises(ValueError):
                self.plot.pareto_frontier(data, directions)

    def test_no_cross_family_line_and_order_rejection(self):
        _, ax = self.plot.frontier_plot([1, 2, 3], [2, 3, 4], families=["a", "b", "a"])
        self.assertEqual(len(ax.lines), 0)
        with self.assertRaises(ValueError):
            self.plot.ordered_line([2, 1], [1, 2])
        with self.assertRaises(ValueError):
            self.plot.comparison(["a"], [1], [-.1])

    def test_annotations_above_error_caps_and_export_size(self):
        fig, ax = self.plot.comparison(["a", "b"], [1, 2], [.5, .2])
        self.assertEqual(ax.texts[0].xy[1], 1.5)
        self.assertGreater(ax.texts[0].get_position()[1], 4)
        with tempfile.TemporaryDirectory() as directory:
            report = self.plot.export_figure(fig, Path(directory) / "comparison")
            self.assertEqual(len(report["files"]), 3)
            self.assertFalse(report["audit"]["off_canvas_text"])
            svg = visual.analyze_file(Path(directory) / "comparison.svg")
            self.assertAlmostEqual(svg["physical_mm"][0], 160, places=3)
            self.assertFalse(svg["small_text"])

    def test_audit_detects_offcanvas_and_small_text(self):
        fig, _ = self.plot.figure_mm()
        fig.text(1.2, .5, "outside", fontsize=7)
        report = self.plot.audit_figure(fig)
        self.assertIn("outside", report["off_canvas_text"])
        self.assertEqual(report["small_text"][0]["font_pt"], 7)

    @unittest.skipUnless(importlib.util.find_spec("pymupdf") or importlib.util.find_spec("fitz"), "PyMuPDF unavailable; PDF integration not executed")
    def test_pdf_all_pages_and_renders(self):
        try:
            import pymupdf as backend
        except ImportError:
            import fitz as backend
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "two.pdf"
            with backend.open() as document:
                for text in ("first", "second"):
                    page = document.new_page()
                    page.insert_text((30, 30), text, fontsize=7)
                document.save(path)
            report = visual.analyze_file(path, render_dir=Path(directory) / "render")
            self.assertEqual(report["page_count"], 2)
            self.assertTrue(all(page["small_text"] and Path(page["render"]).is_file() for page in report["pages"]))


if __name__ == "__main__":
    unittest.main()
