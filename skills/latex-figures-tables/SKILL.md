---
name: latex-figures-tables
description: Use when inserting, revising, or laying out figures and tables in LaTeX.
---

# Figures and tables

Inspect the existing project, figure sources, table data and class rules before editing. Preserve data values, units, image provenance, captions, labels and cited sources. Prefer an existing vector asset for diagrams when it is suitable; use a raster asset at adequate resolution for photographs. Do not replace evidence with an invented image or silently change plotted values.

Size figures to the actual available line or column width and keep paths relative to the project. Keep captions informative about what is shown and where necessary disclose units and source. Place the label after the caption so references target the correct counter. Float options are requests to the layout engine: check where content lands instead of assuming exact placement.

For tables, match numeric alignment and column headings to the data, distinguish missing values from zero, and make notes readable. Use a long-table mechanism if the content truly must cross pages; a regular float cannot split. For wide material, consider restructuring or an authorized landscape layout before shrinking text to illegibility. Avoid unnecessary rules that obscure the values.

Build the main document using the project's established command, then inspect warnings and render all affected pages, including where floats move. Verify image crop, aspect ratio, text size, table overflow, captions and cross-references. Report a missing asset or unavailable build/render step; do not claim visual verification from a successful compile alone.
