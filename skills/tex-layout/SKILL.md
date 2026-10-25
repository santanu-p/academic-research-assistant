---
name: tex-layout
description: Improve LaTeX page structure, typography, spacing, and navigation through measured layout decisions and inspection of freshly built pages.
---

# TeX layout

Use this method for page design, typography, spacing, navigation, and layout repairs in LaTeX documents. Apply the [research contract](../../docs/RESEARCH-CONTRACT.md). Layout should make the argument readable while respecting content and required formatting; it must not hide missing evidence or silently change scientific meaning.

## Identify constraints before styling

Determine document class, engine, target page size, required template, page limit, audience, and expected reading medium. Read the existing preamble and relevant sources before adding packages. Separate mandatory specifications from preferences. For a supplied journal or institutional class, use its supported interfaces before overriding dimensions or redefining internals.

Inspect a current build when available. Record concrete defects such as a clipped equation, cramped table, orphaned heading, unreadably small caption, or excessive blank area. Avoid a broad restyling pass when a local repair satisfies the task. Preserve semantic sectioning and logical source order rather than using visual commands to simulate structure.

## Establish the page system

Choose a legible text size and measure for the intended page and reader. Balance margins, line length, leading, and heading spacing together. There is no universal margin or line-length setting appropriate to every document. Use the venue's constraints, then inspect representative pages containing normal prose, mathematics, figures, tables, and references.

Keep heading hierarchy consistent and meaningful. Use proper section commands so navigation, numbering, and cross-references remain coherent. Configure headers, footers, and page numbering according to the document type; check transitions between front matter and main content. Avoid placing essential information only in a running header.

For new unconstrained notes, an understandable geometry choice may be:

~~~tex
\usepackage[a4paper,margin=27mm]{geometry}
~~~

Treat this as an editable choice, not a universal recommendation. Verify that it does not conflict with class settings or mandatory templates. Select fonts available in the actual build environment and compatible with the engine. Do not assume that a font visible on the author's machine will be available elsewhere.

## Repair actual layout problems

For long equations, reconsider mathematical grouping and use appropriate multiline environments. Preserve equality and implication meanings when breaking lines. For dense tables, improve headings, units, significant figures, or structure before shrinking text. For figures, size by label legibility and intended prominence; inspect the embedded version rather than judging only the standalone source.

Let floats participate in page composition. Use placement hints with an understanding of surrounding text and the class's rules. Excessive forced placement can create blank areas or detached captions. When a figure must occur near a discussion, revise source order or surrounding structure carefully and verify subsequent pages.

Resolve overfull boxes by locating the actual content: long identifiers, unbreakable URLs, wide mathematics, or table columns often need different remedies. Use local changes where possible. Do not globally loosen spacing or suppress diagnostics solely to make the log look clean. Underfull warnings may be harmless or visible defects; inspect before deciding.

For a hard page limit, remove repetition through [academic editing](../academic-editing/SKILL.md), consolidate presentation where meaning survives, and adjust permissible layout choices proportionately. Do not reach the limit by making body text, references, or figure labels impractical to read.

## Deliver and verify

Return the modified source and fresh output when compilation is available. Explain material layout choices and any mandatory constraints that prevent a preferred arrangement. Use [build repair](../tex-build-repair/SKILL.md) for compiler issues and [document production](../document-production/SKILL.md) for delivery packaging.

Inspect every changed page plus adjacent pages after reflow. Check the first page, section transitions, dense mathematical pages, figure and table placement, final page, bibliography, and navigation. Confirm page count from the actual fresh PDF. Preserve content, citations, and equation numbering across the layout pass. Report any remaining warnings with their visual consequence or explain that they still need inspection.

