---
name: compag-elsevier-paper-editing
description: Use when drafting, revising, shortening, polishing, or auditing technical manuscript text for an Elsevier Computers and Electronics in Agriculture style. Prioritize precision, concision, evidence-bounded claims, terminology consistency, and high information density while preserving frozen technical content. Avoid colons and italic emphasis in manuscript prose and use hyphens only where technically or grammatically standard.
---

Use this skill for paper text, captions, method descriptions, result interpretation, abstracts, introductions, discussions, conclusions, and reviewer-response prose when the requested style is Elsevier or COMPAG-like.

Preservation rules

- Do not change frozen numerical values, definitions, equations, metrics, experimental protocols, task groupings, baselines, symbols, or evaluation scope.
- Preserve technical meaning unless the user explicitly requests a conceptual change.
- Do not silently strengthen claims.
- If a statement exceeds the available evidence, weaken it to the strongest defensible form or identify the gap.

Writing rules

- Prefer precise, compact, evidence-driven sentences.
- Use natural forward logic.
- Minimize rhetorical contrast constructions such as "not ... but", "rather than", and unnecessary "whereas" clauses.
- Remove redundancy and repeated explanations.
- Keep one technical purpose per sentence when possible, while maintaining paragraph flow.
- Use terminology, symbols, metric names, capitalization, and tense consistently.
- Prefer mechanism-level explanations over generic claims such as "improves robustness" or "enhances performance".
- State comparisons only when the underlying data directly support them.
- Keep causal interpretations narrower than the experimental manipulation.
- Do not use colon punctuation in manuscript prose or headings unless the user explicitly permits it or the syntax is technically mandatory.
- Do not use italic emphasis.
- Avoid em dashes and decorative hyphenation.
- Use hyphens only in standard compounds, established technical terms, variable names, ranges, or syntax where omission would be incorrect or ambiguous.
- Do not introduce defensive wording, inflated novelty claims, or broad generalizations.

Paragraph logic

Build paragraphs around a necessary question.

- Establish the concrete technical need.
- Introduce the definition, model, equation, or design that is needed to address it.
- Explain what the design changes in the system and why that change is relevant.
- State only the consequence supported by theory, implementation, diagnostics, or experiments.
- End by identifying the next unresolved technical question when a transition is needed.

Do not force every paragraph into a single causal chain. When multiple technical problems are parallel, state the common objective and develop the branches separately.

Method sections

When technically valid, use design-reason-driven progression. Connect each mechanism to the concrete issue that motivates it, explain the operational change made by the mechanism, and avoid manual-like sequences of disconnected definitions.

Results and discussion

- Report the measured result first.
- Interpret only the factor isolated by the experiment.
- Keep ablation, comparison, and diagnostic evidence conceptually separate.
- Do not infer causality from correlated metric changes alone.
- Use exact scopes such as evaluated cases, matched cases, tested operating conditions, or the stated dataset when generalization is not demonstrated.

Final editing pass

1. Verify all numbers and frozen definitions against the source text or supplied data.
2. Check every comparative and causal claim against direct evidence.
3. Unify terminology, symbols, metrics, and tense.
4. Remove redundant sentences and repeated rationale.
5. Remove prohibited colon punctuation and italic emphasis.
6. Normalize hyphen usage.
7. Reduce contrast-heavy constructions.
8. Check that each equation, figure reference, and experiment has a clear argumentative function.

Read `references/style-audit.md` when a stricter manuscript-level audit is required.
