---
name: document-production
description: Produce editable academic documents and checked deliverables through explicit source, build, rendering, inspection, and packaging steps.
---

# Document production

Use this method to turn approved content or a clear document brief into an editable artifact and its requested delivery formats. Start with the [research contract](../../docs/RESEARCH-CONTRACT.md). Content validity, build success, visual quality, and delivery completeness are distinct checks; perform the ones required by the task and report their actual outcomes.

## Define the artifact

Identify document type, audience, length, target format, source format, required template, accessibility needs, and delivery location. Inspect supplied material and applicable institutional or venue instructions. Preserve figures, references, permissions, source credits, and contribution details. Do not invent an official template or claim compliance with instructions that have not been checked.

Choose an authoring route that leaves the user an editable source. For mathematical documents, LaTeX is often appropriate; for collaborative prose, an editable word-processing format may fit better. Preserve existing working structures when practical. For a new project, use a dedicated folder with main source, references, figures, and a short build note. Avoid copying unrelated generated files into a delivery package.

## Build a coherent source

Organize the document around its reader's task. Establish heading levels, notation, references, figure conventions, and reusable styles before filling long sections. Prefer a small understandable preamble over an accumulation of packages. A minimal original TeX starting point is:

~~~tex
\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage[margin=28mm]{geometry}
\title{A research note}
\author{Author supplied name}
\date{}
\begin{document}
\maketitle
\section{Question}
State the question and the evidence available.
\section{Result}
Present the result with its assumptions.
\end{document}
~~~

This is a starting structure, not a venue template or a promised installed package set. Replace provisional metadata with supplied facts. Add bibliography and cross-reference support only as needed and compatible with the chosen engine. Keep document content separate from styling choices when that makes revision safer.

Use [mathematics notation](../mathematics-notation/SKILL.md), [figures and tables](../tex-figures-tables/SKILL.md), and [TeX layout](../tex-layout/SKILL.md) for detailed work. Preserve editable figure sources when available. For image-only inputs, distinguish faithful transcription from interpretation and flag uncertain text or symbols.

## Produce and inspect the deliverable

Determine which build tools are actually available before promising a PDF. Compile through an appropriate available runtime, capture diagnostics, and resolve consequential errors using [build repair](../tex-build-repair/SKILL.md). Do not equate opening an editor with compilation or a saved PDF with a successful current build.

Render the fresh output and inspect every page when final visual delivery is requested. Check first-page metadata, headings, line breaks, equations, captions, tables, figure legibility, references, blank pages, and page boundaries. Inspect at reading size and zoom into dense material. For a long document, use a contact sheet to locate problems, then inspect the pages individually; a contact sheet alone does not establish small-text readability.

Confirm that graphics retain labels and that tables do not clip. Check bookmarks, links, searchable text, or accessibility features when the delivery specification requires them and available tools can inspect them. If a check cannot be performed, preserve the artifact and report the unverified property.

## Accessible delivery

When accessible delivery is requested, establish the intended readers, format, and any applicable requirements. Preserve semantic headings, lists, document language, meaningful link text, and logical reading order in the editable source. Provide useful text alternatives for informative figures and identify decorative material appropriately; keep captions and alternatives consistent with the evidence. Use table headers and a coherent cell order, and provide mathematical content in an accessible form supported by the chosen destination. Do not assume that a visually faithful image of an equation is accessible mathematics.

Check the destination's actual support and the capabilities of the chosen authoring and export tools before promising a tagged PDF or a specific accessibility standard. Inspect tags and reading order, heading hierarchy, language, alternatives, links, tables, and mathematics with available tools and, where practical, assistive technology. Check that exported text corresponds to the visual content, including symbols and order. Searchable or selectable text, a successful build, and an automated check alone do not establish accessibility. Report the checks performed, failures or unsupported features, and any required manual or assistive-technology review; offer an accessible editable source or alternative format when the requested export cannot be verified.

## Package and verify

Deliver the requested final format, editable source, necessary figures and bibliography, and concise build or usage instructions. Use relative asset paths within the package. Avoid embedding personal absolute paths, temporary credentials, or unrelated source collections.

Verify the package opens or builds from its intended structure when feasible. Compare content against the brief, especially numerical results, citations, author names, and final-wording changes. Report the actual build and inspection status, remaining warnings, and any unavailable checks. A draft, a successful compile, and a visually inspected final artifact should be named accurately so the user can judge what remains.

