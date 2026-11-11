# GPT-6 Astra governing visual grammar

This is normative. The official GPT-6 Astra system card at
https://deploymentsafety.openai.com/gpt-6-astra/gpt-6-astra.pdf governs all
scientific and quantitative figures and tables produced by this skill.

Gold-standard tables: 1, 2, 4, 6, 7, 8.
Gold-standard figures: 1, 2, 5, 6, 9, 12, 13, 14, 17, 19.

Precedence: scientific fidelity; venue/accessibility requirements; this
governing grammar; other references; plotting defaults. Plotting defaults may
never determine the finished visual.

## Hard system rules

- Build at final physical size; inspect the 100% render and grayscale render.
- Minimum ordinary text is 7.5 pt; prefer 8–9 pt.
- Use a white field, near-black text, quiet neutral baselines, and one focal
  teal accent. Reserve red/orange for actual risk or regression.
- Use sentence case, regular/semibold hierarchy, and tabular numerals.
- Titles state the analytical claim. Align title, subtitle, plot, table, and
  caption origins.
- Evidence must occupy at least 55% of canvas width. Increase dimensions for
  long labels or category count instead of compressing text.
- Suppress top/right spines; use no grid or faint major gridlines only.
- Use direct labels for separated endpoints; run collision resolution and
  fall back to one shared legend when necessary. Never repeat legends.
- Bars start at zero. Use a dot/deviation plot for small differences.
- Use lines only for ordered x. Do not connect unrelated model families.
- Compute Pareto frontiers from data and label cost/latency units and desired
  directions.
- Show uncertainty when material and state interval type and sample count.
- If categories × series exceeds 20 marks, reject dense grouped bars and use
  dots, aligned small multiples, or a table-plus-chart.
- Grouped bars are capped at four series per category.
- Heatmaps require meaningful matrix position and an ordered color scale.
- Tables use no vertical rules or boxed cells. Use thin top, header/group, and
  bottom rules, semantic row groups, left-aligned text, decimal/right-aligned
  numerals, meaningful consistent precision, and actual values.
- Delta-only tables are prohibited. Do not shrink a dense table below 7.5 pt;
  shorten, group, transpose, split, or move exhaustive detail to supplement.
- Keep model order, palette, precision, uncertainty treatment, panel grammar,
  and table rules consistent across the entire manuscript.
- Explicit generative-image, illustration, artwork, and photorealistic-image
  requests remain outside this workflow unless the user asks to combine them.

## Mandatory rejection gates

Regenerate if any title/label clips; text is below 7.5 pt; the scientific point
is not visible within five seconds; axes/grid dominate data; direct labels
collide; more than two non-semantic accent hues appear; grouped bars exceed four
series; bars use an undisclosed nonzero baseline; log scaling is undisclosed;
uncertainty semantics are missing; a frontier connects unrelated families; a
table uses vertical rules, boxed cells, mixed precision, or delta-only values;
raster output is below 2× intended display resolution; grayscale loses a
required comparison; or the artifact resembles an untouched plotting default.

## Required loop

Generate → render at final size → inspect actual raster → inspect grayscale →
compare as a manuscript family → run structural checks → diagnose
system-level failures → correct reusable rules/source → regenerate. Do not
deliver while a rejection gate remains.
