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

## Explain statistical results

Adapt the explanation to the reader's background and the actual design. Identify the quantity being estimated, the comparison or reference value, the observations and their units, and the method used. Translate a coefficient or effect into the original scale when possible, with the reference group and adjustment set made clear. Explain what a positive or negative value means in that particular coding scheme; do not call an association causal without a defensible identification argument.

For a null-hypothesis test, explain the p-value as the probability, under the stated null model and its assumptions, of a test statistic at least as extreme as the observed statistic according to the chosen test. It is not the probability that the null hypothesis is true, nor the chance that the result arose by chance alone. Report the estimate and interval alongside the p-value when available. A threshold crossing does not measure effect size or practical importance; a result above a threshold does not prove no effect. Multiple testing and selective reporting affect interpretation.

Explain a frequentist confidence procedure through its long-run coverage under its assumptions: across repeated samples, the stated proportion of intervals would cover the fixed parameter. A particular interval gives a range compatible with the data and model at the stated confidence level, not a probability that the fixed parameter lies in that realized interval. A Bayesian credible interval instead summarizes the posterior distribution conditional on the model, prior, and data. Do not interchange the two interpretations.

### Interpret magnitude and comparisons

For binary outcomes, give event counts and denominators, the observation period, and each group's absolute risk where the design permits risk estimation. State which group is the reference. Report an absolute risk difference in percentage points alongside a risk ratio when useful; relative changes alone hide baseline risk. An odds ratio compares event odds, not probabilities, and can differ substantially from the risk ratio, particularly when events are common. Do not convert an adjusted odds ratio directly into a risk ratio or an absolute difference without an appropriate baseline risk and the model assumptions. Case-control sampling generally does not provide population risks from the sampled group proportions alone.

Hypothetical example: over the same period, 20 of 100 people in group A and 10 of 100 in group B experience an event. Their observed risks are 20% and 10%; A minus B is 10 percentage points, and the risk ratio A/B is 2. The odds are 20/80 and 10/90, so the odds ratio A/B is 2.25. These are descriptive sample comparisons, with no uncertainty or causal claim implied. With 2 events per 1,000 versus 1 per 1,000, the risk ratio is also 2, but the absolute difference is 1 per 1,000.

For correlation, identify the variables, units, sample and correlation measure. Pearson's correlation describes the direction and strength of a linear association; a weak value does not rule out a nonlinear relationship, and outliers or restricted ranges can alter it. For regression, explain the outcome scale, reference category, predictor increment, adjustment set, and link function. In an additive linear model, a slope describes a fitted mean difference per unit of predictor conditional on other included variables; it need not apply outside the observed range or to every individual. An exponentiated logistic coefficient is an odds ratio, not an absolute probability change. Adjustment does not by itself resolve unmeasured confounding or establish causation.

Hypothetical example: in an additive linear model predicting test score from hours of study, the fitted slope is 2 points per hour. Comparing otherwise identical covariate values within the modeled range, a one-hour difference corresponds to a 2-point difference in fitted mean score; it does not establish that adding an hour causes that change. A correlation of 0.6 in the same data would describe a positive linear association, not a 60% increase or a causal effect.

Interpret effect size in its units, uncertainty, baseline, outcome importance, costs, and decision context. Explain standardized effects using the standardizer and population rather than applying universal small/medium/large labels mechanically. A precise small difference may matter at scale, while an imprecise large estimate may be compatible with a wide range of effects. State missing denominators, uncertainty, relevant thresholds, or design details rather than inventing them.

Distinguish standard deviation, which describes spread in observations, from standard error, which describes sampling variability of an estimator under a specified procedure. A narrow standard error does not rule out systematic bias. Explain statistical power as the probability of rejecting a specified null under a particular alternative and design; it depends on the assumed effect, variability, sample size, and test. Do not infer the probability that an observed finding is true from power or calculate retrospective power from the observed p-value as a substitute for uncertainty analysis.

When asked to teach a concept, use a small clearly labeled hypothetical example and identify its assumptions. If actual output is supplied, quote its values faithfully and flag absent information that limits interpretation. Separate statistical precision, practical relevance, and possible bias; describe what additional data or design information would resolve the most consequential uncertainty. Avoid declaring a result significant, robust, or generalizable without the relevant evidence.

## Deliverable and verification

Deliver an analysis plan or executed report, reproducible code, provenance and transformation notes, tables or figures, diagnostics, sensitivity results, and a limitations statement. Verify units, signs, labels, denominators, and reported numbers against executed outputs. Independently check a consequential calculation where feasible. If runtime or data access prevents execution, return proposed code and clearly state that it has not produced validated results. Route evidence pooling to [meta-analysis](../meta-analysis/SKILL.md) and design changes to [methodology design](../methodology-design/SKILL.md).
