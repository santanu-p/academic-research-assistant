---
name: methodology-design
description: Design an empirical, qualitative, theoretical, or computational study whose evidence and analysis can answer a specified research question.
---

# Methodology design

Use this Academic Research Assistant skill to connect a research question to a feasible study protocol. Apply the [research contract](../../docs/RESEARCH-CONTRACT.md). The deliverable is an executable design with justified choices, not a list of fashionable methods. If the question remains ambiguous, resolve its consequential parts with [research question](../research-question/SKILL.md).

## Establish the design target

Obtain the question, intended claim, unit of analysis, setting, available data or materials, constraints, and relevant prior evidence. Identify which decisions are fixed by the user and which remain open. State the target population, process, mathematical domain, or computational regime, and the narrower domain actually accessible to the project.

Classify the claim before selecting tools. Description needs adequate coverage and measurement; explanation needs explicit alternatives; causal inference needs defensible identification; prediction needs honest evaluation; interpretation needs an articulated analytic position and contextual grounding. One study may serve several purposes, but each claim requires its own evidential support.

## Construct the protocol

1. Draw or describe the sequence from selection through observation to analysis. Specify inclusion and exclusion rules, recruitment or sampling, measurement occasions, data provenance, and the roles of people, instruments, and software.
2. Identify the main threats to the intended inference. Examples include selection, confounding, measurement error, missingness, treatment interference, researcher influence, model misspecification, and numerical instability. Tie each threat to a mitigation or an acknowledged limit.
3. Define primary outcomes or analytic targets before inspecting results where appropriate. Separate confirmatory decisions from exploratory work and record how later changes will be disclosed. A preregistration is useful only if its commitments are clear and the actual procedure can be compared with them.
4. Choose an analysis that matches the design and data structure. Account for repeated observations, nesting, dependence, censoring, or unequal exposure. Specify model diagnostics, uncertainty calculations, and sensitivity analyses that could change the interpretation.
5. Plan data management: identifiers, versioning, codebooks, access controls, retention, permitted reuse, and an audit trail. Determine whether ethics review, consent, agreements, or specialist oversight is required before collection. Do not imply that a drafted protocol constitutes approval.
6. Define feasibility milestones and stopping rules. A pilot should answer concrete questions about recruitment, instrument behavior, computation, or workflow; it should not be described as adequately powered evidence of an effect without justification.

## Mode-specific decisions

For quantitative studies, specify the estimand and an estimator or identification argument. Justify sample size through precision, power under explicit assumptions, design simulation, or a realistic resource limit with consequences. Include attrition and clustering where applicable. Do not invent an expected effect to produce a convenient sample size. Decide how multiplicity, missing observations, and deviations will be handled.

For qualitative studies, justify the relationship between epistemological stance, sampling, data generation, and analysis. Explain why interviews, observation, documents, or another material can illuminate the question. Use a reasoned sample adequacy strategy appropriate to the approach; do not promise universal saturation thresholds. Include reflexive documentation and practical handling of sensitive accounts.

For theoretical work, state assumptions, definitions, intermediate claims, proof or derivation strategy, and the scope of proposed conclusions. Identify limiting cases and counterexamples. For computational work, separate mathematical formulation, discretization or approximation, implementation, and scientific interpretation. Specify reference cases, convergence checks, tolerances, random seeds where relevant, and resource requirements. Good agreement with one benchmark does not validate every regime.

## Deliverable and verification

Produce a protocol with a question-to-evidence map, design rationale, sampling or domain rules, procedures, analysis plan, quality checks, ethics and data considerations, timeline, and a table of unresolved choices. Include at least one plausible alternative design and why the selected design better fits the actual constraints.

Check that every planned conclusion has supporting observations or arguments and that every major design choice is documented. Verify methodological citations rather than supplying remembered references as confirmed. Route detailed execution to [statistical analysis](../statistical-analysis/SKILL.md), [qualitative analysis](../qualitative-analysis/SKILL.md), or [research validation](../research-validation/SKILL.md) as needed. State what the protocol can establish and which stronger claims would remain unsupported.
