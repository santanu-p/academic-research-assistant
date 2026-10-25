# Work-plan schema

Start with a project statement: intended scientific question; deliverables; explicit exclusions; fixed deadlines; available effort; resource constraints; and assumptions not yet verified. Avoid embedding an expected favorable result in the definition of completion.

## Work items

| Column | Required interpretation |
|---|---|
| item_id | Stable identifier referenced by dependencies and risks |
| output | Concrete artifact or demonstrated capability |
| action | Work required to produce that output |
| owner | Agreed owner or unassigned role |
| prerequisites | Item IDs and external conditions that must hold |
| effort_range | Person-time estimate and basis |
| duration_range | Calendar time including waits and access limits |
| target_dates | Planned dates distinguished from fixed commitments |
| acceptance_evidence | Observable evidence that the output is usable |
| status | Current state, backed by a file or other evidence when complete |
| next_decision | Choice that can change the subsequent work |

Use milestone rows for consequential decisions. Record the criterion, evidence available, options, responsible decision-maker, and deadline. A successful milestone might support continuation; a negative but informative outcome can support a changed scope. Preserve both outcomes honestly.

## Risk and change records

For each consequential risk record: linked item; uncertain condition; observable trigger; effect on question, inference, schedule, or cost; mitigation; fallback; owner; and review date. A mitigation should be an action capable of changing exposure or consequence, not “monitor closely” without a decision criterion.

For changes record: date; prior assumption or scope; new evidence; decision; affected items; revised estimates; and scientific implications. Retain superseded plans when their history explains the current design.

At each update, report completed evidence, changed assumptions, active blockers, next executable work, and decisions needed. Do not mark a task complete merely because effort was spent, a deadline passed, or an output file exists. For long-running computations, distinguish queued, running, terminated, completed, checked, and scientifically interpreted states.
