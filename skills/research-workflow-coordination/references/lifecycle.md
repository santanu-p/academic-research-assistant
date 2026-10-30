# Research lifecycle coordination

For an optional read-only consistency check of recorded phases, dependencies and file hashes, see the [checkpoint checker](checkpoint-checker.md). It does not execute work or validate research claims.

Use this guide when a request spans stages or requires a resumable project record. Choose only applicable stages; research is iterative and results can require a return to an earlier decision. The listed records can be sections of existing documents rather than separate files. Adapt methods and checks to the discipline, study design, and user's scope.

| Stage | Useful concrete output | Decision or check before dependent work |
| --- | --- | --- |
| Frame | Research question, scope, intended audience, constraints, and success criteria | Is the question answerable with the available resources? Mark assumptions requiring a decision. |
| Locate and assess evidence | Search record with sources, dates, queries and selection criteria; source list or evidence table with links and limitations | Can the claims be traced to the actual sources? Record gaps, conflicting evidence, and searches not performed. |
| Design | Protocol or methods plan identifying data, variables, procedures, comparison, analysis, and limitations | Are data access, permissions, ethics review, and feasibility resolved where applicable? A proposed method is not an executed one. |
| Prepare and collect | Data inventory, collection log, codebook, and versioned raw inputs or authorized pointers | Are inputs accessible, suitable, and permitted for the intended use? Preserve raw data; document transformations and missingness. |
| Analyze and validate | Reproducible analysis, output tables or figures, run details, checks, and deviations | Do outputs follow from identified inputs and methods? Record failed checks, uncertainty, and sensitivity or limitations relevant to the claim. |
| Interpret and write | Claim-to-evidence links, manuscript or requested communication, citations and limitations | Does each material claim match its evidence and uncertainty? Distinguish observed results, interpretation, and proposals. |
| Review and deliver | Review issues and resolutions, final editable artifacts and requested exports, with checks performed | Are deliverables complete and validated for their intended use? Keep submission, sharing, and publication distinct from preparing a draft and perform them only when authorized. |
| Maintain or extend | Versioned revisions, correction log, archived supporting materials, or follow-on plan | Preserve the prior record and identify which results, decisions, and artifacts changed. |

When a gate is unmet, continue independent authorized work and label dependent outputs as blocked or provisional. Never treat a missing source, review, run, approval, or submission as completed. Record exact conditions for resuming and distinguish an actual external action from a proposed one. If sensitive data cannot be copied into a handoff, record an authorized location and access conditions without exposing the data.

## Resumable phase states and checkpoints

This is guidance for a person or assistant maintaining a project record. It does not implement a runner or automatic recovery. The optional checkpoint checker can derive a review status from recorded dependencies and file hashes, but does not change the recorded state. Use this guide only where the project needs continuity; a small task may use a short note instead.

For each applicable phase record its dependencies and one current state:

| State | Meaning and next transition |
| --- | --- |
| Pending | Work has not started; begin when required inputs and authorization are available. |
| Active | Work is underway; record progress without presenting unfinished outputs as complete. |
| Blocked | A named dependency or decision prevents progress; resume only when that condition is resolved. Independent authorized work may continue. |
| Needs recheck | An input, assumption, method, or upstream output changed, or the checkpoint cannot be verified. Assess affected work before relying on it. |
| Completed | The phase's defined outputs and acceptance checks have been recorded and met for the identified inputs. Completion does not establish validity beyond those checks. |
| Stopped | Work ended without meeting the phase criteria. Record the reason and the decision required to continue, change scope, or close the work. |

At each material handoff or interruption, save a checkpoint containing the phase and state; goal and scope; identifiable input and output versions or hashes where practical; dependencies; checks and their actual results; unresolved issues; decisions and authorizations; attempts and limits; and the next authorized action. Link to supporting evidence and logs rather than inferring success from a file's existence. Record the time or revision of the checkpoint and protect sensitive locations and material.

On resumption, inspect the latest checkpoint and the referenced artifacts. Confirm that inputs, scope, authorization, and acceptance evidence still apply. Resume unfinished work only after checking its prerequisites; retain completed work when its inputs and evidence remain valid. If the record is missing, ambiguous, or inconsistent with the artifacts, mark the affected phases as needing recheck, reconstruct what can be evidenced, and record unknowns. Do not assume a phase passed merely because an output exists.

## Changes, retries, and failure handoffs

When a material input or decision changes, identify affected downstream claims, computations, checks, and deliverables. Mark their phases as needing recheck and retain the earlier record for provenance. Reuse unaffected work only after confirming its dependencies; perform the relevant checks again before marking affected work complete. A changed scope or authorization can also restrict what may be resumed.

Set a proportionate retry or resource limit before repeating a phase, and record each attempt, what changed, and the observed outcome. Retry when a specific recoverable cause or new evidence justifies it; repeated unchanged failures are not progress. When the limit is reached, stop that branch and record the unresolved issue, available evidence, and a decision or new condition needed to proceed. A retry limit is a resource boundary, not a scientific success criterion.

For a failed check, preserve the failure evidence and hand off the affected claim or artifact, its version, inputs, attempted checks, observed failure, impact on downstream work, and a concrete next investigation. Return to an earlier phase when its assumptions, design, or implementation need repair; use a blocked state when access, evidence, or a decision is missing. After repair, rerun the relevant checks and update dependent phases. Distinguish a failed scientific check from an unavailable tool or an unexecuted check.

## A compact resume record

Keep this alongside the project only when continuity is useful. Link to existing artifacts instead of copying evidence, and update it after material changes:

- **Goal and scope:** requested outcome, current stage, relevant constraints and any explicit authorization.
- **Artifacts and evidence:** paths or stable links, versions or dates, source and data provenance, and the checks actually performed. Preserve raw inputs, analysis, decisions and correspondence where available and permitted; distinguish unavailable records from records that were not checked.
- **State:** completed work and observed results; preliminary work and its uncertainties; outstanding tasks and dependencies.
- **Decisions and blockers:** decision made or needed, who can decide if known, why it matters, and the specific missing input, access, tool or condition.
- **Next action:** a concrete authorized step and acceptance check; for external actions include their actual status, not an assumed completion.

## Worked continuity check

A researcher asks for a report comparing two measurement methods. A local dataset and a draft are available; the calibration notes are missing. Inventory and identify the dataset and draft versions, document the question and intended comparison, and inspect the data and draft within the authorized scope. Prepare a methods plan and a table of the measurements and limitations that can be supported. Mark calibration-dependent accuracy claims as blocked or provisional, with the missing notes as the unblock condition. Record the actual files inspected, any computations and checks run, and the next step: obtain or locate calibration information, then reassess the comparison. A draft or planned analysis alone does not establish a validated comparison. If notes become available later, update the record and rerun affected checks before promoting the claim.
