---
name: presentations-posters
description: Create research talks, slide decks, Beamer sources, and academic posters with audience-appropriate claims, readable visuals, and rehearsal-based timing.
---

# Presentations and posters

Use this method for scientific talks, interview presentations, lectures, conference slides, and research posters. Begin with the [research contract](../../docs/RESEARCH-CONTRACT.md). A short format needs disciplined selection, not stronger claims than the research supports.

## Define audience and constraints

Collect purpose, audience knowledge, venue, time limit, question period, slide or poster dimensions, required branding, available figures, and requested editable format. Distinguish public explanation from specialist reporting and a research presentation from a proposal. Identify the single conclusion or decision the audience should retain.

Map each planned message to supplied evidence. Preserve the difference between completed work, preliminary results, collaborative contributions, and proposed next steps. Do not invent performance numbers, impact, novelty, or personal ownership to strengthen a presentation. Put essential assumptions and uncertainty where the audience can see or hear them.

## Build the talk narrative

Choose a sequence that establishes the problem, makes the question understandable, explains the approach at the necessary depth, presents the strongest relevant evidence, and ends with its bounded implication. The appropriate sequence may vary by interview, classroom, conference, or public audience; do not force every talk into the same storyline.

Give each slide a clear communicative purpose. Prefer a title that states the slide's message when that message is supported. Use figures, equations, and examples because they help the audience reason. Simplify a figure by removing irrelevant series or detail while preserving axes, units, comparison conditions, and uncertainty needed to interpret it.

For public audiences, introduce technical terms through concrete meaning before using shorthand. Explain what a model or analogy reveals and where it stops applying. For specialists, expose the critical assumptions, comparison, and validation evidence rather than filling slides with every derivation step. Place deeper derivations and likely questions in a clearly separated backup or Q&A artifact.

For Beamer, begin with a modest source structure:

~~~tex
\documentclass[aspectratio=169]{beamer}
\title{A question the audience can follow}
\author{Author supplied name}
\begin{document}
\frame{\titlepage}
\begin{frame}{What the evidence shows}
State one supported result and display its evidence.
\end{frame}
\end{document}
~~~

Adapt theme, aspect ratio, and overlays to actual requirements. Reveal content only when the sequencing helps explanation; ensure the exported state is understandable.

## Handle timing and posters

Allocate the talk's limited time across essential messages and transitions. Prepare a speakable script or speaker notes in the requested style. Word count and slide count provide rough planning information; they do not establish compliance with a hard time limit. Time an actual rehearsal, including slide changes and demonstrations where relevant. Shorten lower-priority content and rehearse again. Report a target or estimate honestly when no rehearsal occurred.

For posters, design a reading path from question to approach, evidence, and conclusion. Choose dimensions and text size for viewing distance and actual print size. Provide enough methods and provenance for scientific interpretation without turning the poster into a dense manuscript. Ensure charts remain legible when placed in columns. A digital thumbnail is not proof of print readability.

## Deliver and verify

Deliver editable slides or poster source, requested exports, speaker notes or script, and any separate Q&A material. Use [figures and tables](../tex-figures-tables/SKILL.md) for evidence displays and [document production](../document-production/SKILL.md) for rendering and packaging.

Inspect every slide or poster region at the intended reading size. Check text overflow, contrast, figure labels, equations, alignment, citations, animation states, and export order. Verify timing from the actual rehearsal record when performed. Confirm that the spoken conclusion, final slide, abstract, and source evidence agree. State which build, visual, and timing checks were executed and which remain. Do not call a presentation final solely because all slides compiled.

