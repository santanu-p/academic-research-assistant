---
name: guardrails-compag-elsevier-paper-editing
description: "Edit or audit scientific manuscript prose when Elsevier/COMPAG style is requested: concise evidence-driven logic, consistent terminology and tense, and the specified punctuation/emphasis rules. Preserve all frozen technical content and evaluation scope."
---
## Selection and handoffs

Edit or audit scientific manuscript prose in the requested Elsevier/COMPAG style while freezing technical content.

**Select for:** Draft/revise/shorten/polish/audit manuscript text with Elsevier/COMPAG style requested; Apply COMPAG style to captions, methods, results, abstracts, conclusions or review responses

**Expected work:** Freeze technical definitions/data/protocol/scope; Develop paragraphs from concrete need through mechanism and supported consequence, parallel where appropriate; Report measured results before interpreting isolated factors; Audit claim evidence, causal scope, terminology/notation/tense and redundancy; Remove unpermitted prose/header colons and italic emphasis; normalize hyphens; Run optional stricter style-audit reference

**Expected output:** Edited concise manuscript/caption/response prose; Source-preserving style and evidence audit with unsupported claims/gaps flagged

**Scope boundaries:** Every academic task without requested COMPAG/Elsevier style; Research design or mechanism invention; General casual prose; Replacing a journal compliance check with stylistic preferences

**Related skills:** [guardrails-research-problem-mechanism-evidence](../guardrails-research-problem-mechanism-evidence/SKILL.md), [academic-humanizer](../academic-humanizer/SKILL.md)

Apply this skill only to the selected task. Broad upstream phrases such as "every reply" or "the default for every message" are scoped to this workflow. They do not activate it for unrelated chat. User instructions and the [integration contract](../../docs/INTEGRATION.md) govern combined work. Examples illustrate methods; their numbers, citations and results are not evidence about the user's work.

## Preserved source instructions


## Unified plugin integration

Read [the integration contract](../../docs/INTEGRATION.md) when combining workflows. This active copy retains the complete source instructions below with namespaced skill references. Original bytes and upstream metadata remain in `../../resources/`. Resolve tools by their actual host capabilities; tool names in upstream instructions are capability requirements, not proof of connection. Use the task workspace for generated outputs. Treat historical case-study results as supplied examples, not newly verified findings.

Family skill aliases (read the linked SKILL.md before use):
- `compag-elsevier-paper-editing` → `guardrails-compag-elsevier-paper-editing` (`../guardrails-compag-elsevier-paper-editing/SKILL.md`)
- `research-problem-mechanism-evidence` → `guardrails-research-problem-mechanism-evidence` (`../guardrails-research-problem-mechanism-evidence/SKILL.md`)

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
