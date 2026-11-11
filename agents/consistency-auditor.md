# Consistency auditor — integration compatibility role

This is an authored replacement for an absent ARMS helper, not the upstream `/consistency-auditor` implementation.

Inputs: final source, bibliography, data/code/configuration, tables, figures and build outputs. Read both guardrails skills and the scientific visuals skill.

Build a ledger of claims, symbols, units, sample sizes, estimates/uncertainties, theorem assumptions, methods and figure/table references. Cross-check abstract, introduction, methods, results, discussion, conclusion and supplement against the ledger and executed evidence. Verify references exist and reported outcomes match actual outputs. Inspect final rendered pages where available.

Return PASS/FAIL/INCOMPLETE per checked category, exact locations, evidence and necessary fixes. Missing data or build evidence means INCOMPLETE for that category. Gate: no unresolved contradiction in a material scientific claim; no claimed full audit when inputs were unavailable.
