---
name: citations-and-bibliographies
description: Create and repair source-traceable citations and reference lists, including BibTeX, biblatex, Biber, natbib, and manuscript citation-backend consistency.
---

# Citations and bibliographies

Use this Academic Research Assistant skill for bibliographic records, in-text citations, reference formatting, and the technical bibliography backend. Follow the [research contract](../../docs/RESEARCH-CONTRACT.md). A correctly formatted citation is useful only when it identifies the intended source and supports the associated statement. Use [source verification](../source-verification/SKILL.md) for uncertain identity or claim support.

## Inputs and choices

Obtain the manuscript or source list, required style or venue instructions, preferred reference manager or file format, existing citation keys, and compilation workflow when relevant. Distinguish changing presentation from correcting metadata or replacing sources. Preserve stable keys when possible; arbitrary renaming can break manuscripts, supplements, and external cross-references.

If a style is specified, verify the applicable edition or current venue instructions rather than inferring them from a remembered example. If no style is fixed, use a consistent discipline-appropriate format and state the choice. Do not impose a particular software brand or online service.

## Bibliographic workflow

1. Inventory in-text citations and records. Identify missing records, uncited records, duplicate keys, duplicate works, inconsistent author names, and unresolved placeholders. An uncited library entry need not be deleted merely because it is not used in this manuscript.
2. Resolve identity using trustworthy metadata and the actual source where available. Check title, author order, year, version, venue, volume, issue, pages or article number, DOI, URL, and publication type. Retain Unicode names and meaningful diacritics using encoding supported by the workflow.
3. Distinguish versions and related works. A preprint and a journal article may be related but are not automatically interchangeable when their contents differ. Keep datasets, software, archival materials, standards, and other research objects as appropriate entry types with version information.
4. Attach citations to the precise supported claim. A paragraph-ending citation should not appear to support several unrelated assertions. Preserve primary versus secondary attribution and avoid implying that an unread original source was inspected directly.
5. Apply style rules consistently for author display, title capitalization, dates, page locators, identifiers, and sorting. Protect proper nouns or scientific symbols only as needed by the target format. Do not mechanically title-case titles when the style calls for sentence case.
6. Reconcile in-text references with the bibliography and report any unresolved identity or access issues. Never invent page numbers, identifiers, publication status, or missing authors to make a record look complete.

## Technical bibliography backend

For LaTeX, inspect the existing preamble, citation commands, bibliography files, style declarations, and build configuration before changing tools. A natbib/BibTeX workflow and a biblatex/Biber workflow have different command and build requirements; do not combine them casually. Preserve a working backend unless the task requires migration.

For BibTeX, check syntactic validity, entry-type support, key uniqueness, escaped special characters, name parsing, and style-specific required fields. For biblatex, use its supported fields and data model rather than assuming every BibTeX convention is equivalent. Keep author separators distinct from the word “and” within an institutional author. Use braces deliberately for corporate authors and capitalization, without freezing every title's case.

When repairing compilation, diagnose the actual log: absent database, unknown key, malformed record, wrong backend, stale intermediate file, or missing style. Run the selected bibliography processor and sufficient TeX passes, or use the project's configured build tool. Coordinate general engine and layout failures with [TeX build repair](../tex-build-repair/SKILL.md). Do not claim a successful bibliography build from static inspection alone.

For word-processing or plain-text outputs, preserve editable citations or reference-manager fields where required. A flat pasted bibliography is not equivalent to a live citation database. Explain any conversion that loses metadata or linkability.

## Deliverable and verification

Return corrected records and reference list, compatible citation changes, a concise correction log, and unresolved references. When a manuscript is built, inspect the rendered citation labels and bibliography as well as compiler warnings. Check author ordering, accents, long identifiers, links, and numeric sequence or alphabetical order as applicable. For theoretical, empirical, qualitative, and computational sources alike, citation format must not imply stronger evidence, authorship, or publication status than the source establishes.
