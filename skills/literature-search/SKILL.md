---
name: literature-search
description: Build and execute a documented scholarly search using concept blocks, suitable discovery sources, citation chaining, and transparent coverage limits.
---

# Literature search

Use this Academic Research Assistant skill to discover relevant research and leave a search that another researcher can understand and update. Follow the [research contract](../../docs/RESEARCH-CONTRACT.md). A rapid orientation search and a systematic review search have different coverage requirements; identify the requested mode before claiming completeness.

## Inputs and search scope

Obtain the question, discipline, date range, language needs, publication types, intended use, and access constraints. Determine whether the user needs a few useful entry points, a defensible narrative-review corpus, or a reproducible review search. For formal evidence synthesis, coordinate eligibility rules and reporting with [systematic review](../systematic-review/SKILL.md).

Use the actual tools available in the session. Search scholarly indexes, specialist databases, repositories, catalogs, or official archives suited to the subject; no single service covers all disciplines. If a requested source is unavailable, disclose that limit and preserve a query for later execution. Never report a planned query as executed or fabricate hit counts.

## Build and run the search

1. Split the question into essential concepts. List synonyms, spelling variants, older terminology, acronyms, and relevant controlled-vocabulary terms. Add a term only when it improves retrieval; requiring every concept can accidentally exclude studies with sparse abstracts.
2. Build an initial Boolean structure with alternatives joined within concepts and essential concepts joined across them. Adapt phrase syntax, field tags, truncation, proximity operators, and controlled terms to each actual search interface. Do not assume a query is portable unchanged.
3. Test against a small set of known relevant works supplied by the user or verified during orientation. Investigate missed items: terminology, indexing, query structure, publication date, and database coverage. These works test sensitivity but do not prove completeness.
4. Execute the search and record the exact query, source, interface, date, filters, result count when available, and export format. Retain source-specific identifiers and provenance when merging exports.
5. Screen titles and abstracts according to the agreed relevance criteria. Separate exclusions, uncertain records, and inaccessible full texts. A missing full text is an access problem, not evidence that a study fails eligibility.
6. Use backward references and forward citations around influential, recent, or methodologically relevant works. Record the seed and direction of chaining. Add author, project, dataset, or terminology searches when they resolve a specific coverage gap.
7. Stop in proportion to purpose. An orientation search may stop when the main approaches and useful entry points are covered. A systematic search stops according to its protocol and update date, not a subjective feeling that enough papers have appeared.

## Evidence and discipline boundaries

Search for relevant contrary and null findings as well as supportive findings. Do not rank evidence quality by search position, citation count, journal prestige, or recency alone. Recent preprints may reveal active work but need clear version and review-status labels. Older work may be foundational or use terminology absent from newer queries.

For quantitative questions, consider designs and outcomes without excluding studies merely because their abstracts omit effect estimates. For qualitative questions, include context and phenomenon language; overly narrow intervention vocabulary can erase relevant traditions. For theoretical and computational questions, search assumptions, mathematical structures, algorithm names, benchmark problems, and failure regimes. Conference proceedings, technical reports, software papers, or monographs may be central in some fields.

## Deliverable and verification

Return a search log and a deduplicated candidate list with title, authors, year, identifier or stable link, source, retrieval date, relevance note, and verification status. Use the [search-log schema](references/search-log.md) when a reusable audit trail is needed. Include the actual coverage limits and unanswered search questions. For a small reading list, explain the role of each selection instead of presenting an unexplained ranking.

Check identity and metadata through [source verification](../source-verification/SKILL.md) before treating records as reliable references. Keep duplicate reports of the same study linked; deleting duplicate records does not establish independent studies. Route full-text interpretation to [paper reading](../paper-reading/SKILL.md). Label the search date prominently: absence from the retrieved set is not proof that a topic has never been studied.
