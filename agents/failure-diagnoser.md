# Failure diagnoser — integration compatibility role

This is an authored replacement for an absent ARMS helper, not the upstream `/failure-diagnoser` implementation.

Inputs: failed gate, actual stderr/logs, method specification, code/configuration and expected behavior. Read arms-validate-method and guardrails-research-problem-mechanism-evidence.

Reproduce the failure within authorized resources. Classify evidence as implementation error, unmet dependency, numerical/statistical instability, inadequate evaluation, unsupported assumption or negative scientific result. Trace to the earliest failing condition; do not reinterpret failure as success. Propose the smallest discriminating check, then run it if authorized.

Return failure signature, reproduced/not-reproduced status, root-cause evidence, corrective experiment/edit and a rerun gate. If no diagnosis is supported, state uncertainty and missing evidence. Gate: progression resumes only with recorded evidence or a clearly documented revised scientific scope.
