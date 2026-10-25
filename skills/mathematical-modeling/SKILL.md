---
name: mathematical-modeling
description: Build and analyze mathematical models with explicit assumptions, dimensions, boundary conditions, identifiability, and limits of interpretation.
---

# Mathematical modeling

Use this method when a research problem needs equations, a reduced model, an inference model, or analysis of an existing formulation. Start with the [research contract](../../docs/RESEARCH-CONTRACT.md). Keep model construction separate from implementation testing and agreement with observations; those checks belong to [research validation](../research-validation/SKILL.md).

## Specify the modeling purpose

Identify the system, question, intended prediction or explanation, audience, and acceptable approximation. A model built to interpolate measurements may need different structure from one used to infer a mechanism or extrapolate to a new regime. State the target outputs, relevant scales, known inputs, unknown parameters, and available observations.

Create a symbol inventory before a long derivation: name, meaning, domain, dimension, convention, and whether each quantity is observed, controlled, estimated, or latent. Clarify coordinate, normalization, sign, indexing, and stochastic conventions. Distinguish dimensional quantities from nondimensional ones. When a convention is supplied by the researcher, retain it unless changing it is necessary and explicitly documented.

## Construct the formulation

Begin with the smallest structure capable of answering the question. State assumptions as claims that can later be relaxed or tested. Derive governing relations from the relevant balance, symmetry, constitutive, probabilistic, or optimization principles. Explain phenomenological terms as modeling choices rather than deductions. Identify closure assumptions and what information they discard.

For differential equations, specify domain, initial conditions, boundary conditions, regularity assumptions, and admissible solution class. Check that conditions match equation order and physical constraints. For stochastic models, define the random quantities, conditioning, dependence assumptions, noise interpretation, and likelihood or estimating equations. For optimization, define the feasible set, objective, constraints, and treatment of multiple solutions.

For empirical parameter models, distinguish structural parameters from tuning choices and nuisance parameters. Ask whether distinct parameter values could generate indistinguishable outputs over the available observations. For qualitative or conceptual research, use a formal model only when its variables and relations have a defensible interpretation; do not manufacture numbers for concepts that were not measured.

## Analyze before adding complexity

Check dimensions term by term and recover known limits. Examine positivity, conservation, monotonicity, symmetries, and boundedness where the model should possess them. Explore zero-input, large-scale, small-scale, and degenerate cases that have a clear interpretation. A failed limit may reveal an error or define a genuine regime boundary; document which.

Where feasible, analyze existence, uniqueness, stability, equilibrium structure, and parameter sensitivity. State whether a result is proved, numerically observed, or conjectured. Show essential derivation steps and cite external mathematical results actually used. Avoid presenting a symbolic solver's output as a proof without checking its domain conditions.

Choose nondimensional variables to reveal scale ratios and approximation regimes. Compare reduced and fuller formulations in the same conventions. If numerical solution is required, state the proposed discretization or algorithm, expected failure modes, and observables needed to assess convergence. Do not report numerical accuracy before carrying out those checks.

## Deliver and verify

Deliver a model specification containing equations, symbol inventory, assumptions, conditions, derivation, parameter interpretation, anticipated limitations, and the next validation steps. Provide executable expressions or code only when requested or useful, with sufficient conventions to reproduce them. Use [mathematics notation](../mathematics-notation/SKILL.md) to prepare readable TeX.

Re-derive at least one central relation independently or check it through a limiting case, dimensional argument, or equivalent formulation. Confirm that approximations are used only within their stated regime and that inferred parameters have not been conflated with directly measured quantities. List unresolved identifiability or well-posedness concerns explicitly. A model can be useful without being unique or universally accurate; the conclusion must explain the particular purpose for which its construction is defensible.

