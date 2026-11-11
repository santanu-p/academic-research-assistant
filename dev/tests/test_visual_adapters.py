"""Regressions for active-only visual helper adaptations.

The source copies are fixtures, never edit targets. Optional real Matplotlib
and PyMuPDF integration tests skip when those dependencies are unavailable.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import typing
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/originals/scientific-visual-table-style/2.2.0/skills/scientific-visual-table-style"
FIXTURE_ROOT = ROOT / "work/visual-tests"
ADAPTER = ROOT / "build_tools/adapt_visuals.py"
SKILL_PATH = Path("skills/visuals-scientific-visual-table-style")
HELPERS = (
    "templates/openai_visuals.py",
    "scripts/table_qa.py",
    "scripts/select_references.py",
    "scripts/visual_qa.py",
    "examples/example_openai_visuals.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def apply_adapter(package: Path) -> list[dict]:
    # Running this file before the adapter exists exercises the original bugs.
    if not ADAPTER.is_file():
        return []
    return load_module(ADAPTER, "visual_adapter_under_test").adapt_visuals(package)


def load_function(path: Path, name: str, namespace: dict):
    """Run the real cache resolver without importing optional plotting libs."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    node = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)
    code = ast.Module(body=[node], type_ignores=[])
    exec(compile(ast.fix_missing_locations(code), str(path), "exec"), namespace)
    return namespace[name]


def write_pdf(path: Path, font_size: float = 12.0) -> None:
    """Write a small, valid one-page PDF using a built-in Helvetica font."""
    content = f"BT /F1 {font_size:g} Tf 20 100 Td (Scientific label) Tj ET\n".encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 200] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"endstream",
    ]
    data = bytearray(b"%PDF-1.4\n%" + b"fixture padding " * 100 + b"\n")
    offsets = [0]
    for index, value in enumerate(objects, 1):
        offsets.append(len(data))
        data.extend(f"{index} 0 obj\n".encode("ascii") + value + b"\nendobj\n")
    xref = len(data)
    data.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("ascii"))
    for offset in offsets[1:]:
        data.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    data.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii"))
    path.write_bytes(data)


class FixturePage:
    """Controlled optional-backend boundary for preflight branch tests."""

    rect = SimpleNamespace(width=300.0, height=200.0)

    def __init__(self, font_size: float, render_error: bool = False):
        self.font_size = font_size
        self.render_error = render_error

    def get_images(self, full=True):
        return []

    def get_text(self, kind):
        if kind == "blocks":
            return [(20.0, 20.0, 100.0, 40.0, "Scientific label", 0, 0)]
        if kind == "dict":
            return {"width": 300.0, "height": 200.0, "blocks": [{
                "number": 0, "type": 0, "bbox": (20.0, 20.0, 100.0, 40.0),
                "lines": [{"wmode": 0, "dir": (1.0, 0.0), "bbox": (20.0, 20.0, 100.0, 40.0), "spans": [{
                    "size": self.font_size, "flags": 0, "font": "Helvetica", "color": 0,
                    "ascender": 1.075, "descender": -0.299, "text": "Scientific label",
                    "origin": (20.0, 30.0), "bbox": (20.0, 20.0, 100.0, 40.0),
                }]}],
            }]}
        raise AssertionError(f"Unexpected text extraction mode: {kind}")

    def get_pixmap(self, *, matrix, alpha=False):
        if self.render_error:
            raise RuntimeError("fixture rasterizer unavailable")
        return SimpleNamespace(width=300, height=200, alpha=False)


class FixtureDocument:
    def __init__(self, pages):
        self.pages = pages

    def __len__(self):
        return len(self.pages)

    def __getitem__(self, index):
        return self.pages[index]

    def close(self):
        pass


class VisualAdapterTests(unittest.TestCase):
    def setUp(self):
        FIXTURE_ROOT.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="adapter-", dir=FIXTURE_ROOT)
        self.package = Path(self.temporary.name).resolve()
        self.assertTrue(self.package.is_relative_to(FIXTURE_ROOT.resolve()))
        self.addCleanup(self.temporary.cleanup)
        self.skill = self.package / SKILL_PATH
        self.source_digests = {name: digest(SOURCE / name) for name in HELPERS}
        for name in HELPERS:
            target = self.skill / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, target)
        self.records = apply_adapter(self.package)
        self.pdf = self.package / "figure.pdf"
        write_pdf(self.pdf)

    def tearDown(self):
        self.assertEqual({name: digest(SOURCE / name) for name in HELPERS}, self.source_digests)

    def helper(self, name):
        suffix = f"{self.id().split('.')[-1]}_{name.replace('/', '_').replace('.', '_')}"
        return load_module(self.skill / name, suffix)

    def test_writable_cache_fallback_does_not_require_unix_or_home(self):
        # Break caught: getuid on Windows and a cache created under the home directory.
        home = self.package / "home-is-a-file"
        home.write_text("leave this path alone", encoding="utf-8")
        temp = self.package / "cache"
        temp.mkdir()
        task_os = SimpleNamespace(environ={}, getpid=lambda: 4242)
        resolver = load_function(self.skill / HELPERS[0], "_ensure_writable_matplotlib_config", {
            "Path": Path, "os": task_os,
            "tempfile": SimpleNamespace(gettempdir=lambda: str(temp)),
        })
        with mock.patch.object(Path, "home", return_value=home):
            try:
                resolver()
            except (AttributeError, OSError) as error:
                self.fail(f"Portable cache fallback failed: {error}")
        selected = Path(task_os.environ.get("MPLCONFIGDIR", ""))
        self.assertTrue(selected.is_relative_to(temp))
        self.assertTrue(selected.is_dir())
        self.assertEqual(home.read_text(encoding="utf-8"), "leave this path alone")

    def test_explicit_cache_setting_is_preserved(self):
        chosen = str(self.package / "explicit-cache")
        task_os = SimpleNamespace(environ={"MPLCONFIGDIR": chosen})
        resolver = load_function(self.skill / HELPERS[0], "_ensure_writable_matplotlib_config", {
            "Path": Path, "os": task_os, "tempfile": None,
        })
        resolver()
        self.assertEqual(task_os.environ["MPLCONFIGDIR"], chosen)

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "Matplotlib is unavailable")
    def test_frontier_default_does_not_connect_unrelated_models(self):
        # Break caught: a default line invents continuity between independent models.
        with mock.patch.dict(os.environ, {"MPLCONFIGDIR": str(self.package / "mpl-cache"), "MPLBACKEND": "Agg"}):
            module = self.helper(HELPERS[0])
            fig, axes = module.new_figure()
            try:
                mask = module.plot_pareto_frontier(axes, [1, 2, 3], [1, 2, 3], ["A", "B", "C"], annotate=False)
                self.assertEqual(mask.tolist(), [True, True, True])
                self.assertEqual(len(axes.lines), 0)
            finally:
                module.plt.close(fig)

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "Matplotlib is unavailable")
    def test_explicit_family_connection_remains_supported(self):
        with mock.patch.dict(os.environ, {"MPLCONFIGDIR": str(self.package / "mpl-cache"), "MPLBACKEND": "Agg"}):
            module = self.helper(HELPERS[0])
            fig, axes = module.new_figure()
            try:
                module.plot_pareto_frontier(axes, [1, 2], [1, 2], ["Family low", "Family high"], connect_frontier=True, annotate=False)
                self.assertEqual(len(axes.lines), 1)
            finally:
                module.plt.close(fig)

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "Matplotlib is unavailable")
    def test_horizontal_comparison_values_clear_errorbar_caps(self):
        # Break caught: annotations start at the estimate and overlap its uncertainty.
        with mock.patch.dict(os.environ, {"MPLCONFIGDIR": str(self.package / "mpl-cache"), "MPLBACKEND": "Agg"}):
            module = self.helper(HELPERS[0])
            fig, axes = module.new_figure(width_mm=85, height_mm=55)
            try:
                bars = module.plot_horizontal_comparison(axes, ["Baseline", "Focal"], [8.0, 12.0], errors=[4.0, 2.0])
                axes.set_xlim(0, 20)
                fig.canvas.draw()
                renderer = fig.canvas.get_renderer()
                self.assertEqual([patch.get_width() for patch in bars.patches], [8.0, 12.0])
                self.assertEqual([text.get_text() for text in axes.texts], ["8.0", "12.0"])
                for text, cap_x, row in zip(axes.texts, [12.0, 14.0], [0, 1]):
                    outer_cap = axes.transData.transform((cap_x, row))[0]
                    self.assertGreater(text.get_window_extent(renderer).x0, outer_cap + 1.0)
                self.assertAlmostEqual(fig.get_figwidth() * 25.4, 85.0)
                self.assertAlmostEqual(fig.get_figheight() * 25.4, 55.0)
            finally:
                module.plt.close(fig)

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "Matplotlib is unavailable")
    def test_bar_labels_clear_signed_vertical_errorbars(self):
        with mock.patch.dict(os.environ, {"MPLCONFIGDIR": str(self.package / "mpl-cache"), "MPLBACKEND": "Agg"}):
            module = self.helper(HELPERS[0])
            fig, axes = module.new_figure(width_mm=85, height_mm=55)
            try:
                bars = axes.bar([0, 1], [-4.0, 4.0], yerr=[1.0, 1.0], capsize=2)
                module.annotate_bar_values(axes, bars)
                axes.set_ylim(-8, 8)
                fig.canvas.draw()
                renderer = fig.canvas.get_renderer()
                negative, positive = axes.texts
                self.assertEqual([negative.get_text(), positive.get_text()], ["-4.0", "4.0"])
                self.assertLess(negative.get_window_extent(renderer).y1, axes.transData.transform((0, -5.0))[1] - 1.0)
                self.assertGreater(positive.get_window_extent(renderer).y0, axes.transData.transform((1, 5.0))[1] + 1.0)
            finally:
                module.plt.close(fig)

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "Matplotlib is unavailable")
    def test_audit_rejects_text_fully_outside_canvas(self):
        # Break caught: an intersection guard hides completely off-canvas text.
        with mock.patch.dict(os.environ, {"MPLCONFIGDIR": str(self.package / "mpl-cache"), "MPLBACKEND": "Agg"}):
            module = self.helper(HELPERS[0])
            fig, axes = module.new_figure(constrained_layout=False)
            try:
                fig.text(1.2, 0.5, "Fully outside")
                report = module.audit_matplotlib_figure(fig)
                self.assertFalse(report.passed)
                self.assertIn("clipped_text", [issue.code for issue in report.issues])
            finally:
                module.plt.close(fig)

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "Matplotlib is unavailable")
    def test_reliability_example_keeps_endpoint_labels_inside_final_canvas(self):
        # Break caught: endpoint labels clip after export at the final PNG DPI.
        with mock.patch.dict(os.environ, {"MPLCONFIGDIR": str(self.package / "mpl-cache"), "MPLBACKEND": "Agg"}):
            module = self.helper(HELPERS[0])
            captured = []
            real_save = module.save_figure

            def capture_save(fig, *args, **kwargs):
                captured.append(fig)
                return real_save(fig, *args, **kwargs)

            with mock.patch.object(module, "save_figure", side_effect=capture_save), mock.patch.dict(sys.modules, {"openai_visuals": module}):
                example = self.helper(HELPERS[4])
                paths = example.build_reliability_curve(self.package / "example-output")
            fig = captured[0]
            try:
                self.assertTrue(all(path.is_file() for path in paths))
                self.assertAlmostEqual(fig.get_figwidth() * 25.4, 85.0)
                self.assertAlmostEqual(fig.get_figheight() * 25.4, 55.0)
                fig.set_dpi(300)
                fig.canvas.draw()
                axes = fig.axes[0]
                self.assertEqual([line.get_ydata().tolist() for line in axes.lines],
                                 [[76, 69, 60, 49, 35], [82, 77, 70, 61, 49], [88, 85, 81, 75, 67]])
                self.assertEqual([text.get_text() for text in axes.texts], ["External baseline", "Prior model", "Focal model"])
                renderer = fig.canvas.get_renderer()
                # Keep a six-point export margin, so backend font metrics do
                # not crop labels that only just fit in an interactive draw.
                export_margin = 6.0 * fig.dpi / 72.0
                for text in axes.texts:
                    self.assertLessEqual(text.get_window_extent(renderer).x1, fig.bbox.x1 - export_margin)
            finally:
                module.plt.close(fig)

    def test_grouped_fractional_numbers_are_parsed(self):
        # Break caught: grouped fractional numbers silently disappear from numeric QA.
        module = self.helper(HELPERS[1])
        cases = [("1,234.50", 1234.5, 2), ("−1,234.50", -1234.5, 2),
                 ("+12,345.6e-2", 123.456, None), ("1,234", 1234.0, 0),
                 ("1234.50", 1234.5, 2), (".5", 0.5, 1)]
        for value, number, decimals in cases:
            with self.subTest(value=value):
                cell = module.parse_numeric(value)
                self.assertIsNotNone(cell)
                self.assertAlmostEqual(cell.value, number)
                self.assertEqual(cell.decimals, decimals)
        self.assertIsNone(module.parse_numeric("12,34.5"))

    def test_grouped_decimal_table_column_participates_in_qa(self):
        module = self.helper(HELPERS[1])
        path = self.package / "grouped-decimals.csv"
        path.write_text('Method,Score\nBaseline,"1,234.50"\nFocal,"2,345.60"\n', encoding="utf-8")
        report = module.inspect_table(path)
        self.assertEqual(report.metadata["numeric_columns"], ["Score"])

    def test_reference_type_annotations_can_be_resolved(self):
        module = self.helper(HELPERS[2])
        try:
            hints = typing.get_type_hints(module.format_markdown)
        except NameError as error:
            self.fail(f"Public helper type annotations do not resolve: {error}")
        self.assertEqual(hints["return"], str)

    def test_missing_pdf_backend_explicitly_fails_incomplete_preflight(self):
        # Break caught: missing PDF inspection dependency is reported as PASS.
        module = self.helper(HELPERS[3])
        with mock.patch.dict(sys.modules, {"fitz": None}):
            report = module.inspect_visual(self.pdf)
        self.assertFalse(report.passed)
        self.assertIn("missing_pdf_dependency", [issue.code for issue in report.issues])
        self.assertFalse(report.metadata.get("pdf_inspection_complete", True))

    def pdf_with_backend(self, pages, minimum=8.0):
        module = self.helper(HELPERS[3])
        backend = SimpleNamespace(open=lambda path: FixtureDocument(pages), Matrix=lambda x, y: (x, y))
        with mock.patch.dict(sys.modules, {"fitz": backend}):
            return module.inspect_visual(self.pdf, min_font_pt=minimum)

    def test_pdf_font_threshold_is_applied_on_later_pages(self):
        # Break caught: PDF font checking is omitted or limited to the first page.
        report = self.pdf_with_backend([FixturePage(12.0), FixturePage(6.0)])
        self.assertFalse(report.passed)
        self.assertIn("small_pdf_text", [issue.code for issue in report.issues])
        self.assertEqual(report.metadata.get("minimum_pdf_font_size_pt"), 6.0)

    def test_pdf_font_threshold_override_reaches_inspector(self):
        report = self.pdf_with_backend([FixturePage(6.0)], minimum=5.5)
        self.assertTrue(report.passed)
        self.assertTrue(report.metadata.get("pdf_inspection_complete", False))

    def test_pdf_render_failure_is_reported_as_incomplete(self):
        # Break caught: successful parsing masks a rasterizer failure.
        report = self.pdf_with_backend([FixturePage(12.0, render_error=True)])
        self.assertFalse(report.passed)
        self.assertIn("pdf_render_failure", [issue.code for issue in report.issues])
        self.assertFalse(report.metadata.get("pdf_inspection_complete", True))

    @unittest.skipUnless(importlib.util.find_spec("fitz"), "PyMuPDF is unavailable; controlled backend tests cover QA branches")
    def test_real_pdf_backend_detects_small_text(self):
        module = self.helper(HELPERS[3])
        write_pdf(self.pdf, font_size=6.0)
        report = module.inspect_visual(self.pdf)
        self.assertFalse(report.passed)
        self.assertIn("small_pdf_text", [issue.code for issue in report.issues])

    def test_adapter_is_idempotent_and_logs_only_active_helpers(self):
        self.assertEqual(len(self.records), 5)
        for record in self.records:
            self.assertTrue(record["path"].startswith(SKILL_PATH.as_posix() + "/"))
            self.assertNotEqual(record["before_sha256"], record["after_sha256"])
        before = {name: digest(self.skill / name) for name in HELPERS}
        self.assertEqual(apply_adapter(self.package), [])
        self.assertEqual({name: digest(self.skill / name) for name in HELPERS}, before)


if __name__ == "__main__":
    unittest.main()
