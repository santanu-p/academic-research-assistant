---
name: evidence-evidence-answer
description: "Answer what research says across verified sources, explaining effect magnitude, disagreements, limitations and evidence strength."
---
## Selection and handoffs

Answer a question across verified research sources.

**Select for:** Answer what research says across verified sources, explaining effect magnitude, disagreements, limitations and evidence strength.

**Expected work:** Actual search; Best-fit evidence selection; Effect magnitude and populations; Five-level certainty; Disagreements; Verified factual citations; Causation restraint

**Expected output:** Output format
**Bottom line:** 2 to 3 sentences with the answer and the confidence level.
**What the evidence shows:** key findings with citations.
**How strong is it:** strong, moderate, limited, conflicting or insufficient, with the reason (study designs, sizes, consistency).
**Where studies disagree:** and possible reasons (populations, methods, measures).
**Limits and open questions.**
**Key sources:** the references used.

**Scope boundaries:** Do not activate solely because the family was used earlier or for unrelated chat.; Use the adjacent specialist when its distinct task is requested: scholar-evidence-synthesis. Candidate only for identical cross-study question/context and confidence-first output. Preserve actual retrieval/verification mode and scholar's clearly labeled unverified planning fallback.

**Related skills:** [scholar-evidence-synthesis](../scholar-evidence-synthesis/SKILL.md)

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

# Evidence Answer


## Purpose
Give the user the honest bottom line of the research, not just a list of papers.

## Steps
1. Restate the question precisely.
2. Search for the best evidence: systematic reviews and meta-analyses first, then strong primary studies.
3. Synthesize: what most good studies find, how big the effect is, and for whom.
4. Grade the strength of the evidence (see study-designs-and-evidence-levels).
5. Note disagreements, gaps and limits.
6. Cite every factual claim to a verified source.

## Output format
**Bottom line:** 2 to 3 sentences with the answer and the confidence level.
**What the evidence shows:** key findings with citations.
**How strong is it:** strong, moderate, limited, conflicting or insufficient, with the reason (study designs, sizes, consistency).
**Where studies disagree:** and possible reasons (populations, methods, measures).
**Limits and open questions.**
**Key sources:** the references used.

## Evidence strength scale
- **Strong:** several high-quality reviews or large studies agree.
- **Moderate:** consistent findings with some design limits.
- **Limited:** few or small studies.
- **Conflicting:** good studies disagree.
- **Insufficient:** not enough research to conclude.

## Rules
- Correlation is not causation; say so when the evidence is observational.
- Do not overstate: use "suggests" or "is associated with" when that is what the studies show.
