"""Advisory prose measurements, without authorship or quality classification.

Run ``python -X utf8 -B tools/prose_metrics.py FILE --json``. LaTeX is read
as one file: includes, macros, bibliographies and rendered reading order are
not resolved. Markdown and TeX stripping is deliberately conservative.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

LIMITS = [
    "Counts are advisory measurements, not a quality score or AI detector.",
    "Markdown and LaTeX stripping is heuristic; custom macros and nested markup may affect counts.",
    "LaTeX includes, bibliographies, macro expansion and rendered reading order are not resolved.",
    "Sentence splitting is approximate, especially for abbreviations and multilingual prose.",
]
WORD = re.compile(r"[^\W\d_]+(?:[’'\-][^\W\d_]+)*", re.UNICODE)
NUMBER = re.compile(r"(?<!\w)[+−-]?(?:\d+(?:[.,]\d+)*|\.\d+)(?:[eE][+−-]?\d+)?(?:\s*%)?")


def prose_text(text: str, format: str = "plain") -> str:
    """Remove common protected regions while preserving paragraph breaks."""
    if format not in {"plain", "markdown", "latex"}:
        raise ValueError("format must be plain, markdown, or latex")
    if format == "markdown":
        text = re.sub(r"(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1[^\n]*$", "\n", text)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        text = re.sub(r"`+[^`\n]*`+", "", text)
        text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
        text = re.sub(r"(?m)^\s{0,3}(?:#{1,6}|>|[-*+]\s|\d+[.)]\s)\s*", "", text)
    if format == "latex":
        text = re.sub(r"(?m)(?<!\\)%[^\n]*", "", text)
        text = re.sub(r"\\begin\{(verbatim\*?|lstlisting|minted|equation\*?|align\*?|gather\*?|displaymath)\}.*?\\end\{\1\}", "\n", text, flags=re.S)
        text = re.sub(r"\\verb(.).*?\1", "", text)
        text = re.sub(r"\\(?:label|ref|eqref|cite\w*|bibliography|bibliographystyle|include|input)\*?(?:\[[^\]]*\])?\{[^}]*\}", "", text)
    if format in {"markdown", "latex"}:
        text = re.sub(r"(?s)(?<!\\)\$\$.*?(?<!\\)\$\$|\\\[.*?\\\]|\\\(.*?\\\)", " ", text)
        text = re.sub(r"(?<!\\)\$(?:\\.|[^$])*?(?<!\\)\$", " ", text)
    if format == "latex":
        text = re.sub(r"\\(?:begin|end)\{[^}]*\}", "", text)
        text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", "", text)
        text = text.replace("{", "").replace("}", "").replace("~", " ")
    return text


def _summary(values: list[int]) -> dict:
    return {"count": len(values), "minimum": min(values, default=0),
            "maximum": max(values, default=0), "mean": statistics.mean(values) if values else 0,
            "median": statistics.median(values) if values else 0}


def analyze_text(text: str, format: str = "plain", short_paragraph_words: int | None = None) -> dict:
    """Return descriptive measurements. No value is treated as a pass/fail threshold."""
    if short_paragraph_words is not None and short_paragraph_words < 1:
        raise ValueError("short_paragraph_words must be positive")
    cleaned = prose_text(text, format)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", cleaned) if WORD.search(p)]
    # A decimal point is not a sentence boundary. Splitting requires whitespace.
    sentences = [s for s in re.split(r"(?<=[.!?])\s+(?=[\"'‘“(]*[A-ZÀ-ÖØ-Þ])", cleaned) if WORD.search(s)]
    lengths = [len(WORD.findall(p)) for p in paragraphs]
    words = WORD.findall(cleaned)
    numbers = NUMBER.findall(cleaned)
    report = {"format": format, "words": len(words), "characters": len(cleaned),
              "sentences": _summary([len(WORD.findall(s)) for s in sentences]),
              "paragraphs": _summary(lengths), "paragraph_word_counts": lengths,
              "numeric_expressions": len(numbers),
              "numeric_expressions_per_100_words": 100 * len(numbers) / len(words) if words else 0,
              "shortest_paragraphs": [{"paragraph": i + 1, "words": n} for i, n in sorted(enumerate(lengths), key=lambda row: (row[1], row[0]))[:5]],
              "limits": LIMITS}
    if short_paragraph_words is not None:
        report["short_paragraphs"] = {"user_threshold_words": short_paragraph_words,
                                      "paragraphs": [i + 1 for i, n in enumerate(lengths) if n <= short_paragraph_words]}
    return report


def analyze_file(path: str | Path, format: str = "auto", **kwargs) -> dict:
    path = Path(path)
    if format == "auto":
        format = {".tex": "latex", ".md": "markdown", ".markdown": "markdown"}.get(path.suffix.lower(), "plain")
    return {"file": str(path), **analyze_text(path.read_text(encoding="utf-8-sig"), format, **kwargs)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--format", choices=["auto", "plain", "markdown", "latex"], default="auto")
    parser.add_argument("--exemplar", type=Path, help="Optional author-supplied sample; report descriptive differences only")
    parser.add_argument("--short-paragraph-words", type=int, help="User-selected advisory cutoff; no default quality threshold")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = analyze_file(args.file, args.format, short_paragraph_words=args.short_paragraph_words)
        if args.exemplar:
            exemplar = analyze_file(args.exemplar)
            report["exemplar"] = exemplar
            report["difference_from_exemplar"] = {"mean_sentence_words": report["sentences"]["mean"] - exemplar["sentences"]["mean"], "mean_paragraph_words": report["paragraphs"]["mean"] - exemplar["paragraphs"]["mean"]}
        print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else
              f"{report['words']} words; {report['sentences']['count']} approximate sentences; {report['paragraphs']['count']} paragraphs.\n" + "\n".join(LIMITS))
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False) if args.json else f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
