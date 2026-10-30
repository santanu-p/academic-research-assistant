---
name: systematic-review
description: Plan and conduct protocol-driven evidence reviews with explicit eligibility, reproducible searching, study linkage, screening records, appraisal, and transparent synthesis.
---

# Systematic review

Use this Academic Research Assistant skill when evidence selection must be explicit, reproducible, and auditable. Follow the [research contract](../../docs/RESEARCH-CONTRACT.md). Choose the review type deliberately: an effect review, qualitative evidence synthesis, diagnostic review, methodological review, and scoping review answer different questions. A scoping review is not simply an effect review with the appraisal step omitted.

## Inputs and protocol

Obtain the review question, intended use, disciplinary scope, team capacity, time, access, and any required reporting or registration guidance. Establish inclusion criteria for populations or materials, concepts, settings, designs, outcomes where appropriate, dates, languages, and publication types. Justify restrictions and explain the likely coverage loss.

Write a protocol before screening at scale. Specify discovery sources, search strategy, deduplication, screening stages, reviewer roles, disagreement resolution, extraction fields, appraisal approach, synthesis plan, and amendment handling. Verify current requirements if registration or a reporting guideline is requested. Drafting a registry entry does not mean it was submitted or accepted.

## Execute the review

1. Run the documented search through [literature search](../literature-search/SKILL.md). Preserve exact queries, search dates, filters, counts, and exported records. Include supplemental discovery methods where justified by the subject and log their contribution.
2. Deduplicate records while retaining provenance. Link multiple reports of the same underlying study. Distinguish the counts of records, reports, and studies throughout the review.
3. Pilot eligibility criteria on varied examples. Clarify ambiguous criteria before broad screening and record protocol changes. During screening retain include, exclude, and uncertain decisions rather than forcing uncertainty into an exclusion.
4. Perform title/abstract screening and full-text assessment according to the protocol. Record a primary full-text exclusion reason that reflects an actual criterion. Track inaccessible reports separately from excluded studies.
5. Use independent reviewers when required by the protocol or methodological standard. If only one reviewer or one assistant performed a task, state that fact and its implications; do not invent independence, consensus, or inter-reviewer agreement.
6. Extract evidence with a piloted codebook through [evidence extraction](../evidence-extraction/SKILL.md). Record study/report relationships, outcome definitions, time points, and values capable of affecting the synthesis.
7. Appraise evidence with criteria suited to each design through [research appraisal](../research-appraisal/SKILL.md). Decide prospectively how judgments affect synthesis and sensitivity analyses. Avoid turning unrelated quality domains into an unexplained total score.
8. Synthesize according to the question and compatibility of evidence. Use [meta-analysis](../meta-analysis/SKILL.md) only when pooling has a defensible interpretation. A structured narrative synthesis should explain patterns, uncertainty, dependence, and differences in methods; it should not count significant studies as votes.

## Screening and flow accounting in practice

Set up a record ledger before importing search results. Give each imported record a stable identifier and retain its source, search date, export batch, and available bibliographic fields. Preserve the original exports and record how duplicate candidates were identified and resolved; ambiguous matches need review rather than automatic merging. Keep a mapping from each imported record to its retained record so counts can be reconciled. A report is a publication or other document; a study may have several reports. Maintain separate identifiers and links for records, reports, and studies, and do not infer study identity from similar titles alone.

Pilot the eligibility rules on a small varied set and compare decisions to identify unclear wording. Record the clarification and its effective date; revisit earlier decisions when a change could affect them. For each screening stage retain reviewer identity, decision, and date. If independent screening is planned, preserve each initial decision before reconciliation, document the resolution method and final decision, and keep uncertain cases visible until resolved. If only one person screens, describe that limitation rather than implying independent review.

Track full-text retrieval separately from eligibility. Record reports sought, obtained, unavailable, awaiting retrieval, and assessed, without assigning an eligibility exclusion to an unseen report. For an assessed report that fails eligibility, record one reproducible primary reason tied to the prespecified criteria; preserve additional reasons if useful without counting the report multiple times in a primary-reason total. Link multiple reports to their study before counting included studies, and check whether an apparently excluded report belongs to an otherwise included study.

Reconcile each stage using the actual ledger and explicitly defined units: imported records equal removed duplicates plus records retained; screened records equal excluded records plus records advanced plus unresolved records; reports sought equal obtained, unavailable, and still pending reports; and assessed reports equal excluded, included, and unresolved reports, provided those statuses are mutually exclusive. Account separately for records identified by supplemental methods and for review updates so they are not counted twice. Explain any change of unit between stages and report pending items rather than forcing a balanced completed flow. Retain the search date and the version of the ledger used to generate the flow. These checks establish arithmetic consistency, not the correctness or completeness of the search or decisions.

## Boundaries across evidence types

For quantitative reviews, define effect measures, unit-of-analysis issues, missing information, subgroup hypotheses, and handling of multiple eligible outcomes. For qualitative synthesis, specify an interpretive or aggregative approach and preserve context, meaning, and researcher judgments. For theoretical or computational reviews, formulate reproducible eligibility around problem definitions, assumptions, algorithms, evaluation regimes, and artifact types. Do not force these works into intervention-study categories.

Assess confidence in the body of evidence using a framework appropriate to the review purpose when needed. Explain reasons for uncertainty, including bias, inconsistency, indirectness, imprecision, and missing evidence where relevant. Do not infer that a long checklist makes the conclusion certain.

## Select frameworks deliberately

Choose question elements for the type of evidence sought. For an intervention effect, PICO can help specify population, intervention, comparator, and outcome; for an exposure question, PECO may be a better fit. For mapping concepts across contexts, PCC can help frame a scoping question. These are aids to precise eligibility and searching, not compulsory fields for every discipline. Define terms operationally and adapt them when the research question does not fit; explain omissions or changes.

Choose a study-level appraisal method for the actual design and the specific result being assessed. For example, consider RoB 2 for randomized intervention results and ROBINS-I for eligible nonrandomized intervention studies, after checking the current instrument's scope, instructions, and expertise requirements. Other designs and questions need appropriate methods; do not mechanically apply an intervention tool to all studies or replace domain judgments with an unsupported total score. Document the version, reviewer process, evidence for each judgment, and unresolved information.

Distinguish a judgment about an individual study result from confidence in a body of evidence for a particular outcome and comparison. Where appropriate, consider GRADE for quantitative outcome-level certainty or GRADE-CERQual for confidence in qualitative review findings. Verify the current framework guidance, intended use, and any reporting requirements before application; record the evidence and rationale for each judgment, and mark assessments pending when the necessary information or expertise is unavailable. Do not imply a formal assessment was completed merely because a framework was named.

Use the editable [screening and flow worksheet](templates/screening-flow.md) to record the actual decisions and counts. It is a blank working aid, not a completed review or a substitute for the reporting guideline chosen for the project. For extraction fields and data dictionaries, use [evidence extraction tables](../evidence-extraction-tables/SKILL.md).

## Deliverable and verification

Deliver the protocol and amendments, search log, screening decisions, study linkage, extraction codebook and dataset, appraisal records, synthesis, and a flow accounting. Reconcile counts with actual logs; do not invent numbers to complete a diagram. Include the last search date and an update plan if the intended use requires currency.

Verify a sample of exclusions and conclusion-driving extraction values against sources, following the actual review team's agreed checks. Clearly state uncompleted stages and access limits. A protocol, a pilot search, or partially screened corpus should be labeled by that stage and must not be presented as a completed systematic review.
