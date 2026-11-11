---
name: guardrails-research-problem-mechanism-evidence
description: "Audit or develop scientific and technical arguments by connecting an observable problem, the exact mechanism changed, expected intermediate effects and evidence-bounded conclusions. Distinguish theory, implementation, ablation, comparison and diagnostics; preserve frozen content."
---
## Selection and handoffs

Audit or develop technical reasoning from observable problem through actual mechanism to evidence-bounded consequence.

**Select for:** Scientific claim audit; Explain what a technical design changes and which evidence supports its consequence; Interpret ablations, comparisons, diagnostics or implementation without causal overreach

**Expected work:** Name the real system-level failure before adding a module/formula; Explain why current design cannot address it; Identify changed variable/relation/freedom/constraint/time scale/information flow; State expected intermediate consequence; Classify theory/implementation/ablation/comparison/diagnostic evidence; Match claim strength and scope to direct evidence; Verify five final problem/design/mechanism/rationale/support questions and flag missing links

**Expected output:** Problem→mechanism→observable consequence→evidence map; Evidence-bounded technical argument or claim corrections; Missing-link, attribution and confounding flags

**Scope boundaries:** Casual writing; Stylistic cleanup with no scientific reasoning; Claiming a measured benefit from design intent alone; Forcing all parallel technical branches into one causal chain

**Related skills:** [guardrails-compag-elsevier-paper-editing](../guardrails-compag-elsevier-paper-editing/SKILL.md), [evidence-claim-checker](../evidence-claim-checker/SKILL.md)

Apply this skill only to the selected task. Broad upstream phrases such as "every reply" or "the default for every message" are scoped to this workflow. They do not activate it for unrelated chat. User instructions and the [integration contract](../../docs/INTEGRATION.md) govern combined work. Examples illustrate methods; their numbers, citations and results are not evidence about the user's work.

## Preserved source instructions


## Unified plugin integration

Read [the integration contract](../../docs/INTEGRATION.md) when combining workflows. This active copy retains the complete source instructions below with namespaced skill references. Original bytes and upstream metadata remain in `../../resources/`. Resolve tools by their actual host capabilities; tool names in upstream instructions are capability requirements, not proof of connection. Use the task workspace for generated outputs. Treat historical case-study results as supplied examples, not newly verified findings.

Family skill aliases (read the linked SKILL.md before use):
- `compag-elsevier-paper-editing` → `guardrails-compag-elsevier-paper-editing` (`../guardrails-compag-elsevier-paper-editing/SKILL.md`)
- `research-problem-mechanism-evidence` → `guardrails-research-problem-mechanism-evidence` (`../guardrails-research-problem-mechanism-evidence/SKILL.md`)

---

Apply this skill whenever the task involves research reasoning, technical design, method development, experiment interpretation, or scientific claims.

Core rule

Real problem → mechanistic intervention → observable consequence → evidence-bounded conclusion.

Workflow

1. Identify the real technical problem before discussing a module, formula, loss, cost, constraint, algorithm, or experimental result.
2. Express the problem as a concrete system behavior or failure mode. Examples include increased error, insufficient response, excessive control action, prediction–execution mismatch, plan oscillation, infeasibility, solver instability, increased computation, reduced task efficiency, or sensitivity to operating conditions.
3. Explain why the existing design is insufficient for that specific behavior.
4. Describe the intervention mechanistically. State what variable, relation, decision freedom, constraint set, time scale, or information flow changes.
5. Explain the intermediate consequence expected from that change before making a performance claim.
6. Match every conclusion to the strongest evidence that directly supports it.
7. Preserve all user-declared frozen data, definitions, metrics, experimental protocols, terminology, and interfaces.

Evidence discipline

- Theory supports only conclusions that follow from the stated assumptions and derivation.
- Implementation evidence establishes what the system actually computes, constrains, schedules, or executes.
- Ablations support the incremental effect of the factor that was actually changed.
- Method comparisons support performance differences between complete methods under the stated protocol.
- Diagnostic metrics support whether an intended mechanism behaved as expected.
- If multiple factors change together, do not attribute the outcome to a single factor without an additional control.
- If direct evidence is absent, use mechanism-level wording such as "is used to", "is designed to", "enables", "allows", or "reduces the risk of". Do not present an intended effect as a verified result.

Structural discipline

- Separate shared backbone, paper-specific innovation, and adaptive mechanisms.
- Attribute experimental effects to the interface that actually changes.
- Do not invent a linear causal chain merely for narrative smoothness.
- When accuracy, feasibility, computation, continuity, or prediction consistency are parallel problems, establish the higher-level objective and treat them as parallel branches.
- Advance sections and paragraphs by cognitive increment. Each part should add information needed to answer a previously unresolved question.
- Treat equations, figures, and experiments as components of the argument. Equations explain implementation of a mechanism, figures clarify structure or relations, and experiments test expected consequences.

Before finalizing, verify that the argument can answer all five questions below.

1. What is the real technical problem?
2. Why is the current or prior design insufficient?
3. What exactly does the new mechanism change?
4. Why could that change mitigate the problem?
5. What do the available data, definitions, implementation, theory, and experiments actually support?

If any link is missing, weaken the claim or flag the evidence gap instead of filling it with an invented explanation.

Read `references/evidence-guide.md` when detailed claim-strength or experiment-attribution rules are needed.
