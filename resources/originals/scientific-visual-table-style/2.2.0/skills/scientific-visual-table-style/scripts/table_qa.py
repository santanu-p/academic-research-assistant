#!/usr/bin/env python3
"""Lint CSV/TSV data before styling it as a publication table.

The linter checks structural validity, table density, missing-value notation,
actual-value versus delta usage, numerical precision consistency, possible unit
ambiguity, and label length. It does not inspect final typesetting; render the
final table at delivery width and apply the visual quality gates separately.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Literal, Sequence

Severity = Literal["error", "warning", "info"]

MISSING_CANONICAL = "—"
MISSING_TOKENS = {
    "",
    "-",
    "--",
    "—",
    "na",
    "n/a",
    "n.e.",
    "n/e",
    "nan",
    "none",
    "null",
}
DELTA_HEADER_RE = re.compile(r"(?:^|\b)(?:delta|change|difference|diff)(?:\b|$)|Δ", re.IGNORECASE)
UNIT_IN_HEADER_RE = re.compile(r"%|\b(?:usd|chf|eur|gbp|ms|s|sec|seconds?|min|minutes?|h|hours?|tokens?|bytes?|kb|mb|gb|w|kw|j|kj)\b", re.IGNORECASE)
NUMBER_RE = re.compile(
    r"^\s*"
    r"(?P<prefix>[$€£]?)\s*"
    r"(?P<sign>[+−-]?)"
    r"(?P<number>(?:\d{1,3}(?:,\d{3})+|\d+|\d*\.\d+)(?:[eE][+\-]?\d+)?)"
    r"\s*(?P<percent>%?)"
    r"\s*(?P<suffix>[A-Za-zµμ]+)?"
    r"\s*$"
)


@dataclass(frozen=True)
class Issue:
    severity: Severity
    code: str
    message: str
    row: int | None = None
    column: str | None = None


@dataclass(frozen=True)
class NumericCell:
    value: float
    decimals: int | None
    percent: bool
    currency: str
    suffix: str
    explicit_sign: bool


@dataclass
class Report:
    path: str
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

    def add(
        self,
        severity: Severity,
        code: str,
        message: str,
        *,
        row: int | None = None,
        column: str | None = None,
    ) -> None:
        self.issues.append(Issue(severity, code, message, row, column))
        if severity == "error":
            self.passed = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "passed": self.passed,
            "metadata": self.metadata,
            "issues": [asdict(issue) for issue in self.issues],
            "limitations": self.limitations,
        }


def is_missing(value: str) -> bool:
    return value.strip().lower() in MISSING_TOKENS


def decimal_places(number_text: str) -> int | None:
    normalized = number_text.replace(",", "")
    if "e" in normalized.lower():
        return None
    if "." not in normalized:
        return 0
    return len(normalized.rsplit(".", 1)[1])


def parse_numeric(value: str) -> NumericCell | None:
    text = value.strip().replace("−", "-")
    if is_missing(text):
        return None
    match = NUMBER_RE.match(text)
    if not match:
        return None
    number_text = match.group("number")
    sign = match.group("sign")
    numeric = float(number_text.replace(",", ""))
    if sign == "-":
        numeric = -numeric
    return NumericCell(
        value=numeric,
        decimals=decimal_places(number_text),
        percent=bool(match.group("percent")),
        currency=match.group("prefix") or "",
        suffix=match.group("suffix") or "",
        explicit_sign=sign in {"+", "-"},
    )


def read_table(path: Path, delimiter: str | None = None) -> tuple[list[str], list[list[str]], str]:
    text = path.read_text(encoding="utf-8-sig")
    if delimiter is None:
        try:
            dialect = csv.Sniffer().sniff(text[:8192], delimiters=",\t;|")
            delimiter = dialect.delimiter
        except csv.Error:
            delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    reader = csv.reader(text.splitlines(), delimiter=delimiter)
    rows = list(reader)
    if not rows:
        raise ValueError("table is empty")
    headers = rows[0]
    body = rows[1:]
    return headers, body, delimiter


def nonempty(values: Iterable[str]) -> list[str]:
    return [value for value in values if not is_missing(value)]


def inspect_table(
    path: Path,
    *,
    delimiter: str | None = None,
    max_main_rows: int = 18,
    max_numeric_columns: int = 8,
) -> Report:
    report = Report(path=str(path))
    if not path.exists():
        report.add("error", "missing_file", "File does not exist.")
        return report
    if not path.is_file():
        report.add("error", "not_a_file", "Path is not a regular file.")
        return report

    try:
        headers, body, resolved_delimiter = read_table(path, delimiter)
    except (OSError, UnicodeError, ValueError) as exc:
        report.add("error", "parse_failure", str(exc))
        return report

    report.metadata.update(
        {
            "delimiter": resolved_delimiter,
            "columns": len(headers),
            "data_rows": len(body),
            "headers": headers,
        }
    )

    if any(not header.strip() for header in headers):
        report.add("error", "empty_header", "One or more columns have empty headers.")
    duplicates = [header for header, count in Counter(headers).items() if count > 1]
    if duplicates:
        report.add("error", "duplicate_headers", f"Duplicate headers: {duplicates}")

    expected_width = len(headers)
    for row_number, row in enumerate(body, 2):
        if len(row) != expected_width:
            report.add(
                "error",
                "ragged_row",
                f"Row has {len(row)} cells; expected {expected_width}.",
                row=row_number,
            )

    if len(body) > max_main_rows:
        report.add(
            "warning",
            "dense_row_count",
            f"Table has {len(body)} data rows; main-text tables should normally be grouped, split, or summarized beyond about {max_main_rows} rows.",
        )

    missing_tokens = Counter()
    for row in body:
        for cell in row:
            normalized = cell.strip().lower()
            if normalized in MISSING_TOKENS:
                missing_tokens[cell.strip() or "<empty>"] += 1
    used_missing = [token for token, count in missing_tokens.items() if count > 0]
    if len(used_missing) > 1:
        report.add(
            "warning",
            "mixed_missing_notation",
            f"Multiple missing-value notations are used: {used_missing}. Prefer a single em dash and define exceptions.",
        )

    columns: list[list[str]] = []
    for index in range(expected_width):
        columns.append([row[index] for row in body if len(row) == expected_width])

    numeric_column_indices: list[int] = []
    delta_column_indices: list[int] = []
    non_delta_numeric_indices: list[int] = []

    for index, (header, values) in enumerate(zip(headers, columns)):
        available = nonempty(values)
        parsed = [parse_numeric(value) for value in available]
        parsed_numeric = [item for item in parsed if item is not None]
        numeric_fraction = len(parsed_numeric) / len(available) if available else 0.0
        if numeric_fraction >= 0.60 and parsed_numeric:
            numeric_column_indices.append(index)
            is_delta = bool(DELTA_HEADER_RE.search(header))
            if is_delta:
                delta_column_indices.append(index)
            else:
                non_delta_numeric_indices.append(index)

            decimals = [item.decimals for item in parsed_numeric if item.decimals is not None]
            unique_decimals = sorted(set(decimals))
            if len(unique_decimals) > 2:
                report.add(
                    "warning",
                    "mixed_precision",
                    f"Numeric column uses decimal precisions {unique_decimals}; define one meaningful precision for the metric family.",
                    column=header,
                )
            elif len(unique_decimals) == 2 and abs(unique_decimals[0] - unique_decimals[1]) > 1:
                report.add(
                    "warning",
                    "precision_gap",
                    f"Numeric column mixes {unique_decimals[0]} and {unique_decimals[1]} decimal places.",
                    column=header,
                )

            percent_flags = {item.percent for item in parsed_numeric}
            currencies = {item.currency for item in parsed_numeric if item.currency}
            suffixes = {item.suffix.lower() for item in parsed_numeric if item.suffix}
            if len(percent_flags) > 1:
                report.add(
                    "error",
                    "mixed_percent_notation",
                    "Column mixes percent-marked and unmarked numeric values.",
                    column=header,
                )
            if len(currencies) > 1:
                report.add(
                    "error",
                    "mixed_currency",
                    f"Column mixes currency symbols: {sorted(currencies)}.",
                    column=header,
                )
            if len(suffixes) > 1:
                report.add(
                    "warning",
                    "mixed_units",
                    f"Column contains multiple unit suffixes: {sorted(suffixes)}.",
                    column=header,
                )

            units_in_cells = bool(any(item.percent or item.currency or item.suffix for item in parsed_numeric))
            if units_in_cells and not UNIT_IN_HEADER_RE.search(header):
                report.add(
                    "warning",
                    "unit_not_in_header",
                    "Units appear in cells but not in the header; move the unit to the header for cleaner alignment.",
                    column=header,
                )

            if is_delta:
                explicit_sign_fraction = sum(item.explicit_sign for item in parsed_numeric) / len(parsed_numeric)
                if explicit_sign_fraction < 0.80:
                    report.add(
                        "warning",
                        "unsigned_delta",
                        "Delta/change column does not consistently show explicit signs.",
                        column=header,
                    )

        long_cells = [(row_number, value) for row_number, value in enumerate(values, 2) if len(value.strip()) > 60]
        if long_cells:
            first_row, value = long_cells[0]
            report.add(
                "warning",
                "long_cell_text",
                f"Long cell text ({len(value.strip())} characters) may make the table difficult to scan.",
                row=first_row,
                column=header,
            )

    report.metadata["numeric_columns"] = [headers[index] for index in numeric_column_indices]
    if len(numeric_column_indices) > max_numeric_columns:
        report.add(
            "warning",
            "too_many_numeric_columns",
            f"Table has {len(numeric_column_indices)} numeric columns; consider transposing or splitting beyond about {max_numeric_columns}.",
        )

    if delta_column_indices and not non_delta_numeric_indices:
        report.add(
            "error",
            "delta_only_table",
            "The table contains delta/change columns but no actual-value numeric column. Restore actual values and keep deltas subordinate.",
        )
    elif delta_column_indices and len(delta_column_indices) >= len(non_delta_numeric_indices):
        report.add(
            "warning",
            "delta_dominant_table",
            "Deltas occupy as much or more space than actual values; make actual values primary.",
        )

    first_column = columns[0] if columns else []
    if first_column:
        empty_first = sum(is_missing(value) for value in first_column)
        if empty_first:
            report.add(
                "warning",
                "missing_row_labels",
                f"First column contains {empty_first} missing row label(s).",
                column=headers[0],
            )
        duplicate_labels = [label for label, count in Counter(value.strip() for value in first_column if value.strip()).items() if count > 1]
        if duplicate_labels:
            report.add(
                "info",
                "duplicate_row_labels",
                f"Repeated first-column labels detected; ensure semantic grouping makes them unambiguous: {duplicate_labels[:6]}",
                column=headers[0],
            )

    report.limitations.extend(
        [
            "CSV/TSV linting cannot inspect borders, padding, font size, alignment, bolding, or final page width.",
            "The linter cannot determine whether zero is a genuine result or a missing-value placeholder.",
            "Render the final table and inspect it at actual delivery width.",
        ]
    )
    return report


def render_text(report: Report) -> str:
    status = "PASS" if report.passed else "FAIL"
    lines = [f"{status}: {report.path}"]
    if report.metadata:
        lines.append("Metadata:")
        for key, value in sorted(report.metadata.items()):
            lines.append(f"  {key}: {value}")
    if report.issues:
        lines.append("Findings:")
        for issue in report.issues:
            location = ""
            if issue.row is not None or issue.column is not None:
                location = f" ({'row ' + str(issue.row) if issue.row is not None else ''}{', ' if issue.row is not None and issue.column is not None else ''}{'column ' + repr(issue.column) if issue.column is not None else ''})"
            lines.append(f"  [{issue.severity.upper()}] {issue.code}{location}: {issue.message}")
    if report.limitations:
        lines.append("Limitations:")
        for limitation in report.limitations:
            lines.append(f"  - {limitation}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="CSV or TSV file.")
    parser.add_argument("--delimiter", default=None, help="Explicit delimiter; default auto-detect.")
    parser.add_argument("--max-main-rows", type=int, default=18)
    parser.add_argument("--max-numeric-columns", type=int, default=8)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Return failure when warnings are present.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.max_main_rows < 1 or args.max_numeric_columns < 1:
        print("thresholds must be positive", file=sys.stderr)
        return 2
    report = inspect_table(
        args.path,
        delimiter=args.delimiter,
        max_main_rows=args.max_main_rows,
        max_numeric_columns=args.max_numeric_columns,
    )
    print(json.dumps(report.to_dict(), indent=2) if args.json else render_text(report))
    if not report.passed:
        return 1
    if args.strict and any(issue.severity == "warning" for issue in report.issues):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
