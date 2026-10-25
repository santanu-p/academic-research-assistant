---
name: source-verification
description: Verify a scholarly source's identity, version, provenance, publication status, and support for a specific claim without confusing metadata checks with quality appraisal.
---

# Source verification

Use this Academic Research Assistant skill when references, quotations, publication details, or claim support need checking. Apply the [research contract](../../docs/RESEARCH-CONTRACT.md). Verification establishes what a source is and what it supports. Its existence, a valid identifier, or publication in a journal does not establish the quality of its methods.

## Inputs and verification questions

Collect the supplied citation, identifier, link, file, quoted text, and the claim being attributed to it. Determine whether the task concerns bibliographic identity, document authenticity, version status, quotation accuracy, or substantive support. Preserve the original supplied reference so corrections remain auditable.

Use available official or authoritative records: the publisher's article record, a repository's version history, an institutional archive, an identifier registry, or the document itself. Search results and secondary summaries can locate a source but are weaker confirmation of its exact contents. If access is limited, state what was checked and what remains unverified.

## Verification procedure

1. Resolve the candidate identity. Match title, authors, year, venue, identifier, and publication type. Investigate inconsistent combinations rather than selecting the first similar title. A working DOI that resolves to a different article does not validate the supplied citation.
2. Establish the document version. Distinguish a preprint, accepted manuscript, version of record, conference abstract, proceedings paper, correction, supplement, and later revision. Record the version actually read and connect related versions where useful.
3. Check status information on authoritative records when the task requires current status. Look for corrections, expressions of concern, withdrawal, retraction, and updated files. A missing warning in one database is not affirmative proof that no notice exists. Describe search coverage without alleging misconduct from an unexplained discrepancy.
4. Locate the relevant passage, table, figure, theorem, appendix, dataset, or code record. Record page or section plus a stable locator where possible. Inspect surrounding qualifications, definitions, sample restrictions, and whether a statement is the authors' result or a citation to someone else's work.
5. Compare the proposed claim with the source. Distinguish direct support, partial support, a reasonable but explicit inference, contradiction, and no located support. Separate the existence of an observed association from causal interpretation and a proposed mechanism from a tested mechanism.
6. Verify quotations against the consulted version, retaining punctuation and meaningful omissions. Do not silently improve a quotation. For translation, provide the original locator and label the translated wording; do not present it as an original-language direct quote.
7. Follow important secondary attributions to their original source when accessible. If the primary work cannot be consulted, attribute the secondary account honestly instead of implying direct inspection.

## Research-mode boundaries

For quantitative claims, check the outcome definition, denominator, population, estimate, uncertainty, and analysis type. An adjusted and an unadjusted estimate are different claims. For qualitative claims, preserve who said or interpreted something, the context, and whether the statement represents a participant, an analytic theme, or a generalization by the authors.

For theoretical claims, check assumptions and quantifiers: a result under special conditions does not establish a universal theorem. For computational claims, verify version, dataset split, benchmark setting, metric direction, hardware or resource qualifications, and whether the comparison uses equivalent conditions. Supplementary material may carry essential restrictions absent from the abstract.

## Deliverable and next step

Return a verification table with supplied reference, resolved identity, consulted version, evidence location, status checked and date, claim-support verdict, corrections, and unresolved access limits. Use “not verified” when evidence is missing; reserve “incorrect” for an established mismatch. Never manufacture a replacement reference to fill a gap.

Route technical bibliography repair to [citations and bibliographies](../citations-and-bibliographies/SKILL.md), interpretation to [paper reading](../paper-reading/SKILL.md), and validity questions to [research appraisal](../research-appraisal/SKILL.md). Before final delivery, ensure every confident correction can be traced to the record or document actually consulted.
