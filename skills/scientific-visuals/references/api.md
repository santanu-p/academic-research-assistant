# Scientific helper API

The project uses optional NumPy and Matplotlib for plotting. Install the plotting dependencies in an environment you control. Importing the helper module itself does not import Matplotlib. On first plotting use, the helper sets `MPLCONFIGDIR` to a temporary directory if the caller has not already selected a location, avoiding an implicit home-directory cache. In a restricted environment, set `TEMP`/`TMP` and optionally `MPLCONFIGDIR` to a writable scratch directory before launching Python.

```python
from tools.scientific_visuals import comparison, export_figure
fig, ax = comparison(["A", "B"], [2.0, 3.5], [0.2, 0.4],
                     ylabel="Response (unit)", title="Illustrative comparison")
result = export_figure(fig, "outputs/comparison")
print(result["audit"])
```

This code's numbers are synthetic. State the actual uncertainty definition in the caption.

| Function | Inputs and result |
| --- | --- |
| `contrast_ratio(foreground, background)` | Relative-luminance contrast for opaque sRGB `#RGB` or `#RRGGBB` colors. Returns an unrounded ratio from 1 to 21 and requires no plotting dependencies. |
| `figure_mm(width=160, height=100, min_font_pt=8)` | Positive finite dimensions in millimetres; font floor at least 8 pt. Returns figure and axes. |
| `comparison(labels, values, uncertainty=None, kind="dots", ...)` | `kind` is `dots` or `bars`. Error magnitudes have shape `(n,)` or lower/upper `(2,n)` and must be finite and nonnegative. Numeric annotations are offset above upper error caps. Bars include zero. |
| `ordered_line(x, y, uncertainty=None, ...)` | Finite, aligned sequences with strictly increasing `x`. Optional uncertainty magnitudes create a band. No sorting or aggregation is inferred. |
| `interval_plot(labels, estimates, lower, upper, reference=None, ...)` | Endpoints must satisfy `lower <= estimate <= upper`; optional vertical reference. |
| `paired_plot(values, labels, subject_labels=None, ...)` | A nonempty `(n,2)` array with one unit per row and two condition labels. NaN or masked entries remain missing; a partial pair is an unconnected point. Rows missing both values and infinities are rejected. Optional string labels align by row. |
| `distribution_plot(groups, labels, ...)` | One nonempty finite numeric vector per labeled group. Displays every supplied observation, including duplicates, with deterministic horizontal displacement and no inferred summary. |
| `grid_heatmap(values, x_labels, y_labels, value_label="Value", vmin=None, vmax=None, ...)` | A nonempty 2D grid with one string label per column and row. The first row appears at the top. NaN or masked cells have a separate missing key; infinities and all-missing grids are rejected. Optional finite increasing `vmin` and `vmax` are supplied together and must include all observed values. |
| `pareto_frontier(points, directions=("lower", "higher"))` | Finite `(n,d)` array and one objective direction per column. Returns nondominated input indices, retaining exact duplicates. |
| `frontier_plot(x, y, directions=..., labels=None, families=None, connect=False, ...)` | Two-objective scatter. Rings global nondominated observations. Default draws no line; explicit connection draws each family's own frontier separately. |
| `audit_figure(fig, min_font_pt=8)` | Draws the canvas and reports visible text below the font floor or outside the canvas. |
| `export_figure(fig, stem, formats=("svg", "png", "pdf"), dpi=300)` | Creates parent directory; returns `files` and `audit`. DPI affects raster resolution, not canvas millimetres. |

Plot constructors accept `width`, `height` and `title`; axes labels are documented in their signatures. Other Matplotlib features can be configured directly through the returned objects. Close figures after use in long-running processes.

The contrast calculation follows the [W3C definition](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum). Compare the unrounded result against criteria applicable to the actual medium and content. It does not assess transparency, gradients, color-vision distinctions, line thickness, font size, or overall accessibility; inspect the rendered output and use redundant encodings.

# Pareto algorithm

Transform each objective to a higher-is-better coordinate by negating lower-is-better columns. For each observation B, examine all observations A. A dominates B when every coordinate of A is greater than or equal to B and at least one is strictly greater. Retain B if no such A exists. Exact duplicates do not dominate each other. Complexity is O(n²d), intended for small scientific/editorial datasets. Finite inputs prevent NaN comparisons from quietly becoming favorable. This algorithm does not model uncertainty or tolerance; near-equality and uncertain objective values require a separately justified method.

# Command-line inspections

```text
python -X utf8 -B tools/prose_metrics.py draft.md --json
python -X utf8 -B tools/prose_metrics.py draft.tex --exemplar author.txt --short-paragraph-words 20 --json
python -X utf8 -B tools/table_qa.py results.tsv --decimal . --grouping , --json
python -X utf8 -B tools/visual_qa.py figure.svg --json
python -X utf8 -B tools/visual_qa.py article.pdf --render-dir outputs/pages --json
python -X utf8 -B examples/scientific_figures.py --out outputs/synthetic
```

Inspection CLIs return 0 when the requested inspection ran, 2 for invalid input or execution failure, and visual QA returns 3 when an optional backend is absent. None defines a scientific pass. Prose metrics strips common markup without expanding TeX includes or macros. Table inspection defaults to English-style decimal/group separators; choose `--decimal , --grouping .` explicitly for grouped decimal-comma numbers. Quoted grouped CSV cells are required when the separator is also a comma. `±`, `+/-`, last-digit parenthesis uncertainty, signs, exponents and a limited unit suffix grammar are recognized. Table notes describe notation, not significant-figure correctness.

## Paired observations and grids

These constructors preserve the supplied order, not subject matching or spatial geometry inferred from data. `paired_plot` shows individual observed values and draws a line only for complete rows; it does not estimate a mean, interval, or paired effect. Subject labels are optional and can overlap for dense data. Include the number and meaning of missing observations in the accompanying text, especially when a whole unit is absent from the input. Do not infer why data are missing.

`distribution_plot` uses horizontal displacement only to spread marks; it carries no numerical meaning and is not a density estimate. It preserves duplicate measurements but cannot guarantee visible separation when groups are dense. It rejects missing and infinite values rather than silently omitting them. Report group sizes, observation units and known missingness; inspect the final render and use another form if overplotting obscures observations. It does not connect paired observations or compute summary statistics.

`grid_heatmap` uses equally spaced categorical cells, not physical coordinates or irregular bin boundaries. Its first input row is the top row, with no interpolation. For physical grids with unequal cell widths or meaningful aspect ratio, construct an appropriate plot directly. Set a common explicit color range for comparable panels when justified; the helper rejects limits that exclude observed values. The legend distinguishes missing cells, but does not explain the cause of missingness. Inspect the colorbar, labels, missing key, contrasts and exported figure at final size. Neither constructor checks statistical meaning or produces accessible alternative text.
