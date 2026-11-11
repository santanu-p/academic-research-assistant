# Deterministic Visual-Form Selection

Use this file before implementation. Select the form from the analytical question, not from plotting convenience.

## 1. First decision: table, chart, diagram, or combination

### Use a table when

- readers need exact values for lookup;
- more than one metric must be compared per row;
- values have heterogeneous units;
- conditions, caveats, or missing entries matter;
- the comparison is an ablation with many discrete configurations;
- a model card or scorecard requires auditable detail;
- the dataset is small enough to scan but too multidimensional for one truthful chart.

### Use a chart when

- the primary task is pattern recognition, ranking, trend, trade-off, uncertainty, or distribution;
- the message should be understood before exact values are read;
- values share a meaningful scale;
- visual position can reduce cognitive load.

### Use a diagram when

- the primary question is process, architecture, relationship, data flow, or intervention location;
- quantitative values are secondary or can be placed in an adjacent table/chart.

### Use a table + chart pair when

- both immediate interpretation and exact auditing matter;
- a main figure should show the core pattern while a compact table provides values;
- a dense table contains one decision-critical comparison worth visual emphasis.

Do not repeat the full same data in both without a reason. The chart should answer a question; the table should enable verification.

## 2. Core decision tree

Apply in order.

1. **Is the x variable ordered or continuous?**
   - Yes, and the goal is change/trend → line chart.
   - Yes, and the goal is relationship between two quantitative variables → scatter.
   - Yes, with uncertainty around effects → line + ribbon or dot-and-interval.
   - No → continue.

2. **Are categories being ranked or compared on one metric?**
   - Up to ~12 categories with long labels → horizontal bar.
   - Narrow nonzero range or uncertainty is central → horizontal dot/interval.
   - Two paired conditions on same entities → dumbbell or slope.
   - More than ~12 categories → grouped table, lollipop only if ranking is essential, or top-k plus appendix.

3. **Are parts of a common total being compared?**
   - 2–5 ordered outcomes summing to a common total → stacked bar.
   - More categories or precise segment comparison needed → table or small multiples.

4. **Are two quantitative deployment variables central?**
   - Capability vs cost/latency/energy/memory → scatter/frontier.
   - Multiple ordered settings per model → connect within model family only.
   - Three quantitative variables → encode the third only if point size/color remains interpretable; otherwise use facets.

5. **Is uncertainty the main message?**
   - Signed effect vs reference → forest/dot-and-interval.
   - Group means with modest categories → point estimate + interval.
   - Temporal/continuous estimate → line + restrained interval band.

6. **Is the full distribution important?**
   - Comparing full shapes robustly → ECDF.
   - Showing intuitive frequency shape → histogram.
   - Compact comparison across groups → box or violin + points.
   - Small sample → strip/swarm with summary.

7. **Is there a meaningful matrix?**
   - Row/column geometry matters → heatmap.
   - Exact cell values matter more than regions → table.
   - Pairwise effects with signed estimates → matrix of dots/intervals or table, not necessarily heatmap.

8. **Are there repeated benchmark panels with identical structure?**
   - 2–6 benchmarks → small multiples with shared scales when valid.
   - Many benchmarks with heterogeneous scales → table, normalized plot with explicit interpretation, or grouped facet families.

9. **Is the question about calibration or reliability?**
   - Predicted confidence vs observed accuracy → calibration curve.
   - Success under multiple samples → pass@k.
   - Failure under repeated exposure → worst-of-k.
   - Time-to-event/failure → survival curve if statistically appropriate.

10. **Is the result an ablation?**
    - Discrete components/configurations → table or horizontal dot plot.
    - Ordered strength/budget → line or dose-response plot.
    - Factorial interaction → small multiples or interaction plot with uncertainty.

## 3. Form rules by common research task

| Analytical task | Default form | Use instead when | Prohibited shortcut |
|---|---|---|---|
| Compare model scores on one benchmark | Horizontal bar or dot plot | Use table for exact audit across many models | Radar chart |
| Compare models across many benchmarks | Small multiples or grouped table | Heatmap only when pattern regions matter | One giant grouped bar chart |
| Show improvement over baseline | Paired dots/dumbbell or actual-value table | Bar chart if zero baseline is meaningful | Delta-only table |
| Show cost/performance | Frontier scatter | Table when only 2–3 points and exact values dominate | Composite efficiency score |
| Show latency/performance | Frontier scatter | Aligned panels if latency distribution also matters | Dual y-axis |
| Show trend over training steps/time | Line chart | Step plot for discrete releases/interventions | Connecting unordered categories |
| Show scaling with compute | Line/scatter with observed points | Log axes if range spans orders of magnitude | Smoothed curve without method |
| Show uncertainty in effects | Dot-and-interval | Bars only when zero baseline is semantically required | Error bars without interval definition |
| Show outcome composition | 100% stacked bar | Table for many small segments | Pie chart with many categories |
| Show before/after same units | Dumbbell/slope | Paired scatter if many units | Independent bars that hide pairing |
| Show model calibration | Reliability diagram | Table for very small bin count | Accuracy bar chart |
| Show pass@k or worst-of-k | Line curve | Table for very few k values | Reporting only k=max |
| Show pairwise win rates | Matrix table or heatmap | Directed graph only when network structure matters | Dense chord diagram |
| Show dataset composition | Horizontal bars | Pie only for <=4 coarse categories and true part-to-whole | Decorative icons |
| Show geographic values | Map only if geography explains pattern | Ranked bar if location is merely a label | Choropleth with incomparable areas |
| Show process/architecture | Minimal diagram | Sequence diagram for temporal interaction | Decorative infographic |

## 4. Deterministic thresholds

These are defaults, not scientific laws. Override only with a clear reason.

### Number of categories

- 1–4: simple bar/dot; direct labels.
- 5–12: horizontal bar/dot; sort meaningfully.
- 13–25: compact table, lollipop, or grouped facets.
- >25: distribution, heatmap, top-k + complete appendix, or interactive view.

### Number of series

- 1–3: direct labels; no legend unless repeated across panels.
- 4–6: direct labels if collision-free; otherwise one shared legend.
- 7–9: small multiples or strong hierarchy with muted baselines.
- >=10 equally important series: split, aggregate only if valid, or use a table.

### Grouped bars

- 2–4 conditions per category.
- Prefer <=8 category groups.
- Beyond that, use small multiples or a table.

### Stacked bars

- 2–5 segments.
- Direct-label only segments large enough for readable text.
- If readers must compare middle segments precisely, choose another form.

### Heatmaps

- Cell labels are acceptable only when final-size font can remain >=8 pt for paper.
- If >20×20 cells, default to sparse ticks and no per-cell labels.
- If ordering is arbitrary, cluster only when clustering itself is part of the analysis and document the method.

### Tables

- <=8 numeric columns at normal manuscript size.
- <=12–18 body rows in the main paper before semantic grouping/splitting is considered.
- Wider/longer tables require transposition, landscape, appendix, or a summary table.

## 5. Ranking and ordering rules

Choose exactly one ordering rationale and apply it consistently:

1. causal/process order;
2. chronological/model-generation order;
3. predefined benchmark order;
4. baseline-to-focal comparison order;
5. numeric rank, when ranking is the message;
6. semantic group order.

Never alphabetize by default. Never reorder the same models differently across related panels unless the panel explicitly presents a ranking and the changed order is clearly signaled.

## 6. Baseline and focal-series rules

- Required baselines stay visible.
- Put the focal/current method last in tables by default and use the highest visual contrast.
- Prior methods use medium gray; secondary/external baselines use light gray.
- Do not visually erase a strong baseline.
- If the focal method is not best, preserve the same focal styling and let the data show the result.
- Do not change chart form to conceal a negative or null result.

## 7. Uncertainty decision rules

Show uncertainty when any of the following holds:

- estimates come from multiple seeds/samples;
- ranking changes under plausible variation;
- the conclusion depends on a small difference;
- subgroup counts differ materially;
- human ratings or sampling are involved;
- a statistical interval is standard for the metric.

Use:

- whiskers for compact category comparisons;
- ribbons for continuous x with few series;
- bootstrap/credible/confidence intervals only with correct labels;
- raw points when sample count is small enough to display.

Do not invent uncertainty from unavailable information. State `uncertainty unavailable` in the caption/note when omission could mislead.

## 8. Cost, latency, and resource trade-offs

For each point, define:

- score/capability metric;
- price basis or hardware/runtime basis;
- batch size/concurrency if relevant;
- input/output length assumptions if relevant;
- aggregation statistic for latency;
- reasoning-effort or compute setting;
- date/version for changing prices when relevant.

Pareto-frontier procedure:

1. transform all metrics so the preferred direction is explicit;
2. compare only points under the same evaluation protocol;
3. compute nondominated points;
4. visually connect only ordered settings belonging to one family;
5. label frontier points directly;
6. keep dominated points visible but muted;
7. avoid a smoothed frontier unless the interpolation is scientifically meaningful.

## 9. Main-text versus supplementary allocation

Place in the main text:

- the result needed to understand the central claim;
- decisive comparisons and necessary baselines;
- uncertainty or reliability that changes interpretation;
- one compact exact-value table when auditability is central.

Move to supplementary material:

- exhaustive per-dataset/per-seed detail;
- visually redundant variants;
- diagnostic plots that do not alter the main interpretation;
- full large tables after a decision-focused summary is provided.

Do not move inconvenient negative evidence merely to improve visual appearance.

## 10. Form-selection self-check

Before plotting, answer yes/no:

- Does this form match the analytical question?
- Does position/length encode the main comparison more accurately than color/area?
- Will exact values still be available when needed?
- Are paired observations shown as paired?
- Are continuous variables treated as continuous and categories as categories?
- Does the form preserve required baselines and uncertainty?
- Can the main claim be read without a legend lookup loop?
- Would a table or small multiples be clearer than this chart?
- Is any chosen transformation, normalization, or log scale explicit?

Any `no` requires form revision before styling.
