# Visual and Table Quality Gates

A visual is complete only when every critical gate passes after the most recent change. Programmatic linting is supportive; final-size visual inspection is mandatory.

## Gate 0 — Scope and evidence lock (critical)

Pass only if:

- source values and labels are identified;
- metric definition, unit, direction, denominator, and aggregation are known or explicitly marked unavailable;
- required baselines and experimental conditions are preserved;
- uncertainty definition and sample/seed count are preserved when available;
- the visual-authorship task has not silently changed science, wording, claims, or experimental conclusions;
- the intended final medium and dimensions are recorded.

Automatic fail:

- any fabricated value or interval;
- omitted negative/null result because it is visually inconvenient;
- altered label that changes scientific meaning;
- incomparable conditions plotted as directly comparable without disclosure.

## Gate 1 — Claim and form (critical)

Pass only if:

- the visual has one primary question and one sentence-level claim;
- the chosen form follows `form_selection.md` or has a documented exception;
- categories, ordered variables, paired observations, and distributions are encoded appropriately;
- a chart is not used merely because the data can be plotted;
- a table is not retained merely because it already exists.

Five-second test:

Show the final-size visual without its surrounding prose. A technically competent reader should be able to state the main comparison or pattern within five seconds. If not, revise form, hierarchy, grouping, or title before polishing.

## Gate 2 — Quantitative integrity (critical)

Check every visual against the source:

- values;
- signs;
- units;
- rounding;
- category/series order;
- model names and versions;
- sample size/denominator;
- uncertainty interval type;
- axis transformation;
- missing values;
- baseline/reference line;
- cost/latency assumptions.

Required spot check:

- all emphasized values;
- minimum and maximum values;
- at least three non-emphasized values;
- every panel’s first and last category;
- every statistic cited in an annotation.

For programmatic pipelines, compare plotted arrays/table cells to a structured source and fail on mismatch.

## Gate 3 — Hierarchy and decoding cost (critical)

Pass only if:

- focal evidence is immediately visible;
- baselines remain readable and honest;
- readers do not need repeated legend lookup;
- titles, axes, data labels, and annotations have distinct hierarchy;
- only decision-relevant elements receive emphasis;
- whitespace creates a stable reading path;
- no decorative element competes with data.

Automatic correction triggers:

- more than one equally dominant title/callout;
- many equally saturated series;
- every value bolded or labeled;
- detached legend for <=5 easily direct-labeled series;
- large colored panel backgrounds;
- redundant labels repeated across facets.

## Gate 4 — Geometry and final-size legibility (critical)

Render at exact delivery dimensions and inspect at 100%.

Pass only if:

- manuscript text is >=8 pt unless venue explicitly permits smaller;
- slide figure text is >=14 pt;
- web text is >=12 CSS px;
- no clipping, overlap, occlusion, or cut-off glyphs;
- labels do not collide with marks or error bars;
- panel gutters and margins are consistent;
- line weights and markers remain legible in print;
- the visual is not dependent on zoom.

Do not treat high DPI as a substitute for readable type.

## Gate 5 — Axes and statistical presentation (critical)

Pass only if:

- bars start at zero or are explicitly deviation bars around a visible reference;
- line plots use ordered/continuous x;
- log scales are labeled and justified;
- dual y-axes are absent unless the user explicitly requires them and the exception is documented;
- uncertainty is shown when available and interpretation-relevant;
- intervals are correctly named;
- trend lines state or imply a defined estimator;
- Pareto-frontier claims match computed nondominance;
- reference lines have semantic meaning.

Automatic fail:

- truncated bars without explicit deviation encoding;
- line connecting unordered categories;
- unexplained smoothing;
- misleading area/volume encoding;
- hiding a null result through axis limits.

## Gate 6 — Table quality (critical for tables)

Pass only if:

- no vertical rules or boxed-cell grid;
- row groups are semantic and visually clear;
- labels are left-aligned and numbers are decimal/right-aligned;
- units and metric direction are explicit;
- precision is consistent by metric family;
- actual values are present and deltas are subordinate;
- missing values use a defined symbol rather than zero;
- emphasis is sparse and predetermined;
- statistically indistinguishable values are not arbitrarily declared unique winners;
- table remains readable at final width;
- table notes define non-obvious abbreviations, intervals, and exceptions.

Density correction order:

1. shorten labels safely;
2. move units to headers;
3. remove unjustified precision;
4. add semantic grouping;
5. transpose;
6. split by conceptual family;
7. move exhaustive detail to appendix.

Never solve density by shrinking below the minimum text size.

## Gate 7 — Color and accessibility (critical)

Inspect:

- full color;
- grayscale;
- at least one common red/green color-vision-deficiency simulation when tools permit;
- typical office-print contrast.

Pass only if:

- the visual remains interpretable without color;
- risk colors are used semantically;
- text/background contrast is sufficient;
- focal and baseline series remain distinguishable;
- thin light-gray elements do not disappear;
- no meaning relies solely on red versus green.

## Gate 8 — Cross-visual consistency (critical for sets)

For every figure/table in the same work, verify:

- model names and capitalization;
- model order;
- model-to-color mapping;
- marker/line-style mapping;
- unit conventions;
- number precision;
- title grammar;
- panel-label placement;
- axis direction phrases;
- table rule and header style;
- caption structure;
- export dimensions.

A locally attractive figure fails if it breaks the document-wide visual system.

## Gate 9 — Export and artifact integrity (critical)

Pass only if:

- editable source is retained;
- line art has vector output (`SVG` or `PDF`) when possible;
- PNG preview is at least 2× target pixel density when raster is required;
- no JPEG is used for line art;
- no font file is redistributed;
- output opens in an independent viewer;
- dimensions/aspect ratio match the requested target;
- transparency behaves as intended;
- embedded raster elements are not visibly low resolution;
- the final inspected render corresponds to the final source revision.

Use:

```bash
python scripts/visual_qa.py figure.svg --target-width-mm 85 --target-height-mm 55
python scripts/visual_qa.py figure.pdf --target-width-mm 178
python scripts/table_qa.py results.csv
```

## Gate 10 — Adversarial review (critical)

Perform at least two deliberate passes.

### Pass A: skeptical scientific reader

Ask:

- Could the axis, ordering, aggregation, or omitted baseline lead me to a stronger conclusion than the data supports?
- Are uncertainty and denominators sufficient?
- Are compared conditions genuinely comparable?
- Does the title overstate causality or generality?
- Is the “best” emphasis justified?

### Pass B: hostile visual editor

Ask:

- What can be removed without losing evidence?
- Where does my eye go first, and is that correct?
- What requires unnecessary decoding?
- Is any label repeated?
- Is any color decorative rather than semantic?
- Does the figure remain calm at actual size?
- Are alignment, padding, and gutters optically consistent?

Revise and repeat the final-size render after either pass finds a defect.

## Weighted scorecard

Use this score only after all critical pass/fail gates have passed.

| Dimension | Points |
|---|---:|
| Scientific fidelity and completeness | 25 |
| Claim clarity and form selection | 15 |
| Final-size legibility and geometry | 15 |
| Hierarchy and decoding efficiency | 15 |
| Axes/statistics/uncertainty integrity | 10 |
| Table or chart craft | 8 |
| Cross-visual consistency | 5 |
| Accessibility | 4 |
| Export/source quality | 3 |
| **Total** | **100** |

Shipping threshold:

- no critical failure;
- total score >=90;
- scientific fidelity score =25/25;
- final-size legibility score >=14/15.

A score does not override a critical failure.

## Required completion record

For nontrivial work, retain an internal record containing:

- source-data path or identifier;
- visual-spec path or text;
- final dimensions;
- selected references;
- programmatic QA output;
- date/time of final render review;
- corrections made after adversarial passes;
- delivered files and formats.

This record need not be shown to the user unless requested, but it prevents accidental delivery of an unverified intermediate.
