---
name: research-appraisal
description: Appraise a study or research manuscript by matching claims to design, evidence, analysis, reporting, and inference, with actionable and proportionate judgments.
---

# Research appraisal

Use this Academic Research Assistant skill for critical appraisal of published studies, preprints, protocols, or manuscript drafts. Apply the [research contract](../../docs/RESEARCH-CONTRACT.md). This is the common appraisal stage for both studies and manuscripts: evaluate the underlying inference and its reporting together while distinguishing a methodological flaw from missing documentation.

## Inputs and appraisal frame

Obtain the full available work, supplements, protocol or registration when relevant, the review purpose, disciplinary context, and any assessment framework required by the user. Establish the version and access limits. A review based only on the abstract cannot establish the adequacy of uninspected methods or analyses.

Identify the central claims and their intended scope. Select criteria appropriate to the design rather than treating a generic checklist as a universal quality score. If using an external appraisal instrument, verify its current guidance, reproduce only permitted material, and document any adaptation. Do not calculate an overall numerical score unless that scoring rule is justified for the actual task.

## Appraise the evidence chain

1. Reconstruct the question-to-conclusion chain: sampling or premises, observations or derivations, analysis, findings, and interpretation. State the study's strongest supportable claim before evaluating stronger claims.
2. Examine selection and applicability. Determine how participants, cases, materials, parameter regimes, or texts were chosen; what is absent; and how this constrains transfer to the target domain.
3. Check measurement and data generation. Are key concepts operationalized appropriately? Could instruments, coding decisions, researcher involvement, preprocessing, or data quality systematically affect the findings?
4. Examine the analysis in relation to the design. Look for dependence, confounding, missingness, inappropriate comparisons, researcher degrees of freedom, multiplicity, and unexplained deviations. Distinguish a sensitivity analysis that tests a real alternative from one that repeats the same assumption.
5. Compare reported results with the conclusions. Check direction, magnitude, uncertainty, denominator, exceptions, and counterevidence. Avoid treating a p-value as a complete argument, a persuasive quotation as population prevalence, or an attractive simulation as empirical validation.
6. Assess transparency and reproducibility: availability of methods, data, code, derivations, model settings, and provenance sufficient for the claimed result. Inaccessibility is a reproducibility limitation; it does not alone prove that a result is false.
7. Review reporting for omitted information that prevents judgment. Ask for specific missing details rather than asserting that an unreported procedure was not performed. Note discrepancies with protocols or registrations without assuming intent.

For each concern that could change a central claim, make the causal or inferential pathway explicit: identify the observed design or analysis feature and its source location; explain how it could affect the particular comparison, outcome, and time point; and state its implication for the claim. Describe a plausible direction or magnitude only when the evidence and assumptions support it; otherwise leave it undetermined. If reporting is insufficient, label the judgment uncertain and specify the missing information or a feasible sensitivity check. Precision does not by itself rule out systematic bias.

## Apply the appropriate lens

For quantitative research, assess the estimand, design, identification assumptions, precision, model diagnostics, missing-data handling, and alternative explanations. Separate internal validity from generalizability and statistical uncertainty from systematic bias.

For qualitative research, assess coherence among the question, methodological stance, sampling, engagement, interpretation, reflexivity, and evidence excerpts. Consider context and analytic depth. Do not impose blinding, randomization, numerical saturation rules, or inter-rater agreement as universal requirements when they conflict with the chosen approach.

For theoretical work, inspect definitions, assumptions, logical dependencies, limiting cases, and counterexamples. Clearly distinguish an identified gap in a proof from a disproven theorem. For computational work, assess implementation verification, numerical error, convergence, benchmark fairness, leakage, baseline selection, and the separation of model adequacy from code correctness.

## Deliverable and verification

Produce an appraisal with a concise overall assessment, supported strengths, consequential concerns, reporting requests, and feasible remedies. For each concern provide a source location, observation, inferential consequence, and proposed check or revision. Rank concerns by their effect on the central claim; do not bury a fatal identification problem among punctuation edits.

Check every criticism against the available text and label uncertainty. Separate “must resolve to support this claim” from optional improvements. Avoid novelty guarantees, editorial predictions, or allegations unsupported by evidence. Route writing fixes to [academic editing](../academic-editing/SKILL.md), new analyses to [statistical analysis](../statistical-analysis/SKILL.md) or [qualitative analysis](../qualitative-analysis/SKILL.md), and response preparation to [reviewer response](../reviewer-response/SKILL.md).
