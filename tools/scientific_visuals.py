"""Small, explicit Matplotlib helpers for scientific figures.

Requires NumPy and Matplotlib when plotting. These functions do not choose a
scientific interpretation, infer uncertainties, fit data, or verify provenance.
All dimensions are final canvas millimetres. No tight bounding-box export is
used: that would silently change the requested physical dimensions.
"""
from __future__ import annotations

import atexit
import math
import os
import re
import shutil
import tempfile
from pathlib import Path


def contrast_ratio(foreground, background):
    """Return the WCAG sRGB luminance contrast of two opaque hex colors.

    Accepts #RGB or #RRGGBB; transparency and other color spaces must be
    resolved by the caller. A ratio alone does not establish accessibility.
    """
    def luminance(value):
        if not isinstance(value, str) or not re.fullmatch(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})", value):
            raise ValueError("colors must be opaque sRGB hex values in #RGB or #RRGGBB form")
        digits = value[1:]
        if len(digits) == 3:
            digits = ''.join(c * 2 for c in digits)
        channels = [int(digits[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return sum(weight * channel for weight, channel in zip((0.2126, 0.7152, 0.0722), linear))

    a, b = luminance(foreground), luminance(background)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def _dependencies():
    # Matplotlib may otherwise create a cache under the user's home directory.
    if "MPLCONFIGDIR" not in os.environ:
        cache = tempfile.mkdtemp(prefix="academic-mpl-")
        os.environ["MPLCONFIGDIR"] = cache
        atexit.register(shutil.rmtree, cache, ignore_errors=True)
    try:
        import numpy as np
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Scientific plotting requires numpy and matplotlib; install the optional plotting dependencies.") from exc
    return np, plt


def _vector(values, name):
    np, _ = _dependencies()
    result = np.asarray(values, dtype=float)
    if result.ndim != 1 or not len(result) or not np.isfinite(result).all():
        raise ValueError(f"{name} must be a nonempty one-dimensional sequence of finite numbers")
    return result


def _error(values, count, name="uncertainty"):
    if values is None:
        return None
    np, _ = _dependencies()
    result = np.asarray(values, dtype=float)
    if result.shape not in {(count,), (2, count)} or not np.isfinite(result).all() or (result < 0).any():
        raise ValueError(f"{name} must have shape (n,) or (2,n), be finite and nonnegative")
    return result


def figure_mm(width=160, height=100, min_font_pt=8):
    """Return (figure, axes) using a physical canvas and an 8 pt default floor."""
    if not all(math.isfinite(float(v)) and float(v) > 0 for v in (width, height, min_font_pt)):
        raise ValueError("canvas dimensions and font size must be finite and positive")
    if min_font_pt < 8:
        raise ValueError("min_font_pt must be at least 8 pt; increase the final canvas if needed")
    _, plt = _dependencies()
    with plt.rc_context({"font.size": min_font_pt, "axes.labelsize": min_font_pt + 1,
                         "axes.titlesize": min_font_pt + 2, "xtick.labelsize": min_font_pt,
                         "ytick.labelsize": min_font_pt, "legend.fontsize": min_font_pt,
                         "svg.fonttype": "none", "pdf.fonttype": 42}):
        fig, ax = plt.subplots(figsize=(width / 25.4, height / 25.4), layout="constrained")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    return fig, ax


def comparison(labels, values, uncertainty=None, *, kind="dots", ylabel="Value", title=None, width=160, height=100):
    """Category dots or zero-baseline bars; numeric labels clear upper error caps.

    ``uncertainty`` is symmetric (n,) or lower/upper (2,n), in data units.
    The caller must state its statistical meaning in the caption.
    """
    np, _ = _dependencies()
    y = _vector(values, "values")
    if len(labels) != len(y) or not all(isinstance(label, str) for label in labels):
        raise ValueError("labels must contain one string per value")
    if kind not in {"dots", "bars"}:
        raise ValueError("kind must be dots or bars")
    error = _error(uncertainty, len(y))
    fig, ax = figure_mm(width, height)
    x = np.arange(len(y))
    if kind == "bars":
        ax.bar(x, y, color="#277DA8", width=.65)
        ax.axhline(0, color="0.3", linewidth=.7)
    else:
        ax.scatter(x, y, color="#277DA8", zorder=3)
    if error is not None:
        ax.errorbar(x, y, yerr=error, fmt="none", ecolor="0.2", capsize=4)
    upper = error if error is not None and error.ndim == 1 else error[1] if error is not None else np.zeros(len(y))
    for xx, yy, ee in zip(x, y, upper):
        ax.annotate(f"{yy:g}", (xx, yy + ee), xytext=(0, 9), textcoords="offset points", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x, labels)
    ax.set_ylabel(ylabel)
    ax.margins(x=.15, y=.25)
    if title:
        ax.set_title(title)
    return fig, ax


def ordered_line(x, y, *, uncertainty=None, xlabel="Ordered coordinate", ylabel="Value", title=None, width=160, height=100):
    """Connect strictly increasing x observations, optionally with an error band."""
    np, _ = _dependencies()
    x, y = _vector(x, "x"), _vector(y, "y")
    if len(x) != len(y) or not (np.diff(x) > 0).all():
        raise ValueError("x and y lengths must match, and x must be strictly increasing")
    error = _error(uncertainty, len(y))
    fig, ax = figure_mm(width, height)
    ax.plot(x, y, "o-", color="#277DA8", markersize=4)
    if error is not None:
        lower, upper = (error, error) if error.ndim == 1 else error
        ax.fill_between(x, y - lower, y + upper, color="#277DA8", alpha=.18)
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title or "")
    return fig, ax


def interval_plot(labels, estimates, lower, upper, *, xlabel="Estimate", reference=None, title=None, width=160, height=100):
    """Horizontal intervals; lower/upper are endpoints, not error magnitudes."""
    np, _ = _dependencies()
    center, low, high = (_vector(values, name) for values, name in ((estimates, "estimates"), (lower, "lower"), (upper, "upper")))
    if not (len(labels) == len(center) == len(low) == len(high)) or (low > center).any() or (center > high).any():
        raise ValueError("interval lengths must match and lower <= estimate <= upper")
    if reference is not None and not math.isfinite(float(reference)):
        raise ValueError("reference must be finite")
    fig, ax = figure_mm(width, height)
    positions = np.arange(len(center))
    ax.errorbar(center, positions, xerr=np.vstack((center - low, high - center)), fmt="o", color="#277DA8", capsize=4)
    if reference is not None:
        ax.axvline(reference, color="0.4", linestyle="--", linewidth=.8)
    ax.set_yticks(positions, labels)
    ax.invert_yaxis()
    ax.set(xlabel=xlabel, title=title or "")
    ax.margins(y=.2)
    return fig, ax



def distribution_plot(groups, labels, *, ylabel="Value", title=None, width=160, height=100):
    """Show each supplied observation without estimating a distribution or interval.

    Each group is a nonempty finite vector. Horizontal displacement is a
    deterministic display aid, has no quantitative meaning, and does not
    guarantee separation in dense data. Missing observations must be handled
    and reported by the caller rather than silently discarded here.
    """
    np, _ = _dependencies()
    groups = list(groups)
    if not groups or len(labels) != len(groups) or not all(isinstance(label, str) for label in labels):
        raise ValueError("labels must contain one string per nonempty group")
    vectors = [_vector(group, "group") for group in groups]
    fig, ax = figure_mm(width, height)
    for index, values in enumerate(vectors):
        offsets = np.linspace(-.2, .2, len(values)) if len(values) > 1 else np.zeros(1)
        ax.scatter(index + offsets, values, color="#277DA8", s=20, alpha=.8)
    ax.set_xticks(np.arange(len(vectors)), labels)
    ax.set(ylabel=ylabel, title=title or "")
    ax.margins(x=.2, y=.15)
    return fig, ax


def paired_plot(values, labels, *, subject_labels=None, ylabel="Value", title=None, width=160, height=100):
    """Plot each row as one paired unit; NaN marks an unavailable observation.

    Rows with one missing value retain the observed point without a connection.
    Rows missing both observations are rejected because they cannot be shown.
    """
    np, _ = _dependencies()
    data = np.ma.asarray(values, dtype=float).filled(np.nan)
    if data.ndim != 2 or data.shape[0] == 0 or data.shape[1] != 2:
        raise ValueError("values must have shape (n, 2) with at least one row")
    if np.isinf(data).any() or np.isnan(data).all(axis=1).any():
        raise ValueError("values cannot contain infinity or rows with both observations missing")
    if len(labels) != 2 or not all(isinstance(label, str) for label in labels):
        raise ValueError("labels must contain two strings")
    if subject_labels is not None and (len(subject_labels) != len(data) or
                                      not all(isinstance(label, str) for label in subject_labels)):
        raise ValueError("subject_labels must contain one string per row")
    fig, ax = figure_mm(width, height)
    for i, row in enumerate(data):
        ax.plot([0, 1], row, marker="o", color="#277DA8", linewidth=.8, markersize=4, alpha=.8)
        if subject_labels is not None:
            last = int(np.flatnonzero(~np.isnan(row))[-1])
            ax.annotate(subject_labels[i], (last, row[last]), xytext=(5, 4),
                        textcoords="offset points", fontsize=8)
    ax.set_xticks([0, 1], labels)
    ax.set(ylabel=ylabel, title=title or "")
    ax.margins(x=.2, y=.15)
    return fig, ax


def grid_heatmap(values, x_labels, y_labels, *, value_label="Value", xlabel="", ylabel="",
                 vmin=None, vmax=None, title=None, width=160, height=100):
    """Display an ordered categorical grid with row zero at the top.

    NaN and masked entries appear as missing, rather than being interpolated.
    Optional color limits must be a finite, increasing pair containing all
    observed values, so extremes cannot silently saturate at the scale ends.
    """
    np, _ = _dependencies()
    data = np.ma.asarray(values, dtype=float).filled(np.nan)
    if data.ndim != 2 or not all(data.shape) or np.isinf(data).any() or np.isnan(data).all():
        raise ValueError("values must be a nonempty 2D grid with finite data and optional missing cells")
    if (len(x_labels) != data.shape[1] or len(y_labels) != data.shape[0] or
        not all(isinstance(label, str) for label in (*x_labels, *y_labels))):
        raise ValueError("x_labels and y_labels must match grid columns and rows")
    if (vmin is None) != (vmax is None):
        raise ValueError("supply both vmin and vmax, or neither")
    if vmin is not None and (not math.isfinite(float(vmin)) or not math.isfinite(float(vmax)) or vmin >= vmax):
        raise ValueError("vmin and vmax must be finite and increasing")
    if vmin is not None and ((data < vmin).any() or (data > vmax).any()):
        raise ValueError("vmin and vmax must include all observed values")
    fig, ax = figure_mm(width, height)
    import matplotlib
    cmap = matplotlib.colormaps["viridis"].copy()
    cmap.set_bad("#d0d0d0")
    image = ax.imshow(np.ma.masked_invalid(data), origin="upper", interpolation="nearest",
                      aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_xticks(np.arange(data.shape[1]), x_labels)
    ax.set_yticks(np.arange(data.shape[0]), y_labels)
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title or "")
    fig.colorbar(image, ax=ax, label=value_label)
    if np.isnan(data).any():
        from matplotlib.patches import Patch
        ax.legend(handles=[Patch(facecolor="#d0d0d0", edgecolor="0.3", label="Missing")],
                  loc="upper left", bbox_to_anchor=(1.02, 1))
    return fig, ax


def pareto_frontier(points, directions=("lower", "higher")):
    """Return nondominated input indices, retaining exact duplicate points.

    A dominates B iff A is at least as good in every objective and strictly
    better in at least one. O(n² d), suitable for small editorial datasets.
    All objectives and entries are checked; NaN/inf are rejected.
    """
    np, _ = _dependencies()
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[0] == 0 or points.shape[1] == 0 or not np.isfinite(points).all():
        raise ValueError("points must be a nonempty finite (n,d) array")
    if len(directions) != points.shape[1] or any(direction not in {"higher", "lower"} for direction in directions):
        raise ValueError("provide one higher/lower direction per objective")
    signed = points * np.asarray([1 if d == "higher" else -1 for d in directions])
    return [i for i, point in enumerate(signed) if not ((signed >= point).all(axis=1) & (signed > point).any(axis=1)).any()]


def frontier_plot(x, y, *, directions=("lower", "higher"), labels=None, families=None, xlabel="Objective 1", ylabel="Objective 2", connect=False, title=None, width=160, height=100):
    """Scatter two objectives; ring nondominated points. No line by default.

    Explicit ``connect=True`` connects each family's own frontier separately,
    sorted by x. A connecting segment is a visual guide, not a feasible model.
    """
    np, _ = _dependencies()
    x, y = _vector(x, "x"), _vector(y, "y")
    if len(x) != len(y):
        raise ValueError("x and y lengths must match")
    if labels is not None and len(labels) != len(x):
        raise ValueError("labels must match points")
    families = list(families) if families is not None else ["Observations"] * len(x)
    if len(families) != len(x) or not all(isinstance(family, str) for family in families):
        raise ValueError("families must contain one string per point")
    points = np.column_stack((x, y))
    selected = pareto_frontier(points, directions)
    fig, ax = figure_mm(width, height)
    palette = ["#277DA8", "#B75B19", "#7A5195", "#247A53"]
    for index, family in enumerate(dict.fromkeys(families)):
        group = [i for i, value in enumerate(families) if value == family]
        ax.scatter(x[group], y[group], label=family, color=palette[index % len(palette)], marker=["o", "s", "^", "D"][index % 4])
        if connect:
            local = [group[i] for i in pareto_frontier(points[group], directions)]
            local.sort(key=lambda i: x[i])
            ax.plot(x[local], y[local], color=palette[index % len(palette)], alpha=.5, linewidth=.8)
    ax.scatter(x[selected], y[selected], s=100, facecolors="none", edgecolors="0.15", linewidths=.8, label="Nondominated")
    if labels:
        for xx, yy, label in zip(x, y, labels):
            ax.annotate(str(label), (xx, yy), xytext=(6, 6), textcoords="offset points", fontsize=8)
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title or "")
    ax.margins(.18)
    ax.legend(loc="best")
    return fig, ax


def audit_figure(fig, min_font_pt=8):
    """Inspect visible text font size and canvas bounds after drawing.

    Does not detect overlap, label-to-mark collisions, inaccessible colors,
    invalid data or scientific misrepresentation. Inspect the final export.
    """
    if not math.isfinite(float(min_font_pt)) or min_font_pt <= 0:
        raise ValueError("min_font_pt must be positive and finite")
    from matplotlib.text import Text
    fig.canvas.draw()
    renderer, bounds = fig.canvas.get_renderer(), fig.bbox
    # Axis.draw omits ticks outside the view interval even though their Text
    # objects retain visible=True. Do not report these unused locator labels.
    unused_tick_labels = set()
    for axes in fig.axes:
        for axis in (axes.xaxis, axes.yaxis):
            low, high = sorted(axis.get_view_interval())
            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                if not low <= tick.get_loc() <= high:
                    unused_tick_labels.update((id(tick.label1), id(tick.label2)))
    small, outside = [], []
    for item in fig.findobj(match=Text):
        if id(item) in unused_tick_labels or not item.get_visible() or not item.get_text().strip():
            continue
        if item.get_fontsize() < min_font_pt:
            small.append({"text": item.get_text(), "font_pt": item.get_fontsize()})
        box = item.get_window_extent(renderer)
        if box.x0 < bounds.x0 - 1 or box.y0 < bounds.y0 - 1 or box.x1 > bounds.x1 + 1 or box.y1 > bounds.y1 + 1:
            outside.append(item.get_text())
    return {"minimum_font_pt": min_font_pt, "small_text": small, "off_canvas_text": outside,
            "canvas_mm": [float(value) * 25.4 for value in fig.get_size_inches()],
            "limits": "Checks text only; cannot verify data, semantics or overlap. Final-size visual inspection is required."}


def export_figure(fig, stem, formats=("svg", "png", "pdf"), dpi=300):
    """Export physical-size SVG/PNG/PDF; return paths and a text audit."""
    if not math.isfinite(float(dpi)) or dpi <= 0:
        raise ValueError("dpi must be positive and finite")
    formats = tuple(formats)
    if not formats or any(fmt not in {"svg", "png", "pdf"} for fmt in formats):
        raise ValueError("formats must contain svg, png and/or pdf")
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    audit = audit_figure(fig)
    _, plt = _dependencies()
    paths = []
    with plt.rc_context({"svg.fonttype": "none", "pdf.fonttype": 42}):
        for fmt in formats:
            path = stem.with_suffix("." + fmt)
            fig.savefig(path, format=fmt, dpi=dpi, metadata={"Creator": "Academic Research Assistant scientific_visuals"})
            paths.append(str(path))
    return {"files": paths, "audit": audit}
