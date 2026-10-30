---
name: teaching-materials
description: Design lessons, lecture notes, problem sets, examinations, and worked solutions with aligned learning goals, defensible difficulty, and checked mathematical or scientific content.
---

# Teaching materials

Use this method to prepare academic lessons, notes, worksheets, problem sets, assessments, or worked solutions. Begin with the [research contract](../../docs/RESEARCH-CONTRACT.md). Educational clarity must preserve the distinction between a simplifying teaching model and the full scientific claim.

## Define the learning task

Identify audience, prerequisites, learning goals, available teaching time, delivery format, accessibility needs, and assessment conditions. Ask what learners should be able to explain, calculate, interpret, or critique afterward. Convert broad goals into observable tasks rather than treating topic coverage as evidence of learning.

Inspect supplied curriculum or examination requirements. Distinguish instructor materials from student-facing materials, particularly answer keys and assessment rubrics. Preserve source attribution and permissions for reused questions, diagrams, or extracts. Create new examples when useful, labeling invented datasets as synthetic.

## Build the instructional sequence

Choose a small progression from familiar ideas to the target skill. Introduce necessary concepts and notation before combining them. Include a motivating question with a specific payoff, a worked example that exposes the reasoning, an opportunity for guided practice, and a task that requires transfer to a new case. Adjust this sequence to the available time and learner background.

For scientific explanations, state what the model assumes and where the simplification breaks down. Use analogies to illuminate a defined relationship, then explain the analogy's limits. Avoid replacing a difficult concept with a memorable but false statement. For mathematics, show enough intermediate steps for the intended audience and explain why each method is applicable.

For computational teaching, provide a reproducible minimal example, expected behavior, and common failure modes. Make software and data requirements explicit. A code listing is not a demonstrated result unless it was executed and checked. For qualitative or interpretive teaching, design tasks around evidence, context, alternative readings, and justified arguments rather than a falsely unique numerical answer.

## Design assessment and feedback

Align every question with a learning goal. Vary the cognitive task intentionally: recall, application, interpretation, synthesis, or critique. Do not make a task difficult merely through cumbersome arithmetic or ambiguous wording unless those features are themselves being assessed.

Solve each quantitative question independently before presenting it. Check that all required information is available, the problem has the intended number of solutions, units are consistent, and the requested precision is meaningful. If a parameter choice creates a singularity or an unintended trivial case, either revise it or make that case part of the lesson.

Prepare a marking guide that gives credit for substantive reasoning and identifies acceptable alternatives. For open responses, state evidence and reasoning criteria instead of pretending that one wording is compulsory. Separate conceptual errors from minor algebraic or transcription mistakes when that distinction matters educationally.

Estimate completion time by actually working through representative tasks and considering the learner's unfamiliarity. An instructor's fluent solution time is not a reliable student timing estimate. For high-stakes assessments, identify any institutional review or accommodations requirements that still need confirmation.

## Produce the material

Organize student materials with clear instructions, readable spacing, consistent numbering, and enough working area. Keep solutions separate when requested. Use [mathematics notation](../mathematics-notation/SKILL.md), [figures and tables](../tex-figures-tables/SKILL.md), or [presentations and posters](../presentations-posters/SKILL.md) for the chosen format.

A worked solution should state the approach, show the essential steps, give the result with units and conditions, and include a quick interpretation or plausibility check. Do not reveal assessment solutions in a student-facing export accidentally.

## LaTeX assessment production

When a LaTeX exam is requested, inspect the institution's template before selecting a class. If compatible and installed, the [exam class](https://ctan.org/pkg/exam) supports questions, parts, point values and grading tables. Its solution-printing switch can produce student and instructor versions from the same source. The following self-contained synthetic exercise illustrates the workflow; it is not an institutional template:

~~~tex
\documentclass[addpoints]{exam}
\noprintanswers % For the instructor copy, change this to \printanswers.
\begin{document}
\begin{center}Practice assessment\end{center}
\begin{questions}
  \question[2] A sample travels 12 metres in 3 seconds at constant speed.
  Calculate the speed and state its unit.
  \begin{solution}
    Speed is distance divided by time: $12/3=4$ metres per second.
  \end{solution}
\end{questions}
\end{document}
~~~

Compile the student and instructor variants to clearly distinct filenames or directories, with the same question source and an explicit record of the switch used. Run the necessary repeat passes for a grading table or references and check the log. Compare question numbering, point values, totals and intended answers across the versions; check that space reserved for working is adequate. Inspect every fresh student page and searchable text for solutions and answer cues, and inspect the instructor pages for complete, correct solutions. If student-facing source files are distributed, removing solutions from the PDF alone is insufficient: prepare a separate source without the key or deliver only the authorized student artifact. Treat the key and source containing it as instructor material.

The example depends on an installed compatible class and compiler. A template may require a different class or accessibility format; check those requirements and do not present an unbuilt or uninspected file as a verified exam. A rendered solution shows only what was typeset, not that an independent subject-matter or accessibility review occurred.

## Books and course notes

For a long-form book or set of course notes, identify the intended course sequence, prerequisites, target length, existing template, and which front matter, appendices, references, glossary, index, exercises, and solution volumes are actually requested. Organize chapters and shared notation so learners can follow the progression and find definitions again. Preserve established numbering and stable cross-chapter labels when revising existing material; avoid an unsolicited reorganization of the author's project.

Use a maintainable source structure with portable asset paths and a documented main document. Define a consistent approach to references and distinguish general references from chapter-specific lists when needed. If a glossary or index is requested, determine the actual tools and configuration, mark entries deliberately, and include their generation in the build instructions. Check the generated lists for missing or duplicate entries, incorrect page references, ordering, and links after the final build. Do not promise a complete index based only on automatically collected terms; review its usefulness for readers.

When exercises and solutions are separate, trace identifiers and versions across the two deliverables, verify every answer against its question, and inspect the student export for solution leakage. Review chapter starts, navigation, cross-references, front and back matter, and representative dense pages in the fresh output; inspect every page when delivering a final paginated document. Use [document production](../document-production/SKILL.md) for accessible delivery and packaging, and report unavailable build or inspection steps.

## Deliver and verify

Deliver editable materials, requested rendered files, solutions or rubric in the appropriate separate artifact, and a short note about prerequisites and expected duration. Verify scientific claims, calculations, citations, question numbering, answer alignment, and actual file contents. Inspect freshly rendered pages for clipped equations, insufficient working space, and answer-key leakage. Mark unexecuted code, unverified source claims, or untested timing estimates honestly. Completion requires materials that learners and instructors can actually use under the stated conditions.

