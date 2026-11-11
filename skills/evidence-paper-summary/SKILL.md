---
name: evidence-paper-summary
description: "Summarize a supplied or located paper's question, methods, numerical findings and limitations at brief or detailed depth, including which claims it supports."
---
## Selection and handoffs

Summarize one paper at an appropriate depth.

**Select for:** Summarize a supplied or located paper's question, methods, numerical findings and limitations at brief or detailed depth, including which claims it supports.

**Expected work:** Read full available text; Verify title-only inputs; Abstract-only fallback; Key numeric findings; Stated/missed limitations; Three depths; Good-for-citing-when

**Expected output:** Output format
**Citation:** full reference.
**In one sentence:** what the study found.
**Question:** ...
**Methods:** design, sample, setting, duration, measures.
**Key findings:** 3 to 6 bullets with numbers.
**Limitations:** ...
**What it means:** practical takeaway and how much to trust it.
**Good for citing when:** the kind of claim this paper supports.

**Scope boundaries:** Do not activate solely because the family was used earlier or for unrelated chat.; Use the adjacent specialist when its distinct task is requested: scholar-paper-breakdown. Keep specialized modes: three depth levels and citing-use guidance differ from persistent page-grounded paper Q&A and supplement inspection.

**Related skills:** [scholar-paper-breakdown](../scholar-paper-breakdown/SKILL.md)

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

# Paper Summary


## Steps
1. Read the full text the user provides. If only a title is given, search for the paper and verify it before summarizing. If you cannot access it, say so and summarize only the abstract or ask the user to paste the text.
2. Identify the question, design, sample, measures and main results.
3. Pull the key numbers: effect sizes, percentages, confidence intervals.
4. Note the limitations the authors state and any they miss.

## Output format
**Citation:** full reference.
**In one sentence:** what the study found.
**Question:** ...
**Methods:** design, sample, setting, duration, measures.
**Key findings:** 3 to 6 bullets with numbers.
**Limitations:** ...
**What it means:** practical takeaway and how much to trust it.
**Good for citing when:** the kind of claim this paper supports.

## Levels
Offer three depths: a 3-line summary, a standard summary (above), or a detailed critical summary with appraisal (see study-appraisal).

## Rules
Do not add findings that are not in the paper. Quote only short exact phrases, with page numbers when available.
