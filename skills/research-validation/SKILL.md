---
name: research-validation
description: Design and perform proportionate validation of scientific claims, analyses, models, and computational results with traceable evidence and explicit limits.
---

# Research validation

Use this method to assess whether a research claim or artifact has survived the checks appropriate to its intended use. Apply the [research contract](../../docs/RESEARCH-CONTRACT.md). Validation is a relationship between a claim, a method, and evidence. Passing a check does not automatically validate a broader claim, a different parameter regime, or an entire project.

## Define what will be assessed

Write the exact target claim and its intended audience or decision. Identify the artifact being tested, its version or immutable identifier when available, the data or sources used, and the environment required to reproduce the result. Separate correctness of implementation, adequacy of the model, quality of evidence, and validity of interpretation.

Build a check ledger with: target; failure mode; check; acceptance criterion; required inputs; actual outcome; and residual concern. Set criteria from the scientific question, known standards, or justified tolerances before examining the answer where feasible. If criteria were chosen after seeing outcomes, disclose that fact rather than calling the exercise prespecified.

## Choose checks that expose failures

For empirical quantitative work, inspect provenance, inclusion rules, missingness, measurement definitions, units, and denominators. Reconcile sample counts across data, tables, and text. Check whether the statistical model matches design and dependence structure. Examine assumptions and appropriate sensitivity analyses. Distinguish uncertainty from sampling, measurement, and modeling; do not imply that one interval captures all of them.

For qualitative work, inspect how source material supports codes and interpretations, how selection decisions were documented, and whether counterexamples or competing interpretations were considered. Assess reflexive notes and analytic transparency when supplied. Member checking or multiple coders may be appropriate in some designs, but their absence is not automatically a defect in every qualitative tradition.

For theoretical work, verify definitions, quantifiers, domain restrictions, dependencies, and nontrivial proof steps. Test candidate counterexamples and special cases. Confirm that cited propositions apply under the actual assumptions. Label computer-assisted evidence distinctly from a complete proof unless the computational certification and its conditions are established.

For computational work, separate software verification from model validation. Reproduce a benchmark with known behavior; inspect convergence with resolution, precision, truncation, or solver tolerance as relevant. Compare an independent method when feasible. Investigate conditioning, stopping criteria, branch selection, and conservation or invariants. A small residual may coexist with a wrong solution branch or an inadequate model.

For an iterative numerical or parameter-dependent calculation, use [the computational check guide](references/computational-checks.md) to build a reproducible run record, test resolution and precision separately, and track solution identity across parameter changes. The guide describes checks to perform; it does not supply a solver or establish the accuracy of unexecuted calculations.

When results compare methods or manuscript formulas depend on code, use [the comparison and implementation ledgers](references/comparison-and-implementation-ledgers.md) to track comparator coverage, formula-to-code checks, discrepancies, and affected claims through the handoff. These records guide human or assistant review; they do not automatically inspect code or run evaluations.

### Plan study-appropriate comparisons

Before evaluating results where feasible, specify the comparator, the quantity and units to compare, the applicable inputs or population, and the criterion or uncertainty needed to interpret disagreement. A comparator may be an analytical limit, independently implemented method, benchmark dataset, control group, baseline model, or alternative explanation; choose it for the claim rather than availability alone. Record shared assumptions and dependencies, since agreement between methods with the same error source is not independent confirmation. If a comparator or threshold is chosen after results are visible, disclose that choice and treat the comparison accordingly.

For an analytical or computational claim, start with dimensional and limiting-case checks, then select applicable exact cases, independent calculations, convergence studies, and residual or invariant checks. Record the tested parameter range and numerical settings, and investigate disagreement before deciding whether it reflects approximation, implementation, or differing assumptions. Agreement at selected points does not establish accuracy elsewhere.

For an empirical claim, identify the comparison groups or baseline, measurement procedure, sampling and assignment, time frame, and possible sources of bias. Check data quality and the planned estimate against the design; use suitable uncertainty and sensitivity analyses. If an external dataset or replication is available, examine differences in population, measurement, and setting before interpreting agreement or disagreement. Observational associations need an explicit identification argument before causal conclusions are drawn.

## Execute and interpret

Run available checks and record actual commands, inputs, outputs, and relevant versions without exposing secrets. If execution is unavailable, deliver a validation plan and mark it unexecuted. For a failure, isolate whether the cause is input integrity, method choice, implementation, environment, or interpretation before proposing a repair. Preserve the failing evidence.

Use sensitivity analysis to learn which conclusions change under defensible alternative choices. Distinguish robustness within tested alternatives from universal robustness. Where multiple comparisons or exploratory searches were performed, describe the scope and avoid selectively presenting favorable checks. Stop repeating successful checks unless a change or unresolved failure supplies a reason.

Route manuscript corrections to [academic editing](../academic-editing/SKILL.md), equation design issues to [mathematical modeling](../mathematical-modeling/SKILL.md), and missing reasoning to [scientific reasoning](../scientific-reasoning/SKILL.md).

## Deliver and verify

Provide the target claim, executed checks with outcomes, failed or unavailable checks, necessary repairs, and a conclusion bounded by the evidence. Distinguish “reproduced the supplied result,” “passed these checks,” and “supports this scientific interpretation.” Each asserts something different.

Confirm that every reported pass has a recorded outcome, every important failure has a disposition, and acceptance criteria have not quietly shifted. Cross-check figures and tables against underlying results when accessible. Preserve uncertainty, negative findings, and unresolved discrepancies in the final record. A credible validation report may conclude that the claim needs narrowing or that further work is required; it must not declare completion solely because a script exited successfully.

Report unfavorable results alongside favorable ones, including failed checks, discrepancies, and credible alternatives, and explain their implications for the specific claim. Separate observations from interpretation and identify which checks remain planned or unavailable. Offer a conditional go/no-go decision only if the user has defined decision criteria; show how the observed evidence relates to each criterion and state when missing evidence prevents a decision. Otherwise provide an evidence-bounded assessment and the unresolved choices without inventing a decision threshold.

