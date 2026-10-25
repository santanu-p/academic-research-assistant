---
name: evidence-extraction
description: Extract auditable study-level or claim-level evidence into a defined schema while preserving source locations, missing values, versions, and dependent reports.
---

# Evidence extraction

Use this Academic Research Assistant skill to convert papers and associated materials into a structured evidence dataset. Follow the [research contract](../../docs/RESEARCH-CONTRACT.md). Extraction preserves what the source reports; later appraisal and synthesis decide what that evidence means. Do not silently replace reported values with preferred interpretations.

## Inputs and schema design

Obtain the review question, eligible records, source files or links, required variables, and intended analysis. Agree on the extraction unit: publication, study, cohort, experiment, comparison, outcome, time point, claim, or qualitative finding. One publication can contain several studies; several publications can describe the same participants. Assign stable identifiers and record these relationships before counting evidence.

Create a codebook before large-scale extraction. Each field needs a definition, allowed representation, unit, and rule for unavailable or ambiguous information. Use the [extraction-schema reference](references/extraction-schema.md) when building the tables. Distinguish “not reported,” “not applicable,” “unclear,” and a genuine zero. Use a long format when multiple outcomes or time points would otherwise create ambiguous columns. Preserve verbatim text in a separate field from coded interpretation.

## Extraction procedure

1. Verify document identity and version with [source verification](../source-verification/SKILL.md). Connect supplements, protocols, registrations, corrections, and companion reports. Record which source supplies each item.
2. Pilot the schema on a few varied records. Look for fields that cannot be applied consistently, repeated information, and important differences hidden by a single category. Revise the codebook and version the change before continuing.
3. Extract design, setting, sampling, eligibility, participant or material characteristics, intervention or exposure, comparator, procedure, outcome definitions, analysis, and relevant funding or conflicts. Include only fields needed for the review purpose or inference.
4. Attach an exact locator to consequential evidence: page, section, table, figure, appendix, theorem, or code version. A general article link is insufficient when a reviewer must check a particular result.
5. For quantitative data, retain the reported estimate, uncertainty, denominator, analysis population, adjustment, unit, direction, and time point. Keep raw numbers distinct from calculated quantities. If deriving a value, document the formula, inputs, assumptions, and independent check.
6. For qualitative evidence, retain the analytic finding, supporting excerpt where permitted, context, participant or author voice, and the extractor's interpretation as separate items. Do not reduce a rich interpretation to a frequency unless the intended synthesis justifies that transformation.
7. Log discrepancies across text, tables, figures, versions, or reports. Do not silently select the more favorable result. Record the resolution rule, unresolved ambiguity, and any sensitivity implication.

## Specialized boundaries

For theoretical sources, extract definitions, premises, quantifiers, result statements, proof status, and applicable regimes. A numerical illustration is not a proof. For computational sources, retain algorithm version, dataset provenance, preprocessing, splits, metrics, baselines, tolerances, seeds, and resource conditions relevant to comparison. Separate claimed availability of code or data from verified availability.

Graph digitization, unit conversion, imputation, and effect-size conversion introduce assumptions. Obtain the user's intended treatment when the choice affects synthesis, use reproducible operations, and preserve the original representation. Never reconstruct missing variance as though it were reported. A contact request may be drafted, but sending it requires authorization for that external action.

## Quality control and deliverable

Use independent duplicate extraction or a second-person check when required by the review protocol. Otherwise perform targeted verification of fields capable of changing the conclusion, and describe the actual checking performed. Resolve disagreements against the source and codebook; keep a disagreement log for judgment calls.

Deliver the evidence table, codebook, provenance map, transformation log, and unresolved-data list in editable formats suited to the task. Confirm identifiers are unique at the declared unit, categories follow the codebook, units are consistent, and linked reports are not treated as independent studies. Route judgments about trustworthiness to [research appraisal](../research-appraisal/SKILL.md) and pooling decisions to [meta-analysis](../meta-analysis/SKILL.md). State which fields remain unverified and how their absence limits downstream use.
