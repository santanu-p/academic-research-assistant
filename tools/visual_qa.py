"""Inspect exported SVG, raster and PDF metadata; optionally render every PDF page.

This is a structural audit. It cannot verify data, semantics, overlap, visual
balance or readability. Missing optional backends produce an incomplete report
and a nonzero CLI exit code, never an apparent pass.
"""
from __future__ import annotations

import argparse
import importlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

LIMITS = ["Cannot verify data, semantics, overlap, reading order or final-size readability.",
          "Inspect every final page or figure visually; metadata is not a scientific quality verdict."]
LENGTH = re.compile(r"^\s*([+]?(?:\d+(?:\.\d*)?|\.\d+))\s*(mm|cm|in|pt|pc|px)?\s*$")


def _length_pt(value):
    match = LENGTH.fullmatch(value or "")
    if not match:
        return None
    scale = {"mm": 72 / 25.4, "cm": 72 / 2.54, "in": 72, "pt": 1, "pc": 12, "px": .75, None: .75}
    number = float(match[1]) * scale[match[2]]
    return number if math.isfinite(number) else None


def inspect_svg(path: str | Path, min_font_pt=8):
    path = Path(path)
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise ValueError(f"Malformed SVG: {exc}") from exc
    if root.tag.split("}")[-1] != "svg":
        raise ValueError("XML root is not svg")
    width, height = (_length_pt(root.get(key)) for key in ("width", "height"))
    notes = []
    viewbox = None
    if root.get("viewBox"):
        try:
            viewbox = [float(value) for value in re.split(r"[\s,]+", root.get("viewBox").strip())]
        except ValueError as exc:
            raise ValueError("SVG viewBox must be numeric") from exc
        if len(viewbox) != 4 or not all(math.isfinite(value) for value in viewbox) or viewbox[2] <= 0 or viewbox[3] <= 0:
            raise ValueError("SVG viewBox needs four finite values with positive dimensions")
    if width is None or height is None or width <= 0 or height <= 0:
        notes.append("Physical dimensions are unavailable or nonpositive; percentages need a containing viewport.")
    if viewbox is None:
        notes.append("No viewBox; coordinate scaling cannot be inspected.")
    external, embedded, text_nodes, sizes, fonts = [], 0, 0, [], set()
    # SVG user units scale with the viewport; pt in a font attribute is CSS pt.
    scale = height / viewbox[3] if height and viewbox else .75
    def walk(node, inherited):
        nonlocal embedded, text_nodes
        style = dict(inherited)
        style.update({key: node.attrib[key] for key in ("font-size", "font-family") if key in node.attrib})
        for part in node.get("style", "").split(";"):
            if ":" in part:
                key, value = part.split(":", 1)
                style[key.strip()] = value.strip()
        tag = node.tag.split("}")[-1]
        if tag in {"text", "tspan"} and node.text and node.text.strip():
            text_nodes += 1
            font = style.get("font-family")
            if font:
                fonts.add(font)
            raw = style.get("font-size", "")
            match = LENGTH.fullmatch(raw)
            if match:
                size = float(match[1]) * scale if match[2] is None else _length_pt(raw) / .75 * scale
                sizes.append({"text": node.text.strip(), "font_pt": size})
            else:
                notes.append("At least one text size cannot be resolved from inline/inherited attributes.")
        href = node.get("href") or node.get("{http://www.w3.org/1999/xlink}href")
        if href:
            if href.startswith("data:"):
                embedded += 1
            elif not href.startswith("#"):
                external.append(href)
        if tag == "style":
            notes.append("Stylesheet rules are not evaluated; font counts may be incomplete.")
        for child in node:
            walk(child, style)
    walk(root, {})
    if not text_nodes:
        notes.append("No live text found; text may be absent or converted to paths, so font sizes cannot be verified.")
    return {"format": "svg", "status": "complete", "physical_mm": [value / 72 * 25.4 if value is not None else None for value in (width, height)],
            "viewbox": viewbox, "live_text_nodes": text_nodes, "font_families": sorted(fonts),
            "small_text": [item for item in sizes if item["font_pt"] < min_font_pt], "minimum_font_pt": min_font_pt,
            "external_references": external, "embedded_resources": embedded, "notes": list(dict.fromkeys(notes)), "limits": LIMITS}


def inspect_raster(path: str | Path):
    try:
        from PIL import Image
    except ImportError:
        return {"format": "raster", "status": "incomplete", "error": "Pillow is required to inspect raster images", "limits": LIMITS}
    with Image.open(path) as image:
        image.load()
        dpi = image.info.get("dpi")
        return {"format": image.format, "status": "complete", "pixels": list(image.size), "mode": image.mode,
                "dpi": list(dpi) if isinstance(dpi, tuple) else dpi,
                "notes": [] if dpi else ["DPI metadata is missing; physical print dimensions are unknown."], "limits": LIMITS}


def inspect_pdf(path: str | Path, min_font_pt=8, render_dir: str | Path | None = None, dpi=120):
    try:
        try:
            backend = importlib.import_module("pymupdf")
        except ImportError:
            backend = importlib.import_module("fitz")
        if not hasattr(backend, "open") or not hasattr(backend, "Matrix"):
            raise ImportError("The imported fitz module is not PyMuPDF")
    except ImportError:
        return {"format": "pdf", "status": "incomplete", "error": "PyMuPDF is required for all-page PDF font inspection and rendering", "limits": LIMITS}
    if not math.isfinite(float(dpi)) or dpi <= 0:
        raise ValueError("render DPI must be positive and finite")
    output = Path(render_dir) if render_dir else None
    if output:
        output.mkdir(parents=True, exist_ok=True)
    pages = []
    with backend.open(path) as document:
        if document.needs_pass:
            raise ValueError("Encrypted PDF needs a password")
        for index, page in enumerate(document):
            spans = [span for block in page.get_text("dict")["blocks"] for line in block.get("lines", []) for span in line["spans"] if span.get("text", "").strip()]
            fonts = page.get_fonts(full=True)
            font_metadata = [{"xref": font[0], "extension": font[1], "type": font[2], "name": font[3],
                              "embedded": bool(document.extract_font(font[0])[3]) if font[0] else None} for font in fonts]
            result = {"page": index + 1, "size_mm": [page.rect.width / 72 * 25.4, page.rect.height / 72 * 25.4],
                      "fonts": font_metadata, "text_spans": len(spans),
                      "small_text": [{"text": span["text"], "font_pt": span["size"]} for span in spans if span["size"] < min_font_pt],
                      "notes": [] if spans else ["No extractable text; fonts may be outlined or scanned and cannot be checked."]}
            if output:
                rendered = output / f"page-{index + 1:03}.png"
                page.get_pixmap(matrix=backend.Matrix(dpi / 72, dpi / 72), alpha=False).save(str(rendered))
                result["render"] = str(rendered)
            pages.append(result)
    return {"format": "pdf", "status": "complete", "pages": pages, "page_count": len(pages), "minimum_font_pt": min_font_pt, "limits": LIMITS}


def analyze_file(path: str | Path, min_font_pt=8, render_dir=None, dpi=120):
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"File does not exist: {path}")
    if not math.isfinite(float(min_font_pt)) or min_font_pt <= 0:
        raise ValueError("minimum font size must be positive and finite")
    if path.suffix.lower() == ".svg":
        report = inspect_svg(path, min_font_pt)
    elif path.suffix.lower() == ".pdf":
        report = inspect_pdf(path, min_font_pt, render_dir, dpi)
    elif path.suffix.lower() in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp", ".bmp"}:
        report = inspect_raster(path)
    else:
        raise ValueError("Supported formats: SVG, PDF, PNG, JPEG, TIFF, WebP, BMP")
    return {"file": str(path), **report}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--min-font-pt", type=float, default=8)
    parser.add_argument("--render-dir", type=Path)
    parser.add_argument("--dpi", type=float, default=120)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = analyze_file(args.file, args.min_font_pt, args.render_dir, args.dpi)
        print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else
              f"{report['format']}: inspection {report['status']}.\n" + "\n".join(report.get("notes", []) + report["limits"]))
        return 0 if report["status"] == "complete" else 3
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"status": "incomplete", "error": str(exc)}) if args.json else f"Inspection incomplete: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
