# OpenAI Quantitative Visual Design Specification

Use these rules as the style contract and rejection checklist for Codex or a reusable visual-design skill.

## Reference weighting — Critical

**Rule:** Treat current OpenAI launch pages and Deployment Safety Hub assets as canonical; use paper figures for scientific forms, not for brand styling.

**Implementation:** Weight Tier 1 highest in retrieval and few-shot selection; separate “OpenAI-designed” from merely “OpenAI-authored.”

**Reject:** Averaging all sources into one inconsistent style.

## Visual thesis — Critical

**Rule:** Every figure must have one sentence-level claim that is visible before detailed reading.

**Implementation:** Use claim-led titles or a short declarative annotation; remove any element that does not support that claim.

**Reject:** Neutral titles such as “Results” or “Performance” with no takeaway.

## Typography — Critical

**Rule:** Use a neutral sans-serif, sentence case, tabular numerals, and only two dominant font weights.

**Implementation:** Use semibold for hierarchy and regular for data labels; preserve real minus signs and consistent typographic quotes.

**Reject:** Bold-heavy dashboards, uppercase headers, mixed typefaces.

## Color hierarchy — Critical

**Rule:** Near-black text, a white or warm-white background, and one primary accent; prior models and competitors are progressively muted.

**Implementation:** Reserve red/orange for risk, errors, or regressions; preserve the same model-to-color mapping across a paper.

**Reject:** Rainbow palettes, saturated fills, decorative gradients.

## Axes and scales — Critical

**Rule:** Remove nonessential spines; use few ticks; name units and metric direction explicitly.

**Implementation:** Write “Higher is better” or “Lower is better”; start bars at zero; mark log scales prominently.

**Reject:** Truncated bars, unexplained log axes, dense minor grids.

## Gridlines — High

**Rule:** Use no grid or only faint major gridlines that aid estimation.

**Implementation:** Gridlines must be lower contrast than uncertainty bands and all data marks.

**Reject:** Dark full-grid graph paper.

## Direct labeling — Critical

**Rule:** Label endpoints, focal series, and operating points directly whenever this removes legend lookup.

**Implementation:** Use short model names adjacent to marks; keep labels collision-free and horizontal where possible.

**Reject:** Detached legends requiring color memorization.

## Model ordering — High

**Rule:** Keep a meaningful and stable model order across related figures.

**Implementation:** Order by generation, capability, or value—not alphabetically—then keep it constant across panels.

**Reject:** Reordering models in every panel.

## Comparison emphasis — Critical

**Rule:** Make the focal model visually dominant while preserving honest visibility of baselines.

**Implementation:** Use dark/accent for focal, medium gray for prior OpenAI, and light neutral for external baselines.

**Reject:** Hiding baselines or using unequal visual weight that misrepresents values.

## Uncertainty — High

**Rule:** Show uncertainty when it changes interpretation, using thin whiskers, restrained ribbons, or dot/interval plots.

**Implementation:** State interval type and sample or seed count in the caption or note.

**Reject:** Large opaque error bands or unlabeled intervals.

## Cost and latency — Critical

**Rule:** For deployment trade-offs, plot capability against real cost or elapsed time and highlight the empirical frontier.

**Implementation:** Use log x when values span orders of magnitude; direct-label frontier points; disclose price assumptions.

**Reject:** Dual y-axes or normalized “efficiency scores” with unclear units.

## Small multiples — High

**Rule:** Prefer facets with shared scales to one overloaded multi-series chart.

**Implementation:** Use common axis limits, aligned baselines, short facet titles, and suppress repeated labels.

**Reject:** Every panel using different scales or full repeated legends.

## Heatmaps — High

**Rule:** Use heatmaps for matrices only when spatial failure regions are the message.

**Implementation:** Use a perceptually ordered scale, sparse ticks, value labels only when legible, and explicit missing-data encoding.

**Reject:** Rainbow heatmaps or tiny annotated cells.

## Distributions — Medium

**Rule:** Show distributions when averages conceal task heterogeneity or reliability.

**Implementation:** Use histograms, ECDFs, box or violin plots, or pass-rate distributions with a clear sample unit.

**Reject:** Adding a distribution figure with no interpretive purpose.

## Reliability curves — High

**Rule:** For worst-of-k, pass@k, or scaling, show a small family of lines with shared x values and end-state emphasis.

**Implementation:** Limit line count, direct-label where possible, and make k or compute semantics explicit.

**Reject:** Markers on every point when they create clutter.

## Table structure — Critical

**Rule:** Do not use vertical rules; use thin horizontal separators, grouped row families, and generous left padding.

**Implementation:** Put units and direction in headers, align numbers on decimals, and bold only best or focal values.

**Reject:** Boxing every cell, dark zebra striping, centered long labels.

## Table precision — Critical

**Rule:** Use consistent, meaningful precision within each metric family.

**Implementation:** Percentages usually use zero or one decimal; costs use two or three significant figures; use an em dash for unavailable.

**Reject:** Mixed precision or false precision such as 83.000%.

## Table hierarchy — High

**Rule:** Create a clear path: group label → benchmark → metric note → values → footnotes.

**Implementation:** Use section rows or whitespace rather than color blocks; repeat headers only across page breaks.

**Reject:** Multiple nested headers with equal weight.

## Annotations — High

**Rule:** Annotations should explain a causal change, threshold, frontier, or exact operating point—not decorate.

**Implementation:** Use one to three concise callouts, aligned to whitespace, with thin leader lines only when necessary.

**Reject:** Speech bubbles, icons, or narrative paragraphs inside plots.

## Captions and notes — Critical

**Rule:** Captions define task, sample, estimator, uncertainty, exclusions, and metric direction.

**Implementation:** Lead with what is plotted; put methodological caveats in a smaller note beneath.

**Reject:** Captions that merely repeat the title.

## Density — High

**Rule:** Aim for one main insight and roughly three to seven visually distinct series per chart.

**Implementation:** Split dense comparisons into aligned panels or a table-plus-chart pair.

**Reject:** Ten-plus equally weighted series in one chart.

## Accessibility — Critical

**Rule:** Do not rely on color alone and preserve readable contrast at actual manuscript size.

**Implementation:** Combine color with position, line style, marker shape, labels, or grouping; test grayscale.

**Reject:** Red/green-only distinctions and tiny 6–7 pt text.

## Export — High

**Rule:** Use SVG for deterministic diagrams and line art; use 2× or 3× PNG only for raster-heavy outputs.

**Implementation:** Preserve vector text where possible; export light and dark variants only when both are genuinely needed.

**Reject:** Screenshots of charts, low-resolution JPEGs, rasterized text.

## Consistency — Critical

**Rule:** Related figures must reuse typography, palette, model order, scales, and annotation grammar.

**Implementation:** Define a shared style module and reusable figure templates in code.

**Reject:** Each figure independently styled by a plotting default.

## Avoid — Critical

**Rule:** Avoid 3D, dual y-axes, drop shadows, gradients, large gray panels, decorative icons, and detached legends.

**Implementation:** Require an explicit exception rationale for any of these devices.

**Reject:** Dashboard aesthetics leaking into scientific figures.
