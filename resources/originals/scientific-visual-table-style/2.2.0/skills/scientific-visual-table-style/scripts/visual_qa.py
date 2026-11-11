#!/usr/bin/env python3
"""Preflight SVG, PNG/JPEG/WebP, and PDF visual artifacts.

The tool checks file integrity, dimensions, effective raster resolution,
aspect-ratio drift, vector metadata, embedded raster use, and detectable font
sizes. It cannot replace scientific or final-size human visual review.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

Severity = Literal["error", "warning", "info"]
LENGTH_RE = re.compile(
    r"^\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)\s*(px|pt|pc|mm|cm|in)?\s*$",
    re.IGNORECASE,
)
FONT_STYLE_RE = re.compile(r"(?:^|;)\s*font-size\s*:\s*([^;]+)", re.IGNORECASE)


@dataclass(frozen=True)
class Issue:
    severity: Severity
    code: str
    message: str


@dataclass
class Report:
    path: str
    format: str
    passed: bool = True
    metadata: dict[str, Any] | None = None
    issues: list[Issue] | None = None
    limitations: list[str] | None = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}
        if self.issues is None:
            self.issues = []
        if self.limitations is None:
            self.limitations = []

    def add(self, severity: Severity, code: str, message: str) -> None:
        self.issues.append(Issue(severity, code, message))
        if severity == "error":
            self.passed = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "format": self.format,
            "passed": self.passed,
            "metadata": self.metadata,
            "issues": [asdict(issue) for issue in self.issues],
            "limitations": self.limitations,
        }


def parse_length_to_mm(value: str | None) -> float | None:
    """Parse an SVG/CSS absolute length into millimetres."""

    if value is None:
        return None
    match = LENGTH_RE.match(value)
    if not match:
        return None
    number = float(match.group(1))
    unit = (match.group(2) or "px").lower()
    factors = {
        "px": 25.4 / 96.0,
        "pt": 25.4 / 72.0,
        "pc": 25.4 / 6.0,
        "mm": 1.0,
        "cm": 10.0,
        "in": 25.4,
    }
    return number * factors[unit]


def parse_length_to_pt(value: str | None) -> float | None:
    mm = parse_length_to_mm(value)
    return None if mm is None else mm * 72.0 / 25.4


def parse_svg_font_size_to_pt(
    value: str | None,
    *,
    user_unit_scale_pt: float | None,
) -> float | None:
    """Parse an SVG font size into physical points.

    Matplotlib writes font sizes as ``px`` while its SVG viewBox is expressed
    in point-like user units. When physical root dimensions and a viewBox are
    available, scale user-unit sizes through that mapping instead of assuming
    standalone CSS 96-dpi pixels.
    """

    if value is None:
        return None
    match = LENGTH_RE.match(value)
    if not match:
        return None
    number = float(match.group(1))
    unit = (match.group(2) or "px").lower()
    if unit == "px" and user_unit_scale_pt is not None:
        return number * user_unit_scale_pt
    return parse_length_to_pt(value)


def assess_aspect_ratio(
    report: Report,
    actual_width: float | None,
    actual_height: float | None,
    target_width_mm: float | None,
    target_height_mm: float | None,
) -> None:
    if not all(
        value is not None and value > 0
        for value in (actual_width, actual_height, target_width_mm, target_height_mm)
    ):
        return
    actual_ratio = float(actual_width) / float(actual_height)
    target_ratio = float(target_width_mm) / float(target_height_mm)
    relative_error = abs(actual_ratio / target_ratio - 1.0)
    report.metadata["actual_aspect_ratio"] = actual_ratio
    report.metadata["target_aspect_ratio"] = target_ratio
    report.metadata["aspect_ratio_relative_error"] = relative_error
    if relative_error > 0.10:
        report.add(
            "error",
            "aspect_ratio_mismatch",
            f"Aspect ratio differs from target by {relative_error * 100:.1f}%.",
        )
    elif relative_error > 0.02:
        report.add(
            "warning",
            "aspect_ratio_drift",
            f"Aspect ratio differs from target by {relative_error * 100:.1f}%.",
        )


def inspect_raster(
    path: Path,
    report: Report,
    *,
    target_width_mm: float | None,
    target_height_mm: float | None,
    min_raster_dpi: float,
) -> None:
    try:
        from PIL import Image
    except ImportError:
        report.add("error", "missing_dependency", "Pillow is required to inspect raster images.")
        return

    try:
        with Image.open(path) as image:
            width_px, height_px = image.size
            report.metadata.update(
                {
                    "width_px": width_px,
                    "height_px": height_px,
                    "mode": image.mode,
                    "frames": getattr(image, "n_frames", 1),
                    "embedded_dpi": image.info.get("dpi"),
                }
            )
            assess_aspect_ratio(
                report,
                float(width_px),
                float(height_px),
                target_width_mm,
                target_height_mm,
            )
            if target_width_mm:
                effective_dpi = width_px / (target_width_mm / 25.4)
                report.metadata["effective_dpi_at_target_width"] = effective_dpi
                if effective_dpi < min_raster_dpi:
                    report.add(
                        "error",
                        "low_effective_dpi",
                        f"Effective resolution is {effective_dpi:.0f} dpi at {target_width_mm:g} mm; minimum is {min_raster_dpi:g} dpi.",
                    )
                elif effective_dpi < 300:
                    report.add(
                        "warning",
                        "suboptimal_effective_dpi",
                        f"Effective resolution is {effective_dpi:.0f} dpi; 300 dpi is preferred for manuscript figures.",
                    )
            elif width_px < 900:
                report.add(
                    "warning",
                    "small_raster_width",
                    f"Raster width is only {width_px} px and no target width was supplied.",
                )

            if getattr(image, "n_frames", 1) > 1:
                report.add(
                    "warning",
                    "animated_raster",
                    "Raster contains multiple frames; static publication output should normally contain one frame.",
                )
            if image.mode in {"P", "1"}:
                report.add(
                    "warning",
                    "limited_color_mode",
                    f"Image mode {image.mode!r} may cause antialiasing or palette limitations.",
                )
    except Exception as exc:  # Pillow raises format-specific exceptions.
        report.add("error", "raster_parse_failure", f"Unable to parse raster image: {exc}")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def inspect_svg(
    path: Path,
    report: Report,
    *,
    target_width_mm: float | None,
    target_height_mm: float | None,
    min_font_pt: float,
) -> None:
    try:
        root = ET.parse(path).getroot()
    except Exception as exc:
        report.add("error", "svg_parse_failure", f"Unable to parse SVG XML: {exc}")
        return

    width_attr = root.attrib.get("width")
    height_attr = root.attrib.get("height")
    viewbox_attr = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    width_mm = parse_length_to_mm(width_attr)
    height_mm = parse_length_to_mm(height_attr)
    viewbox = None
    if viewbox_attr:
        try:
            values = [float(value) for value in re.split(r"[ ,]+", viewbox_attr.strip()) if value]
            if len(values) == 4 and values[2] > 0 and values[3] > 0:
                viewbox = values
        except ValueError:
            viewbox = None

    user_unit_scale_pt = None
    if viewbox and width_mm and height_mm:
        width_pt = width_mm * 72.0 / 25.4
        height_pt = height_mm * 72.0 / 25.4
        x_scale = width_pt / viewbox[2]
        y_scale = height_pt / viewbox[3]
        if x_scale > 0 and y_scale > 0:
            user_unit_scale_pt = math.sqrt(x_scale * y_scale)

    report.metadata.update(
        {
            "width_attribute": width_attr,
            "height_attribute": height_attr,
            "width_mm": width_mm,
            "height_mm": height_mm,
            "viewBox": viewbox,
            "user_unit_scale_pt": user_unit_scale_pt,
        }
    )

    if viewbox is None:
        report.add("warning", "missing_viewbox", "SVG has no valid viewBox; responsive scaling may be unreliable.")
    if width_attr is None or height_attr is None:
        report.add("warning", "missing_svg_size", "SVG lacks explicit width or height attributes.")

    if viewbox:
        assess_aspect_ratio(
            report,
            viewbox[2],
            viewbox[3],
            target_width_mm,
            target_height_mm,
        )
    else:
        assess_aspect_ratio(report, width_mm, height_mm, target_width_mm, target_height_mm)

    text_nodes = 0
    image_nodes = 0
    detected_font_sizes: list[float] = []
    font_families: set[str] = set()
    for element in root.iter():
        name = local_name(element.tag)
        if name == "text":
            text_nodes += 1
        elif name == "image":
            image_nodes += 1
        if "font-size" in element.attrib:
            size = parse_svg_font_size_to_pt(
                element.attrib.get("font-size"),
                user_unit_scale_pt=user_unit_scale_pt,
            )
            if size is not None:
                detected_font_sizes.append(size)
        style = element.attrib.get("style", "")
        style_match = FONT_STYLE_RE.search(style)
        if style_match:
            size = parse_svg_font_size_to_pt(
                style_match.group(1).strip(),
                user_unit_scale_pt=user_unit_scale_pt,
            )
            if size is not None:
                detected_font_sizes.append(size)
        family = element.attrib.get("font-family")
        if family:
            font_families.add(family)

    report.metadata.update(
        {
            "text_nodes": text_nodes,
            "embedded_image_nodes": image_nodes,
            "detected_font_sizes_pt": sorted(set(round(size, 3) for size in detected_font_sizes)),
            "font_families": sorted(font_families),
        }
    )

    if image_nodes:
        report.add(
            "warning",
            "embedded_raster",
            f"SVG contains {image_nodes} embedded raster image node(s); verify their effective resolution.",
        )
    if detected_font_sizes:
        minimum = min(detected_font_sizes)
        maximum = max(detected_font_sizes)
        if minimum < min_font_pt:
            if maximum >= min_font_pt and minimum >= 0.65 * min_font_pt:
                report.add(
                    "warning",
                    "small_svg_math_component",
                    f"Detected {minimum:.2f} pt SVG text below the {min_font_pt:.2f} pt body minimum; this may be a math superscript/subscript. Inspect it at final size.",
                )
            else:
                report.add(
                    "error",
                    "small_svg_text",
                    f"Detected SVG font size {minimum:.2f} pt below the {min_font_pt:.2f} pt minimum.",
                )
    elif text_nodes:
        report.add(
            "warning",
            "undetectable_svg_font_size",
            "SVG contains text but no absolute font sizes could be parsed; inspect the final-size render manually.",
        )
    if not text_nodes:
        report.add(
            "info",
            "no_live_text",
            "No SVG <text> nodes detected; labels may have been converted to paths and are not programmatically auditable.",
        )


def inspect_pdf(
    path: Path,
    report: Report,
    *,
    target_width_mm: float | None,
    target_height_mm: float | None,
) -> None:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        report.add(
            "warning",
            "missing_pdf_dependency",
            "PyMuPDF is unavailable; PDF dimensions and embedded images were not inspected.",
        )
        report.limitations.append("Install PyMuPDF for full PDF preflight.")
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
                f"PDF first page contains {len(images)} embedded image object(s); verify no low-resolution rasterization occurred.",
            )
        if not text_blocks:
            report.add(
                "info",
                "no_extractable_pdf_text",
                "No extractable text blocks found; text may be vector paths or the figure may be image-only.",
            )
    finally:
        document.close()


def inspect_visual(
    path: Path,
    *,
    target_width_mm: float | None = None,
    target_height_mm: float | None = None,
    min_raster_dpi: float = 220.0,
    min_font_pt: float = 8.0,
) -> Report:
    """Inspect one visual artifact and return a structured report."""

    suffix = path.suffix.lower().lstrip(".")
    report = Report(path=str(path), format=suffix or "unknown")
    if not path.exists():
        report.add("error", "missing_file", "File does not exist.")
        return report
    if not path.is_file():
        report.add("error", "not_a_file", "Path is not a regular file.")
        return report
    size_bytes = path.stat().st_size
    report.metadata["size_bytes"] = size_bytes
    if size_bytes == 0:
        report.add("error", "empty_file", "File is empty.")
        return report
    if size_bytes < 1024:
        report.add("warning", "very_small_file", f"File size is only {size_bytes} bytes; verify export completeness.")

    if suffix in {"png", "jpg", "jpeg", "webp"}:
        inspect_raster(
            path,
            report,
            target_width_mm=target_width_mm,
            target_height_mm=target_height_mm,
            min_raster_dpi=min_raster_dpi,
        )
    elif suffix == "svg":
        inspect_svg(
            path,
            report,
            target_width_mm=target_width_mm,
            target_height_mm=target_height_mm,
            min_font_pt=min_font_pt,
        )
    elif suffix == "pdf":
        inspect_pdf(
            path,
            report,
            target_width_mm=target_width_mm,
            target_height_mm=target_height_mm,
        )
    else:
        report.add(
            "error",
            "unsupported_format",
            f"Unsupported extension .{suffix}; supported: SVG, PNG, JPEG, WebP, PDF.",
        )

    report.limitations.extend(
        [
            "Programmatic preflight cannot verify scientific correctness or omitted evidence.",
            "Programmatic preflight cannot reliably detect label collisions, hierarchy, or the five-second message.",
            "Inspect a final-size rendered image after the most recent edit.",
        ]
    )
    return report


def render_text(report: Report) -> str:
    status = "PASS" if report.passed else "FAIL"
    lines = [f"{status}: {report.path} ({report.format})"]
    if report.metadata:
        lines.append("Metadata:")
        for key, value in sorted(report.metadata.items()):
            lines.append(f"  {key}: {value}")
    if report.issues:
        lines.append("Findings:")
        for issue in report.issues:
            lines.append(f"  [{issue.severity.upper()}] {issue.code}: {issue.message}")
    if report.limitations:
        lines.append("Limitations:")
        for item in report.limitations:
            lines.append(f"  - {item}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="SVG, PNG/JPEG/WebP, or PDF to inspect.")
    parser.add_argument("--target-width-mm", type=float, default=None)
    parser.add_argument("--target-height-mm", type=float, default=None)
    parser.add_argument("--min-raster-dpi", type=float, default=220.0)
    parser.add_argument("--min-font-pt", type=float, default=8.0)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument("--strict", action="store_true", help="Return failure when warnings are present.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    for name, value in (
        ("target width", args.target_width_mm),
        ("target height", args.target_height_mm),
        ("minimum raster DPI", args.min_raster_dpi),
        ("minimum font size", args.min_font_pt),
    ):
        if value is not None and value <= 0:
            print(f"{name} must be positive", file=sys.stderr)
            return 2

    report = inspect_visual(
        args.path,
        target_width_mm=args.target_width_mm,
        target_height_mm=args.target_height_mm,
        min_raster_dpi=args.min_raster_dpi,
        min_font_pt=args.min_font_pt,
    )
    print(json.dumps(report.to_dict(), indent=2) if args.json else render_text(report))
    if not report.passed:
        return 1
    if args.strict and any(issue.severity == "warning" for issue in report.issues):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
