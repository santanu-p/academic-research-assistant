# Provenance and Reference Policy

The bundled reference corpus was assembled from first-party OpenAI pages, OpenAI Deployment Safety Hub assets, official OpenAI technical/system reports, and OpenAI-authored primary research papers. It contains metadata and links rather than redistributed visual assets.

## Reference tiers

1. **Tier 1 — current OpenAI web / Deployment Safety Hub**  
   Use for current visual language: composition, hierarchy, palette restraint, typography, whitespace, direct labeling, and launch-table structure.

2. **Tier 2 — OpenAI technical/system report**  
   Use for risk scorecards, safety evidence, uncertainty, dense technical tables, and formal reporting.

3. **Tier 3 — OpenAI-authored research paper**  
   Use for scientific forms: ablations, calibration, distributions, scaling laws, pass@k/worst-of-k, evaluator studies, and human–AI comparisons. Do not assume conference-paper styling is current OpenAI brand styling.

4. **Tier 4 — historical OpenAI report**  
   Use only for enduring plot forms that lack a current equivalent. Modernize typography and spacing using Tier 1.

## Reference selection constraints

- Prefer exact direct assets, exact chart anchors, or exact PDF pages.
- Use the nearest stable section only when an individual web-native chart has no stable asset or anchor.
- Do not infer an official color code or font from a raster screenshot.
- Do not redistribute proprietary fonts or copyrighted image files as part of the skill.
- External links may change; the structured corpus records publication, caption, direct asset URL, parent URL, and link precision to support repair.
- When current style matters materially, verify live first-party pages because web design and product visual language can evolve.

## Corpus files

- `openai_visual_reference_library.jsonl`: one reference per line for deterministic retrieval.
- `top_reference_set.md`: ranked canonical set.
- `direct_asset_manifest.txt`: asset URLs and captions.
- `reference_design_spec.md`: the compact source synthesis from which this expanded skill was derived.
