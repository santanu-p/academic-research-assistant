---
name: latex-build-debugging
description: Use when a LaTeX project fails to compile, has build warnings, or produces incorrect references.
---

# LaTeX build debugging

Identify the intended root document, engine, build tool, output directory and bibliography backend from project configuration or existing scripts. Inspect the first meaningful error in a fresh build log and the source context it identifies; later errors may be consequences. Preserve the original sources and avoid deleting user files or changing project-wide configuration without a reason.

Reproduce the failure with the project's established command. Check missing inputs, package availability, encoding, engine-specific commands and mismatched environments in that order as evidence suggests. Make the smallest correction that explains the failure; do not suppress diagnostics or install a large toolchain merely to mask an error. If a dependency or external operation is unavailable, report it and the command needed rather than asserting success.

For unresolved references, run the appropriate bibliography and engine passes, and check keys, labels and duplicate definitions. Address overfull boxes where they materially affect output; distinguish harmless informational warnings from unresolved, user-visible issues. A build that exits zero may still contain missing glyphs, citations or assets.

Run a fresh complete build after the final source change. Confirm the PDF corresponds to that build, inspect logs and render affected pages to check the actual result. For a full document deliverable inspect every page. Record the commands and remaining limitations, including any missing visual or bibliography verification.
