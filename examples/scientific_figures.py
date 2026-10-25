"""Generate three explicitly synthetic illustrations; no experimental claims.

From the project root:
python -X utf8 -B examples/scientific_figures.py --out ./outputs/synthetic
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.scientific_visuals import comparison, ordered_line, frontier_plot, export_figure


def generate(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    reports = {}
    fig, _ = comparison(["Method A", "Method B", "Method C"], [3.2, 4.1, 3.7], [.4, .25, .3],
                        ylabel="Synthetic response (a.u.)", title="Synthetic comparison", height=105)
    reports["comparison"] = export_figure(fig, out / "comparison")
    fig, _ = ordered_line([0, 1, 2, 3, 4], [.98, .94, .89, .80, .65],
                          uncertainty=[.01, .02, .03, .04, .05], xlabel="Synthetic stress (a.u.)",
                          ylabel="Synthetic reliability (fraction)", title="Synthetic reliability", height=105)
    reports["reliability"] = export_figure(fig, out / "reliability")
    fig, _ = frontier_plot([1, 2, 3, 2.5, 4], [.60, .76, .84, .65, .81],
                           labels=["A", "B", "C", "D", "E"], families=["Family 1", "Family 1", "Family 1", "Family 2", "Family 2"],
                           xlabel="Synthetic cost (a.u.; lower is better)", ylabel="Synthetic score (higher is better)",
                           title="Synthetic trade-off", height=110)
    reports["frontier"] = export_figure(fig, out / "frontier")
    manifest = {"provenance": "All numbers are invented deterministic examples, not measurements or fitted predictions.",
                "uncertainty": "Comparison error bars and reliability bands are arbitrary symmetric illustration widths, not confidence intervals.",
                "frontier": "Directions are lower cost and higher score. Rings identify observed nondominated points; no interpolation is asserted.",
                "figures": reports}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(generate(args.out), indent=2))
