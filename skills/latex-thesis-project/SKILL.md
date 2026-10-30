---
name: latex-thesis-project
description: Use when creating or editing a multi-chapter thesis or dissertation in LaTeX.
---

# Thesis projects

Identify the institution's applicable template and requirements, the main file, included chapters, bibliography, appendices and build commands. Work within the existing project organization and preserve author content, labels, citations and source assets. Treat institutional requirements as version-specific; verify current rules when a final submission is requested.

Separate substantive editing from formatting. Preserve the status and attribution of research, data and sources, including previously published material. Use consistent chapter structure and reusable macros while retaining existing references. Place front matter, lists, appendices and bibliography according to the actual template; do not invent committee names, approvals, declarations or results.

Check cross-file paths and label uniqueness when moving chapters. Ensure the chosen engine and bibliography system support the project's languages, fonts and citations. If generating a new structure, include editable chapter and bibliography sources and clearly mark information that only the author can supply. Do not overwrite an established template or reorganize unrelated files without authorization.

## Page design and navigation

Determine paper size, single- or double-sided output, required inside and outside margins, and whether a binding allowance is specified. Check whether the class or institutional template already sets these values before adding a layout package. When `geometry` is appropriate, its `bindingoffset` adds an allowance at the binding edge; use the institution's actual dimension and check the resulting text area and both odd and even pages. A printed proof or accurate page measurement may still be needed to establish physical compliance. Do not assume a PDF's apparent margins prove suitability after printing and binding.

Establish the required pagination sequence and which pages display numbers. Some classes provide front-matter and main-matter commands; use the class's own mechanism when available. For a class without those commands, a deliberate page-numbering transition can use `\pagenumbering{roman}` followed by `\pagenumbering{arabic}` at the required boundary. These commands reset the page counter, so coordinate them with page breaks, title pages, the table of contents, and PDF anchors. Check numbering and links in the rendered document, including blank pages introduced by two-sided chapter starts; do not reset counters repeatedly to hide layout problems.

Set line spacing using the supported class or template controls. If compatible with the project, `setspace` offers document-wide and local spacing controls, but the actual rule may differ for quotations, captions, notes, and references. Inspect those elements as well as body text. Avoid layering multiple spacing mechanisms without understanding their interaction; verify the result against the institution's specification rather than a guessed default.

## Glossaries and incremental work

If abbreviations or a glossary are required, first identify the project's existing package, entry definitions, sorting backend, and build automation. For the indexed `glossaries` workflow, the preamble initializes glossary generation and a TeX run writes auxiliary data; `makeglossaries` processes the document's auxiliary file before another TeX pass. Other workflows, including no-index and `bib2gls` approaches, have different setup and build steps. Follow the installed package documentation and project configuration, including its output directory and bibliography tool, rather than assuming one command works for every project. Check missing entries, sort order, first-use forms, page references, and links in the fresh PDF. See the [glossaries manual](https://tug.ctan.org/macros/latex/contrib/glossaries/glossaries-user.html).

For a large project built with `\include`, `\includeonly` can restrict a development build to selected included files while retaining auxiliary information from omitted files. It does not select files brought in with `\input`, and stale or missing auxiliary files can make cross-references and counters misleading. Keep selective builds clearly labeled as partial, and remove the restriction for a clean final full build with the required bibliography, glossary, and reference passes. Inspect the resulting complete PDF after the final change.

Run the project's full build from the root and repeat required bibliography and cross-reference passes. Review logs for undefined labels, missing citations and overfull content. For a completed thesis PDF, render and inspect every page, especially title/front matter, chapter starts, landscape pages, tables and appendices. State any missing sources or checks that prevent submission readiness.
