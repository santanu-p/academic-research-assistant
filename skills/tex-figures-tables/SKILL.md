---
name: tex-figures-tables
description: Construct and integrate research figures and tables in LaTeX with faithful data, interpretable labels, accessible encodings, and checked placement.
---

# TeX figures and tables

Use this method when a document needs figures, tables, captions, or integration of existing visual material. Follow the [research contract](../../docs/RESEARCH-CONTRACT.md). A visual must preserve the underlying evidence and distinguish measured, computed, illustrative, and schematic content.

## Define the communication task

Identify the question the figure or table should answer, intended audience, final display size, source data, units, uncertainty, and document constraints. Inspect the underlying material before choosing a chart or table. Record whether values are supplied, computed, extracted from a source, or illustrative. Never invent scientific measurements for a polished example.

Choose a table when precise values, categories, or textual comparisons are the reader's task. Choose a figure when trends, distributions, geometry, or relationships carry the argument. Use a diagram for conceptual structure without implying empirical magnitudes. Avoid redundant displays unless each serves a distinct reading need.

## Build faithful visual content

For quantitative charts, select axes and encodings appropriate to the comparison. State units, scales, transformations, normalizations, and uncertainty definitions. Use a baseline appropriate to the mark type and question; explain a truncated scale when it could materially affect interpretation. Do not smooth away scientifically relevant structure or connect categories as though they were continuous measurements.

Distinguish uncertainty bands, standard deviations, standard errors, confidence intervals, credible intervals, and numerical tolerances. Use the quantity actually computed and explain it in the caption or legend. Report sample sizes or denominators where needed. For computational results, retain conventions, resolution, and parameter values essential to interpreting the plot. For qualitative displays, preserve the relationship between categories and the supplied material without implying unmeasured prevalence.

Use color redundantly with line style, markers, labels, or position when practical. Check contrast and legibility at the final embedded size. Keep labels and legends large enough to read without magnification. Preserve vector output for suitable diagrams and plots, and sufficient raster resolution for images. Do not upscale a small raster image and call its information content improved.

For tables, use meaningful headings, units in headings where appropriate, consistent significant figures, and explicit missing-value symbols. Align comparable numerical quantities. State what bolding, symbols, or uncertainty columns mean. Avoid reporting more precision than the measurements or analysis justify.

## Integrate into LaTeX

Use semantic floats, captions, and labels. An original insertion pattern is:

~~~tex
\begin{figure}[tbp]
  \centering
  \includegraphics[width=0.82\linewidth]{figures/response.pdf}
  \caption{Response as a function of the controlled input.
  Define the plotted quantity, units, and uncertainty here.}
  \label{fig:response}
\end{figure}
~~~

Replace the explanatory caption with content grounded in the actual figure. Place labels after captions and reference the float by its key in prose. Keep filenames and paths portable. For multi-panel figures, make panel labels unambiguous and explain them in a coherent caption. Avoid captions that simply repeat the title without explaining encodings and conditions.

Use appropriate table environments for width and multipage behavior. If a table is too wide, revise columns, split logically, or change orientation before making text unreadable. Coordinate placement with [TeX layout](../tex-layout/SKILL.md).

## Deliver and verify

Deliver editable visual sources when available, exported figures, table source, captions, and provenance notes. The optional [scientific visuals helper](../../tools/scientific_visuals.py), [visual QA helper](../../tools/visual_qa.py), and [table QA helper](../../tools/table_qa.py) may support generation or inspection after their available interfaces are checked.

Compare plotted or tabulated values with the source, including units, totals, ordering, missingness, and transformations. Inspect legends, panel labels, scale limits, and text at final size in a fresh build. Confirm every figure and table is cited, every label resolves, and credits or permissions accompany reused material where required. Report automated checks separately from visual and scientific inspection; none alone establishes the validity of the underlying research.

