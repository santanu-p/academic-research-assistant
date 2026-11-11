---
name: evidence-source-verification
description: "Verify citation identity and DOI matches, then check retractions, corrections, venue reliability and peer-review status."
---
## Selection and handoffs

Audit source existence and publication status.

**Select for:** Verify citation identity and DOI matches, then check retractions, corrections, venue reliability and peer-review status.

**Expected work:** Exact title; DOI target match; Publisher record; Retractions; Predatory signs; Peer review; Authors/conflicts; Errata/replies; Five-status verdict; No invented repairs

**Expected output:** Output format
For each reference: Verified / Partly matches / Could not verify / Retracted / Questionable venue, with what you checked and a corrected reference where possible.

**Scope boundaries:** Do not activate solely because the family was used earlier or for unrelated chat.; Use the adjacent specialist when its distinct task is requested: scholar-source-evaluation. Keep: bibliographic identity/status audit differs from broad authority, bias, relevance and appropriate viewpoint-use judgments.

**Related skills:** [scholar-source-evaluation](../scholar-source-evaluation/SKILL.md)

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

# Source Verification


## Check a citation is real
1. Search the exact title in quotes.
2. Resolve the DOI through doi.org and confirm the title, authors, year and journal match.
3. Check the journal's own website or the database record.
4. Mismatched authors, a DOI pointing to a different paper, or no record at all means the citation is likely fabricated.

## Check the source is trustworthy
- **Retractions:** search the Retraction Watch Database and look for notices on the publisher page.
- **Predatory journals:** warning signs include guaranteed fast acceptance, aggressive email invitations, fake impact metrics, no clear peer review and unclear editorial boards. Check membership in DOAJ or COPE for open-access journals.
- **Peer review:** preprints (arXiv, SSRN, OSF) are not yet peer reviewed.
- **Authors:** affiliation, track record and conflicts of interest.
- **Corrections and comments:** check for errata and published replies.

## Output format
For each reference: Verified / Partly matches / Could not verify / Retracted / Questionable venue, with what you checked and a corrected reference where possible.

## Rules
Never "fix" a fake citation by inventing a plausible real one. Suggest a genuine, verified source instead, or say none was found.
