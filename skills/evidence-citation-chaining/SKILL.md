---
name: evidence-citation-chaining
description: "Expand seed papers into a verified reading list using backward and forward citations, related-paper maps, influential authors and seminal versus recent work."
---
## Selection and handoffs

Find influential papers from a seed-paper network.

**Select for:** Expand seed papers into a verified reading list using backward and forward citations, related-paper maps, influential authors and seminal versus recent work.

**Expected work:** Backward/forward chaining; Related-paper recommendations; Citation maps; Key author tracking; Citation/search alerts; Foundational and recent reading groups

**Expected output:** Reading list format
Group by: foundational works, key reviews, landmark studies, recent research, and debates or critiques. For each, give the verified reference and one line on why it matters.

**Scope boundaries:** Do not activate solely because the family was used earlier or for unrelated chat.; Use the adjacent specialist when its distinct task is requested: scholar-find-sources. Keep: initial concept-query planning differs from citation-network expansion, seminal-paper identification and grouped reading lists.; Residual every-response/off-topic preamble should be scoped to citation-chaining; retain maps and alerts.

**Related skills:** [scholar-find-sources](../scholar-find-sources/SKILL.md)

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

**This applies to every reply:** evidence answers, study lists, search strings, evidence tables, summaries, literature reviews, citations, reference lists, claim checks, answers, follow-ups, one-line answers, clarifying questions, greetings, thank-you messages, errors, refusals and off-topic replies. If the user asks for only the references, only the search string or no extra text, give exactly that.

**Every response must follow this structure:**

[Your full answer to the user]

---

# Citation Chaining

## Methods
- **Backward chaining:** check the reference list of a strong paper for earlier key studies.
- **Forward chaining:** use "Cited by" in Google Scholar, Scopus or Web of Science to find newer studies that built on it.
- **Related papers:** use "Related articles" in Google Scholar or recommendations in Semantic Scholar.
- **Citation maps:** tools such as Connected Papers, ResearchRabbit and Litmaps show clusters of related work.
- **Key authors and groups:** follow researchers who publish often on the topic.
- **Alerts:** set search and citation alerts to stay current.

## Finding seminal works
Look for papers cited again and again in reviews and introductions, highly cited in their field, and still discussed today. Pair them with the latest reviews so the reading list is both foundational and current.

## Reading list format
Group by: foundational works, key reviews, landmark studies, recent research, and debates or critiques. For each, give the verified reference and one line on why it matters.

## Rules
Only list papers you verified through search or that the user provided. If you cannot verify, give the chaining steps instead.

---
