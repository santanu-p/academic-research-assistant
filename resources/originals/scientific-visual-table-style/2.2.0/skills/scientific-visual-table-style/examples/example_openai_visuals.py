#!/usr/bin/env python3
"""Generate three smoke-test figures using the shared visual template.

The data are synthetic and exist only to verify the implementation and export
workflow. Outputs are written to the directory supplied with ``--out``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
if str(TEMPLATES) not in sys.path:
    sys.path.insert(0, str(TEMPLATES))

from openai_visuals import (  # noqa: E402
    DEFAULT_THEME,
    metric_axis_label,
    new_figure,
    plot_horizontal_comparison,
    plot_line_series,
    plot_pareto_frontier,
    save_figure,
)


def build_model_comparison(output_dir: Path) -> list[Path]:
    """Create a compact direct-labeled model comparison."""

    labels = ["External baseline", "Prior model", "Focal model"]
    values = [68.2, 74.6, 81.3]
    errors = [1.5, 1.1, 0.9]
    fig, ax = new_figure(width_mm=85, height_mm=55)
    plot_horizontal_comparison(
        ax,
        labels,
        values,
        focal_label="Focal model",
        baseline_labels={"External baseline"},
        errors=errors,
        value_formatter="{:.1f}",
        title="Accuracy improves by 6.7 points",
        xlabel=metric_axis_label("Accuracy", "%", "higher"),
    )
    ax.set_xlim(0, 94)
    ax.set_xticks([0, 20, 40, 60, 80])
    saved, _ = save_figure(
        fig,
        output_dir / "model_comparison",
        formats=("svg", "png"),
        metadata={"Title": "Synthetic OpenAI-style model comparison"},
    )
    return saved


def build_reliability_curve(output_dir: Path) -> list[Path]:
    """Create a worst-of-k reliability curve with endpoint labels."""

    k = [1, 2, 4, 8, 16]
    series = {
        "External baseline": [76, 69, 60, 49, 35],
        "Prior model": [82, 77, 70, 61, 49],
        "Focal model": [88, 85, 81, 75, 67],
    }
    fig, ax = new_figure(width_mm=85, height_mm=55)
    plot_line_series(
        ax,
        k,
        series,
        focal="Focal model",
        baselines={"External baseline"},
        title="Reliability degrades more slowly",
        xlabel="Attempts, k",
        ylabel=metric_axis_label("Score", "%", "higher"),
    )
    ax.set_xticks(k)
    ax.set_xlim(0.5, 19)
    ax.set_ylim(25, 94)
    ax.set_yticks([30, 45, 60, 75, 90])
    saved, _ = save_figure(
        fig,
        output_dir / "reliability_curve",
        formats=("svg", "png"),
        metadata={"Title": "Synthetic OpenAI-style reliability curve"},
    )
    return saved


def build_cost_frontier(output_dir: Path) -> list[Path]:
    """Create a cost/performance frontier with computed nondominated points."""

    labels = ["Baseline A", "Baseline B", "Prior low", "Prior high", "Focal low", "Focal high"]
    cost = [0.02, 0.05, 0.08, 0.18, 0.06, 0.14]
    score = [51, 61, 67, 76, 72, 84]
    fig, ax = new_figure(width_mm=120, height_mm=68)
    plot_pareto_frontier(
        ax,
        cost,
        score,
        labels,
        x_preference="lower",
        y_preference="higher",
        focal_labels={"Focal low", "Focal high"},
        title="The focal model shifts the frontier",
        xlabel=metric_axis_label("Cost per task", "USD", "lower", scale="log10"),
        ylabel=metric_axis_label("Task score", "%", "higher"),
    )
    ax.set_xscale("log")
    ax.set_xlim(0.015, 0.27)
    ax.set_ylim(45, 90)
    saved, _ = save_figure(
        fig,
        output_dir / "cost_frontier",
        formats=("svg", "png"),
        metadata={"Title": "Synthetic OpenAI-style cost frontier"},
    )
    return saved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("openai_visual_examples"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    paths: list[Path] = []
    paths.extend(build_model_comparison(args.out))
    paths.extend(build_reliability_curve(args.out))
    paths.extend(build_cost_frontier(args.out))
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
