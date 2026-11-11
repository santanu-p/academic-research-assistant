#!/usr/bin/env python3
"""Select form-matched visual references from the bundled OpenAI corpus.

Examples
--------
python select_references.py --query "cost latency pareto frontier" --limit 5
python select_references.py --form heatmap --max-tier 3 --format json
python select_references.py --tag "benchmark table" --require-direct-asset
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

TOKEN_RE = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class ScoredReference:
    score: float
    row: dict[str, Any]
    reasons: tuple[str, ...]


def tokenize(text: str) -> set[str]:
    """Return normalized alphanumeric search tokens."""

    return set(TOKEN_RE.findall(text.lower()))


def parse_tier(value: str) -> int:
    """Extract the leading numeric tier from a reference-tier string."""

    match = re.match(r"\s*([1-9][0-9]*)", value or "")
    return int(match.group(1)) if match else 99


def rank_value(row: dict[str, Any]) -> int | None:
    value = row.get("recommended_rank")
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def load_corpus(path: Path) -> list[dict[str, Any]]:
    """Load and validate the JSONL corpus."""

    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"Line {line_number} is not a JSON object")
            rows.append(row)
    return rows


def score_reference(
    row: dict[str, Any],
    *,
    query_tokens: set[str],
    form_tokens: set[str],
    tag_tokens: set[str],
    require_direct_asset: bool,
) -> ScoredReference | None:
    """Score a reference using transparent deterministic heuristics."""

    if require_direct_asset and not row.get("direct_asset_url"):
        return None

    tier = parse_tier(str(row.get("reference_tier", "")))
    score = max(0.0, 50.0 - 10.0 * (tier - 1))
    reasons = [f"tier {tier}"]

    rank = rank_value(row)
    if rank is not None:
        rank_bonus = max(0.0, 26.0 - float(rank))
        score += rank_bonus
        reasons.append(f"top-{rank}")

    title_tokens = tokenize(str(row.get("title_caption", "")))
    type_tokens = tokenize(str(row.get("visual_type", "")))
    tag_field_tokens = tokenize(str(row.get("design_tags", "")))
    demonstration_tokens = tokenize(str(row.get("what_it_demonstrates", "")))
    publication_tokens = tokenize(str(row.get("source_publication", "")))

    if query_tokens:
        title_overlap = query_tokens & title_tokens
        type_overlap = query_tokens & type_tokens
        tag_overlap = query_tokens & tag_field_tokens
        prose_overlap = query_tokens & demonstration_tokens
        publication_overlap = query_tokens & publication_tokens
        score += 8.0 * len(title_overlap)
        score += 7.0 * len(type_overlap)
        score += 6.0 * len(tag_overlap)
        score += 2.0 * len(prose_overlap)
        score += 1.0 * len(publication_overlap)
        if title_overlap:
            reasons.append(f"title:{','.join(sorted(title_overlap))}")
        if type_overlap:
            reasons.append(f"type:{','.join(sorted(type_overlap))}")
        if tag_overlap:
            reasons.append(f"tags:{','.join(sorted(tag_overlap))}")

    if form_tokens:
        overlap = form_tokens & (type_tokens | tag_field_tokens)
        if not overlap:
            return None
        score += 12.0 * len(overlap)
        reasons.append(f"form:{','.join(sorted(overlap))}")

    if tag_tokens:
        overlap = tag_tokens & tag_field_tokens
        if not overlap:
            return None
        score += 10.0 * len(overlap)
        reasons.append(f"tag-filter:{','.join(sorted(overlap))}")

    if row.get("direct_asset_url"):
        score += 3.0
        reasons.append("direct asset")
    precision = str(row.get("link_precision", "")).lower()
    if "exact" in precision or "direct" in precision:
        score += 2.0
        reasons.append("precise link")

    if query_tokens and not (
        query_tokens
        & (
            title_tokens
            | type_tokens
            | tag_field_tokens
            | demonstration_tokens
            | publication_tokens
        )
    ):
        score -= 20.0

    return ScoredReference(score=score, row=row, reasons=tuple(reasons))


def select_references(
    rows: Iterable[dict[str, Any]],
    *,
    query: str = "",
    form: str = "",
    tags: Iterable[str] = (),
    max_tier: int = 4,
    limit: int = 5,
    require_direct_asset: bool = False,
) -> list[ScoredReference]:
    """Return the highest-scoring references under the supplied constraints."""

    if max_tier < 1:
        raise ValueError("max_tier must be >= 1")
    if limit < 1:
        raise ValueError("limit must be >= 1")
    query_tokens = tokenize(query)
    form_tokens = tokenize(form)
    tag_tokens = tokenize(" ".join(tags))

    scored: list[ScoredReference] = []
    for row in rows:
        if parse_tier(str(row.get("reference_tier", ""))) > max_tier:
            continue
        result = score_reference(
            row,
            query_tokens=query_tokens,
            form_tokens=form_tokens,
            tag_tokens=tag_tokens,
            require_direct_asset=require_direct_asset,
        )
        if result is not None:
            scored.append(result)

    scored.sort(
        key=lambda item: (
            -item.score,
            rank_value(item.row) if rank_value(item.row) is not None else 9999,
            str(item.row.get("source_publication", "")).lower(),
            str(item.row.get("title_caption", "")).lower(),
        )
    )
    return scored[:limit]


def format_markdown(results: Sequence[ScoredReference]) -> str:
    """Render selected references as a compact Markdown table."""

    lines = [
        "| Score | ID | Visual | Type | Tier | Link | Direct asset |",
        "|---:|---|---|---|---:|---|---|",
    ]
    for item in results:
        row = item.row
        title = str(row.get("title_caption", "")).replace("|", "\\|")
        visual_type = str(row.get("visual_type", "")).replace("|", "\\|")
        source = row.get("exact_or_closest_url") or row.get("parent_url")
        link = f"[source]({source})" if source else "—"
        asset = f"[asset]({row['direct_asset_url']})" if row.get("direct_asset_url") else "—"
        lines.append(
            f"| {item.score:.1f} | {row.get('id', '')} | {title} | {visual_type} | "
            f"{parse_tier(str(row.get('reference_tier', '')))} | {link} | {asset} |"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--library",
        type=Path,
        default=root / "references" / "openai_visual_reference_library.jsonl",
        help="Path to the JSONL corpus.",
    )
    parser.add_argument("--query", default="", help="Free-text retrieval query.")
    parser.add_argument("--form", default="", help="Required visual form/type tokens.")
    parser.add_argument("--tag", action="append", default=[], help="Required design tag token(s); repeatable.")
    parser.add_argument("--max-tier", type=int, default=4, help="Maximum provenance tier to include.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum references returned.")
    parser.add_argument("--require-direct-asset", action="store_true", help="Return only rows with direct SVG/PNG assets.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json", "jsonl"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument("--show-reasons", action="store_true", help="Include scoring reasons in JSON output.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.library.exists():
        print(f"Corpus not found: {args.library}", file=sys.stderr)
        return 2
    try:
        corpus = load_corpus(args.library)
        results = select_references(
            corpus,
            query=args.query,
            form=args.form,
            tags=args.tag,
            max_tier=args.max_tier,
            limit=args.limit,
            require_direct_asset=args.require_direct_asset,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not results:
        print("No references matched the supplied constraints.", file=sys.stderr)
        return 1

    if args.format == "markdown":
        print(format_markdown(results))
    elif args.format == "json":
        payload = []
        for item in results:
            record = dict(item.row)
            record["retrieval_score"] = item.score
            if args.show_reasons:
                record["retrieval_reasons"] = list(item.reasons)
            payload.append(record)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for item in results:
            record = dict(item.row)
            record["retrieval_score"] = item.score
            if args.show_reasons:
                record["retrieval_reasons"] = list(item.reasons)
            print(json.dumps(record, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
