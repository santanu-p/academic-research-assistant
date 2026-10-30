---
name: latex-custom-command-design
description: Use when designing, reviewing, or repairing reusable LaTeX commands, environments, counters, or semantic notation.
---

# Reusable LaTeX commands

Inspect the document's class, engine, preamble, local style files, existing command definitions and call sites before adding or changing a macro. Identify whether the request concerns notation, presentation, structure, or an environment; preserve the mathematical meaning and the project's existing conventions.

Prefer a clear semantic command for repeated concepts, with explicit arguments and a name unlikely to collide with a package or standard command. Check whether the existing definition already serves the purpose. Avoid redefining a built-in command merely to save characters, and do not change global spacing, catcodes, numbering, or document-wide formatting without a demonstrated reason and authorization.

For commands with optional arguments, nested content, fragile material, references or moving arguments, check the requirements of the actual engine and packages. Define defaults deliberately and document argument order. For an environment or counter, define scope, resets and interactions with labels before implementation. Keep private macros in a local style or preamble that the main file actually loads; avoid duplicate or circular inputs.

Use a minimal compile case that exercises ordinary arguments, an empty or optional argument where supported, nesting, and representative contexts such as a caption or heading. Test existing call sites as well. For math, compare symbols, indices, domains and spacing with the intended expressions; a successful compile does not prove mathematical correctness.

After integration, run the project's real build, inspect errors and material warnings, then render affected pages. Report changed definitions, required packages and any compatibility or verification limits. Preserve editable source and avoid presenting a proposed macro as tested if the engine was unavailable.
