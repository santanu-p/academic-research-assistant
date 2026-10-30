---
name: latex-pgfplots-charts
description: Use when creating or editing data charts using PGFPlots in LaTeX.
---

# PGFPlots charts

Locate the data, units, plotting code and main document before making changes. Confirm the desired variables, transformations, grouping and uncertainty representation with the supplied evidence. Keep raw data and the plotting source reproducible; never generate measured values or conceal exclusions, smoothing, or a change of scale.

Use explicit axis labels with units, appropriate limits and tick formatting. Choose linear or logarithmic axes according to the analysis, and handle zeros or negative values deliberately on log axes. Use a legend and distinguishable line or marker styles where needed. If values come from a file, use project-relative paths and verify column names and numeric parsing. Respect an existing PGFPlots compatibility setting unless a change is necessary and tested.

Check that uncertainties, normalizations and legends match the underlying data and captions. Avoid graphics that suggest precision beyond the input; if uncertainty is not supplied, do not manufacture error bars. For large datasets consider project-supported precomputation or externalization while preserving the source data and noting the method.

Build the actual document using its configured engine and inspect warnings for missing data, invalid coordinates and clipped values. Render all affected pages and verify curves, labels, legends, data extent and readability at final size. If a build or visual inspection cannot be performed, state that limitation alongside the editable artifact.
