# Computational checks for a numerical research result

Use this guide when a calculation has convergence, branch-selection, truncation, precision, or reproducibility risks. Adapt the checks to the actual equations and requested claim; do not apply a universal tolerance. An available host, solver, libraries, and data remain separate requirements.

## Prepare the record

Record the equation or objective, domain and boundary or initial conditions, conventions, units, requested observables, parameter values and parameter ranges. Identify the exact code revision, dependency versions, executable command, precision, inputs, and random seed when applicable. Preserve raw output and errors. State an acceptance criterion with its physical or numerical rationale before examining the result when possible; disclose a criterion chosen afterward.

Create a run table with one row per execution. Include parameter value, method, discretization or truncation, tolerance, precision, initial guess or continuation seed, solver status, observable, residual or constraint error, and output location. Distinguish a run that failed to finish from a value computed but failing a check. Do not infer a missing row.

## Test the result

1. Check units, boundary conditions and any relevant conserved quantities or positivity constraints. Compare a known analytic case or independently calculated reference in matching conventions when one is actually available.
2. Vary resolution, truncation or solver tolerance systematically while holding other settings fixed. Compare the same observable across runs, record successive changes and estimate error only under assumptions appropriate to the method. A small successive change alone is not a general error bound.
3. Test numerical precision separately when conditioning or cancellation may matter. A small algebraic residual does not prove that discretization error, branch choice, or model error is small.
4. For parameter sweeps or eigenproblems, record how solutions are matched between neighboring parameter values. Compare overlap or another justified identity measure, inspect crossings and degeneracies, and flag ambiguous matches instead of silently relabeling modes. Vary seeds or compare another method when feasible.
5. Investigate any failed check before drawing conclusions. Preserve results that disagree and separate an implementation defect, numerical instability, model limitation, and an unresolved discrepancy.

For a complex-valued observable, report real and imaginary parts with their conventions, units, and appropriate absolute or relative differences. Near zero, relative differences alone may be misleading. Report the tested parameter range, acceptance thresholds, unfinished or unavailable tests, and which conclusions follow from the recorded runs. Passing checks within one range does not establish behavior outside it.

## Example of a bounded check

For a supplied parameter-dependent eigenproblem, record the operator and boundary conditions, compute a benchmark with a known solution if available, then repeat selected parameter points at several resolutions and precisions. Match the solution branch using a problem-appropriate observable or eigenvector overlap and inspect uncertain crossings. Deliver the executable source, run table, outputs and a conclusion limited to the tested points. If no solver or benchmark is available, provide the plan and mark the calculations unexecuted.
