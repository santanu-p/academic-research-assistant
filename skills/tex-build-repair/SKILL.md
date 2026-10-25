---
name: tex-build-repair
description: Diagnose and repair LaTeX build failures and consequential warnings while preserving document meaning, project structure, and reproducible build instructions.
---

# TeX build repair

Use this method when a LaTeX project fails to compile, produces broken references, or has warnings that may affect the final artifact. Apply the [research contract](../../docs/RESEARCH-CONTRACT.md). Diagnose the actual project and available runtime before changing source or promising a successful PDF.

## Establish the build context

Identify the project root, intended main file, engine, bibliography workflow, required assets, class or template, and existing build instructions. Inspect the relevant source and the earliest meaningful error in a fresh log. If several main files are plausible, use supplied project instructions or obtain a selection rather than guessing which document matters.

Check which tools are available. A missing executable, unavailable package, absent image, malformed source, and stale auxiliary file are different failure categories. Preserve the source and existing artifacts before making consequential changes. Avoid deleting generated files indiscriminately when some may contain necessary indexes, externalized graphics, or evidence of the previous build.

Run the documented build through an available mechanism and record the result. Do not infer current success from an old PDF or a previously successful log. Keep paths and filenames exact, especially when working across operating systems or with spaces and non-ASCII characters.

## Diagnose and repair locally

For syntax errors, inspect the immediate context and matching braces, environments, math delimiters, and commands. The compiler may report a later location than the cause, so trace backward carefully. For undefined commands, determine whether the cause is a typo, missing definition, missing package, or incompatible engine. Do not add a large package merely to suppress an unexplained command error.

For missing files, verify the intended asset, relative path, case, extension, and generation step. Restore a correct reference to an available file when appropriate. Do not create a blank substitute image that makes a build succeed while silently removing scientific content.

For package conflicts, examine load order, options, and overlapping responsibilities. Prefer a small compatible change over replacing the document class or rebuilding the preamble without need. For engine-specific fonts or Unicode issues, retain intended characters and semantics while choosing a supported route. Explain any required environment change.

For bibliography problems, identify whether the project expects BibTeX, Biber, manual entries, or another supported workflow. Check citation keys, bibliography filenames, syntax, and build passes. Do not invent a reference to satisfy a missing key. If source metadata is incomplete, flag it for verification.

## Address warnings by consequence

Undefined references and citations require source or build-sequence attention. Overfull boxes require locating the actual line, equation, URL, or table; route layout changes through [TeX layout](../tex-layout/SKILL.md). Inspect underfull boxes before deciding whether they matter. Font substitution, missing glyphs, duplicate labels, and unavailable figures can change the output even when the compiler exits successfully.

Rebuild after each coherent repair and compare the new first error or warning state. Avoid chains of speculative edits that make it impossible to identify which change helped. If a repair changes an equation, citation, caption, or other scientific content, explain that change separately and verify its intended meaning.

Stop repeated retries when the same missing environment dependency prevents progress. Preserve the project and provide an exact diagnosis, required dependency, and unexecuted next step rather than reporting an imagined successful build.

## Deliver and verify

Deliver the repaired source, fresh build output when available, concise change summary, actual build method, and remaining diagnostics. Use relative paths where the project should be portable. Do not claim that compilation establishes scientific correctness.

Inspect the fresh PDF, especially changed pages, equations, references, figures, and page boundaries. For a final document request, use [document production](../document-production/SKILL.md) to inspect all pages and package essential sources. Confirm that the expected document was built and that missing content was not hidden by fallback placeholders. Report separately whether the project compiled, whether warnings remain, and whether visual inspection was performed.

