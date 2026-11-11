"""Apply narrow compatibility fixes to active scientific-visual helper copies.

The builder calls ``adapt_visuals(package_root)`` after copying the skill.
Nothing in originals or provenance is an edit target. Every change has hashes
and a reason, and a repeated call leaves already adapted files untouched.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path


SKILL_PATH = Path("skills/visuals-scientific-visual-table-style")

_CACHE_RESOLVER = '''def _ensure_writable_matplotlib_config() -> None:
    """Respect an explicit cache or use a portable writable temporary cache."""

    # Active adapter: portable-mpl-cache. Avoid home writes and Unix-only APIs.
    if os.environ.get("MPLCONFIGDIR"):
        return
    fallback = Path(tempfile.gettempdir()) / f"academic_research_mplconfig_{os.getpid()}"
    fallback.mkdir(parents=True, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(fallback)
'''

_PDF_INSPECTOR = '''def inspect_pdf(
    path: Path,
    report: Report,
    *,
    target_width_mm: float | None,
    target_height_mm: float | None,
    min_font_pt: float = 8.0,
) -> None:
    """Preflight PDF rendering and extractable text sizes on every page."""

    # Active adapter: explicit-pdf-preflight. A skipped render cannot pass.
    report.metadata["pdf_inspection_complete"] = False
    report.metadata["pdf_pages_rendered"] = 0
    report.metadata["pdf_font_inspection_complete"] = False
    try:
        import fitz  # PyMuPDF
    except ImportError:
        report.add(
            "error",
            "missing_pdf_dependency",
            "PyMuPDF is unavailable; PDF render and font preflight are incomplete.",
        )
        report.limitations.append("Install or select a runtime with PyMuPDF to complete PDF preflight.")
        return

    try:
        document = fitz.open(path)
    except Exception as exc:
        report.add("error", "pdf_parse_failure", f"Unable to parse PDF: {exc}")
        return

    try:
        page_count = len(document)
        report.metadata["page_count"] = page_count
        if page_count == 0:
            report.add("error", "empty_pdf", "PDF contains no pages.")
            return
        if page_count > 1:
            report.add(
                "warning",
                "multipage_pdf",
                f"PDF contains {page_count} pages; a standalone figure normally contains one page.",
            )
        page = document[0]
        rect = page.rect
        width_pt, height_pt = float(rect.width), float(rect.height)
        width_mm = width_pt * 25.4 / 72.0
        height_mm = height_pt * 25.4 / 72.0
        images = page.get_images(full=True)
        text_blocks = page.get_text("blocks")
        report.metadata.update(
            {
                "page_width_pt": width_pt,
                "page_height_pt": height_pt,
                "page_width_mm": width_mm,
                "page_height_mm": height_mm,
                "embedded_images_first_page": len(images),
                "text_blocks_first_page": len(text_blocks),
            }
        )
        assess_aspect_ratio(report, width_pt, height_pt, target_width_mm, target_height_mm)
        if images:
            report.add(
                "info",
                "pdf_embedded_images",
                f"PDF first page contains {len(images)} embedded image object(s); verify their effective resolution.",
            )
        if not text_blocks:
            report.add(
                "info",
                "no_extractable_pdf_text",
                "No extractable text blocks found on the first page; labels may be paths or raster content.",
            )

        font_sizes: list[float] = []
        for page_index in range(page_count):
            current = document[page_index]
            try:
                # In-memory rasterization confirms the optional renderer works.
                # It does not substitute for inspecting the delivered render.
                current.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), alpha=False)
            except Exception as exc:
                report.add(
                    "error",
                    "pdf_render_failure",
                    f"Unable to render PDF page {page_index + 1}; preflight is incomplete: {exc}",
                )
                return
            report.metadata["pdf_pages_rendered"] += 1
            for block in current.get_text("dict").get("blocks", []):
                if block.get("type", 0) != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if not str(span.get("text", "")).strip():
                            continue
                        size = float(span.get("size", 0.0))
                        if math.isfinite(size) and size > 0:
                            font_sizes.append(size)

        report.metadata["detected_pdf_font_sizes_pt"] = sorted({round(size, 3) for size in font_sizes})
        report.metadata["pdf_font_inspection_complete"] = bool(font_sizes)
        if font_sizes:
            minimum = min(font_sizes)
            report.metadata["minimum_pdf_font_size_pt"] = minimum
            report.metadata["pdf_inspection_complete"] = True
            if minimum < min_font_pt - 1e-6:
                report.add(
                    "error",
                    "small_pdf_text",
                    f"Detected PDF text {minimum:.2f} pt below the {min_font_pt:.2f} pt minimum; inspect mathematical scripts and any permitted exception at final size.",
                )
        else:
            report.add(
                "warning",
                "uninspectable_pdf_font_size",
                "PDF renders, but no extractable font sizes are available; font preflight is incomplete.",
            )
            report.limitations.append("Inspect path-based or rasterized PDF labels manually at final size.")
    except Exception as exc:
        report.metadata["pdf_inspection_complete"] = False
        report.add("error", "pdf_inspection_failure", f"PDF preflight is incomplete: {exc}")
    finally:
        document.close()
'''


def _replace_once(source: str, old: str, new: str, label: str) -> str:
    if new in source:
        return source
    if source.count(old) != 1:
        raise ValueError(f"Cannot safely apply {label}: expected one source anchor")
    return source.replace(old, new, 1)


def _replace_function(source: str, name: str, replacement: str, marker: str) -> str:
    if marker in source:
        return source
    functions = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(functions) != 1:
        raise ValueError(f"Expected one function named {name}")
    node = functions[0]
    lines = source.splitlines(keepends=True)
    return "".join(lines[: node.lineno - 1]) + replacement + "".join(lines[node.end_lineno :])


def adapt_visuals(package_root: Path) -> list[dict]:
    """Adapt active helpers and examples with auditable per-file change records.

    Source anchors are deliberately strict: an unfamiliar upstream version
    fails before any write. Symlinks/junctions cannot redirect edits outside
    the actual active skill directory. No optional dependency is imported.
    """

    package_root = Path(package_root).resolve(strict=True)
    skill_root = package_root / SKILL_PATH
    if not skill_root.is_dir():
        raise FileNotFoundError(f"Active visual skill is missing: {skill_root}")
    if skill_root.resolve(strict=True) != skill_root:
        raise ValueError("Active visual skill cannot be a symlink or junction")

    operations = {
        "templates/openai_visuals.py": [
            "Use a writable temporary Matplotlib cache without home-directory writes or os.getuid.",
            "Default to unconnected frontier points; explicit family connections remain available.",
            "Place estimate labels beyond outward error-bar endpoints without changing their values.",
            "Report text completely outside the figure canvas as clipped.",
        ],
        "scripts/table_qa.py": ["Recognize grouped fractional numbers such as 1,234.50 in numeric-table QA."],
        "scripts/select_references.py": ["Import Sequence so public helper annotations resolve."],
        "scripts/visual_qa.py": [
            "Fail PDF preflight explicitly when the PDF backend or rasterizer is unavailable.",
            "Propagate the requested font minimum and inspect extractable text sizes on every PDF page.",
        ],
        "examples/example_openai_visuals.py": [
            "Reserve export margin for reliability-curve endpoint labels while retaining all values and final figure dimensions.",
        ],
    }
    pending: list[tuple[Path, str, bytes, list[str]]] = []
    for relative, changes in operations.items():
        target = skill_root / relative
        if not target.is_file() or target.resolve(strict=True) != target:
            raise ValueError(f"Expected a regular active helper: {target}")
        raw = target.read_bytes()
        source = raw.decode("utf-8")
        if relative == "templates/openai_visuals.py":
            changed = _replace_function(source, "_ensure_writable_matplotlib_config", _CACHE_RESOLVER, "Active adapter: portable-mpl-cache")
            changed = _replace_once(changed, "    connect_frontier: bool = True,", "    connect_frontier: bool = False,", "safe frontier default")
            old_loop = "    for patch in bars.patches:\n"
            new_loop = '''    # Active adapter: estimate-label-errorbar-clearance.
    error_segments = []
    if getattr(bars, "errorbar", None) is not None:
        error_segments = [collection.get_segments() for collection in bars.errorbar.lines[2]]
    for index, patch in enumerate(bars.patches):
'''
            changed = _replace_once(changed, old_loop, new_loop, "error-bar label iteration")
            old_vertical = '''            y = patch.get_y() + value
            va = "bottom" if value >= 0 else "top"
'''
            new_vertical = '''            y = patch.get_y() + value
            for segments in error_segments:
                if index < len(segments):
                    segment = np.asarray(segments[index], dtype=float)
                    if segment.shape == (2, 2) and np.isfinite(segment).all() and np.allclose(segment[:, 0], x):
                        y = max(y, float(segment[:, 1].max())) if value >= 0 else min(y, float(segment[:, 1].min()))
            va = "bottom" if value >= 0 else "top"
'''
            changed = _replace_once(changed, old_vertical, new_vertical, "vertical error-bar clearance")
            old_horizontal = '''            y = patch.get_y() + patch.get_height() / 2.0
            ha = "left" if value >= 0 else "right"
'''
            new_horizontal = '''            y = patch.get_y() + patch.get_height() / 2.0
            for segments in error_segments:
                if index < len(segments):
                    segment = np.asarray(segments[index], dtype=float)
                    if segment.shape == (2, 2) and np.isfinite(segment).all() and np.allclose(segment[:, 1], y):
                        x = max(x, float(segment[:, 0].max())) if value >= 0 else min(x, float(segment[:, 0].min()))
            ha = "left" if value >= 0 else "right"
'''
            changed = _replace_once(changed, old_horizontal, new_horizontal, "horizontal error-bar clearance")
            old_clip = '''            intersects_canvas = not (
                bbox.x1 < figure_bbox.x0
                or bbox.x0 > figure_bbox.x1
                or bbox.y1 < figure_bbox.y0
                or bbox.y0 > figure_bbox.y1
            )
            if intersects_canvas and (
                bbox.x0 < figure_bbox.x0 - tolerance_px
'''
            new_clip = '''            # Active adapter: fully-outside-text-is-clipped.
            if (
                bbox.x0 < figure_bbox.x0 - tolerance_px
'''
            changed = _replace_once(changed, old_clip, new_clip, "fully outside canvas text detection")
        elif relative == "scripts/table_qa.py":
            changed = _replace_once(source, r"(?:\d{1,3}(?:,\d{3})+|\d+|\d*\.\d+)", r"(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+|\d*\.\d+)", "grouped fractional numbers")
        elif relative == "scripts/select_references.py":
            changed = _replace_once(source, "from typing import Any, Iterable", "from typing import Any, Iterable, Sequence", "Sequence import")
        elif relative == "scripts/visual_qa.py":
            changed = _replace_function(source, "inspect_pdf", _PDF_INSPECTOR, "Active adapter: explicit-pdf-preflight")
            old_call = '''    elif suffix == "pdf":
        inspect_pdf(
            path,
            report,
            target_width_mm=target_width_mm,
            target_height_mm=target_height_mm,
        )'''
            new_call = old_call.replace("            target_height_mm=target_height_mm,\n", "            target_height_mm=target_height_mm,\n            min_font_pt=min_font_pt,\n")
            changed = _replace_once(changed, old_call, new_call, "PDF font-minimum forwarding")
        else:
            changed = _replace_once(
                source,
                "    ax.set_xlim(0.5, 19)\n",
                '''    ax.set_xlim(0.5, 19)
    # Active adapter: reserve six physical points beyond endpoint labels.
    export_margin_fraction = (6.0 / 72.0) / fig.get_figwidth()
    fig.get_layout_engine().set(rect=(0.0, 0.0, 1.0 - export_margin_fraction, 1.0))
''',
                "reliability endpoint export margin",
            )
        if changed != source:
            compile(changed, str(target), "exec")
            pending.append((target, changed, raw, changes))

    records = []
    for target, changed, raw, changes in pending:
        after = changed.encode("utf-8")
        target.write_bytes(after)
        records.append({
            "path": target.relative_to(package_root).as_posix(),
            "kind": "active_visual_helper_adaptation",
            "changes": changes,
            "before_sha256": hashlib.sha256(raw).hexdigest(),
            "after_sha256": hashlib.sha256(after).hexdigest(),
        })
    return records
