# Reference and dependency audit

The machine link audit (`reference-links.json`) checks actual local Markdown targets in active skills, docs, workflows and roles. All catalog routes and required root manifest paths are separately checked. Source inspection records every source Markdown link, external URL, dependency line and Python import. Independent audits read the full text and distinguish resource dependencies from illustrative paths/output filenames.

## Explicitly unresolved source references

| Source reference | Status / disposition |
|---|---|
| ARMS `_shared/scoring_rubric.md` | Not supplied; exact private rubric unavailable. Source preserves reference; active instructions use the included rubric only with that limitation. |
| ARMS failure-diagnoser, consistency-auditor, venue-compliance-gate | Missing original helpers; newly authored procedural replacement roles supplied in agents/ and labelled as substitutions. |
| ARMS telemetry hooks, auditor/apply scripts, snapshots and macOS LaunchAgent | Not supplied; full README specifications preserved as unavailable private infrastructure. |
| ARMS root / skill-local research brief templates | Both preserved. Richer root author-grounded template preferred; local statistics-specific template remains accessible. |
| ARMS `neurips_2025.sty` and manuscript PDF | Absent; no full manuscript build claimed. Six supplied figure PDFs retained. |
| ARMS `validated_results`, mve_results.csv, stress_tests_combined.csv | Runtime input/output layout differs from shipped data names. No silent rename of historical results into purported rerun outputs. Use a task copy and resolve experiment provenance before a full rerun. |
| ARMS private exemplar, production evaluation generators/raw datasets | Absent; bundled small examples and advisory default metrics retained. Supply an actual user exemplar for `--ref`. |
| Clinical trials_data.csv/ARMS-Biostat disclaimer | Absent from this snapshot; treated as historical cross-repository text. |
| Academic PPTX `pptx` skill, editing.md and pptxgenjs.md | Separate backend docs absent; host authoring backend required for actual PPTX file operations. |
| Academic PPTX `LICENSE.txt` | Inaccurate metadata reference; actual supplied LICENSE is MIT, retained verbatim. |
| Visual corpus URLs, fonts, GPT-6 Astra referenced paper and external assets | Metadata/links preserved; most remote contents not bundled or freshly fetched. No official endorsement/source verification inferred. |
| LaTeX sample results.pdf, figure.pdf, refs.bib and before/after images | Illustrative runtime/user file placeholders, not omitted supplied files. |
| Host Read/Bash/Task/WebSearch/Agent tool names and named models | Host-specific capability requirements; mapped conceptually to available tools with actual execution checks. |

## Active copy changes

Unique skill namespaces and relative package paths resolve supplied siblings/support files. Global studio activation is scoped to relevant tasks. Missing footer text is not fabricated. The three standalone repositories preserve all support resources in active copies and the original source tree. Component adapter records describe narrow script portability/correctness changes and regression checks.

## Visual inspection of supplied resources

All 25 supplied PNGs were decoded and visually inspected on a labelled contact sheet. All seven PDFs were parsed and rendered: the five-page academic presentation guide was inspected page-by-page through a contact sheet, and the six one-page ARMS figures were inspected. These are historical assets, not newly authored research findings. The ARMS method overview has overlapping small labels; the comparison figure has excessive white space and source-weight figure has crowded labels. These observations are retained as source-quality limitations; original scientific artifacts were preserved unchanged, and no claim that they passed the unified publication visual gate is made.
