---
name: evidence-statistics-explained
description: "Explain research statistics in plain language, emphasizing uncertainty, effect magnitude, absolute risk and common interpretation traps."
---
## Selection and handoffs

Teach statistical meaning and common interpretation traps.

**Select for:** Explain research statistics in plain language, emphasizing uncertainty, effect magnitude, absolute risk and common interpretation traps.

**Expected work:** p/CI/effect/risk/r/regression/power; Absolute versus relative; Natural frequency example; P-hacking/subgroups/selection/averages traps; One-sentence implication

**Expected output:** Output format
Explain each number the user asks about, then say what it means for the conclusion in one plain sentence.

**Scope boundaries:** Do not activate solely because the family was used earlier or for unrelated chat.; Use the adjacent specialist when its distinct task is requested: scholar-results-interpreter. Keep: concept teaching and traps differ from reading a supplied test output and drafting a formal reported result.; Statistical thresholds, model defaults and test matrices are contextual heuristics, not universal rules or executed analyses.

**Related skills:** [scholar-results-interpreter](../scholar-results-interpreter/SKILL.md)

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

# Statistics Explained


## Key ideas
- **p-value:** how surprising the data would be if there were no real effect. p < 0.05 is a convention, not proof. It does not tell you the size or importance of the effect.
- **Confidence interval (CI):** the range of plausible values for the true effect. Narrow means precise; a CI crossing zero (or 1 for ratios) means no clear effect.
- **Effect size:** how big the effect is. Cohen's d: about 0.2 small, 0.5 medium, 0.8 large. Always ask "how much?", not just "is it significant?".
- **Relative vs absolute:** "doubles the risk" can mean going from 1 in 10,000 to 2 in 10,000. Always look for absolute numbers.
- **Correlation (r):** strength of a linear relationship from -1 to 1. It does not show cause.
- **Regression:** estimates one variable's link with an outcome while adjusting for others; it cannot adjust for factors that were not measured.
- **Power and sample size:** small studies can miss real effects and exaggerate the ones they find.

## Common traps
- Significant but tiny effects.
- Many outcomes tested, only the "significant" one reported (p-hacking).
- Subgroup findings presented as main results.
- Survivorship and selection effects.
- Averages hiding very different groups.

## Output format
Explain each number the user asks about, then say what it means for the conclusion in one plain sentence.
