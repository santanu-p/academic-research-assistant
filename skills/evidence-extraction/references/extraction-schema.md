# Extraction schema

Choose only fields that serve the research question. Separate linked entities instead of repeating a mixture of publication, participant, and outcome attributes in one ambiguous row.

## Minimal linked tables

**Reports:** report_id; citation; persistent_identifier; version; source_file; access_date; related_report_ids; study_id; linkage_evidence.

**Studies or cases:** study_id; design; context; sampling_or_selection; eligibility; materials_or_participants; procedure; relevant_dates; overlap_with_other_studies; protocol_or_registration; study_notes.

**Evidence items:** item_id; study_id; report_id; item_type; research_target; reported_content; source_locator; extraction_status; extractor; extraction_date; codebook_version; unresolved_issue.

An evidence item may be an effect estimate, a participant account, an author interpretation, a theorem, or an algorithmic comparison. Store its type explicitly. If several documents support the same item, use a related provenance table or multiple locators rather than inventing independent items.

## Conditional fields

For quantitative items: outcome_definition; contrast; time_point; population_analyzed; estimate_type; estimate; lower_limit; upper_limit; interval_level; standard_error_or_variance; denominator; unit; direction; adjustment_set; dependence_group. Record reported and derived values in separate fields.

For qualitative items: source_voice; context; verbatim_excerpt_or_location; author_finding; extractor_interpretation; analytic_approach; related_or_contrary_items. A participant excerpt and an author's analytic finding are different evidence types.

For theoretical items: definitions; assumptions; result_statement; quantifiers; proof_status; applicability_domain; counterexample_or_limiting_case. For computational items: algorithm_version; dataset_version; split; preprocessing; baseline; metric_definition; resource_conditions; numerical_tolerance; uncertainty; artifact_availability.

## Codebook and transformation record

For every field record its definition, type, allowed values, unit, missingness codes, and decision rule. Avoid using a blank to mean several different things. Keep a transformation table with item_id, original_value, operation, inputs, formula_or_code_location, assumptions, derived_value, and check_status.

When resolving a disagreement, record the disputed field, competing readings, source location, decision, reason, and remaining uncertainty. Correction of an extraction value should preserve its history when it can change the synthesis. The schema documents evidence; it does not certify that evidence as valid or independent.
