---
name: document-conversion
description: Convert academic documents among LaTeX, word-processing, Markdown, HTML, and PDF workflows while tracking semantic, structural, and visual fidelity.
---

# Document conversion

Use this method when academic content must move between formats or be recovered from an existing artifact. Apply the [research contract](../../docs/RESEARCH-CONTRACT.md). Conversion quality has several dimensions: content, meaning, document structure, editability, references, and visual layout. Agree which dimensions matter for the requested destination.

## Inspect source and destination

Identify source files, target format, intended editor, required template, accessibility needs, and whether the source or a rendered output is authoritative. Prefer editable source when available. A PDF is a presentation format and may omit the logical structure needed for faithful reconstruction.

Inventory headings, lists, equations, tables, figures, captions, citations, footnotes, cross-references, comments, tracked changes, metadata, and supplementary material. Record features the destination may not support. Determine whether active comments or deletions should be preserved, accepted, or reported separately; do not silently discard meaningful revision history.

Check the actual conversion tools available before choosing a workflow. Use a direct converter where it preserves the needed structure, or a staged conversion with explicit intermediate checks. Do not promise exact layout preservation when moving between fundamentally different page and flow systems.

## Preserve meaning during conversion

Map semantic structures before styling. A heading should remain a heading, a table should retain its cells and headers, and an equation should remain editable mathematics when feasible. Avoid representing all content as page images unless the task explicitly values appearance over editability. Keep language, names, units, and numerical precision intact.

For LaTeX to word-processing formats, inspect custom macros, mathematical environments, bibliography commands, and floats that may require special handling. Expand or map semantic macros carefully and retain the original source. Check that citation relationships survive even if bibliography styling changes.

For word-processing formats to LaTeX, map heading styles, lists, emphasis, tables, and equations into a consistent source structure. Inspect equations that arrive as images or embedded objects. Do not claim editable mathematical recovery until symbols and structure have been verified.

For Markdown or HTML, preserve hierarchy, links, code, math delimiters, and references supported by the target system. Recognize that platform-specific extensions may render differently. Use portable syntax when practical and document required extensions.

For scanned PDFs or images, separate optical recognition from correction. Flag uncertain characters, negative signs, decimals, superscripts, subscripts, and reference identifiers. Reconstruct tables by rows and columns, then reconcile values with the visible source. Never silently invent text hidden by cropping or illegibility.

## Spreadsheet or CSV to a LaTeX table

Identify the workbook, sheet, exact range, header rows, units, formula cells and whether the user wants displayed values or formulas. Preserve the original workbook. CSV export can lose multiple sheets, formulas, number formats, leading zeros, dates and metadata; compare the export against the intended workbook cells and record the export settings. Determine delimiter, encoding, decimal convention, and meanings of blanks and missing-value markers before processing. Record the source path, sheet or range, export date, row order and any changes; never silently turn blank or unavailable cells into zero.

For a simple UTF-8 comma-separated file containing a single header row and plain text cells, the following Python standard-library example produces an editable `tabular` fragment. Save it as `csv_to_tex.py` and run `python csv_to_tex.py input.csv output.tex` with a new output path. It preserves cell strings without numeric conversion or rounding, escapes LaTeX special characters, rejects inconsistent widths and multiline cells, leaves blank cells blank, and refuses to overwrite an existing output. It does not recover spreadsheet formulas or formatting, interpret units or missingness, or support embedded LaTeX commands; document those limitations and choose a richer workflow when needed.

~~~python
import csv
import sys
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("Usage: python csv_to_tex.py input.csv output.tex")
source, destination = map(Path, sys.argv[1:])
if source.resolve() == destination.resolve():
    raise SystemExit("Input and output must be different files")
with source.open(encoding="utf-8-sig", newline="") as stream:
    rows = list(csv.reader(stream, strict=True))
if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
    raise SystemExit("Expected a nonempty rectangular CSV with a header")
if any("\n" in cell or "\r" in cell for row in rows for cell in row):
    raise SystemExit("Multiline cells require a different table workflow")
escapes = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
           "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
           "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
def escape(cell):
    return "".join(escapes.get(character, character) for character in cell)
lines = [r"\begin{tabular}{" + "l" * len(rows[0]) + "}", r"\hline"]
for index, row in enumerate(rows):
    lines.append(" & ".join(escape(cell) for cell in row) + r" \\")
    if index == 0:
        lines.append(r"\hline")
lines.extend([r"\hline", r"\end{tabular}"])
with destination.open("x", encoding="utf-8", newline="\n") as stream:
    stream.write("\n".join(lines) + "\n")
~~~

Keep units in unambiguous headers or an accompanying note, and define whether blank, unavailable and not applicable cells differ. For numeric alignment or long and wide tables, adapt the fragment using the project's table packages without altering values. Reconcile row and column counts and compare every value, sign, decimal spelling and unit against the authoritative source, especially after sorting, formatting or unit conversion. Compile in a minimal wrapper using the intended engine, then inspect the actual table at delivery size for clipped columns, wrapped labels, missing glyphs and correct rendering of escapes. Report whether the script ran, the table compiled and the output was visually inspected as separate checks.

## Rebuild and compare

Produce a trial conversion and inspect representative difficult content before processing a long document. Revise the mapping if equations, citations, or tables fail. Preserve asset files with portable relative paths and meaningful names. Keep captions attached to the correct figures and references.

Compare the converted text with the source using a structure inventory and targeted checks. Count sections, equations, tables, figures, and reference entries when useful. Treat differences as questions to inspect rather than assuming every difference is an error. A visual converter may change line breaks legitimately while losing a minus sign impermissibly.

Use [mathematics notation](../mathematics-notation/SKILL.md) for formula reconstruction, [figures and tables](../tex-figures-tables/SKILL.md) for complex displays, and [build repair](../tex-build-repair/SKILL.md) for a LaTeX destination.

## Deliver and verify

Deliver editable target files, required assets, retained original source when appropriate, and a concise conversion report. List unsupported or manually reconstructed features and unresolved ambiguities. Preserve source credits and required licensing information attached to retained material.

Open or render the destination through an available tool and inspect the actual result. For paginated final delivery, inspect every page, with special attention to mathematical symbols, citations, tables, captions, footnotes, and page boundaries. Verify searchable or selectable text and link behavior when relevant. Report whether the destination was produced, opened, rendered, compiled, or visually inspected; these are separate facts. Do not label a conversion lossless merely because a converter exited successfully.

