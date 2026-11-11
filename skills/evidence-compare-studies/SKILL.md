---
name: evidence-compare-studies
description: "Compare studies in an aligned evidence table, explain agreement or disagreement, and weigh their conclusions by quality."
---
## Selection and handoffs

Explain why several named studies agree or differ.

**Select for:** Compare studies in an aligned evidence table, explain agreement or disagreement, and weigh their conclusions by quality.

**Expected work:** Matched-field extraction; Side-by-side table; Population/measure/dose/time/design/era disagreement analysis; Quality-weighted judgment

**Expected output:** Output format
The table, then "Where they agree", "Where they differ and why", and "Overall weight of evidence".

**Scope boundaries:** Do not activate solely because the family was used earlier or for unrelated chat.; Use the adjacent specialist when its distinct task is requested: evidence-data-extraction. Keep: extraction records reported values; comparison adds cross-study explanation and adjudication.

**Related skills:** [evidence-data-extraction](../evidence-data-extraction/SKILL.md)

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

# Compare Studies


## Steps
1. List the studies with full references.
2. Extract the same fields from each (see data-extraction).
3. Line them up in a comparison table.
4. Explain agreements and differences.
5. Give an overall judgment weighted by quality.

## Comparison table columns
Study, design, sample (size and who), setting, intervention or exposure, outcome measure, main result (with numbers), quality rating.

## Why studies disagree
- Different populations or settings.
- Different definitions and measures of the outcome.
- Different time frames or doses.
- Design strength and risk of bias.
- Small samples producing noisy results.
- Publication era: newer methods or data.

## Output format
The table, then "Where they agree", "Where they differ and why", and "Overall weight of evidence".
