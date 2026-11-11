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
