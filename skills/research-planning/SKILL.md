---
name: research-planning
description: Convert a research objective into a dependency-aware plan with concrete outputs, decision milestones, resource constraints, risks, and honest completion criteria.
---

# Research planning

Use this Academic Research Assistant skill to make a research project manageable and reviewable. Follow the [research contract](../../docs/RESEARCH-CONTRACT.md). A useful plan handles uncertainty and dependencies; it does not disguise uncertain discovery as a predictable sequence of guaranteed results.

## Inputs and planning horizon

Obtain the objective, current stage, fixed deadlines, available people and effort, facilities or data access, budget limits, known dependencies, and existing commitments. Distinguish a plan for an application from an operational plan for work already authorized. If the user supplies a schedule, improve its feasibility without silently expanding the scientific scope.

Choose a useful planning horizon: the whole project for major dependencies and a nearer interval for detailed actions. Record assumptions about effort, review time, access, and procurement. Calendar duration and person-time differ; several tasks can run concurrently only when resources and dependencies allow it.

## Build the plan

1. Decompose the objective into tangible outputs: a verified corpus, a protocol, a calibrated instrument, a proof draft, a tested implementation, an analysis dataset, or a manuscript section. Name the evidence that would show each output is usable.
2. Identify prerequisites and owners. Separate scientific dependencies from administrative and technical dependencies. A calculation may depend on a parameter convention, while data collection may depend on access and ethics approval. Do not schedule dependent work as though these prerequisites already exist.
3. Estimate effort and duration using ranges where uncertainty matters. Explain the basis: prior experience, known workload, a pilot, or an explicitly provisional assumption. Avoid false precision and distinguish committed deadlines from internal targets.
4. Define milestones as decisions or verified capabilities. “Code written” is weaker than “reference cases agree within a justified tolerance.” “Interviews complete” does not establish adequate analysis. Milestones should make continuation, revision, or stopping possible.
5. Build a dependency-aware sequence and identify tasks with little scheduling flexibility. Include review, rework, documentation, and handoff time. Limit concurrent work where the same researcher or resource is a bottleneck.
6. Create a risk register with trigger, consequence, mitigation, fallback, owner, and decision date. Focus on risks that could alter the question, inference, schedule, or resource needs. Avoid a decorative inventory of hypothetical problems with no action attached.
7. Define how progress will be updated: evidence completed, assumptions changed, blockers, next decisions, and revised estimates. Preserve an amendment history for consequential scope or method changes. A missed target should trigger replanning rather than retrospective relabeling of incomplete work.

## Adapt to research uncertainty

For quantitative projects, plan instrument or data-quality checks, recruitment or acquisition, analysis decisions, missing-data handling, and reproducibility review. Include the time needed to resolve discrepancies, not only to fit models. For qualitative projects, allow iterative sampling, analytic memoing, contextual engagement, and revisions consistent with the chosen method. Do not force all analysis to begin after data generation ends if iteration is integral to the design.

For theoretical work, schedule intermediate lemmas, counterexample searches, limiting cases, and alternative routes. The failure of a conjecture can be an informative result; distinguish that from a failure to perform the planned checks. For computational work, separate implementation, verification, performance, convergence, scientific validation, and artifact packaging. A queued computation or successful software build is not a validated scientific result.

## Deliverable and verification

Deliver an editable plan with work items, outputs, dependencies, owners or unassigned roles, effort ranges, dates, acceptance evidence, and risks. Use the [work-plan schema](references/work-plan.md) when a reusable project record is useful. A concise table is often sufficient; use a visual schedule only when it clarifies concurrency or deadlines. Include the next executable actions and decisions needing the user, while continuing independent work already authorized.

Check that dependencies are coherent, resource allocations do not exceed availability, dates respect fixed constraints, and milestones have observable completion criteria. State which estimates are unvalidated. Route scientific design to [methodology design](../methodology-design/SKILL.md) and funding narratives to [research proposals](../research-proposals/SKILL.md). Do not create reminders, external tasks, messages, or recurring automations merely because they appear in the plan; those actions need the corresponding user request and available capabilities.
