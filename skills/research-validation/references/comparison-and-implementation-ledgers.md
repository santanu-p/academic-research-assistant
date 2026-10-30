# Comparison and implementation ledgers

Use these records when a study compares methods or reports equations tied to an implementation. They are manual guidance, not an automated code auditor, a solver, or evidence that any evaluation ran. Adapt fields to the project and link to existing records rather than duplicating sensitive material. Set the scope and acceptance criteria before inspecting results when feasible; record later changes and their rationale.

## Comparator coverage

Give each planned method or baseline a stable identifier. Preserve the source and version of the specification and implementation, the role of each method, and any changes to the original plan. Record parameter choices, data and evaluation conditions needed for a fair comparison; distinguish identical settings from differences justified by a method's requirements.

| Comparator ID | Intended role and specification | Code/version and configuration | Data and evaluation conditions | Execution evidence | Result locations and coverage | Deviation or unresolved issue |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

For every planned evaluation, check which comparator IDs actually appear in the run record and underlying outputs. Match identifiers to versions and settings, including preprocessing, splits, seeds, metric definitions, direction and resource budgets where relevant. Check that tables, figures and text accurately represent the corresponding results. An implementation that exists but was not run is not a completed comparison; an absent row is not a zero result. Record unavailable or failed runs, exclusions, and changes in coverage with their implications. Do not silently replace a missing comparator or describe the comparison as complete.

## Formula-to-code agreement

Select the equations, algorithms and derived quantities that support the reported claims. Link each to its source version and actual implementation. Record meanings, units, indexing, signs, normalization, constraints, boundary conditions and numerical approximations where they matter. An implementation may legitimately use an equivalent formulation; establish equivalence under its stated conditions rather than requiring textual similarity.

| Formula or quantity and source location | Definitions and conventions | Implementation location/version | Check and inputs | Observed outcome | Disposition and affected claims |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Trace the relevant computation through calling code and configuration, not just a matching symbol. Use appropriate checks such as a hand-computed case, an independent implementation, invariants, limiting cases, or a derivation; record actual inputs, outputs and tolerances. Separate a confirmed mismatch from an unverified link or an expected approximation. If a discrepancy changes interpretation, preserve the evidence and determine whether the specification, implementation, report, or assumptions need correction. Do not change numerical results to make prose and code agree.

## Handoff and recheck

1. Attach or link both ledgers, the input and code versions, configurations, run records, results, and acceptance criteria to the next stage. Mark each item passed, failed, unexecuted, or awaiting evidence, with a reason and owner when known.
2. Identify incomplete comparator/evaluation combinations and every unresolved implementation discrepancy. State which tables, figures, equations, conclusions, or further work depend on each issue. Continue independent authorized work, but mark affected claims provisional or blocked.
3. After an authorized repair or a change to data, code, assumptions, or evaluation settings, identify affected results and rerun the relevant checks. Preserve the earlier records and report what changed. A drafted fix or an existing output file is not proof of a successful rerun.
4. At delivery, distinguish planned, executed, checked, and unavailable comparisons. Explain the remaining limitations and only describe coverage or agreement as complete for the specific scope supported by recorded evidence.
