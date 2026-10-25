---
name: adversarial-revision
description: Critically review and revise research artifacts through bounded, evidence-linked challenge, repair, and rechecking without treating iteration counts as success.
---

# Adversarial revision

Use this method when an argument, manuscript, analysis plan, or research artifact needs a deliberate challenge before release. Follow the [research contract](../../docs/RESEARCH-CONTRACT.md). The purpose is to discover consequential weaknesses and repair them, not to manufacture disagreement or promise that repeated review establishes correctness.

## Define the review boundary

Identify the artifact version, intended audience, central claim, available evidence, and authorized types of change. Determine whether the task concerns scientific validity, argument structure, reporting completeness, language, or artifact reliability. Protect data, quotations, equations, source attribution, contribution statements, and known limitations from cosmetic changes that alter their meaning.

Read the artifact before choosing review lenses. Build a claim-to-evidence map for the central claims. A reviewer who lacks a dataset or cited paper should identify that limitation and formulate a check; they must not invent what inspection would reveal. Decide what would count as a materially improved artifact: corrected reasoning, supported scope, reproducible methods, clearer uncertainty, or repaired presentation.

## Challenge the artifact constructively

Review scientific substance first. Identify the strongest claim that a skeptical reader could reasonably dispute. Trace it to its assumptions and supporting evidence. Seek a counterexample, alternative explanation, missing comparison, boundary case, or mismatch between evidence and wording. Rank findings by likely effect on the conclusion, not by how easy they are to edit.

For empirical work, challenge design, selection, measures, dependence, causal language, and analytical choices relevant to the supplied evidence. For qualitative work, challenge how interpretations are grounded, how context and researcher positioning enter the analysis, and whether contrary material is addressed. For theory, examine definitions, quantifiers, hidden assumptions, nontrivial proof steps, and the applicable domains of external results. For computational work, distinguish conceptual model, numerical method, implementation, and scientific interpretation; ask whether validation checks address each vulnerable link.

Then examine communication: does the abstract outrun the results, does a figure imply unsupported certainty, or does a compressed method omit a necessary decision? Avoid inventing flaws merely to produce a long review. A stylistic preference should be labeled as such and should not displace a scientific issue.

## Repair through a bounded loop

Create a finding ledger with location, issue, evidence, consequence, proposed remedy, and verification needed. For each accepted finding, choose the smallest change that actually addresses it. A missing experiment may require narrowing the claim, not adding confident language. A valid disagreement may require an explanation of assumptions rather than a rewrite.

After repair, recheck the changed passage and its dependent locations, such as abstract, conclusion, caption, table, or equation reference. Record whether the finding is resolved, partly resolved, disputed with reasons, or awaiting evidence. Preserve legitimate unresolved concerns. Stop when the review scope and agreed checks are satisfied, when further progress needs unavailable evidence, or when a resource bound is reached. Report which stopping condition applied. A number of rounds or a favorable reviewer tone is not an acceptance criterion.

The optional [revision helper](../../tools/revise.py) may organize a bounded review workflow if its available interface and provider configuration are inspected. The method does not require a particular paid service or command-line tool. Never transmit private research to a provider without the user's applicable authorization.

The runner takes a manuscript path, two `--reviewer` JSON commands, one `--reviser` JSON command, and `--out` pointing to a new run directory. Optional inputs include `--source`, `--rounds`, `--timeout`, and `--check`. Inspect its help for command encoding. Default preflight performs no subprocess or provider calls and creates no run directory; execution requires `--execute`. Configured commands receive prompts on standard input. Reviewers return a decision of `accept`, `revise`, or `stop` with located issues; an acceptance cannot retain major issues. A reviser reports changes and unresolved issues. For an executed run, exit zero requires both acceptances and successful configured checks; a successful preflight also returns zero without executing any review. Exhaustion, scientific stop, and operational failure remain distinct outcomes. None of these states independently certifies scientific truth.

## Deliver and verify

Return the revised artifact, prioritized finding ledger, meaningful changes, and outstanding evidence needs. Separate scientific repairs from editorial preferences. Route specialized work through [research validation](../research-validation/SKILL.md) or [academic editing](../academic-editing/SKILL.md) when useful.

Compare the final version with the original evidence map. Confirm that repairs have not invented findings, erased uncertainty, displaced attribution, or silently altered numerical results. Check that each claimed resolution has a specific reason or test outcome. Explain the remaining limits of the review, including inaccessible sources and unexecuted analyses. A successful review makes the artifact more defensible within its actual evidence; it does not certify novelty, truth, or publication acceptance.

