"""Reusable OpenAI-inspired quantitative-visual helpers.

This module encodes a restrained, publication-oriented visual system distilled
from first-party OpenAI quantitative visuals. It is not an official brand
package. The helpers prioritize scientific fidelity, final-size legibility,
direct labeling, sparse axes, and grayscale-plus-one-accent styling.

Typical usage
-------------
>>> import matplotlib.pyplot as plt
>>> from openai_visuals import configure_matplotlib, new_figure, style_axes
>>> configure_matplotlib()
>>> fig, ax = new_figure(width_mm=85, height_mm=55)
>>> ax.plot([1, 2, 3], [0.3, 0.5, 0.7])
>>> style_axes(ax, ygrid=True)
>>> fig.savefig("figure.svg")
"""

from __future__ import annotations

import json
import math
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Literal, Mapping, MutableMapping, Sequence


def _ensure_writable_matplotlib_config() -> None:
    """Use a writable Matplotlib cache in read-only shared-skill environments."""

    if os.environ.get("MPLCONFIGDIR"):
        return
    default = Path.home() / ".config" / "matplotlib"
    try:
        default.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    if default.is_dir() and os.access(default, os.W_OK):
        return
    fallback = Path(tempfile.gettempdir()) / f"openai_visual_mplconfig_{os.getuid()}"
    fallback.mkdir(parents=True, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(fallback)


_ensure_writable_matplotlib_config()

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

MM_PER_INCH = 25.4

Direction = Literal["higher", "lower", "neutral", "toward_zero"]
Preference = Literal["higher", "lower"]
Severity = Literal["error", "warning", "info"]


@dataclass(frozen=True)
class Palette:
    """Operational grayscale-plus-accent palette.

    These values are OpenAI-inspired defaults, not official brand colors.
    """

    ink: str = "#111111"
    ink_secondary: str = "#404040"
    muted_text: str = "#6F6F6F"
    baseline: str = "#8D8D88"
    baseline_light: str = "#B6B6B0"
    hairline: str = "#D8D8D4"
    grid: str = "#E8E8E5"
    subtle_fill: str = "#F5F5F2"
    accent: str = "#1F6F5F"
    accent_tint: str = "#DDE9E5"
    risk: str = "#B5473C"
    warning: str = "#9A681A"
    white: str = "#FFFFFF"
    warm_white: str = "#FBFBF9"


@dataclass(frozen=True)
class Theme:
    """Typography and geometry defaults for manuscript-scale figures."""

    palette: Palette = field(default_factory=Palette)
    font_family: tuple[str, ...] = (
        "Arial",
        "Helvetica",
        "Inter",
        "Liberation Sans",
        "DejaVu Sans",
    )
    body_size_pt: float = 8.5
    title_size_pt: float = 10.0
    axis_label_size_pt: float = 8.5
    tick_size_pt: float = 8.0
    annotation_size_pt: float = 8.0
    line_width_pt: float = 1.15
    focal_line_width_pt: float = 1.65
    axis_line_width_pt: float = 0.7
    error_line_width_pt: float = 0.8
    marker_size_pt: float = 4.8
    major_tick_length_pt: float = 3.0
    major_tick_width_pt: float = 0.6
    grid_line_width_pt: float = 0.55
    grid_alpha: float = 1.0


DEFAULT_PALETTE = Palette()
DEFAULT_THEME = Theme()


@dataclass(frozen=True)
class AuditIssue:
    """One programmatic figure-audit finding."""

    severity: Severity
    code: str
    message: str
    axes_index: int | None = None


@dataclass(frozen=True)
class AuditReport:
    """Structured result of :func:`audit_matplotlib_figure`."""

    passed: bool
    min_font_size_pt: float
    issues: tuple[AuditIssue, ...]
    figure_width_in: float
    figure_height_in: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "min_font_size_pt": self.min_font_size_pt,
            "figure_width_in": self.figure_width_in,
            "figure_height_in": self.figure_height_in,
            "issues": [asdict(issue) for issue in self.issues],
        }

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


@dataclass(frozen=True)
class SeriesStyle:
    """Visual encoding for one series."""

    color: str
    linewidth: float
    alpha: float = 1.0
    linestyle: str = "-"
    marker: str | None = None
    zorder: float = 2.0


GENERIC_TITLES = {
    "result",
    "results",
    "performance",
    "comparison",
    "comparisons",
    "evaluation",
    "evaluations",
    "benchmark",
    "benchmarks",
}


def mm_to_inches(value_mm: float) -> float:
    """Convert millimetres to inches."""

    if value_mm <= 0:
        raise ValueError("value_mm must be positive")
    return value_mm / MM_PER_INCH


def relative_luminance(color: str | Sequence[float]) -> float:
    """Return WCAG relative luminance for a Matplotlib-compatible color."""

    r, g, b, _ = mpl.colors.to_rgba(color)

    def linearize(channel: float) -> float:
        return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(foreground: str, background: str) -> float:
    """Return WCAG contrast ratio between two colors."""

    l1 = relative_luminance(foreground)
    l2 = relative_luminance(background)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def configure_matplotlib(theme: Theme = DEFAULT_THEME) -> None:
    """Install the shared restrained visual theme into Matplotlib rcParams.

    Call this once before creating figures. User or venue constraints may
    override individual values after this call.
    """

    p = theme.palette
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": list(theme.font_family),
            "font.size": theme.body_size_pt,
            "font.weight": "regular",
            "text.color": p.ink,
            "axes.facecolor": p.white,
            "axes.edgecolor": p.ink_secondary,
            "axes.labelcolor": p.ink_secondary,
            "axes.labelsize": theme.axis_label_size_pt,
            "axes.labelweight": "regular",
            "axes.titlesize": theme.title_size_pt,
            "axes.titleweight": "semibold",
            "axes.titlecolor": p.ink,
            "axes.titlelocation": "left",
            "axes.linewidth": theme.axis_line_width_pt,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.axisbelow": True,
            "axes.grid": False,
            "axes.unicode_minus": True,
            "xtick.color": p.ink_secondary,
            "ytick.color": p.ink_secondary,
            "xtick.labelsize": theme.tick_size_pt,
            "ytick.labelsize": theme.tick_size_pt,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.size": theme.major_tick_length_pt,
            "ytick.major.size": theme.major_tick_length_pt,
            "xtick.major.width": theme.major_tick_width_pt,
            "ytick.major.width": theme.major_tick_width_pt,
            "grid.color": p.grid,
            "grid.linewidth": theme.grid_line_width_pt,
            "grid.alpha": theme.grid_alpha,
            "lines.color": p.ink,
            "lines.linewidth": theme.line_width_pt,
            "lines.markersize": theme.marker_size_pt,
            "lines.solid_capstyle": "round",
            "lines.dash_capstyle": "round",
            "patch.edgecolor": "none",
            "patch.linewidth": 0.0,
            "legend.frameon": False,
            "legend.fontsize": theme.tick_size_pt,
            "legend.labelcolor": p.ink_secondary,
            "figure.facecolor": p.white,
            "figure.edgecolor": p.white,
            "figure.dpi": 120,
            "savefig.facecolor": p.white,
            "savefig.edgecolor": p.white,
            "savefig.dpi": 300,
            "savefig.transparent": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "mathtext.default": "regular",
        }
    )


def new_figure(
    *,
    width_mm: float = 85.0,
    height_mm: float | None = None,
    aspect_ratio: float = 1.60,
    nrows: int = 1,
    ncols: int = 1,
    sharex: bool | Literal["all", "row", "col", "none"] = False,
    sharey: bool | Literal["all", "row", "col", "none"] = False,
    constrained_layout: bool = True,
    squeeze: bool = True,
    theme: Theme = DEFAULT_THEME,
    **subplot_kwargs: Any,
) -> tuple[Figure, Any]:
    """Create a final-size figure using millimetre dimensions.

    Parameters are deliberately explicit so figures are not designed at a
    large notebook size and shrunk later.
    """

    configure_matplotlib(theme)
    if width_mm <= 0:
        raise ValueError("width_mm must be positive")
    if height_mm is None:
        if aspect_ratio <= 0:
            raise ValueError("aspect_ratio must be positive")
        height_mm = width_mm / aspect_ratio
    if height_mm <= 0:
        raise ValueError("height_mm must be positive")
    if nrows < 1 or ncols < 1:
        raise ValueError("nrows and ncols must be >= 1")

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(mm_to_inches(width_mm), mm_to_inches(height_mm)),
        sharex=sharex,
        sharey=sharey,
        constrained_layout=constrained_layout,
        squeeze=squeeze,
        **subplot_kwargs,
    )
    return fig, axes


def metric_axis_label(
    name: str,
    unit: str | None = None,
    direction: Direction | None = None,
    *,
    scale: str | None = None,
) -> str:
    """Build a concise metric label with unit, direction, and scale."""

    if not name.strip():
        raise ValueError("name must be non-empty")
    label = name.strip()
    qualifiers: list[str] = []
    if unit:
        qualifiers.append(unit.strip())
    if scale and scale != "linear":
        qualifiers.append(f"{scale} scale")
    if qualifiers:
        label += f" ({', '.join(qualifiers)})"
    direction_map = {
        "higher": "higher is better",
        "lower": "lower is better",
        "neutral": "",
        "toward_zero": "closer to zero is better",
        None: "",
    }
    direction_text = direction_map[direction]
    if direction_text:
        label += f" · {direction_text}"
    return label


def style_axes(
    ax: Axes,
    *,
    xgrid: bool = False,
    ygrid: bool = False,
    zero_x: bool = False,
    zero_y: bool = False,
    max_major_ticks: int | None = 5,
    hide_spines: Iterable[str] = ("top", "right"),
    theme: Theme = DEFAULT_THEME,
) -> Axes:
    """Apply sparse OpenAI-inspired axis styling to an existing axes."""

    p = theme.palette
    ax.set_facecolor(p.white)
    ax.set_axisbelow(True)
    for name in hide_spines:
        if name in ax.spines:
            ax.spines[name].set_visible(False)
    for name in ("left", "bottom"):
        if name in ax.spines:
            ax.spines[name].set_color(p.ink_secondary)
            ax.spines[name].set_linewidth(theme.axis_line_width_pt)

    ax.grid(False)
    if xgrid:
        ax.grid(True, axis="x", color=p.grid, linewidth=theme.grid_line_width_pt)
    if ygrid:
        ax.grid(True, axis="y", color=p.grid, linewidth=theme.grid_line_width_pt)

    if zero_x:
        ax.axvline(0, color=p.hairline, linewidth=theme.axis_line_width_pt, zorder=0)
    if zero_y:
        ax.axhline(0, color=p.hairline, linewidth=theme.axis_line_width_pt, zorder=0)

    if max_major_ticks is not None:
        if max_major_ticks < 2:
            raise ValueError("max_major_ticks must be >= 2 or None")
        if ax.get_xscale() == "linear" and not _axis_is_categorical(ax, "x"):
            ax.xaxis.set_major_locator(MaxNLocator(nbins=max_major_ticks, min_n_ticks=3))
        if ax.get_yscale() == "linear" and not _axis_is_categorical(ax, "y"):
            ax.yaxis.set_major_locator(MaxNLocator(nbins=max_major_ticks, min_n_ticks=3))
    return ax


def _axis_is_categorical(ax: Axes, axis: Literal["x", "y"]) -> bool:
    axis_object = ax.xaxis if axis == "x" else ax.yaxis
    formatter_name = axis_object.get_major_formatter().__class__.__name__
    locator_name = axis_object.get_major_locator().__class__.__name__
    categorical_formatters = {"StrCategoryFormatter", "FixedFormatter"}
    categorical_locators = {"StrCategoryLocator", "FixedLocator", "IndexLocator"}
    return formatter_name in categorical_formatters or locator_name in categorical_locators


def format_number(
    value: float,
    *,
    decimals: int | None = None,
    significant: int = 3,
    percent: bool = False,
    unit: str = "",
    missing: str = "—",
) -> str:
    """Format a value with controlled precision and a consistent missing symbol."""

    if value is None or not np.isfinite(value):
        return missing
    numeric = float(value)
    if percent:
        numeric *= 100.0
        if decimals is None:
            decimals = 1
        formatted = f"{numeric:.{decimals}f}%"
    elif decimals is not None:
        formatted = f"{numeric:,.{decimals}f}"
    else:
        if numeric == 0:
            formatted = "0"
        elif abs(numeric) >= 1e4 or abs(numeric) < 1e-3:
            formatted = f"{numeric:.{max(significant - 1, 0)}e}"
        else:
            formatted = f"{numeric:.{significant}g}"
    return f"{formatted}{unit}" if unit else formatted


def build_series_styles(
    names: Sequence[str],
    *,
    focal: str | None = None,
    baselines: Iterable[str] = (),
    theme: Theme = DEFAULT_THEME,
) -> dict[str, SeriesStyle]:
    """Return a stable grayscale-plus-accent style mapping for series names."""

    if len(set(names)) != len(names):
        raise ValueError("series names must be unique")
    baseline_set = set(baselines)
    line_styles = ("-", "--", "-.", ":")
    markers = (None, "o", "s", "^", "D", "v", "P")
    styles: dict[str, SeriesStyle] = {}
    non_special_index = 0

    for name in names:
        if name == focal:
            styles[name] = SeriesStyle(
                color=theme.palette.accent,
                linewidth=theme.focal_line_width_pt,
                alpha=1.0,
                linestyle="-",
                marker=None,
                zorder=4.0,
            )
        elif name in baseline_set:
            styles[name] = SeriesStyle(
                color=theme.palette.baseline,
                linewidth=theme.line_width_pt,
                alpha=0.95,
                linestyle=line_styles[non_special_index % len(line_styles)],
                marker=markers[(non_special_index + 1) % len(markers)],
                zorder=1.5,
            )
            non_special_index += 1
        else:
            color = theme.palette.ink_secondary if non_special_index == 0 else theme.palette.baseline
            styles[name] = SeriesStyle(
                color=color,
                linewidth=theme.line_width_pt,
                alpha=1.0,
                linestyle=line_styles[non_special_index % len(line_styles)],
                marker=markers[non_special_index % len(markers)],
                zorder=2.5,
            )
            non_special_index += 1
    return styles


def annotate_bar_values(
    ax: Axes,
    bars: BarContainer,
    *,
    formatter: str | callable = "{:.1f}",
    orientation: Literal["vertical", "horizontal"] | None = None,
    padding_pt: float = 3.0,
    color: str | None = None,
    fontsize: float | None = None,
) -> None:
    """Direct-label a bar container without a legend lookup.

    Labels are placed outside positive bars and inside/outside negative bars in
    the natural direction. The caller remains responsible for axis headroom.
    """

    if orientation is None:
        orientation = getattr(bars, "orientation", "vertical")
    if orientation not in {"vertical", "horizontal"}:
        raise ValueError("orientation must be 'vertical' or 'horizontal'")

    def render(value: float) -> str:
        if callable(formatter):
            return str(formatter(value))
        return str(formatter).format(value)

    for patch in bars.patches:
        if orientation == "vertical":
            value = patch.get_height()
            x = patch.get_x() + patch.get_width() / 2.0
            y = patch.get_y() + value
            va = "bottom" if value >= 0 else "top"
            offset = (0, padding_pt if value >= 0 else -padding_pt)
            ax.annotate(
                render(value),
                xy=(x, y),
                xytext=offset,
                textcoords="offset points",
                ha="center",
                va=va,
                color=color,
                fontsize=fontsize,
                clip_on=False,
            )
        else:
            value = patch.get_width()
            x = patch.get_x() + value
            y = patch.get_y() + patch.get_height() / 2.0
            ha = "left" if value >= 0 else "right"
            offset = (padding_pt if value >= 0 else -padding_pt, 0)
            ax.annotate(
                render(value),
                xy=(x, y),
                xytext=offset,
                textcoords="offset points",
                ha=ha,
                va="center",
                color=color,
                fontsize=fontsize,
                clip_on=False,
            )


def label_line_ends(
    ax: Axes,
    lines: Sequence[Line2D] | None = None,
    *,
    labels: Sequence[str] | None = None,
    x_offset_pt: float = 4.0,
    y_offsets_pt: Mapping[str, float] | None = None,
    fontsize: float | None = None,
) -> None:
    """Direct-label the final finite point of each line.

    Use ``y_offsets_pt`` to resolve known collisions deterministically.
    """

    selected = list(lines) if lines is not None else list(ax.get_lines())
    if labels is not None and len(labels) != len(selected):
        raise ValueError("labels must have the same length as lines")
    offsets = dict(y_offsets_pt or {})

    for index, line in enumerate(selected):
        x_data = np.asarray(line.get_xdata(), dtype=float)
        y_data = np.asarray(line.get_ydata(), dtype=float)
        finite = np.isfinite(x_data) & np.isfinite(y_data)
        if not finite.any():
            continue
        last = np.flatnonzero(finite)[-1]
        label = labels[index] if labels is not None else line.get_label()
        if not label or label.startswith("_"):
            continue
        ax.annotate(
            label,
            xy=(x_data[last], y_data[last]),
            xytext=(x_offset_pt, offsets.get(label, 0.0)),
            textcoords="offset points",
            ha="left",
            va="center",
            color=line.get_color(),
            fontsize=fontsize,
            fontweight="semibold" if line.get_linewidth() > DEFAULT_THEME.line_width_pt else "regular",
            clip_on=False,
        )


def pareto_mask(
    x: Sequence[float],
    y: Sequence[float],
    *,
    x_preference: Preference = "lower",
    y_preference: Preference = "higher",
) -> np.ndarray:
    """Return a boolean mask for nondominated finite points.

    A point is dominated when another point is at least as good on both axes
    and strictly better on at least one axis, according to the preferences.
    """

    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    if x_arr.shape != y_arr.shape:
        raise ValueError("x and y must have identical shapes")
    if x_arr.ndim != 1:
        raise ValueError("x and y must be one-dimensional")
    if x_preference not in {"higher", "lower"} or y_preference not in {"higher", "lower"}:
        raise ValueError("preferences must be 'higher' or 'lower'")

    finite = np.isfinite(x_arr) & np.isfinite(y_arr)
    result = np.zeros_like(finite, dtype=bool)
    indices = np.flatnonzero(finite)

    for i in indices:
        dominated = False
        for j in indices:
            if i == j:
                continue
            x_at_least = x_arr[j] >= x_arr[i] if x_preference == "higher" else x_arr[j] <= x_arr[i]
            y_at_least = y_arr[j] >= y_arr[i] if y_preference == "higher" else y_arr[j] <= y_arr[i]
            x_strict = x_arr[j] > x_arr[i] if x_preference == "higher" else x_arr[j] < x_arr[i]
            y_strict = y_arr[j] > y_arr[i] if y_preference == "higher" else y_arr[j] < y_arr[i]
            if x_at_least and y_at_least and (x_strict or y_strict):
                dominated = True
                break
        result[i] = not dominated
    return result


def plot_horizontal_comparison(
    ax: Axes,
    labels: Sequence[str],
    values: Sequence[float],
    *,
    focal_label: str | None = None,
    baseline_labels: Iterable[str] = (),
    errors: Sequence[float] | None = None,
    value_formatter: str | callable = "{:.1f}",
    title: str | None = None,
    xlabel: str | None = None,
    sort: Literal["ascending", "descending", "none"] = "none",
    theme: Theme = DEFAULT_THEME,
) -> BarContainer:
    """Create a restrained horizontal model/category comparison."""

    if len(labels) != len(values):
        raise ValueError("labels and values must have equal length")
    if errors is not None and len(errors) != len(values):
        raise ValueError("errors and values must have equal length")
    if len(set(labels)) != len(labels):
        raise ValueError("labels must be unique")

    labels_arr = np.asarray(labels, dtype=object)
    values_arr = np.asarray(values, dtype=float)
    errors_arr = None if errors is None else np.asarray(errors, dtype=float)
    order = np.arange(len(labels_arr))
    if sort == "ascending":
        order = np.argsort(values_arr, kind="stable")
    elif sort == "descending":
        order = np.argsort(-values_arr, kind="stable")
    elif sort != "none":
        raise ValueError("sort must be 'ascending', 'descending', or 'none'")

    labels_arr = labels_arr[order]
    values_arr = values_arr[order]
    if errors_arr is not None:
        errors_arr = errors_arr[order]

    baseline_set = set(baseline_labels)
    colors = []
    for label in labels_arr:
        if label == focal_label:
            colors.append(theme.palette.accent)
        elif label in baseline_set:
            colors.append(theme.palette.baseline_light)
        else:
            colors.append(theme.palette.ink_secondary)

    y = np.arange(len(labels_arr))
    bars = ax.barh(
        y,
        values_arr,
        xerr=errors_arr,
        color=colors,
        ecolor=theme.palette.ink_secondary,
        error_kw={"elinewidth": theme.error_line_width_pt, "capsize": 2.0, "capthick": theme.error_line_width_pt},
    )
    ax.set_yticks(y, labels_arr)
    ax.invert_yaxis()
    if title:
        ax.set_title(title, loc="left", pad=8)
    if xlabel:
        ax.set_xlabel(xlabel)
    style_axes(ax, xgrid=True, ygrid=False, max_major_ticks=5, theme=theme)

    x_min, x_max = ax.get_xlim()
    if np.nanmin(values_arr) >= 0 and x_min > 0:
        ax.set_xlim(left=0)
    annotate_bar_values(
        ax,
        bars,
        formatter=value_formatter,
        orientation="horizontal",
        color=theme.palette.ink_secondary,
        fontsize=theme.annotation_size_pt,
    )
    return bars


def plot_line_series(
    ax: Axes,
    x: Sequence[float],
    series: Mapping[str, Sequence[float]],
    *,
    focal: str | None = None,
    baselines: Iterable[str] = (),
    direct_labels: bool = True,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    theme: Theme = DEFAULT_THEME,
) -> dict[str, Line2D]:
    """Plot a small family of ordered series with stable emphasis."""

    x_arr = np.asarray(x, dtype=float)
    styles = build_series_styles(list(series), focal=focal, baselines=baselines, theme=theme)
    lines: dict[str, Line2D] = {}
    for name, values in series.items():
        y_arr = np.asarray(values, dtype=float)
        if y_arr.shape != x_arr.shape:
            raise ValueError(f"series {name!r} does not match x shape")
        style = styles[name]
        (line,) = ax.plot(
            x_arr,
            y_arr,
            label=name,
            color=style.color,
            linewidth=style.linewidth,
            alpha=style.alpha,
            linestyle=style.linestyle,
            marker=style.marker,
            zorder=style.zorder,
        )
        lines[name] = line

    if title:
        ax.set_title(title, loc="left", pad=8)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    style_axes(ax, ygrid=True, xgrid=False, max_major_ticks=5, theme=theme)
    if direct_labels:
        label_line_ends(ax, list(lines.values()), labels=list(lines), fontsize=theme.annotation_size_pt)
    else:
        ax.legend(loc="best")
    return lines


def plot_dot_intervals(
    ax: Axes,
    labels: Sequence[str],
    estimates: Sequence[float],
    lower: Sequence[float],
    upper: Sequence[float],
    *,
    focal_label: str | None = None,
    reference: float | None = 0.0,
    title: str | None = None,
    xlabel: str | None = None,
    theme: Theme = DEFAULT_THEME,
) -> None:
    """Plot horizontal point estimates and intervals without bar-area bias."""

    arrays = [np.asarray(v, dtype=float) for v in (estimates, lower, upper)]
    if any(len(arr) != len(labels) for arr in arrays):
        raise ValueError("all numeric arrays must match labels")
    est, lo, hi = arrays
    if np.any(lo > est) or np.any(est > hi):
        raise ValueError("intervals must satisfy lower <= estimate <= upper")

    y = np.arange(len(labels))
    colors = [theme.palette.accent if label == focal_label else theme.palette.ink_secondary for label in labels]
    for yi, estimate, lower_i, upper_i, color in zip(y, est, lo, hi, colors):
        ax.plot([lower_i, upper_i], [yi, yi], color=color, linewidth=theme.error_line_width_pt, zorder=2)
        ax.scatter([estimate], [yi], color=color, s=theme.marker_size_pt**2, zorder=3)
    if reference is not None:
        ax.axvline(reference, color=theme.palette.hairline, linewidth=theme.axis_line_width_pt, zorder=0)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    if title:
        ax.set_title(title, loc="left", pad=8)
    if xlabel:
        ax.set_xlabel(xlabel)
    style_axes(ax, xgrid=True, ygrid=False, max_major_ticks=5, theme=theme)


def plot_pareto_frontier(
    ax: Axes,
    x: Sequence[float],
    y: Sequence[float],
    labels: Sequence[str],
    *,
    x_preference: Preference = "lower",
    y_preference: Preference = "higher",
    focal_labels: Iterable[str] = (),
    connect_frontier: bool = True,
    annotate: bool = True,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    theme: Theme = DEFAULT_THEME,
) -> np.ndarray:
    """Plot a computed Pareto frontier with direct labels and muted dominated points."""

    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    if x_arr.shape != y_arr.shape or len(labels) != len(x_arr):
        raise ValueError("x, y, and labels must have identical length")
    frontier = pareto_mask(x_arr, y_arr, x_preference=x_preference, y_preference=y_preference)
    focal_set = set(focal_labels)

    dominated = ~frontier & np.isfinite(x_arr) & np.isfinite(y_arr)
    ax.scatter(
        x_arr[dominated],
        y_arr[dominated],
        color=theme.palette.baseline_light,
        s=theme.marker_size_pt**2,
        alpha=0.9,
        zorder=1,
    )

    frontier_indices = np.flatnonzero(frontier)
    frontier_colors = [theme.palette.accent if labels[i] in focal_set else theme.palette.ink for i in frontier_indices]
    ax.scatter(
        x_arr[frontier_indices],
        y_arr[frontier_indices],
        color=frontier_colors,
        s=(theme.marker_size_pt + 0.8) ** 2,
        zorder=3,
    )

    if connect_frontier and len(frontier_indices) > 1:
        order = np.argsort(x_arr[frontier_indices])
        ordered = frontier_indices[order]
        ax.plot(
            x_arr[ordered],
            y_arr[ordered],
            color=theme.palette.hairline,
            linewidth=theme.axis_line_width_pt,
            zorder=0,
        )

    if annotate:
        for index in range(len(labels)):
            if frontier[index] or labels[index] in focal_set:
                color = theme.palette.accent if labels[index] in focal_set else theme.palette.ink_secondary
                ax.annotate(
                    labels[index],
                    xy=(x_arr[index], y_arr[index]),
                    xytext=(4, 4),
                    textcoords="offset points",
                    fontsize=theme.annotation_size_pt,
                    color=color,
                    ha="left",
                    va="bottom",
                    clip_on=False,
                )

    if title:
        ax.set_title(title, loc="left", pad=8)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    style_axes(ax, xgrid=True, ygrid=True, max_major_ticks=5, theme=theme)
    return frontier


def _visible_text_artists(fig: Figure) -> list[mpl.text.Text]:
    texts: list[mpl.text.Text] = []
    for artist in fig.findobj(match=mpl.text.Text):
        if artist.get_visible() and artist.get_text().strip():
            texts.append(artist)
    return texts


def _bar_orientation(container: BarContainer) -> str | None:
    orientation = getattr(container, "orientation", None)
    return orientation if orientation in {"vertical", "horizontal"} else None


def audit_matplotlib_figure(
    fig: Figure,
    *,
    min_font_size_pt: float = 8.0,
    max_salient_lines: int = 7,
    require_white_canvas: bool = True,
    theme: Theme = DEFAULT_THEME,
) -> AuditReport:
    """Run deterministic preflight checks on a Matplotlib figure.

    This audit cannot judge scientific correctness, label collisions, or the
    five-second message test. It is a supplement to final-size visual review.
    """

    if min_font_size_pt <= 0:
        raise ValueError("min_font_size_pt must be positive")
    fig.canvas.draw()
    issues: list[AuditIssue] = []
    width_in, height_in = fig.get_size_inches()

    if width_in <= 0 or height_in <= 0:
        issues.append(AuditIssue("error", "invalid_size", "Figure dimensions must be positive."))

    if require_white_canvas:
        face = mpl.colors.to_hex(fig.get_facecolor(), keep_alpha=False).upper()
        allowed = {
            mpl.colors.to_hex(theme.palette.white).upper(),
            mpl.colors.to_hex(theme.palette.warm_white).upper(),
        }
        if face not in allowed:
            issues.append(
                AuditIssue(
                    "warning",
                    "nonwhite_canvas",
                    f"Figure canvas is {face}; the default contract uses white or warm white.",
                )
            )

    renderer = fig.canvas.get_renderer()
    figure_bbox = fig.bbox
    inactive_tick_text_ids: set[int] = set()
    for ax in fig.axes:
        for axis_object, limits in ((ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())):
            lower, upper = sorted(float(value) for value in limits)
            tolerance = max(1e-12, abs(upper - lower) * 1e-9)
            for tick in [*axis_object.get_major_ticks(), *axis_object.get_minor_ticks()]:
                try:
                    location = float(tick.get_loc())
                except (TypeError, ValueError):
                    continue
                if not np.isfinite(location) or location < lower - tolerance or location > upper + tolerance:
                    inactive_tick_text_ids.add(id(tick.label1))
                    inactive_tick_text_ids.add(id(tick.label2))

    for text in _visible_text_artists(fig):
        if id(text) in inactive_tick_text_ids:
            continue
        size = float(text.get_fontsize())
        try:
            bbox = text.get_window_extent(renderer=renderer)
            tolerance_px = 1.0
            intersects_canvas = not (
                bbox.x1 < figure_bbox.x0
                or bbox.x0 > figure_bbox.x1
                or bbox.y1 < figure_bbox.y0
                or bbox.y0 > figure_bbox.y1
            )
            if intersects_canvas and (
                bbox.x0 < figure_bbox.x0 - tolerance_px
                or bbox.y0 < figure_bbox.y0 - tolerance_px
                or bbox.x1 > figure_bbox.x1 + tolerance_px
                or bbox.y1 > figure_bbox.y1 + tolerance_px
            ):
                snippet = text.get_text().replace("\n", " ")[:60]
                issues.append(
                    AuditIssue(
                        "error",
                        "clipped_text",
                        f"Text {snippet!r} extends outside the figure canvas; revise dimensions, wrapping, or margins.",
                    )
                )
        except (RuntimeError, ValueError):
            pass
        if size < min_font_size_pt - 1e-6:
            snippet = text.get_text().replace("\n", " ")[:60]
            issues.append(
                AuditIssue(
                    "error",
                    "small_text",
                    f"Text {snippet!r} is {size:.2f} pt, below the {min_font_size_pt:.2f} pt minimum.",
                )
            )
        try:
            color = mpl.colors.to_hex(text.get_color(), keep_alpha=False)
            if contrast_ratio(color, theme.palette.white) < 3.0:
                issues.append(
                    AuditIssue(
                        "warning",
                        "low_text_contrast",
                        f"Text {text.get_text()[:40]!r} has low contrast ({contrast_ratio(color, theme.palette.white):.2f}:1) on white.",
                    )
                )
        except (ValueError, TypeError):
            pass

    for axes_index, ax in enumerate(fig.axes):
        title = ax.get_title().strip().lower()
        if title in GENERIC_TITLES:
            issues.append(
                AuditIssue(
                    "warning",
                    "generic_title",
                    f"Axes title {ax.get_title()!r} is generic; use a specific descriptive or claim-led title.",
                    axes_index,
                )
            )

        for spine_name in ("top", "right"):
            if spine_name in ax.spines and ax.spines[spine_name].get_visible():
                issues.append(
                    AuditIssue(
                        "warning",
                        "extra_spine",
                        f"The {spine_name} spine is visible.",
                        axes_index,
                    )
                )

        if len(ax.get_lines()) > max_salient_lines:
            issues.append(
                AuditIssue(
                    "warning",
                    "too_many_lines",
                    f"Axes contains {len(ax.get_lines())} line artists; consider small multiples or stronger hierarchy.",
                    axes_index,
                )
            )

        legend = ax.get_legend()
        if legend is not None:
            if legend.get_frame_on():
                issues.append(
                    AuditIssue(
                        "warning",
                        "legend_frame",
                        "Legend frame is visible; remove it unless required for overlap contrast.",
                        axes_index,
                    )
                )
            if len(legend.get_texts()) > 6:
                issues.append(
                    AuditIssue(
                        "warning",
                        "large_legend",
                        f"Legend has {len(legend.get_texts())} entries; consider direct labels or facets.",
                        axes_index,
                    )
                )

        for axis_name, scale, label in (
            ("x", ax.get_xscale(), ax.get_xlabel()),
            ("y", ax.get_yscale(), ax.get_ylabel()),
        ):
            if scale != "linear" and "log" not in label.lower() and scale not in label.lower():
                issues.append(
                    AuditIssue(
                        "warning",
                        "unlabeled_scale",
                        f"{axis_name}-axis uses {scale!r} scale but the label does not state it.",
                        axes_index,
                    )
                )

        for container in ax.containers:
            if not isinstance(container, BarContainer) or not container.patches:
                continue
            orientation = _bar_orientation(container)
            if orientation == "vertical":
                y_min, y_max = ax.get_ylim()
                data_values = np.asarray(getattr(container, "datavalues", []), dtype=float)
                if data_values.size and np.nanmin(data_values) >= 0 and not (y_min <= 0 <= y_max):
                    issues.append(
                        AuditIssue(
                            "error",
                            "truncated_bar_axis",
                            "Positive vertical bars are shown on an axis that excludes zero.",
                            axes_index,
                        )
                    )
            elif orientation == "horizontal":
                x_min, x_max = ax.get_xlim()
                data_values = np.asarray(getattr(container, "datavalues", []), dtype=float)
                if data_values.size and np.nanmin(data_values) >= 0 and not (x_min <= 0 <= x_max):
                    issues.append(
                        AuditIssue(
                            "error",
                            "truncated_bar_axis",
                            "Positive horizontal bars are shown on an axis that excludes zero.",
                            axes_index,
                        )
                    )

        visible_grid = [
            line
            for line in [*ax.get_xgridlines(), *ax.get_ygridlines()]
            if line.get_visible()
        ]
        for grid_line in visible_grid:
            try:
                if relative_luminance(grid_line.get_color()) < 0.75:
                    issues.append(
                        AuditIssue(
                            "warning",
                            "dark_grid",
                            "A visible gridline is darker than the restrained grid contract.",
                            axes_index,
                        )
                    )
                    break
            except (ValueError, TypeError):
                pass

    passed = not any(issue.severity == "error" for issue in issues)
    return AuditReport(
        passed=passed,
        min_font_size_pt=min_font_size_pt,
        issues=tuple(issues),
        figure_width_in=float(width_in),
        figure_height_in=float(height_in),
    )


def save_figure(
    fig: Figure,
    output_stem: str | Path,
    *,
    formats: Sequence[str] = ("svg", "pdf", "png"),
    png_dpi: int = 300,
    transparent: bool = False,
    audit: bool = True,
    min_font_size_pt: float = 8.0,
    raise_on_audit_error: bool = True,
    metadata: Mapping[str, str] | None = None,
) -> tuple[list[Path], AuditReport | None]:
    """Audit and save a figure in deterministic vector/raster formats.

    The exact figure dimensions are preserved. ``bbox_inches='tight'`` is not
    used because it changes output geometry; use constrained layout and inspect
    the final render instead.
    """

    stem = Path(output_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    normalized_formats = [fmt.lower().lstrip(".") for fmt in formats]
    allowed = {"svg", "pdf", "png"}
    invalid = sorted(set(normalized_formats) - allowed)
    if invalid:
        raise ValueError(f"unsupported formats: {invalid}; allowed: {sorted(allowed)}")
    if png_dpi < 150:
        raise ValueError("png_dpi must be at least 150; use >=300 for manuscript figures")

    report = audit_matplotlib_figure(fig, min_font_size_pt=min_font_size_pt) if audit else None
    if report is not None and not report.passed and raise_on_audit_error:
        raise ValueError(f"figure audit failed:\n{report.to_json()}")

    saved: list[Path] = []
    for fmt in normalized_formats:
        path = stem.with_suffix(f".{fmt}")
        kwargs: MutableMapping[str, Any] = {
            "format": fmt,
            "transparent": transparent,
            "metadata": dict(metadata or {}),
        }
        if fmt == "png":
            kwargs["dpi"] = png_dpi
        fig.savefig(path, **kwargs)
        saved.append(path)
    return saved, report


__all__ = [
    "AuditIssue",
    "AuditReport",
    "DEFAULT_PALETTE",
    "DEFAULT_THEME",
    "Palette",
    "SeriesStyle",
    "Theme",
    "annotate_bar_values",
    "audit_matplotlib_figure",
    "build_series_styles",
    "configure_matplotlib",
    "contrast_ratio",
    "format_number",
    "label_line_ends",
    "metric_axis_label",
    "mm_to_inches",
    "new_figure",
    "pareto_mask",
    "plot_dot_intervals",
    "plot_horizontal_comparison",
    "plot_line_series",
    "plot_pareto_frontier",
    "relative_luminance",
    "save_figure",
]
