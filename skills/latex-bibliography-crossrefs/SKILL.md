---
name: latex-bibliography-crossrefs
description: Use when repairing or creating LaTeX citations, bibliographies, labels, and cross-references.
---

# Citations and cross-references

Identify the main file, document class, existing citation system, bibliography files, and build commands before editing. Respect the project's chosen BibTeX, biblatex/biber, or publisher workflow; avoid mixing citation packages without a demonstrated need. Keep citation keys and labels stable unless callers are updated together.

Trace each missing citation or reference from its use to the source entry or label. Check spelling, duplicate keys, file paths and the build sequence before changing content. Preserve authors, titles, publication details and existing citations. Verify added bibliographic details against an appropriate primary record; never fabricate a source or infer unconfirmed metadata. Mark records that remain uncertain for the author.

Place a label where the relevant counter is set, such as after a figure caption, and use distinct descriptive keys. Check repeated labels and ensure a reference still points to the intended object after moving content. Follow the requested citation style and publisher requirements without silently altering substantive claims or adding unsupported citations.

Run the project's complete engine and bibliography passes until references settle, using its existing build tool where available. Inspect logs for missing entries, duplicate labels, undefined citations, and warnings; distinguish an engine failure from a citation issue. Render and review affected pages and the bibliography for links, ordering, line breaks and placement. Report unresolved metadata or unavailable build/visual checks explicitly.
