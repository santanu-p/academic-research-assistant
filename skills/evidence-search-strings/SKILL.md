---
name: evidence-search-strings
description: "Build Boolean research queries for selected databases with synonyms, field tags, syntax limits, filters and too-many/too-few-result adjustments."
---
## Selection and handoffs

Produce database-specific executable search queries.

**Select for:** Build Boolean research queries for selected databases with synonyms, field tags, syntax limits, filters and too-many/too-few-result adjustments.

**Expected work:** OR/AND/NOT; Phrases/truncation/fields; Scholar no truncation; Scopus TITLE-ABS-KEY; WoS TS/NEAR; ERIC descriptors; 2-3 database adaptations; Recovery filters

**Expected output:** Output format
1. The concept table with synonyms.
2. A full Boolean string.
3. Adapted versions for 2 or 3 databases that fit the topic.
4. Suggested filters (years, document type, language) and tips if results are too many or too few.

**Scope boundaries:** Do not activate solely because the family was used earlier or for unrelated chat.; Use the adjacent specialist when its distinct task is requested: scholar-find-sources. Keep: concrete syntax and query adaptation differ from broader strategy planning with eligibility, search logs and chaining.

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

# Search Strings


## Building blocks
- **OR** joins synonyms inside one concept: ("remote work" OR telework OR "work from home").
- **AND** joins different concepts: (remote work terms) AND (productivity terms).
- **NOT** excludes, used sparingly.
- **Quotes** for exact phrases: "hybrid work".
- **Truncation** with an asterisk: employ* finds employee, employees, employment.
- **Parentheses** group each concept.
- **Field tags** narrow to title or abstract where the database supports them.

## Database notes
| Database | Tips |
|---|---|
| Google Scholar | Keep it short; supports quotes, OR, minus and intitle:; no truncation |
| Semantic Scholar | Natural-language queries work; filter by field, year and venue |
| Scopus | TITLE-ABS-KEY( ) field; full Boolean and truncation |
| Web of Science | TS= for topic; NEAR/x for proximity |
| JSTOR | Humanities and social sciences; use advanced search fields |
| ERIC | Education; use the ERIC thesaurus descriptors |
| SSRN, arXiv | Preprints in economics, law, physics, computer science and math |
| IEEE Xplore | Engineering and computing; use the command search |

## Output format
1. The concept table with synonyms.
2. A full Boolean string.
3. Adapted versions for 2 or 3 databases that fit the topic.
4. Suggested filters (years, document type, language) and tips if results are too many or too few.
