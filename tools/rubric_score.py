"""Calculate evidence-tracked weighted summaries from a user-supplied rubric.

This tool does not read a manuscript, select criteria, assign ratings, or judge
whether supplied evidence supports a rating. Unscored criteria remain unscored.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import re
import sys

MAX_INPUT_BYTES = 1_000_000
MAX_CRITERIA = 200
MAX_MAGNITUDE = Decimal("1000000")
ROUNDING = Decimal("0.000001")
LIMITATIONS = [
    "The caller supplies all criteria, weights, scores, evidence notes, and rationales; this program does not inspect the manuscript.",
    "Evidence notes and rationales are recorded, not checked for accuracy or adequacy.",
    "A complete arithmetic result does not validate a rubric, establish reviewer agreement, or predict acceptance.",
    "When criteria are unscored, the reported mean covers scored criteria only; it is not a complete rubric score.",
]


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def _reject_constant(value: str):
    raise ValueError(f"invalid JSON number: {value}")


def _fields(value, required: set[str], optional: set[str], label: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    keys = set(value)
    missing = required - keys
    extra = keys - required - optional
    if missing:
        raise ValueError(f"{label} is missing fields: {', '.join(sorted(missing))}")
    if extra:
        raise ValueError(f"{label} has unknown fields: {', '.join(sorted(extra))}")
    return value


def _text(value, label: str, *, required: bool = True, limit: int = 8000) -> str | None:
    if value is None and not required:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{label} must be text")
    if required and not value.strip():
        raise ValueError(f"{label} must not be empty")
    if len(value) > limit or "\x00" in value:
        raise ValueError(f"{label} is too long or contains a null character")
    return value.strip()


def _number(value, label: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError(f"{label} must be a finite JSON number")
    try:
        number = value if isinstance(value, Decimal) else Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{label} must be a finite JSON number") from exc
    if not number.is_finite() or abs(number) > MAX_MAGNITUDE:
        raise ValueError(f"{label} must be finite and within +/- 1000000")
    if not number.is_zero():
        digits = number.as_tuple().digits
        trailing_zeroes = 0
        for digit in reversed(digits):
            if digit:
                break
            trailing_zeroes += 1
        fractional_places = max(0, -number.as_tuple().exponent - trailing_zeroes)
        if fractional_places > 6:
            raise ValueError(f"{label} may have at most 6 fractional decimal places")
    return number


def _rounded(number: Decimal) -> float:
    return float(number.quantize(ROUNDING, rounding=ROUND_HALF_UP))


def score_review(data: dict) -> dict:
    """Validate a rubric document and calculate its weighted summary."""
    document = _fields(data, {"title", "scale", "criteria"}, set(), "rubric")
    title = _text(document["title"], "title", limit=300)

    scale = _fields(document["scale"], {"min", "max"}, set(), "scale")
    minimum = _number(scale["min"], "scale.min")
    maximum = _number(scale["max"], "scale.max")
    if minimum >= maximum:
        raise ValueError("scale.min must be less than scale.max")

    criteria = document["criteria"]
    if not isinstance(criteria, list) or not 1 <= len(criteria) <= MAX_CRITERIA:
        raise ValueError(f"criteria must be a list containing 1 to {MAX_CRITERIA} entries")

    seen: set[str] = set()
    parsed = []
    total_weight = Decimal(0)
    assessed_weight = Decimal(0)
    weighted_sum = Decimal(0)
    assessed_count = 0

    for index, item in enumerate(criteria, 1):
        label = f"criteria[{index}]"
        row = _fields(item, {"id", "label", "weight", "score"},
                      {"evidence", "rationale", "not_assessed_reason"}, label)
        identifier = _text(row["id"], f"{label}.id", limit=80)
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", identifier):
            raise ValueError(f"{label}.id must use letters, digits, dot, underscore, or hyphen")
        if identifier in seen:
            raise ValueError(f"duplicate criterion id: {identifier}")
        seen.add(identifier)

        criterion_name = _text(row["label"], f"{label}.label", limit=500)
        weight = _number(row["weight"], f"{label}.weight")
        if weight <= 0:
            raise ValueError(f"{label}.weight must be greater than zero")
        total_weight += weight

        score = None
        evidence = _text(row.get("evidence"), f"{label}.evidence", required=False)
        rationale = _text(row.get("rationale"), f"{label}.rationale", required=False)
        not_assessed_reason = _text(row.get("not_assessed_reason"),
                                    f"{label}.not_assessed_reason", required=False)
        if row["score"] is not None:
            score = _number(row["score"], f"{label}.score")
            if not minimum <= score <= maximum:
                raise ValueError(f"{label}.score must be between scale.min and scale.max")
            if not evidence:
                raise ValueError(f"{label}.evidence is required when a score is assigned")
            if not rationale:
                raise ValueError(f"{label}.rationale is required when a score is assigned")
            if not_assessed_reason:
                raise ValueError(f"{label}.not_assessed_reason cannot accompany an assigned score")
            assessed_weight += weight
            weighted_sum += weight * score
            assessed_count += 1
        elif evidence or rationale:
            raise ValueError(f"{label}: leave evidence and rationale empty until a score is assigned")

        parsed.append({
            "id": identifier,
            "label": criterion_name,
            "weight": _rounded(weight),
            "score": _rounded(score) if score is not None else None,
            "evidence": evidence or None,
            "rationale": rationale or None,
            "not_assessed_reason": not_assessed_reason,
            "status": "scored" if score is not None else "not_assessed",
        })

    provisional_mean = weighted_sum / assessed_weight if assessed_weight else None
    provisional_position = ((provisional_mean - minimum) / (maximum - minimum) * Decimal(100)
                            if provisional_mean is not None else None)
    complete = assessed_count == len(parsed)
    status = "complete" if complete else "partial" if assessed_count else "not_scored"
    coverage = assessed_weight / total_weight * Decimal(100)
    return {
        "title": title,
        "scale": {"min": _rounded(minimum), "max": _rounded(maximum)},
        "criteria": parsed,
        "summary": {
            "status": status,
            "criteria_scored": assessed_count,
            "criteria_total": len(parsed),
            "weight_coverage_percent": _rounded(coverage),
            "weighted_mean_of_scored_criteria": (
                _rounded(provisional_mean) if provisional_mean is not None else None),
            "scale_position_percent_of_scored_criteria": (
                _rounded(provisional_position) if provisional_position is not None else None),
            "complete_weighted_mean": _rounded(provisional_mean) if complete else None,
            "complete_scale_position_percent": _rounded(provisional_position) if complete else None,
        },
        "not_assessed": [
            {"id": row["id"], "label": row["label"], "weight": row["weight"],
             "reason": row["not_assessed_reason"]}
            for row in parsed if row["status"] == "not_assessed"
        ],
        "limitations": list(LIMITATIONS),
    }


def load_rubric(path: Path) -> dict:
    raw = path.read_bytes()
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError(f"Input exceeds the {MAX_INPUT_BYTES}-byte limit")
    try:
        return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_unique_object,
                          parse_float=Decimal, parse_constant=_reject_constant)
    except UnicodeError as exc:
        raise ValueError("Input must be UTF-8 JSON") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON at line {exc.lineno}, column {exc.colno}") from exc


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rubric", type=Path, help="JSON file containing caller-supplied scores and evidence notes")
    parser.add_argument("--output", "-o", type=Path, help="new report file; existing files are never overwritten")
    args = parser.parse_args(argv)
    try:
        report = score_review(load_rubric(args.rubric))
        rendered = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
            print(f"Wrote report to {args.output}", file=sys.stderr)
        else:
            sys.stdout.write(rendered)
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
