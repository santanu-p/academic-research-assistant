---
name: paper-reading
description: Read and explain a research paper with a traceable account of its question, methods, results, assumptions, and limitations, including equations and figures when relevant.
---

# Paper reading

Use this Academic Research Assistant skill to understand a specific paper or a small connected set. Follow the [research contract](../../docs/RESEARCH-CONTRACT.md). Match the explanation to the reader's background while preserving the paper's distinctions between observation, argument, interpretation, and speculation.

## Inputs and access

Obtain the paper or stable identifier, the user's learning goal, relevant background, and any passages of interest. Establish the consulted version and available components through [source verification](../source-verification/SKILL.md). If only an abstract is available, give an abstract-based explanation and identify which methodological or numerical details cannot be checked. Do not imply full-text reading from an abstract, metadata record, or another summary.

Choose the reading depth: orientation, section-by-section understanding, replication preparation, or critical appraisal. A user asking for a clear overview does not need every derivation; a replication request does need the missing parameters and procedural details.

## Reading operations

1. Identify the research question, the earlier limitation the authors address, and their claimed contribution. Keep the authors' positioning separate from an independently verified literature gap.
2. Build a map of the paper: inputs or materials, assumptions, procedure or argument, outputs, and claimed interpretation. Read methods and results together so that result labels retain their operational meaning.
3. Extract the central findings with locators. Prefer the actual estimate, comparison, uncertainty, theorem conditions, theme, or numerical error over an adjective such as “significant” or “accurate.” Note where the abstract compresses qualifications that appear later.
4. Explain important figures by naming axes, units, sample or case selection, uncertainty representation, legend, and the comparison that supports the inference. Do not infer exact values from an image when the resolution or scale makes them unreliable.
5. For equations, introduce symbols, assumptions, units or dimensions, and the role of each term. Distinguish an exact identity, an approximation, a model assumption, a fitted relation, and a numerical prescription. If an intermediate step is reconstructed, label it as the assistant's derivation and check it independently.
6. Trace the argument from evidence to conclusion. Identify where the authors rely on previous literature, where they provide new evidence, and where they propose an explanation. Explain an alternative interpretation when it materially changes what the result establishes.
7. Record unresolved questions. Missing details, inaccessible supplements, and ambiguous conventions should appear as open issues rather than being filled from a typical method in the field.

## Adapt the explanation

For quantitative studies, clarify design, selection, measurement, estimand, analysis population, missingness, and uncertainty. Explain the difference between statistical evidence and practical importance. A non-significant result is not automatically evidence of equivalence or absence.

For qualitative studies, explain research context, participant or material selection, data generation, analytic approach, reflexive position, and the relationship between excerpts and interpretation. Avoid converting themes into prevalence estimates unless the study supports that use.

For theoretical papers, map definitions, assumptions, lemmas, and the conclusion, checking precisely where conditions enter. For computational papers, distinguish algorithmic description, implementation, verification, benchmark performance, and interpretation of a modeled system. Record tolerances, convergence evidence, and the domain actually tested when available.

## Deliverable and verification

Return a structured reading note: one-paragraph overview, question, approach, main results with source locations, key concepts or equations, limitations, and questions for further reading or replication. Add a glossary or worked explanation only where it helps the user's goal. Clearly mark your interpretations and reconstructed calculations.

Recheck all quoted text, numerical values, signs, units, and figure references against the paper. Preserve caveats that alter the claim. A reading note can identify likely weaknesses, but a formal quality judgment belongs in [research appraisal](../research-appraisal/SKILL.md); structured cross-paper data belongs in [evidence extraction](../evidence-extraction/SKILL.md). Do not conclude that the paper is correct or novel merely because its argument has been explained coherently.
