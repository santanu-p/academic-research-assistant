---
name: scientific-reasoning
description: Examine scientific arguments, hypotheses, mechanisms, and alternative explanations across empirical, qualitative, theoretical, and computational research.
---

# Scientific reasoning

Use this method to turn a research question or uncertain argument into explicit premises, testable implications, and bounded conclusions. Follow the [research contract](../../docs/RESEARCH-CONTRACT.md). The output is a defensible reasoning structure; it is not a substitute for conducting an experiment, proving a theorem, or validating a numerical implementation.

## Identify the inference being requested

Ask what decision the reasoning should support and what evidence exists. Restate the question narrowly enough that competing answers would imply different observations or arguments. Separate definitions, assumptions, observations, intermediate inferences, and conclusions. Record the level of analysis: individual, group, institution, physical system, or mathematical object. Check that the conclusion does not silently move between these levels.

Construct an argument map in a small table or connected prose: premise; justification; inference rule or mechanism; predicted consequence; and vulnerability. Distinguish a mechanism that could explain a result from evidence that the mechanism actually operated. If necessary information is missing, reason conditionally and make the condition visible.

## Develop and compare explanations

Write the leading explanation and at least one plausible alternative when the question admits alternatives. Alternatives should be concrete enough to change a measurement, prediction, coding decision, or derivation. Consider confounding, selection, measurement error, boundary effects, reverse direction, and artifacts when relevant, without producing an indiscriminate checklist.

For empirical work, define the population, intervention or exposure, comparator, outcome, and time relation appropriate to the question. Identify which parts of the argument concern causal effects and which concern description or prediction. Explain how the design limits the conclusion. Do not treat adjustment for measured variables as automatic removal of all confounding.

For qualitative work, distinguish participants' accounts, observed practice, analytic categories, and the researcher's interpretation. Examine context and positionality. Seek disconfirming cases or plausible alternative readings of the supplied material. Do not force qualitative evidence into invented frequencies or claim that thematic saturation was demonstrated when its basis is unavailable.

For theory, unpack definitions and quantifiers, check whether an implication is reversible, and test limiting or counterexample cases. Trace each conclusion to an assumption or established result. A suggestive calculation remains a heuristic until its required steps are supplied. For computational research, distinguish the modeled system, mathematical formulation, discretization, algorithm, implementation, and reported outputs. An output can be internally consistent while representing the wrong physical or conceptual model.

## Convert reasoning into discriminating work

For each live explanation, state what result would increase confidence, what would weaken it, and what would remain ambiguous. Favor checks that distinguish explanations rather than repeatedly confirming what all explanations predict. Include practical limits such as feasible sample size, instrumentation, data access, or computable parameter ranges when these are known.

Identify the weakest inference in the argument and propose the smallest useful investigation of it. Route formal model construction to [mathematical modeling](../mathematical-modeling/SKILL.md), and evidence or implementation checks to [research validation](../research-validation/SKILL.md). Do not recommend new data collection without describing what inference the additional data would change.

Express uncertainty in a form justified by available information: a quantitative interval when computed appropriately, a sensitivity range when assumptions vary, or a qualitative assessment tied to stated evidence. Avoid assigning arbitrary confidence percentages to make the reasoning look precise.

## Deliver and verify

Deliver the question, argument map, leading and alternative explanations, discriminating tests, and a conclusion with its conditions. State whether each proposed next step is a calculation, literature check, design change, data analysis, or interpretation task.

Verify that every inference uses the evidence level claimed, all crucial assumptions are visible, and the proposed test could actually distinguish the relevant explanations. Check for circular definitions, equivocation, post hoc explanation presented as prediction, and unexplained leaps from plausibility to proof. Preserve unresolved disagreement where evidence cannot adjudicate it. A useful outcome can be a sharper question or a clearly located gap rather than a positive scientific claim.

