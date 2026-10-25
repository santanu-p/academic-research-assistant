---
name: statistical-analysis
description: Plan and execute reproducible quantitative analysis with a defined estimand, design-aware models, diagnostics, uncertainty, and restrained interpretation.
---

# Statistical analysis

Use this Academic Research Assistant skill for quantitative data analysis and statistical interpretation. Apply the [research contract](../../docs/RESEARCH-CONTRACT.md). Start with the scientific target and data-generating design, not a menu of tests. Distinguish analysis planning, executed analysis, and interpretation of supplied output.

## Inputs and inferential target

Obtain the question, dataset and codebook, sampling or assignment design, unit of analysis, outcomes, predictors, planned comparisons, prior protocol, and the intended population. Establish permissions and avoid exposing identifiers or sensitive records in logs. If only summary output is available, identify which diagnostics and data checks cannot be performed.

Define the estimand or prediction target in words before equations: for whom, under which conditions, at what time, and compared with what? Distinguish description, association, causal inference, prediction, equivalence, and decision analysis. A model coefficient is not automatically the estimand, and adjustment alone does not establish a causal interpretation.

## Analysis operations

1. Audit provenance and structure. Confirm row meaning, identifiers, variable types, units, ranges, duplicate records, coding conventions, missing-value representations, and linkage quality. Do not silently remove unusual observations because they weaken the desired result.
2. Summarize the observed data with distributions and suitable plots. Retain the sampling structure and denominators. Examine missingness by relevant groups and times; the cause of missingness is not identifiable from a simple missingness plot alone.
3. Choose methods that match the outcome and design, including dependence from repeated observations, clusters, time, space, or paired measurements. Explain model assumptions and what departures could change the inference. Avoid selecting a test solely from a single normality-test p-value.
4. Implement a documented primary analysis. Record transformations, reference categories, exclusions, weights, uncertainty method, software versions, and random seeds where relevant. Keep exploratory choices visible rather than rewriting them as prespecified decisions.
5. Assess model adequacy using diagnostics relevant to the model and claim: residual structure, influential cases, functional form, dispersion, calibration, separation, convergence, or effective sample size as applicable. A software routine returning an estimate is not proof that the model is adequate.
6. Quantify uncertainty and practical magnitude. Report estimates with intervals, units, and meaningful context. Explain the assumptions behind frequentist or Bayesian interpretations. A confidence interval is not a probability distribution over a fixed parameter; a credible interval depends on its model and prior.
7. Run sensitivities to consequential assumptions, missing-data choices, exclusions, plausible confounders, model form, or prior choices. Distinguish robustness to examined alternatives from robustness to all possible bias.

## Specialized decisions

For confirmatory multiple comparisons, define the family and error criterion or justify a hierarchical analysis. For exploratory analyses, disclose the breadth of searches rather than displaying only favorable results. Failure to reject a null does not establish equivalence; equivalence and noninferiority require justified margins and appropriate designs.

For prediction, separate training, tuning, and evaluation. Prevent leakage through preprocessing, feature selection, repeated entities, or time. Compare meaningful baselines and report calibration and discrimination or loss suitable to the intended use. Cross-validation estimates performance under its split design, not universal deployment reliability.

For causal analysis, make identification assumptions explicit, using a causal structure when helpful. Consider confounding, selection, positivity, interference, timing, and measurement. For simulation or numerical research, distinguish Monte Carlo variability, approximation error, parameter uncertainty, and model discrepancy. For qualitative data, use [qualitative analysis](../qualitative-analysis/SKILL.md) unless a justified quantitative coding design has been specified.

## Deliverable and verification

Deliver an analysis plan or executed report, reproducible code, provenance and transformation notes, tables or figures, diagnostics, sensitivity results, and a limitations statement. Verify units, signs, labels, denominators, and reported numbers against executed outputs. Independently check a consequential calculation where feasible. If runtime or data access prevents execution, return proposed code and clearly state that it has not produced validated results. Route evidence pooling to [meta-analysis](../meta-analysis/SKILL.md) and design changes to [methodology design](../methodology-design/SKILL.md).
