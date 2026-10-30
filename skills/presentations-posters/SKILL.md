---
name: presentations-posters
description: Create research talks, slide decks, Beamer sources, and academic posters with audience-appropriate claims, readable visuals, and rehearsal-based timing.
---

# Presentations and posters

Use this method for scientific talks, interview presentations, lectures, conference slides, and research posters. Begin with the [research contract](../../docs/RESEARCH-CONTRACT.md). A short format needs disciplined selection, not stronger claims than the research supports.

## Define audience and constraints

Collect purpose, audience knowledge, venue, time limit, question period, slide or poster dimensions, required branding, available figures, and requested editable format. For a talk, check aspect ratio, projection or screen conditions, and whether the limit includes demonstrations and questions. For a poster, check physical dimensions and orientation, printer requirements, and any digital submission limits. Use supplied requirements rather than inventing venue specifications; identify assumptions that matter when they are unavailable. Distinguish public explanation from specialist reporting and a research presentation from a proposal. Identify the single conclusion or decision the audience should retain.

Map each planned message to supplied evidence. Preserve the difference between completed work, preliminary results, collaborative contributions, and proposed next steps. Do not invent performance numbers, impact, novelty, or personal ownership to strengthen a presentation. Put essential assumptions and uncertainty where the audience can see or hear them.

## Build the talk narrative

Choose a sequence that establishes the problem, makes the question understandable, explains the approach at the necessary depth, presents the strongest relevant evidence, and ends with its bounded implication. The appropriate sequence may vary by interview, classroom, conference, or public audience; do not force every talk into the same storyline.

Give each slide a clear communicative purpose. Prefer a title that states the slide's message when that message is supported. Use figures, equations, and examples because they help the audience reason. Simplify a figure by removing irrelevant series or detail while preserving axes, units, comparison conditions, and uncertainty needed to interpret it. Identify the source of adapted figures and verify that labels, trends, and numerical values still match the original. Do not imply that a schematic is measured data.

For public audiences, introduce technical terms through concrete meaning before using shorthand. Explain what a model or analogy reveals and where it stops applying. For specialists, expose the critical assumptions, comparison, and validation evidence rather than filling slides with every derivation step. Place deeper derivations and likely questions in a clearly separated backup or Q&A artifact.

Adapt theme, aspect ratio, and reveals to actual requirements. Use animation only when sequencing helps explanation and verify the exported or static state is understandable. Keep critical information accessible in the order it is presented; do not rely on color alone to distinguish comparisons.

## Work in the requested format

Use the requested host format and available authoring tools. Preserve an existing deck or poster's editable objects and notes when editing it. For a new editable deck, keep text, shapes, tables, and charts editable where practical; identify figures, equations, or other elements that remain flattened or depend on external links. A PDF export alone is not an editable slide deck. If the requested format cannot be created or verified in the available environment, explain the limitation and provide the best usable source or intermediate artifact without claiming format fidelity.

For a simple new PowerPoint deck, the optional `../../tools/presentation_builder.py` accepts a UTF-8 JSON object with a `slides` array. Each slide has a `title` string and a `bullets` array of strings. A slide can optionally include `"image":{"path":"figure.png","caption":"Caption supplied by the user"}` to embed a local PNG or JPEG; relative paths resolve from the JSON file's directory. Images are limited to 20 MB and 50 megapixels and are scaled to fit while retaining their aspect ratio. The picture is an editable slide object, but its internal pixels are not an editable chart. Keep source, attribution, and accessibility information with the project, and add alt text in the target application.

Run `python tools/presentation_builder.py input.json output.pptx` from the plugin root; it requires `python-pptx`, a writable destination directory that supports hard links, and refuses to overwrite an existing output. The helper produces editable text boxes and shapes in a fixed widescreen layout. It does not generate content, notes, figures, charts, citations, animations, institutional themes, alt text, or a rendered preview; it does not measure text overflow. Input length limits do not guarantee fit. Inspect every slide in a PowerPoint-compatible application and adapt the layout before delivery.

For a requested Beamer source, a minimal editable starting point is:

```tex
\documentclass[aspectratio=169]{beamer}
\title{A question the audience can follow}
\author{Author supplied name}
\begin{document}
\frame{\titlepage}
\begin{frame}{What the evidence shows}
State one supported result and display its evidence.
\end{frame}
\end{document}
```

Keep supplied source data and figure provenance traceable; do not alter the only copy of an original. Check that linked media, fonts, and any required assets will be available to the recipient. Preserve speaker notes when requested, and indicate whether animations, embedded media, and editable charts survive the chosen export or conversion. Check permissions for reused assets and attribution where relevant.

## Handle timing and posters

Allocate the talk's limited time across essential messages and transitions. Prepare a speakable script or speaker notes in the requested style. Word count and slide count provide rough planning information; they do not establish compliance with a hard time limit. Time an actual rehearsal, including slide changes and demonstrations where relevant. Shorten lower-priority content and rehearse again. Report a target or estimate honestly when no rehearsal occurred.

For posters, design a reading path from question to approach, evidence, and conclusion. Choose dimensions and text size for viewing distance and actual print size. Provide enough methods and provenance for scientific interpretation without turning the poster into a dense manuscript. Ensure charts remain legible when placed in columns. Check image resolution at its placed print size, margins and any supplied bleed or color requirements, and the exported page dimensions. A digital thumbnail is not proof of print readability.

## Deliver and verify

Deliver the requested editable slides or poster source and exports, plus speaker notes, script, or Q&A material when requested or useful for the agreed task. Use [figures and tables](../tex-figures-tables/SKILL.md) for evidence displays and [document production](../document-production/SKILL.md) for rendering and packaging when relevant.

Inspect every slide or poster region at the intended reading size and review the actual exported artifact. Check text overflow, contrast, figure labels, equations, alignment, citations, animation states, and export order. Check the editable file in its intended host when available, including object editability and missing or substituted assets; flag anything that could not be checked. For a poster, inspect at physical print scale as well as the whole-page layout. Verify timing from the actual rehearsal record when performed. Confirm that the spoken conclusion, final slide, abstract, and source evidence agree where those artifacts exist. State which build, visual, host-compatibility, print, and timing checks were executed and which remain. Do not call a presentation final solely because all slides compiled.

