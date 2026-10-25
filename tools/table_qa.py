"""Inspect CSV/TSV structure, numeric notation and missingness using only stdlib.

Numeric recognition is a notation check, not inference of a column's meaning.
Quoted grouped numbers are supported. A locale must be chosen explicitly.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

MISSING = {"", "na", "n/a", "null", "none", "nan", "—", "–", ".."}
LIMITS = ["Cannot verify data accuracy, scientific meaning, units, significant figures, or whether missingness is justified.",
          "Precision notes describe written decimal places, not measurement precision; scientific exponents are retained separately.",
          "Numeric locale is explicit; mixed locales, ranges and custom notations may be classified as text."]


def parse_number(cell: str, decimal: str = ".", grouping: str = ",") -> dict | None:
    """Parse signed/grouped/scientific values, ± errors and last-digit (12) errors.

    Return None for text. Missing tokens return ``{'missing': True}``.
    Parenthesized uncertainty follows the last written decimal place and exponent.
    """
    if decimal not in {".", ","} or grouping == decimal or len(grouping) > 1:
        raise ValueError("decimal must be '.' or ',' and grouping a different single character or empty")
    raw = cell.strip().replace("−", "-")
    if raw.casefold() in MISSING:
        return {"missing": True}
    d, g = re.escape(decimal), re.escape(grouping)
    integer = rf"(?:\d{{1,3}}(?:{g}\d{{3}})+|\d+)" if grouping else r"\d+"
    atom = rf"[+-]?(?:{integer}(?:{d}\d*)?|{d}\d+)(?:[eE][+-]?\d+)?"
    match = re.fullmatch(rf"(?P<value>{atom})(?:\s*(?:±|\+/-)\s*(?P<uncertainty>{atom})|\((?P<digits>\d+)\))?\s*(?P<unit>%|[A-Za-zµμ°][A-Za-z0-9µμ°/^·* -]*)?", raw)
    if not match:
        return None
    def value(token):
        normalized = token.replace(grouping, "") if grouping else token
        return Decimal(normalized.replace(decimal, "."))
    try:
        number = value(match["value"])
        mantissa, _, exponent = re.split(r"([eE])", match["value"], maxsplit=1) if re.search(r"[eE]", match["value"]) else (match["value"], "", "0")
        places = len(mantissa.split(decimal, 1)[1]) if decimal in mantissa else 0
        uncertainty = value(match["uncertainty"]) if match["uncertainty"] else Decimal(match["digits"]) * Decimal(10) ** (int(exponent) - places) if match["digits"] else None
        if uncertainty is not None and uncertainty < 0:
            return None
        return {"missing": False, "value": str(number), "decimal_places": places,
                "exponent": int(exponent), "uncertainty": str(uncertainty) if uncertainty is not None else None,
                "unit": match["unit"] or ""}
    except (InvalidOperation, OverflowError, ValueError):
        return None


def analyze_text(text: str, delimiter: str = ",", decimal: str = ".", grouping: str = ",") -> dict:
    if delimiter not in {",", "\t", ";", "|"}:
        raise ValueError("supported delimiters: comma, tab, semicolon, pipe")
    # Validate locale even if the file is empty or entirely textual.
    parse_number("", decimal, grouping)
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), delimiter=delimiter, strict=True))
    except csv.Error as exc:
        raise ValueError(f"Malformed delimited file: {exc}") from exc
    if not rows or not rows[0]:
        raise ValueError("table is empty")
    header = rows[0]
    width = len(header)
    malformed = [{"row": i + 2, "columns": len(row), "expected": width} for i, row in enumerate(rows[1:]) if len(row) != width]
    if malformed:
        raise ValueError(f"Inconsistent row widths: {malformed[:10]}")
    notes = []
    if len(set(header)) != width:
        notes.append("Duplicate column names; columns are identified by position.")
    if any(not name.strip() for name in header):
        notes.append("One or more column headers are empty.")
    columns = []
    for index, name in enumerate(header):
        parsed = [parse_number(row[index], decimal, grouping) for row in rows[1:]]
        numeric = [cell for cell in parsed if cell is not None and not cell["missing"]]
        missing = [i + 2 for i, cell in enumerate(parsed) if cell is not None and cell["missing"]]
        precision = sorted({cell["decimal_places"] for cell in numeric})
        units = sorted({cell["unit"] for cell in numeric})
        column_notes = []
        if len(precision) > 1:
            column_notes.append("Written decimal places vary; check the intended reporting precision.")
        if len(units) > 1:
            column_notes.append("Unit suffixes vary, including possible bare values; inspect the header and cells.")
        columns.append({"column": index + 1, "name": name, "numeric_cells": len(numeric),
                        "text_cells": sum(cell is None for cell in parsed), "missing_rows": missing,
                        "decimal_places": precision, "unit_suffixes": units,
                        "uncertainty_cells": sum(cell["uncertainty"] is not None for cell in numeric), "notes": column_notes})
    return {"rows": len(rows) - 1, "columns": columns, "delimiter": delimiter,
            "locale": {"decimal": decimal, "grouping": grouping}, "notes": notes, "limits": LIMITS}


def analyze_file(path: str | Path, delimiter: str | None = None, **kwargs) -> dict:
    path = Path(path)
    return {"file": str(path), **analyze_text(path.read_text(encoding="utf-8-sig"), delimiter or ("\t" if path.suffix.lower() == ".tsv" else ","), **kwargs)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--delimiter", choices=["comma", "tab", "semicolon", "pipe"])
    parser.add_argument("--decimal", choices=[".", ","], default=".")
    parser.add_argument("--grouping", default=",")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        delimiter = {"comma": ",", "tab": "\t", "semicolon": ";", "pipe": "|"}.get(args.delimiter)
        report = analyze_file(args.file, delimiter, decimal=args.decimal, grouping=args.grouping)
        print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else
              f"{report['rows']} data rows; {len(report['columns'])} columns.\n" + "\n".join(LIMITS))
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False) if args.json else f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
