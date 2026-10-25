---
name: meta-analysis
description: Assess whether quantitative study results can be pooled and conduct a reproducible synthesis with compatible estimands, dependency handling, uncertainty, and sensitivity analysis.
---

# Meta-analysis

Use this Academic Research Assistant skill to combine compatible quantitative estimates, or explain why pooling would be misleading. Apply the [research contract](../../docs/RESEARCH-CONTRACT.md). Meta-analysis is an analysis of selected evidence; it cannot repair biased study selection or make incompatible questions equivalent. Review eligibility and provenance belong with [systematic review](../systematic-review/SKILL.md).

## Inputs and compatibility decision

Obtain the review question, study-level extraction dataset, codebook, source locations, risk-of-bias judgments, and protocol. Identify the estimand, outcome, time point, comparison, target population, and study design represented by each estimate. Check whether the proposed pooled quantity has a meaningful interpretation across these differences.

Decide whether to pool, separate groups, or provide a structured non-pooled synthesis. Substantive incompatibility matters even if a statistical heterogeneity measure is small. A random-effects model does not justify combining arbitrary populations or outcomes. State when the available number of studies is too small for a proposed diagnostic or moderator model to be informative.

## Prepare and analyze

1. Verify input estimates against their sources using [evidence extraction](../evidence-extraction/SKILL.md). Preserve units, direction, adjustment, denominators, uncertainty, and study/report identifiers. Make sure repeated reports and overlapping participants are not counted as independent evidence.
2. Select a compatible effect measure and document transformations. Distinguish odds ratios, risk ratios, rates, correlations, mean differences, standardized differences, and other measures. Calculate sampling variances from justified information; do not substitute a standard deviation for a standard error.
3. Plan dependence handling for multiple outcomes, time points, intervention groups, or repeated samples. Choose a justified selection rule, multivariate or multilevel model, appropriate covariance model, or another valid approach. Splitting a control group is not a universal solution to correlated effects.
4. Choose the statistical model based on the scientific target. Explain the difference between a common-effect target and a distribution of effects. For random-effects analysis, document the between-study variance estimator and uncertainty method; evaluate their behavior with sparse evidence.
5. Fit the analysis with versioned code and record exclusions, transformations, software versions, and options. Inspect model warnings, influential observations, and extraction anomalies before interpreting the result.
6. Report the pooled estimate and uncertainty, study estimates, weights when meaningful, heterogeneity measures with their uncertainty or limitations, and a prediction interval only when its assumptions and data support it. Explain that a confidence interval for a mean effect and a prediction interval answer different questions.
7. Run prespecified or well-justified sensitivities: study design, bias concerns, transformations, missing variance assumptions, influential cases, dependence structures, and plausible model choices. Label post hoc explorations and keep them distinct from the primary analysis.

## Interpretation limits

Do not vote-count statistical significance. Evaluate direction, magnitude, precision, and applicability together. Treat meta-regression and subgroup analyses cautiously: study-level associations can be confounded and do not automatically describe individual-level effect modification. Avoid overfitting a small number of studies.

Publication-bias and small-study-effect diagnostics have assumptions and limited power, especially with few or heterogeneous studies. A symmetric plot does not establish the absence of missing evidence, and an asymmetry does not uniquely identify publication bias. Do not mechanically “correct” an estimate without explaining the model and its limitations.

Qualitative themes, mathematical theorems, and incompatible computational benchmarks are not effect sizes. Their evidence may inform interpretation, but use an appropriate synthesis instead of manufacturing numeric comparability. Network, diagnostic, individual-participant, and complex dependent-data syntheses require designs and models tailored to those settings.

## Deliverable and verification

Deliver analysis-ready data, transformation documentation, executable analysis, model specification, tables or figures, and an interpretation bounded by evidence quality and compatibility. Use [statistical analysis](../statistical-analysis/SKILL.md) for diagnostics and [scientific visuals](../scientific-visuals/SKILL.md) for publication figures. Recompute a few estimates independently, verify all study counts and labels, and ensure reported values match the executed outputs. If code could not run, label results as a proposed analysis without invented pooled values.
