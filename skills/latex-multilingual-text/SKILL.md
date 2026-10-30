---
name: latex-multilingual-text
description: Use when setting up multilingual or non-Latin text, fonts, directionality, or script-specific typography in a LaTeX project.
---

# Multilingual LaTeX text

Determine the languages and scripts, text direction, required transliteration, supplied fonts, document class and current compiler. Inspect the project before changing engine or language packages. A font available on one machine may not exist on another; distinguish bundled, system and publisher-provided fonts, and respect their actual licenses.

Choose a compatible engine, language setup and font strategy for the scripts and template. Do not assume one package works with every engine or writing system. Check the actual package documentation for language tags, hyphenation, shaping, bidirectional text, numerals, punctuation and mixed-script runs. Preserve existing mathematical notation, references and author-supplied spelling; do not silently translate or normalize names.

## Select a script-aware configuration

Begin with the template's required engine and already loaded language packages. For projects restricted to pdfLaTeX, verify that the installed encodings, fonts and language support cover the actual characters and hyphenation; do not add `fontspec`, which requires XeLaTeX or LuaLaTeX. For Unicode text and system OpenType fonts, a compatible XeLaTeX or LuaLaTeX project can use [fontspec](https://ctan.org/pkg/fontspec). Select fonts that actually contain the required glyphs and shaping features; a successful font lookup alone is not proof that complex text is shaped correctly.

Use one language-management approach supported by the template. [Babel](https://ctan.org/pkg/babel) supports several engines and many locales with varying coverage; [polyglossia](https://ctan.org/pkg/polyglossia) is an alternative for XeLaTeX and LuaLaTeX. Consult the installed version's language documentation to choose language identifiers, main and secondary languages, script settings and hyphenation resources. Do not load both managers by default or switch an existing project merely to match a generic recipe.

For Arabic-script or Hebrew passages, check the chosen language system's bidirectional support and the font's shaping in the intended engine. Examine mixed left-to-right and right-to-left text, citations, punctuation, numbers and mathematical expressions in the actual output. For Indic scripts such as Devanagari, select an OpenType font with the necessary script support and verify conjunct shaping and reordering for the chosen language and engine. A font with visible individual characters can still render combinations incorrectly.

For Chinese, consider the [CTeX](https://ctan.org/pkg/ctex) classes or package when compatible with the project; they support several engines and provide Chinese-specific setup. For a XeLaTeX project requiring CJK text, [xeCJK](https://ctan.org/pkg/xecjk) offers separate CJK font configuration and punctuation handling. For Japanese under LuaLaTeX, [LuaTeX-ja](https://ctan.org/pkg/luatexja) is a relevant specialist option. Match the language, engine, class and font requirements to their documentation; do not assume that the same CJK configuration or font is suitable for all languages. For Korean, evaluate the project's language-specific support and fonts against actual Hangul and any Hanja requirements.

Before implementing a choice, record the exact engine, distribution and package versions, font names and availability, template restrictions, and whether the selected language resources are installed. Use a minimal project-specific specimen as a test, then integrate into the full project without changing its bibliography or layout system unnecessarily. These choices are starting points, not guarantees of linguistic correctness or accessibility; a fluent reader and destination-specific accessibility checks may be needed.

Create a small representative build that includes each script, accented text, punctuation, quotations, numbers, inline mathematics, a citation and a cross-reference. Where right-to-left text is involved, inspect mixed-direction segments and ordering of numbers and mathematical symbols. Flag unsupported glyphs or ambiguous script rendering rather than substituting plausible-looking text.

Build with the chosen engine and all necessary reference passes. Read the log for missing fonts, glyphs, language resources and shaping errors, then inspect the rendered pages at readable scale. Compare names and specialized terms against the supplied text. Record exact engine, font dependencies and any portability limitations. If the required fonts or compiler are unavailable, provide the editable source and missing prerequisites without claiming successful rendering or linguistic review.
