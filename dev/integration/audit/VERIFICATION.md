# Verification results — 25 October 2026

This report separates implemented local functionality, verified preservation and optional untested research/services. Private account saving and desktop activation are distinct from these checks.

## Preservation and inventory

- 174 original files and 140 original directory entries independently inventoried from all five folders/four ZIPs.
- 138 ZIP members: 99 files and 39 directory entries, safely expanded and accounted for.
- All **273 original/expanded file SHA-256 hashes** and **179 directory entries** verified, with zero missing or mismatched files.
- All **117 source skills** integrated as distinct active skills plus **one unified router**. Active family counts: LaTeX33, guardrails2, evidence29, Scholar36, visuals1, ARMS13 and three standalone skills.
- All supplied text/code/configuration/CSV content read/parsed and binary resources inspected. The independent collection and ARMS audits cover the complete corpus. Full source mapping, inspection and adaptation receipts are included.

## Structure, definitions and references

The root manifest and MCP configuration were validated against the official [plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) and [MCP configuration schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json), fetched during this build and included under dev/schemas. Skill/frontmatter names are unique and match their directories; agent YAML, JSON/JSONL/YAML and Python syntax parse. Route destinations and actual local Markdown file targets resolve. See package-validation.json for exact current counts and results. Preserved nested manifests are provenance; one root plugin is packaged.

## Runtime tests

Actual subprocess checks cover initialization, five-tool discovery, task routing, contained/paginated resource reads, tool/protocol errors and clean EOF. The server performs read-only local lookup/integrity/presence checks without a shell, network or credential handler. Protocol error handling was reviewed against the official [MCP base protocol](https://modelcontextprotocol.io/specification/2025-11-25/basic) and [tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools).

Behavior tests cover lifecycle task routing, reachability of every source skill, overlapping capabilities, path escapes, source tampering/missing files and honest dependency status. Independent review caught and resolved broad namespace rewriting in ordinary prose and malformed-request handling. Final suite counts and release checks are recorded in the accompanying machine receipts.

Final combined command: `python -m unittest discover -s tests`, system Python 3.14, **33 tests run in 38.498 seconds: 32 passed, 1 skipped, zero failures**. The skip is the real PyMuPDF integration check; that library is absent. Runtime tests10, ARMS adapter tests6 and visual adapter tests17. The actual MCP smoke process successfully called all five tools, exited zero and emitted no stderr. `suite-results.json` and `mcp-smoke.json` record these receipts.

## Supplied helpers and representative workflows

- Original **and active** Humanizer package validator: PASS, v3.1.0.
- Supplied reference-selection CLI: PASS on uncertainty/interval query, returning actual bundled corpus records. This did not fetch the external source pages.
- Table QA CLI: PASS on the supplied source-weight CSV, with an expected ten-numeric-column density warning. This is structural table QA, not scientific verification.
- ARMS style-metrics CLI and small numerical method/comparator checks: PASS within the independent audit. Root separately ran deterministic NumPy/SciPy fit/predict/width invariants; the receipt clearly labels synthetic fixture values and does not claim a coverage experiment.
- Active ARMS Bash adapter tests use temporary Git repositories and **stub** model commands; no actual model loop ran. They check syntax/preflight, no outputs/models during preflight, explicit Git opt-in, clean-index protection and bounded snapshot paths. Git Bash cannot start inside the sandbox; approved reruns were required.
- Active visual helpers have regression tests for Windows/cache portability, disconnected unrelated Pareto families, grouped decimals, typing, PDF dependency/render/font limits and layout findings. Real PyMuPDF is unavailable, so its integration check is explicitly skipped; controlled-backend tests are not represented as a real PDF backend run.
- Three synthetic supplied-template figures were generated as SVG/PNG and visually inspected. Rendering exposed endpoint clipping and number/errorbar overlap; active fixes and rerenders are recorded before release. These are implementation demonstrations, not research findings.
- All 25 source PNGs were inspected as a labelled contact sheet. All seven source PDFs rendered: five presentation-guide pages and six one-page historical figures inspected. Historical source-layout issues remain documented; originals were not redesigned or falsely approved.

## Independent review

collection-audit.md/.json: full non-ARMS corpus, 32 findings and narrow active helper corrections. arms-audit.md/.json: entire ARMS snapshot, missing dependencies and safe execution limits. package-review.md: preservation, namespace fidelity, MCP handling and reconstruction review. Root reviewed and incorporated findings; per-file adapter hashes identify changes.

## Explicitly untested or unavailable

Full ARMS benchmark/scientific reproduction, current external scholarly searches, authenticated commercial databases/services, live Claude/Codex adversarial loop, absent private rubric/telemetry/helper implementations, full manuscript compilation with missing NeurIPS style, actual PPTX authoring/backend rendering, and real PyMuPDF font/render integration were not completed by package construction. Host skill activation and local server discovery after account installation require the setup checks. See docs/LIMITATIONS.md and docs/ARMS.md for exact technical reasons and labelled compatibility substitutions.

No integration is called connected merely because an endpoint/name appears in preserved text. No scientific result, novelty claim, source verification, installation or authenticated service state is fabricated.

## Reconstruction and release

A new empty workspace reconstructed the preserved input collection, built all117 source skills plus the router, and passed manifest/definition/reference/source-hash validation. The development snapshot includes all authored sources, tests, adapters, official schemas and clearly historical audit records. The final archive is separately inspected for one plugin root, safe entry paths, all118 active skill files, complete source directories and matching file hashes. The external account-save receipt is delivered beside the ZIP; it does not imply desktop activation.
