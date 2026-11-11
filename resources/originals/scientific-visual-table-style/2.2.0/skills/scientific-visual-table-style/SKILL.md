---
name: scientific-visual-table-style
description: Use for scientific, research, quantitative, statistical, benchmark, and data-analysis charts, analytical figures, diagrams, and tables. Preserve evidence, select forms deterministically, apply restrained publication-grade design, and inspect final-size rendered outputs before delivery. Exclude explicit generative-image, illustration, artwork, and photorealistic-image requests unless the user explicitly combines the workflows.
---

# Governing GPT-6 Astra north star

Before substantive work, read `references/gpt6_astra_north_star.md`,
`references/gpt6_astra_reference_index.json`, and
`templates/astra_visual_tokens.json`. The cited Astra tables and figures are
hard governing references, not optional inspiration. Final-size rendered QA is
mandatory. Explicit generative-image requests are excluded.
# Scientific Visuals & Tables

This is a self-contained visual reasoning and production system for scientific, research, quantitative, statistical, and data-analysis figures and tables. It synthesizes transferable principles from first-party OpenAI quantitative visuals and OpenAI-authored technical publications. It is **not an official OpenAI brand guide**. Its purpose is calm, precise, publication-grade evidence communication with minimal decoding cost, adaptive layout, and strict scientific fidelity.


## Canonical identity and activation contract

- **Canonical display name:** `Scientific Visuals & Tables`
- **Stable skill identifier:** `scientific-visual-table-style`
- **Codex explicit invocation:** `$scientific-visual-table-style` or select it through `/skills`.
- **ChatGPT explicit invocation when installed as a skill/plugin:** `@Scientific Visuals & Tables`.

When this skill is explicitly invoked, use it as the default standard for every scientific,
research, quantitative, statistical, benchmark, data-analysis, or analytical figure and table
produced in the current task or chat, unless the user explicitly overrides a rule.

A host must read this full `SKILL.md` and the required core references before substantive visual
work. Merely recognizing the name is not equivalent to loading the skill. If the host cannot
access the installed package, it must say so clearly; it must not claim that the skill was loaded,
reconstruct it from memory, silently substitute a generic plotting style, or rely on a compressed
summary when the full files are available.

### Generative-image boundary

Do **not** route explicit generative-image requests through this skill. Requests to generate an
image, illustration, artwork, photorealistic scene, concept art, or an Images 2 / image-generation-model
output belong to the image-generation workflow unless the user explicitly asks to combine
it with a data-driven scientific visual. In mixed tasks, keep the analytical-visual workflow and
generative-image workflow conceptually and operationally separate.

### Self-containment

This skill must be executable without access to any prior chat. Do not assume knowledge of
previous visuals, prior corrections, examples outside the package, or undocumented preferences.
All durable standards are defined in this file and its bundled references, templates, and scripts.
## Use this skill when

Use it for any task whose primary output includes one or more of the following:

- numerical or model-comparison tables;
- benchmark tables and ablation tables;
- bar, line, scatter, interval, calibration, distribution, or heatmap figures;
- score-versus-cost, score-versus-latency, or Pareto-frontier plots;
- before-versus-after or baseline-versus-method comparisons;
- multi-model, multi-benchmark, or multi-panel result figures;
- quantitative system diagrams or evaluation workflows;
- a visual-authorship pass over existing research evidence;
- a request for an OpenAI-like, premium, restrained, or highly polished scientific visual style.

Do not invoke this skill for explicit generative-image, Images 2, illustration, photography, artwork, or photorealistic-render requests unless the user explicitly asks to combine that workflow with a data-driven quantitative visual.

## Authority and preservation rules

1. **User instructions and supplied templates outrank this skill.** When the user gives an exact format, reproduce it faithfully unless they explicitly request redesign.
2. **Scientific content is immutable unless the user explicitly authorizes scientific edits.** Do not change values, uncertainty, sample definitions, claims, labels, model names, experimental conditions, ordering semantics, or conclusions merely to improve appearance.
3. **Actual values remain primary.** Never replace numerical results with deltas alone. Deltas may be secondary only when they materially aid interpretation.
4. **Visual simplification must not remove evidence.** Reduce decoding overhead, not scientific information.
5. **Do not fabricate missing uncertainty, baselines, sample sizes, costs, or metadata.** Flag their absence in a note or QA report.
6. **Faithful execution outranks creative reinterpretation.** When the intended composition or established visual system is clear, preserve it.

## Required progressive reading

Read only what the task requires, but always read the core files below before substantive visual work:

- `references/style_contract.md` — enforceable design rules and correction patterns.
- `references/form_selection.md` — deterministic chart/table selection rules.
- `references/quality_gates.md` — render, integrity, and adversarial QA gates.

For reference retrieval or style matching, use:

- `references/top_reference_set.md` — canonical few-shot set.
- `references/openai_visual_reference_library.jsonl` — full structured corpus.
- `references/direct_asset_manifest.txt` — direct first-party/paper-hosted asset links.
- `scripts/select_references.py` — deterministic retrieval helper.

For implementation, use or adapt:

- `templates/openai_visuals.py` — Matplotlib theme, plot helpers, and figure audit.
- `templates/openai_table.tex` — LaTeX table skeleton using `booktabs`, `siunitx`, and `threeparttable`.
- `templates/openai_table.css` — HTML table styling.
- `templates/visual_spec.schema.json` — intermediate design-spec schema.

## Non-negotiable workflow

A visual is not finished when the code runs. It is finished only after the final-size render passes all gates.

### 1. Lock the evidence

Before designing, record:

- the exact data source and immutable values;
- metric name, unit, direction, denominator, and aggregation;
- uncertainty definition and sample/seed count, if available;
- required baselines, model order, conditions, and exclusions;
- the one-sentence scientific message the visual must communicate;
- target medium and final dimensions.

If editing an existing manuscript, create a content checksum or structured extraction before redesign when practical. Compare the final labels and values against the source after rendering.

### 2. Write a visual specification before plotting

Create a compact internal specification conforming to `templates/visual_spec.schema.json`. At minimum define:

- `claim`;
- `visual_form`;
- `metric`, `unit`, and `direction`;
- `focal_series` and required baselines;
- stable series/category order;
- target width and height;
- uncertainty treatment;
- annotation plan;
- table precision or axis tick policy;
- output formats.

Do not begin styling until the form and claim are explicit.

### 3. Retrieve form-matched references

Use two layers:

1. **Global language:** select two or three Tier-1 references from `top_reference_set.md`.
2. **Form-specific grammar:** select three to five examples matching the required form.

Example:

```bash
python scripts/select_references.py \
  --query "cost latency pareto frontier" \
  --limit 5 \
  --max-tier 2
```

Reference weighting:

- Tier 1: current OpenAI web pages and Deployment Safety Hub — primary source for typography, hierarchy, color restraint, spacing, and annotation.
- Tier 2: OpenAI technical reports and system cards — primary source for scorecards, uncertainty, and dense evidence presentation.
- Tier 3: OpenAI-authored research papers — primary source for scientific forms such as ablations, distributions, calibration, and scaling curves.
- Tier 4: historical reports — use only when no current equivalent exists.

Do not average every source into one style. Use Tier 1 for the visual language and lower tiers only for form-specific structure.

### 4. Select the simplest truthful form

Use `references/form_selection.md`. Core defaults:

- exact lookup across many metrics → table;
- ranking of up to roughly 12 categories → horizontal bar or dot plot;
- ordered x or time → line plot;
- two quantitative variables → scatter plot;
- capability versus cost/latency → frontier scatter;
- paired before/after → dumbbell, slope, or paired dots;
- uncertainty-centered comparison → dot-and-interval plot;
- matrix with meaningful row/column geometry → heatmap;
- distribution or reliability → ECDF, histogram, box/violin, pass@k, or worst-of-k curve;
- many benchmarks with repeated structure → small multiples with shared scales;
- dense exact ablation values → grouped table; trends across ablation strength → line/dot plot.

Prefer a table-plus-one-chart pair over one overloaded chart when both exact lookup and immediate interpretation are required.

### 5. Build at final size

Never design a large figure and shrink it later. Set the intended final dimensions first.

Default paper sizes when unspecified:

- single-column: 85 mm wide;
- double-column: 178 mm wide;
- default aspect ratio: 1.45–1.80 for one-panel charts;
- compact table width: the exact text block width.

Minimum final-size text:

- manuscript: 8 pt absolute minimum; prefer 8.5–9.5 pt for axes and table body;
- slides: 14 pt absolute minimum within a figure; prefer 16–20 pt;
- web: 12 CSS px absolute minimum; prefer 13–16 px.

If the venue specifies dimensions or font minima, venue rules override these defaults.

### 6. Apply the visual system

Core visual language:

- white or subtly warm-white background;
- near-black primary text;
- one focal accent per figure;
- progressively muted baselines;
- sentence-case labels;
- regular and semibold as the dominant weights;
- no decorative gradient, shadow, 3D effect, or large gray plotting panel;
- few major ticks and no dense minor grid;
- direct labels whenever they remove legend lookup;
- stable model order and color mapping across the whole document;
- visible hierarchy between the main result and supporting evidence;
- generous but controlled whitespace.

Use the exact palette and geometry defaults in `references/style_contract.md` or the implementation template.

### 7. Enforce chart-specific integrity

- Bars start at zero unless the chart is explicitly a deviation plot with a visible reference baseline.
- Line charts require an ordered or continuous x-axis. Do not connect unrelated categories.
- Log scales must be explicitly labeled and justified by order-of-magnitude range.
- Dual y-axes are prohibited by default. Use aligned panels instead.
- Uncertainty must be visible when it changes interpretation.
- Model names, conditions, and reasoning-effort settings must not be hidden in footnotes when they affect the comparison.
- Cost and latency figures use real units and disclose pricing/timing assumptions.
- Pareto claims must be computed from the plotted points, not asserted visually.
- Direct labels must not overlap, cross through marks, or require leader-line tangles.

### 8. Enforce table-specific integrity

- No vertical rules.
- Use thin top, header, group, and bottom rules only.
- Long labels left-aligned; numeric values right- or decimal-aligned.
- Units and metric direction belong in headers or a concise note.
- Group rows semantically; do not use color blocks as a substitute for hierarchy.
- Use consistent meaningful precision by metric family.
- Use an em dash for unavailable/not applicable; never use zero as a missing-value placeholder.
- Bold only the best, focal, or decision-relevant values. Do not bold whole rows.
- When uncertainty intervals overlap materially, do not manufacture a unique winner through bolding.
- Actual values are primary; optional deltas appear in a subordinate column or second line.
- If the table exceeds approximately 8 numeric columns or becomes unreadable at final width, transpose, split by semantic family, or move full detail to an appendix.

### 9. Render, inspect, correct, and re-render

Always render the final artifact at actual delivery dimensions.

Required visual inspection:

- 100% final-size view;
- grayscale view;
- low-vision/color-deficiency-safe distinction check;
- clipping and overlap check;
- label and unit audit;
- value-by-value spot check against source;
- five-second message test;
- cross-figure consistency check.

Use `scripts/visual_qa.py` for SVG/PNG/PDF preflight and `scripts/table_qa.py` for CSV/TSV numerical-table linting. These scripts supplement, not replace, human visual inspection.

### 10. Shipping gate

Do not deliver until all of the following are true:

- the main claim is visible within five seconds;
- every value and label matches the source;
- metric direction and units are unambiguous;
- no text is clipped or too small at final size;
- the focal result is visually dominant but baselines remain honestly visible;
- related figures share the same model order, palette, scales, and terminology;
- table precision and emphasis are consistent;
- uncertainty and denominator information are present where available;
- vector output is available for line art whenever possible;
- editable source is retained;
- the final-size render has been inspected after the most recent change.

## Deterministic defaults

Use these only when the user, venue, or existing document supplies no stronger constraint.

### Palette

- primary ink: `#111111`;
- secondary ink: `#404040`;
- muted text: `#6F6F6F`;
- light baseline: `#B6B6B0`;
- hairline/rule: `#D8D8D4`;
- grid: `#E8E8E5`;
- subtle fill: `#F5F5F2`;
- focal teal: `#1F6F5F`;
- focal tint: `#DDE9E5`;
- risk/regression: `#B5473C`;
- warning: `#9A681A`.

These are an OpenAI-inspired operational palette, not claimed official brand colors. Default to grayscale plus one accent. Use risk colors only semantically.

### Type

Use a neutral sans-serif stack:

`Arial, Helvetica, Inter, Liberation Sans, DejaVu Sans, sans-serif`

Do not bundle, expose, or redistribute proprietary font files. Use tabular numerals where the output format supports them.

### Lines and marks at manuscript size

- axis/rule line: 0.6–0.8 pt;
- baseline series: 1.0–1.2 pt;
- focal series: 1.5–1.8 pt;
- error bars: 0.7–0.9 pt;
- markers: 4–6 pt;
- panel labels: 9–10 pt semibold;
- annotation leader: 0.6–0.8 pt.

### Spacing

- plot outer margin: roughly 4–8% of figure width;
- panel gutter: roughly 4–6% of figure width;
- title-to-plot gap: 6–10 pt;
- axis-label-to-tick gap: 4–7 pt;
- table body leading: 1.25–1.40× font size;
- table horizontal cell padding: 4–7 pt;
- semantic row-group gap: 3–6 pt.

### Number formatting

- percentages: usually 0–1 decimal places;
- proportions: 2–3 decimal places only when that precision is meaningful;
- costs: 2–3 significant figures with currency/unit in header;
- latency: choose one unit per table/axis and convert consistently;
- counts: thousands separators where helpful;
- scientific notation: use only when scale requires it and keep exponent treatment consistent;
- negative values: use a true minus sign where supported;
- unavailable: em dash;
- below detection/threshold: use `<x` only when scientifically defined.


## Empirically hardened adaptive rules

Apply these condition → action → fallback rules before any one-off manual rescue:

1. **Rendered header overflow:** If the title, subtitle, or note exceeds the reserved header block,
   measure the rendered text bounds and increase the header reserve. Do not reduce important text
   below the final-size minimum merely to fit a fixed canvas.
2. **Long categorical labels:** Prefer a horizontal comparator. Increase the left margin according
   to rendered label width; wrap only at semantic boundaries. If labels still dominate the canvas,
   use concise display labels plus a mapping note or an exact-value table.
3. **Dense grouped comparisons:** Use grouped bars only for roughly 2–4 conditions and at most about
   8 groups. Beyond that, switch to aligned dots, small multiples, a heatmap when matrix geometry is
   meaningful, or a table. Never solve density by making bars or text microscopic.
4. **Direct-label collisions:** Attempt deterministic vertical separation while preserving mark-to-
   label association. If collision-free direct labels cannot be achieved without tangled leaders,
   use one compact shared legend outside the data region.
5. **Multiple model families on a trade-off plot:** Compute nondominated points under one protocol,
   but connect ordered operating settings only within the same family. Never draw a line between
   unrelated families merely because both points lie on the global frontier.
6. **Small differences:** Prefer dots, intervals, paired dots, or an exact-value table over bars when
   a zero baseline would compress meaningful variation. Preserve absolute values and disclose any
   narrowed axis explicitly.
7. **Five or more line series:** Direct-label only when endpoint spacing is sufficient. Otherwise use
   small multiples or one shared legend with stable order; mute secondary series without erasing them.
8. **Font availability:** Resolve to an installed neutral sans-serif deterministically. Do not depend
   on proprietary fonts or allow silent fallback to change geometry between renders.
9. **Final-artifact regression:** Every layout change requires a new export and inspection at target
   dimensions. Never assume a source-code correction fixed the rendered artifact.

## Recurring failure modes and mandatory corrections

| Failure | Required correction |
|---|---|
| Default Matplotlib colors or styling | Apply the shared theme before plotting; use grayscale plus one accent. |
| Figure has no obvious message | Rewrite the visual claim and redesign hierarchy before cosmetic work. |
| Legend causes repeated lookup | Direct-label focal series/endpoints or move to aligned small multiples. |
| Too many equally salient series | Mute baselines, aggregate only when scientifically valid, or split into panels. |
| Large gray panel or dashboard cards | Return to a white canvas with sparse rules and whitespace. |
| Saturated rainbow palette | Use position, line style, marker, and one accent instead of many hues. |
| Tiny text after manuscript insertion | Rebuild at final dimensions; never fix by exporting at higher DPI alone. |
| Inconsistent model order/color across panels | Define one document-level mapping and reuse it everywhere. |
| Bars use truncated axis | Start at zero or convert to dot/interval/deviation form with explicit baseline. |
| Line connects unordered categories | Use bars, dots, or facets instead. |
| Dual y-axis | Replace with aligned panels or normalize only with explicit, interpretable units. |
| Table is a boxed grid | Remove vertical rules and most cell borders; create hierarchy with alignment and spacing. |
| Table reports deltas instead of values | Restore actual values; make deltas subordinate. |
| Mixed or false precision | Define precision per metric family and round consistently. |
| Every best-looking value is bold | Bold only the predetermined focal/best values; address statistical ties honestly. |
| Repeated titles, legends, or labels in every panel | Share labels and suppress redundant text. |
| Uncertainty omitted where it changes the conclusion | Add valid intervals or explicitly state that uncertainty is unavailable. |
| Cost/latency metric lacks assumptions | Add a concise methodological note with pricing, hardware, batch, or timing basis. |
| Annotation describes instead of explains | Keep only threshold, causal, frontier, or operating-point annotations. |
| Decorative icons/arrows dominate | Remove them; use geometry, labels, and alignment to communicate structure. |
| Low-resolution raster output | Export SVG/PDF for line art or at least 2×/3× PNG for raster. |
| Visual inspected only in source notebook | Render the final deliverable and inspect the inserted/exported result. |

## Output expectations

For substantive visual work, preserve or deliver as appropriate:

- editable source code;
- source data or a clear data-loading path;
- vector figure (`.svg` or `.pdf`) for line art;
- high-resolution `.png` preview when useful;
- final table source (`.tex`, `.html`, `.docx`, `.xlsx`, or manuscript source);
- a concise visual-spec or caption note documenting metric direction, uncertainty, and conditions.

Do not deliver internal QA renders unless requested.

## Package map

- `SKILL.md` — routing, activation contract, workflow, non-negotiables, and defaults.
- `agents/openai.yaml` — host-facing display metadata and default invocation prompt.
- `references/style_contract.md` — full design and layout contract.
- `references/form_selection.md` — deterministic visual-form decision rules.
- `references/quality_gates.md` — scientific and visual validation.
- `references/top_reference_set.md` — canonical OpenAI reference set.
- `references/reference_design_spec.md` — source synthesis used to construct this skill.
- `references/openai_visual_reference_library.jsonl` — complete reference corpus.
- `references/direct_asset_manifest.txt` — direct asset index.
- `templates/openai_visuals.py` — reusable plotting implementation.
- `templates/openai_table.tex` — publication table implementation.
- `templates/openai_table.css` — web table implementation.
- `templates/visual_spec.schema.json` — intermediate-spec schema.
- `scripts/select_references.py` — reference retrieval.
- `scripts/visual_qa.py` — SVG/PNG/PDF preflight.
- `scripts/table_qa.py` — tabular-data linting.
- `examples/example_openai_visuals.py` — runnable chart examples.
