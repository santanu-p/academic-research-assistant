---
name: mathematics-notation
description: Express mathematical arguments in consistent, readable LaTeX while preserving definitions, domains, dimensions, quantifiers, and the distinction between proof and illustration.
---

# Mathematics notation

Use this method to write, transcribe, normalize, or explain mathematics in a research document. Follow the [research contract](../../docs/RESEARCH-CONTRACT.md). Good notation exposes meaning; it cannot repair an invalid derivation by making it look formal.

## Establish the notation contract

Identify the audience, mathematical domain, document engine, existing conventions, and desired depth of explanation. Gather the relevant definitions and equations before changing symbols. Build a compact symbol ledger with meaning, domain, dimension or units, indexing, and first definition. Distinguish scalars, vectors, matrices, operators, sets, random variables, and estimates where the field does.

Preserve established author or field conventions unless inconsistency creates a real problem. If notation changes, provide an explicit mapping and update all dependent occurrences, captions, prose, and code-facing descriptions. Avoid reusing a symbol for unrelated quantities within the same argumentative context.

For transcriptions from handwriting or images, identify ambiguous subscripts, signs, delimiters, and Greek letters. Use context to propose a reading, but flag uncertainty instead of silently choosing a mathematically consequential interpretation. Do not fabricate steps absent from the supplied source.

## Typeset by mathematical function

Use inline mathematics for short expressions integrated into sentences and display mathematics for statements requiring visual focus or reference. Treat displayed equations as part of the grammar of the surrounding sentence. Define symbols before or close to first use. Label equations that are actually referenced, with stable descriptive keys rather than manually typed numbers.

Use alignment to reveal the logical structure of a derivation. For example:

~~~tex
\begin{align}
E(x) &= a x^2 + b x + c, \\
\frac{\mathrm{d}E}{\mathrm{d}x} &= 2 a x + b.
\end{align}
~~~

These expressions illustrate notation only; their scientific interpretation depends on supplied definitions. Distinguish equality, approximation, proportionality, definition, and implication. Do not replace one with another for visual uniformity.

Choose delimiters, fractions, and operator spacing for readability. Use recognized operator commands for functions and define recurring custom operators semantically when appropriate. State whether a symbol such as a derivative is total, partial, covariant, or functional. Keep differential conventions consistent and explain unusual conventions when they matter.

## Preserve the reasoning

For a derivation, state assumptions, domains, and regularity conditions needed for each consequential step. Check dimensions and indices, particularly in sums, tensors, transformations, and nondimensional variables. Distinguish free indices from dummy indices and maintain consistent ranges. Verify that a denominator can be nonzero and that a function is used within its defined domain.

For probability, specify conditioning, distributions, dependence assumptions, and what expectation or uncertainty means. For estimates, distinguish a parameter from its estimator and observed estimate. For theorem-style material, use definitions, claims, and proofs consistently. A numerical example, graphical observation, or symbolic simplification is not automatically a proof.

When shortening mathematics, retain steps that explain a non-obvious inference. When expanding it pedagogically, add intermediate steps that follow from the supplied assumptions, and mark any newly introduced assumption. Route unresolved formal questions to [mathematical modeling](../mathematical-modeling/SKILL.md) or [scientific reasoning](../scientific-reasoning/SKILL.md).

## Deliver and verify

Deliver editable TeX, a notation ledger when useful, and a list of ambiguities or substantive corrections. Explain changes that affect meaning separately from typography. Keep citation and equation-reference keys intact unless their update is explicitly managed.

Compile using the actual project environment when available. Check undefined commands, missing references, mismatched environments, and visible line overflow through [build repair](../tex-build-repair/SKILL.md). Inspect rendered equations for misplaced scripts, cramped delimiters, broken alignment, and detached conditions. Compare the typeset form with the intended expression symbol by symbol, then test at least one meaningful limiting case or dimensional consistency relation when mathematical correctness is in scope. Report what was checked and avoid claiming a verified proof from typography review alone.

