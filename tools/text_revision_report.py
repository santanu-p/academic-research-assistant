"""Create an offline, readable HTML comparison of two UTF-8 plain-text files.

This is a text-level aid, not a LaTeX-aware or PDF comparison. Inputs are read
only; the report must be a new file. All source text is escaped as HTML.
"""
from __future__ import annotations

import argparse
import difflib
import html
import re
import sys
from pathlib import Path

MAX_BYTES = 1_000_000
MAX_TOKENS = 20_000


def read_tokens(path: Path) -> list[str]:
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"{path}: exceeds {MAX_BYTES} byte limit")
    text = data.decode("utf-8-sig")
    if "\x00" in text:
        raise ValueError(f"{path}: NUL bytes are not supported")
    tokens = re.findall(r"\s+|\S+", text)
    if len(tokens) > MAX_TOKENS:
        raise ValueError(f"{path}: exceeds {MAX_TOKENS} token limit")
    return tokens


def report(before: list[str], after: list[str], old_name: str, new_name: str) -> str:
    pieces = []
    # The standard popularity heuristic avoids pathological work on repeated
    # tokens; it can make the alignment less precise for repetitive prose.
    matcher = difflib.SequenceMatcher(None, before, after, autojunk=True)
    for operation, i, j, k, l in matcher.get_opcodes():
        old = html.escape("".join(before[i:j]))
        new = html.escape("".join(after[k:l]))
        if operation == "equal":
            pieces.append(old)
        else:
            if old:
                pieces.append(f'<del title="Deleted">{old}</del>')
            if new:
                pieces.append(f'<ins title="Added">{new}</ins>')
    return ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<title>Text revision comparison</title><style>"
            "body{font-family:system-ui,sans-serif;max-width:72rem;margin:2rem auto;padding:0 1rem}"
            "pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;line-height:1.6}"
            "del{background:#ffd9d9;text-decoration:line-through}"
            "ins{background:#d8f5d8;text-decoration:underline}"
            "</style></head><body><h1>Text revision comparison</h1>"
            f"<p>Before: {html.escape(old_name)}<br>After: {html.escape(new_name)}</p>"
            "<p>Deletions are struck through; additions are underlined. "
            "Whitespace and punctuation affect alignment. This is a text comparison; "
            "it does not interpret markup, verify scientific meaning, or produce a PDF.</p>"
            "<pre>" + "".join(pieces) + "</pre></body></html>\n")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("output", type=Path, help="New HTML file; existing files are never overwritten")
    args = parser.parse_args(argv)
    try:
        before, after = read_tokens(args.before), read_tokens(args.after)
        rendered = report(before, after, args.before.name, args.after.name)
        with args.output.open("x", encoding="utf-8", newline="") as handle:
            handle.write(rendered)
        print(f"Created {args.output}")
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
