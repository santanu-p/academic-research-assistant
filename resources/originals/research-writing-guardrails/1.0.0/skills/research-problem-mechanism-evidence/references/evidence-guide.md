# Evidence and attribution guide

## Problem test

A valid problem is observable at the system level. "Missing a module", "lacking consistency", "needing robustness", "needing adaptation", or "needing an additional cost" is not yet a technical problem. Continue until the consequence is concrete.

Useful forms include

- tracking or prediction error increases under a defined condition
- control becomes too weak, too aggressive, or delayed
- predicted motion and executed motion diverge
- the planner repeatedly changes decisions
- a constraint becomes infeasible or frequently active
- the solver becomes unstable or exceeds the time budget
- computational cost grows with horizon or task complexity
- task-level efficiency degrades
- performance becomes highly sensitive to operating conditions

## Mechanism test

For each added design, identify at least one direct system change

- a state, control, latent, or scheduling variable
- a mathematical relation or model dependency
- a feasible-set boundary or constraint range
- an optimization degree of freedom
- a decision horizon or time scale
- an information path or feedback path
- a selection, gating, weighting, or update rule

Then explain the intermediate effect of that change.

## Evidence classes

Theory
Supports properties that follow from assumptions, definitions, or derivations. It does not establish empirical superiority.

Implementation
Supports statements about what was implemented and how information flows through the system. It does not establish performance improvement.

Ablation
Supports the incremental effect of the changed mechanism under the evaluated settings. It does not automatically establish why the change produced that effect unless diagnostics or further controls support the explanation.

Comparison
Supports measured differences between complete methods under the stated protocol. It does not isolate which internal component caused the difference.

Diagnostics
Support whether internal quantities changed in the expected direction. They can strengthen a mechanism explanation but do not replace task-level evaluation when task-level performance is claimed.

## Claim strength

Use direct empirical wording only when the corresponding quantity was actually measured under a valid comparison.

Use mechanism wording when the design rationale is supported but the outcome was not isolated experimentally.

Avoid causal wording when several factors changed simultaneously.

Do not extrapolate beyond the tested population, scenario, operating range, horizon, hardware, map, or data regime without explicit evidence.
