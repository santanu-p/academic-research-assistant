---
name: evidence-data-extraction
description: "Extract reported study characteristics, findings and statistics into tables or CSV rows, preserving units and marking missing values."
---
## Selection and handoffs

Capture reported study characteristics and results reproducibly.

**Select for:** Extract reported study characteristics, findings and statistics into tables or CSV rows, preserving units and marking missing values.

**Expected work:** User-agreed fields; Exact reported units/statistics; Not-reported values; Markdown/CSV rows; Means/SD/N or effect/SE/CI for pooling; Qualitative themes

**Expected output:** Requested artifact described by complete workflow sections above.

**Scope boundaries:** Do not activate solely because the family was used earlier or for unrelated chat.; Use the adjacent specialist when its distinct task is requested: evidence-compare-studies. Keep: reusable data capture, including pooling statistics and qualitative themes, does not itself adjudicate studies.

**Related skills:** [evidence-compare-studies](../evidence-compare-studies/SKILL.md)

Apply this skill only to the selected task. Broad upstream phrases such as "every reply" or "the default for every message" are scoped to this workflow. They do not activate it for unrelated chat. User instructions and the [integration contract](../../docs/INTEGRATION.md) govern combined work. Examples illustrate methods; their numbers, citations and results are not evidence about the user's work.

## Preserved source instructions


## Unified plugin integration

Read [the integration contract](../../docs/INTEGRATION.md) when combining workflows. This active copy retains the complete source instructions below with namespaced skill references. Original bytes and upstream metadata remain in `../../resources/`. Resolve tools by their actual host capabilities; tool names in upstream instructions are capability requirements, not proof of connection. Use the task workspace for generated outputs. Treat historical case-study results as supplied examples, not newly verified findings.

Family skill aliases (read the linked SKILL.md before use):
- `citation-chaining` → `evidence-citation-chaining` (`../evidence-citation-chaining/SKILL.md`)
- `citations-and-references` → `evidence-citations-and-references` (`../evidence-citations-and-references/SKILL.md`)
- `claim-checker` → `evidence-claim-checker` (`../evidence-claim-checker/SKILL.md`)
- `compare-studies` → `evidence-compare-studies` (`../evidence-compare-studies/SKILL.md`)
- `data-extraction` → `evidence-data-extraction` (`../evidence-data-extraction/SKILL.md`)
- `database-guide` → `evidence-database-guide` (`../evidence-database-guide/SKILL.md`)
- `debate-and-argument-evidence` → `evidence-debate-and-argument-evidence` (`../evidence-debate-and-argument-evidence/SKILL.md`)
- `decision-evidence` → `evidence-decision-evidence` (`../evidence-decision-evidence/SKILL.md`)
- `evidence-answer` → `evidence-evidence-answer` (`../evidence-evidence-answer/SKILL.md`)
- `evidence-based-writing` → `evidence-evidence-based-writing` (`../evidence-evidence-based-writing/SKILL.md`)
- `evidence-help` → `evidence-evidence-help` (`../evidence-evidence-help/SKILL.md`)
- `evidence-meter` → `evidence-evidence-meter` (`../evidence-evidence-meter/SKILL.md`)
- `field-guides` → `evidence-field-guides` (`../evidence-field-guides/SKILL.md`)
- `find-studies` → `evidence-find-studies` (`../evidence-find-studies/SKILL.md`)
- `literature-review` → `evidence-literature-review` (`../evidence-literature-review/SKILL.md`)
- `meta-analysis` → `evidence-meta-analysis` (`../evidence-meta-analysis/SKILL.md`)
- `open-access-full-text` → `evidence-open-access-full-text` (`../evidence-open-access-full-text/SKILL.md`)
- `paper-summary` → `evidence-paper-summary` (`../evidence-paper-summary/SKILL.md`)
- `plain-language-research` → `evidence-plain-language-research` (`../evidence-plain-language-research/SKILL.md`)
- `research-evidence-finder` → `evidence-research-evidence-finder` (`../evidence-research-evidence-finder/SKILL.md`)
- `research-gaps` → `evidence-research-gaps` (`../evidence-research-gaps/SKILL.md`)
- `research-proposal-background` → `evidence-research-proposal-background` (`../evidence-research-proposal-background/SKILL.md`)
- `research-question` → `evidence-research-question` (`../evidence-research-question/SKILL.md`)
- `search-strings` → `evidence-search-strings` (`../evidence-search-strings/SKILL.md`)
- `source-verification` → `evidence-source-verification` (`../evidence-source-verification/SKILL.md`)
- `statistics-explained` → `evidence-statistics-explained` (`../evidence-statistics-explained/SKILL.md`)
- `study-appraisal` → `evidence-study-appraisal` (`../evidence-study-appraisal/SKILL.md`)
- `study-designs-and-evidence-levels` → `evidence-study-designs-and-evidence-levels` (`../evidence-study-designs-and-evidence-levels/SKILL.md`)
- `systematic-review` → `evidence-systematic-review` (`../evidence-systematic-review/SKILL.md`)

---

# Data Extraction


## Standard extraction fields
| Field | Example |
|---|---|
| Reference | Author, year |
| Country and setting | Schools in Finland |
| Design | Cluster RCT |
| Sample | 1,240 students, ages 12 to 14 |
| Intervention or exposure | Daily 20-minute reading program |
| Comparison | Usual teaching |
| Outcome and measure | Reading score, standardized test |
| Result | +0.18 SD (95% CI 0.05 to 0.31) |
| Follow-up | 1 school year |
| Quality | Moderate risk of bias |
| Notes | Funded by program developer |

## Steps
1. Agree on the fields with the user (add or remove to fit the question).
2. Extract only what the paper reports. Write "not reported" instead of guessing.
3. Keep units and statistics exactly as reported.
4. Output as a Markdown table or CSV-style rows the user can paste into a spreadsheet.

## Tips
- For a meta-analysis, capture means, standard deviations and group sizes, or the effect size with its standard error or confidence interval.
- For qualitative studies, extract themes with a short supporting description.
