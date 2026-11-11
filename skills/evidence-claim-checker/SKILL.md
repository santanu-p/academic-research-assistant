---
name: evidence-claim-checker
description: "Check a research claim or headline against its original study and wider evidence, giving a sourced verdict and an accurate replacement claim."
---
## Selection and handoffs

Check a precise research claim against original and wider evidence.

**Select for:** Check a research claim or headline against its original study and wider evidence, giving a sourced verdict and an accurate replacement claim.

**Expected work:** Original-source tracing; Population/effect/design comparison; Wider-evidence check; Six-category verdict; Distortion checklist; Corrected claim wording

**Expected output:** Output format
**Claim**, **Verdict**, **What the research actually says** (with citations), **What the claim gets wrong or leaves out**, and **A more accurate version of the claim.**

**Scope boundaries:** Do not activate solely because the family was used earlier or for unrelated chat.; Use the adjacent specialist when its distinct task is requested: evidence-source-verification. Keep: proposition truth and claim scope differ from whether a source exists or its DOI matches.

**Related skills:** [evidence-source-verification](../evidence-source-verification/SKILL.md)

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

# Claim Checker


## Steps
1. Restate the exact claim in one sentence.
2. Find the source: the original study, report or data behind it. Trace press releases and news stories back to the paper.
3. Compare the claim with what the study actually found: population, size of effect, design and conclusion.
4. Check the wider evidence (see evidence-answer): does one study stand alone or fit a consistent body of research?
5. Give a verdict.

## Verdict scale
| Verdict | Meaning |
|---|---|
| Supported | Good evidence backs the claim as stated |
| Mostly supported | Broadly right, but overstated or missing context |
| Mixed | Evidence points both ways |
| Not supported | The evidence does not back it |
| False | Good evidence contradicts it |
| Unproven | Too little research to say |

## Common distortions in headlines
- Association reported as cause.
- Relative numbers without absolute numbers.
- Animal or lab findings presented as human results.
- A small or early study presented as settled.
- One study cherry-picked from a larger, different body of evidence.
- "Up to" figures presented as typical.

## Output format
**Claim**, **Verdict**, **What the research actually says** (with citations), **What the claim gets wrong or leaves out**, and **A more accurate version of the claim.**
