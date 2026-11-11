# Quantitative Visual Style Contract

This file is the enforceable visual-design contract for the `scientific-visual-table-style` skill. It generalizes recurring patterns in first-party OpenAI launch pages, research pages, Deployment Safety Hub figures, system cards, and OpenAI-authored technical papers.

It is not an official brand specification. Its purpose is operational consistency.

## 1. Priority order

Apply constraints in this order:

1. Scientific truth and source fidelity.
2. Explicit user instructions.
3. Existing manuscript/template geometry when the user requests preservation.
4. Venue requirements and accessibility.
5. This style contract.
6. Creative alternatives.

Never improve visual aesthetics by weakening evidence, hiding a baseline, changing a value, suppressing uncertainty, or overstating a conclusion.

## 2. Visual objective

Every visual must answer one primary question:

> What should a technically competent reader understand within five seconds?

A successful visual has:

- one dominant message;
- an obvious entry point;
- a stable reading order;
- low legend and cross-reference burden;
- enough detail for verification;
- no decorative element competing with evidence;
- consistent visual grammar across related outputs.

If the five-second message is not clear, do not polish the current composition. Reconsider form, grouping, and hierarchy first.

## 3. Canvas and composition

### 3.1 Background

Default to:

- canvas: `#FFFFFF`;
- optional warm paper fill: `#FBFBF9`;
- plotting area: same as canvas;
- subtle structural region only when needed: `#F5F5F2`.

Do not use large gray plotting panels, card grids, drop shadows, bevels, glossy surfaces, or gradients.

### 3.2 Whitespace

Whitespace is structural, not decorative. Use it to separate semantic groups and create a reading path.

Default targets at manuscript size:

- outside plot margin: 4–8% of width;
- title-to-plot gap: 6–10 pt;
- inter-panel gutter: 4–6% of total figure width;
- annotation breathing room: at least one text-height around the label;
- table row-group gap: 3–6 pt;
- table horizontal padding: 4–7 pt per side.

Avoid both extremes:

- cramped marks and labels;
- excessive empty space that weakens comparison or wastes manuscript area.

### 3.3 Proportions

Set final dimensions before plotting.

Defaults when venue dimensions are unknown:

| Context | Width | Typical height | Minimum text |
|---|---:|---:|---:|
| Paper single column | 85 mm | 48–65 mm | 8 pt |
| Paper double column | 178 mm | 82–115 mm | 8 pt |
| Slide figure region | 150–300 mm | composition-dependent | 14 pt |
| Web/card | 900–1600 px | 500–950 px | 12 CSS px |

Prefer one-panel aspect ratios between 1.45 and 1.80. Use taller formats for long category labels or distributions. Use square formats only when x and y have symmetrical scientific meaning.

### 3.4 Alignment

- Align panel plot areas, not merely outer bounding boxes.
- Align table decimals and shared baselines.
- Align titles, panel labels, and annotations to a deliberate grid.
- Use consistent left edges across a visual series.
- Keep shared axes exactly aligned.
- Avoid optical misalignment caused by unequal label lengths; compensate in layout rather than shifting marks arbitrarily.

## 4. Hierarchy

Use no more than four hierarchy levels:

1. claim/title;
2. focal result;
3. required comparison evidence;
4. metadata, notes, and supporting labels.

The focal result may be emphasized through:

- darker value;
- one accent hue;
- thicker line;
- direct annotation;
- position;
- whitespace.

Use at most two of these simultaneously unless the user explicitly requests stronger emphasis.

Do not:

- enlarge the focal bar area disproportionately;
- suppress competitors below readable contrast;
- use different scales for the focal method;
- place a conclusion in a colored banner detached from the data.

## 5. Typography

### 5.1 Font family

Use a neutral sans-serif stack:

`Arial, Helvetica, Inter, Liberation Sans, DejaVu Sans, sans-serif`

Do not bundle or redistribute proprietary fonts. Prefer metric-compatible system fallbacks.

### 5.2 Weight

Use primarily:

- regular for data, axes, and notes;
- semibold for titles, table headers, and focal labels.

Avoid heavy bold, ultra-light text, italics for large blocks, and mixed font families.

### 5.3 Case and language

- Sentence case by default.
- Preserve official model and benchmark capitalization.
- Avoid all-caps section headers.
- Use concise, concrete labels.
- Use consistent terminology across all figures and tables.

### 5.4 Final-size type defaults

For manuscript figures:

- claim/title: 9.5–11 pt;
- axis labels: 8.5–9.5 pt;
- ticks and data labels: 8–9 pt;
- annotations: 8–9 pt;
- panel labels: 9–10 pt semibold;
- notes inside visual: 7.5–8.5 pt only when unavoidable.

For tables:

- body: 8.5–9.5 pt;
- header: same size or 0.25–0.5 pt larger, semibold;
- footnotes: 7.5–8.5 pt;
- line height: 1.25–1.40× body size.

Never solve small text by increasing raster resolution. Rebuild at the actual delivery size.

### 5.5 Numerals and punctuation

- Use tabular numerals where supported.
- Prefer a true minus sign (`−`) over hyphen-minus for negative values.
- Use an en dash for ranges and an em dash for unavailable values.
- Use thin/nonbreaking spacing between value and unit where supported.
- Keep decimal separators locale-consistent.

## 6. Color system

### 6.1 Operational palette

| Role | Hex | Use |
|---|---|---|
| Primary ink | `#111111` | titles, focal neutral line, primary text |
| Secondary ink | `#404040` | axes, secondary labels |
| Muted text | `#6F6F6F` | notes, supporting labels |
| Baseline gray | `#8D8D88` | prior model or required comparison |
| Light baseline | `#B6B6B0` | external/secondary baselines |
| Hairline | `#D8D8D4` | rules, separators |
| Grid | `#E8E8E5` | faint major grid only |
| Subtle fill | `#F5F5F2` | limited grouping/background region |
| Focal teal | `#1F6F5F` | principal accent |
| Focal tint | `#DDE9E5` | restrained highlight fill |
| Risk/regression | `#B5473C` | errors, harm, regression, danger |
| Warning | `#9A681A` | caution or threshold proximity |

This palette is operational and OpenAI-inspired; it is not claimed to be official.

### 6.2 Color rules

- Default to grayscale plus one accent.
- Use no more than two semantic accents in one figure.
- Keep the focal series at the highest chromatic or luminance contrast.
- Use risk hues only for semantically adverse outcomes.
- Maintain one document-level mapping from series/model to color.
- Use line style, marker, position, or direct label in addition to hue.
- Test in grayscale.

Reject:

- default Matplotlib or Tableau rainbow palettes;
- high-saturation category fills;
- gradients;
- red/green-only distinctions;
- arbitrary changes in model color across panels;
- pale baseline text that becomes unreadable in print.

## 7. Lines, rules, and marks

At manuscript size:

| Element | Default |
|---|---:|
| Axis/hairline | 0.6–0.8 pt |
| Table top/bottom rule | 0.75–0.9 pt |
| Table header/group rule | 0.35–0.55 pt |
| Baseline line | 1.0–1.2 pt |
| Focal line | 1.5–1.8 pt |
| Error bar | 0.7–0.9 pt |
| Annotation leader | 0.6–0.8 pt |
| Marker | 4–6 pt |

Use solid lines for primary series. Use dashed/dotted lines for structurally different conditions, not as arbitrary decoration.

Avoid marker outlines thicker than the line, large circles obscuring data, or heavy black borders around bars.

## 8. Titles, labels, and captions

### 8.1 Title

Preferred title behavior:

- claim-led when the evidence supports a concise conclusion;
- descriptive but specific when neutrality is scientifically necessary;
- one line where possible;
- no terminal period for a short title;
- no generic “Results,” “Comparison,” or “Performance.”

Examples:

- Good: `Replay hurts under abrupt source drift`.
- Good: `Higher reasoning effort improves hard tasks but raises cost`.
- Weak: `Results on our benchmark`.

Do not overclaim causality when the plot shows association.

### 8.2 Axis labels

Axis labels include:

- metric name;
- unit;
- direction when not obvious.

Examples:

- `Accuracy (%) · higher is better`;
- `Median latency (s) · lower is better`;
- `API cost per task (USD, log scale)`.

Do not repeat the same unit in every tick label if it is already in the axis title.

### 8.3 Data labels

Use direct labels when:

- there are at most roughly six focal series;
- endpoints are spatially separated;
- exact values materially improve interpretation;
- legend lookup would be slower.

Do not label every mark in a dense scatter. Label:

- frontier points;
- focal operating points;
- thresholds;
- major outliers;
- endpoints.

### 8.4 Captions and notes

A publication caption should define, in this order when applicable:

1. what is plotted;
2. task/population and sample;
3. aggregation/statistic;
4. uncertainty;
5. relevant exclusions or conditions;
6. metric direction;
7. cost/latency basis.

Do not use the caption to repeat the title. Keep methodological caveats in a smaller note if the venue permits.

## 9. Axes, scales, and grids

### 9.1 Axes

- Remove top and right spines by default.
- Use left/bottom axes only when they aid orientation.
- For direct-labeled plots, axes may be even lighter.
- Use 3–6 major ticks per continuous axis as a default.
- Use human-readable tick steps.
- Keep the zero line slightly stronger only when zero is meaningful.

### 9.2 Bar scales

Bars encode length from a common baseline. Therefore:

- quantitative bars start at zero;
- deviation bars may center on an explicit zero/reference line;
- never crop a bar axis merely to magnify small differences;
- use dots/intervals when a nonzero narrow range is scientifically important.

### 9.3 Log scales

Use a log scale only when:

- values span at least about two orders of magnitude;
- ratios are more meaningful than differences;
- the scale is clearly labeled.

Do not place zero or negative values on a log axis. Do not hide the transformation in a note.

### 9.4 Grid

- No grid by default for bars and simple dot plots.
- Use faint major horizontal gridlines for value estimation when helpful.
- Use no minor gridlines unless the plot is a technical log-scale figure that requires them.
- Gridlines must be lower contrast than uncertainty and all data marks.

## 10. Legends and direct labeling

Use a legend only when direct labeling would create collisions or when the same encoding is reused across many panels.

Legend rules:

- place in unused whitespace, not over data;
- remove frame;
- order entries exactly as they appear visually;
- use one row or a compact vertical stack;
- use short labels;
- avoid repeating a full legend in every panel.

For small multiples, prefer one shared legend or direct panel labels.

## 11. Annotations

Annotations are allowed only when they explain:

- a threshold;
- a causal intervention;
- a change point;
- a frontier operating point;
- a clinically/statistically meaningful region;
- a non-obvious counterexample.

Default:

- one to three annotations;
- 8–9 pt at manuscript size;
- align text into existing whitespace;
- use a thin leader only when spatial relationship is ambiguous;
- use a subtle accent or primary ink, not a colored bubble.

Reject:

- decorative callouts;
- paragraph-length prose inside the plot;
- many crossing leader lines;
- annotations that simply restate a labeled value.

## 12. Multi-panel composition

### 12.1 Panel count

Prefer:

- 1–4 panels for a main figure;
- 2–6 compact facets for a repeated benchmark family;
- additional panels in supplementary material if they do not support the central claim.

### 12.2 Shared structure

- Share axis limits when comparison requires it.
- Align zero/baseline lines.
- Keep model order identical.
- Keep palette and line styles identical.
- Suppress repeated axis titles and legends.
- Use panel labels `(a)`, `(b)`, … only when cited in text or structurally necessary.

### 12.3 Hierarchy

Not every panel needs equal area. Give the primary panel more area only when:

- the evidence importance genuinely differs;
- the scaling does not distort comparison;
- supporting panels remain readable.

Avoid a “hero project” effect in which one panel dominates merely because it was easier to visualize.

## 13. Chart-specific contracts

### 13.1 Horizontal bar and dot charts

Use for ranked or labeled categories.

- Sort by scientific order or value; never default to alphabetical unless categories are identifiers.
- Put long labels on the y-axis.
- Direct-label values at bar/dot endpoints when space permits.
- Use one focal accent and gray baselines.
- Use dot plots instead of bars when the range does not meaningfully include zero.

### 13.2 Grouped bars

Use only when both category and condition comparisons are essential.

- Keep conditions to about 2–4.
- Use position first, color second.
- Keep group gaps larger than within-group gaps.
- Add uncertainty only if valid.
- Consider small multiples when there are more than four conditions.

### 13.3 Stacked bars

Use for part-to-whole outcomes with 2–5 ordered categories.

- Sum to 100% or a clear common total.
- Keep category order semantically stable.
- Put the most decision-relevant segment at a common baseline if possible.
- Direct-label large segments; avoid tiny labels inside narrow segments.
- Do not use stacked bars for independent metrics.

### 13.4 Line charts

Use only for ordered/continuous x.

- Limit to roughly 3–7 salient lines.
- Direct-label endpoints where possible.
- Use markers only for sparse or irregular observations.
- Use a ribbon for uncertainty when it does not obscure other series.
- Highlight change points only when scientifically justified.

### 13.5 Scatter plots

- Use transparency or density methods only when overplotting exists.
- Label focal points/frontier points, not every observation.
- Add trend lines only with a stated estimator.
- Use a diagonal/reference line only when it has scientific meaning.
- Preserve equal aspect ratio when x and y are directly comparable.

### 13.6 Pareto/frontier plots

- Use real cost, latency, energy, or memory units.
- Compute nondominated points from the data.
- Connect only points that belong to an ordered family, such as reasoning effort or batch size.
- Mute dominated points but keep them visible.
- Direct-label frontier/model families.
- If x spans orders of magnitude, use a labeled log scale.
- State pricing/hardware/batch assumptions.

### 13.7 Dot-and-interval / forest plots

- Use a meaningful zero or baseline line.
- Order rows by concept, not estimated effect, unless ranking is the claim.
- Use thin intervals and a clear point estimate.
- Distinguish confidence, credible, bootstrap, or standard-error intervals explicitly.
- Avoid filled bars for signed effects.

### 13.8 Heatmaps

- Use only when both axes form a meaningful matrix.
- Use a perceptually ordered sequential or diverging scale.
- Choose a meaningful center for diverging scales.
- Show missing values distinctly.
- Use cell labels only when final-size text remains readable.
- Use sparse ticks and group separators for large matrices.
- Accompany the heatmap with a colorbar whose unit and direction are explicit.

### 13.9 Distributions

Choose based on the question:

- ECDF: robust comparison across full distributions;
- histogram: intuitive count/density shape;
- box/violin: compact group comparison;
- strip/swarm: small sample visibility;
- ridgeline: only for many ordered distributions and sufficient vertical space.

State whether the y-axis is count, density, probability, or cumulative proportion.

### 13.10 Calibration

- Include the ideal diagonal.
- State whether values are binned.
- Show sample support or uncertainty when available.
- Do not infer calibration from aggregate accuracy alone.

### 13.11 Before/after and paired comparisons

- Use paired dots, dumbbells, or slopes for the same units under two conditions.
- Preserve pairing visually.
- Sort by baseline or change when useful.
- Use arrows only when direction is unambiguous and does not clutter.
- Report actual values; optional deltas are secondary.

### 13.12 Scaling and pass@k/worst-of-k curves

- Define the x-axis compute/sample semantics exactly.
- Use shared x-values and consistent interpolation policy.
- Do not smooth sparse points without stating the method.
- Use endpoint emphasis rather than markers at every point.
- Show the single-sample baseline.

## 14. Table contract

### 14.1 Structure

Use `booktabs` logic:

- top rule;
- header separator;
- optional thin semantic group separators;
- bottom rule;
- no vertical rules;
- no border around every cell.

### 14.2 Column order

Default order:

1. group or benchmark label;
2. metric/condition detail;
3. baseline(s);
4. prior/family models;
5. focal/current method;
6. optional delta or cost column;
7. notes only when essential.

Place the focal model at the right edge when it makes row-wise scanning easier, unless chronology or user template dictates otherwise.

### 14.3 Alignment

- Labels: left.
- Numeric values: decimal/right.
- Short categorical statuses: centered.
- Headers: align with the data beneath them.
- Long method names: never centered.

### 14.4 Headers

- Keep to one or two rows.
- Put units in headers.
- Put metric direction in a concise header note or table note.
- Use spanning headers only for true semantic groups.
- Use visual weight/spacing to distinguish top-level and leaf headers.

### 14.5 Precision

Use the smallest precision that preserves meaningful distinctions.

Default:

- percentages: 0 or 1 decimal;
- scores on 0–1: 2–3 decimals if the benchmark supports that precision;
- costs: 2–3 significant figures;
- latency: one consistent unit and 2–3 significant figures;
- counts: integer;
- confidence intervals: match estimate precision.

Do not display more precision than measurement or evaluator variability supports.

### 14.6 Emphasis

- Bold the focal method or best result only when predefined.
- If many values tie statistically or numerically, mark ties honestly.
- Avoid colored fills across the entire winning row.
- Use a very light tint only for one focal column or one decision-critical region when necessary.
- Never use stars without a defined significance legend.

### 14.7 Missing and exceptional values

- unavailable/not applicable: em dash;
- not evaluated: `n/e` only when defined in the note;
- below threshold: `<x` only when the threshold is part of the measurement;
- missing due to failure: use a distinct symbol and explain it;
- zero: only a measured or meaningful zero.

### 14.8 Density control

If a table is too dense at final width:

1. shorten labels without ambiguity;
2. group rows semantically;
3. move repeated units to headers;
4. reduce only unjustified precision;
5. transpose if models greatly outnumber metrics;
6. split into meaningful table blocks;
7. move full detail to supplementary material and keep a decision-focused main table.

Do not solve density with 6–7 pt text.

## 15. Quantitative diagrams

Use for workflows, evaluation pipelines, context layouts, or systems comparisons.

- Prefer left-to-right reading for processes and top-to-bottom for hierarchies.
- Use one shape family and one corner-radius system.
- Align boxes to a grid.
- Use equal internal padding.
- Use straight or orthogonal connectors where possible.
- Label connectors only when the relationship is not obvious.
- Use one accent to mark the changed/new component.
- Avoid icons unless they encode a necessary domain distinction.
- Keep quantitative results in charts/tables; do not hide them inside decorative boxes.

## 16. Accessibility

A figure must remain interpretable:

- in grayscale;
- under common color-vision deficiencies;
- at final manuscript/slide size;
- on a typical office printer;
- without relying on hover or animation unless the deliverable is explicitly interactive.

Use redundant encodings when needed:

- color + direct label;
- color + line style;
- color + marker;
- position + grouping;
- text status + restrained fill.

Minimum contrast should be appropriate for the medium. Do not use light-gray body text on white.

## 17. Export and source

Preferred outputs:

- SVG: diagrams and web/vector line art;
- PDF: manuscript vector figures;
- PNG: preview or raster-heavy figure at 2×/3× target resolution;
- editable source: Python/R/JavaScript/LaTeX/HTML or native design file;
- data: CSV/JSON or deterministic loading path.

Avoid:

- JPEG for line art;
- screenshots of plots;
- rasterized labels;
- cropped legends or annotations;
- embedding unpublished proprietary font files;
- export settings that change final dimensions unexpectedly.

## 18. Document-level consistency contract

Before shipping a set of visuals, verify:

- identical model names and capitalization;
- identical model order;
- identical model-to-color/style mapping;
- identical unit conventions;
- identical number precision by metric family;
- identical panel-label style;
- identical title grammar;
- aligned plot widths and caption spacing;
- consistent use of `higher/lower is better`;
- consistent baseline and uncertainty notation.

A beautiful individual chart is a failure if it breaks the visual system of the paper.
