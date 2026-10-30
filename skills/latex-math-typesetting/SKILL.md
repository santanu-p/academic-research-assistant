---
name: latex-math-typesetting
description: Use when writing or revising mathematical equations, theorem environments, and proofs in a LaTeX document.
---

# Mathematical typesetting

Begin by inspecting the surrounding notation, theorem conventions, document class, and existing math packages. Preserve the author's mathematical meaning, labels, numbering, and definitions. Ask for missing mathematical content when a transcription is ambiguous; distinguish a proposed correction from a proven result.

Use the existing math setup for display equations. Use aligned environments for relations that belong together, and separate distinct assertions when separate numbering helps references. Align at meaningful relations, supply punctuation as part of the sentence, and choose delimiters for legibility rather than relying on automatic sizing everywhere. Use text in math for words and established operator commands for operators. Do not silently change symbols, assumptions, domains, units, or indices to make a formula fit.

For long expressions, break at mathematically sensible operators and inspect continuation lines. Retain equation labels when moving environments and check all references. When introducing a package or macro, check for existing definitions and class compatibility. For symbol conversion from a scan, compare each ambiguous glyph and report uncertainty rather than guessing.

## Scientific notation and specialist diagrams

Identify the quantity, numerical value, unit, uncertainty and field convention before choosing notation. When the project supports [siunitx](https://ctan.org/pkg/siunitx), its version 3 commands can consistently format a number and its unit, for example `\qty{2.5}{\milli\second}`. This fragment demonstrates formatting only; it is not a measurement. Check the installed package version, journal style and any existing configuration before replacing older syntax. Preserve reported precision and uncertainty, and verify any unit conversion separately; formatted units do not establish dimensional correctness.

For molecular formulas and reactions, [mhchem](https://ctan.org/pkg/mhchem) can format chemical notation; for example, `\ce{CaCO3 -> CaO + CO2}` represents a balanced illustrative equation when the package is loaded. Check atom counts, charge, reaction arrow, states and conditions against the user's source; a syntactically valid equation does not establish that a reaction occurred. Chemical structure diagrams need connectivity, bonds, charge and stereochemistry beyond a molecular formula. Where appropriate, consider [chemfig](https://ctan.org/pkg/chemfig) and inspect the resulting structure with a qualified domain reader.

For quantum notation, [braket](https://ctan.org/pkg/braket) provides bra, ket and inner-product commands; a fragment such as `\braket{\phi|\psi}` denotes an inner product only under the surrounding document's definitions. Preserve the order, normalization and operator placement supplied by the author. For electrical networks, [circuitikz](https://ctan.org/pkg/circuitikz) supplies circuit drawing tools; check connections, component values, polarity and convention against the supplied circuit, not just visual appearance. Route layout and rendering to [TikZ diagrams](../latex-tikz-diagrams/SKILL.md).

These are package options, not bundled runtimes or verified builds. Check package availability, engine and class compatibility, and the installed documentation before use. Compile the actual project and inspect the resulting symbols and diagrams; if a dependency, scientific check or final rendering is unavailable, report it explicitly.

## Theorems and proofs

Inspect the document class and existing definitions before adding theorem machinery: a class may already provide it. Establish which statements need numbered environments, whether theorem, lemma and proposition share a counter, and whether numbering resets within a section or chapter. Preserve established numbering and references when editing an existing document. Use an unnumbered environment only when numbering and cross-references are not required.

When the class permits `amsthm`, define environments in the preamble with `\newtheorem`; use its shared-counter or within-counter form to implement the chosen numbering scheme. Choose styles for statement, definition and remark text according to the venue, and avoid redefining an existing environment. Place a unique label immediately after the numbered environment begins, then use the project's reference conventions; verify the displayed numbers and hyperlinks after the needed compilation passes. Check package order and compatibility with the class and any reference packages rather than introducing duplicates.

Use the existing proof environment for proof text, and check that the end-of-proof symbol appears at the intended end, especially when the proof ends with a display; `\qedhere` may be appropriate within the final display when supported. Keep assumptions, quantifiers, hypotheses and conclusions intact. Do not invent a proof or silently correct a mathematical claim: identify missing steps or suspected errors and distinguish mathematical review from typesetting.

Build the actual main document with its existing engine and bibliography workflow when a source edit is requested. Examine the log for errors, unresolved references and overfull boxes, then render and inspect each affected page at readable scale, including neighboring text and equation breaks. If compilation or rendering is unavailable, report the unverified boundary and preserve the source.
