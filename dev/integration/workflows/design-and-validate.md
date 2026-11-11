# Design, analyze and validate

Inputs: question/hypothesis, domain mechanism, data availability, constraints, existing code and permitted computation.

1. Read `scholar-methodology-design`, `arms-methodology-architect` and `guardrails-research-problem-mechanism-evidence`. Map each claim to a mechanism and a discriminating test. Define comparators, controls, assumptions and failure cases.
2. Quantitative tasks: use `scholar-data-analysis-plan`, `evidence-statistics-explained` and `scholar-results-interpreter`; justify statistical choices, uncertainty and multiplicity. Qualitative tasks: use `scholar-qualitative-analysis` and `scholar-survey-design`; preserve coding decisions and participant context. Mixed methods: specify how the strands answer the same question and are integrated.
3. For modeling, read `arms-paper-modeler`; derive equations and test limiting cases, dimensions and assumptions. For numerical experiments read `arms-validate-method`; execute actual code with controlled seeds/configuration and appropriate accuracy/convergence checks.
4. Apply `scholar-research-ethics` and `scholar-originality-integrity` where participants/data use require it. Do not invent ethics approval, consent or proprietary access.
5. Preserve inputs, processing, code, environment, outputs and failed checks. Run the compatibility failure/consistency roles when helpful; report missing external services rather than simulating their success.

Outputs: design/method specification, analysis plan, code and results if run, validation/failure log and evidence ledger. Gate: the experiment actually tests the claim, provenance is retained, and synthetic illustrations are separated from empirical findings. Roles: `agents/methodologist.md`, `agents/reproducibility-reviewer.md`.
