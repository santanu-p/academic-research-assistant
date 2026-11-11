# Academic Research Assistant

A local collection of research workflows for students, scholars, scientists, and research teams. It brings together detailed methods for finding and evaluating evidence, planning research, writing and editing, scientific analysis, and preparing documents and presentations. A small CLI and optional MCP server help a compatible assistant find and read the relevant instructions; the assistant still needs the appropriate tools and sources to perform the work.

This **4.0.0 release** maps 118 reviewed source skills to 116 canonical methods and two compatibility entries. The complete supporting resources and source notices are retained. [Humanizer](skills/humanizer/SKILL.md) and [Academic Humanizer](skills/academic-humanizer/SKILL.md) remain separate: the latter is intended for scholarly prose where citations, technical meaning, and uncertainty must be preserved.

## Requirements and quick start

Use Node.js 22 or later. The CLI and navigation server use Node's built-in modules and require no npm dependency installation. Scientific scripts, document rendering, online sources, and external models may need additional software, credentials, or separate configuration; see [dependencies](docs/DEPENDENCIES.md).

From this folder, run the following in PowerShell (use `/` paths on Unix):

```powershell
node .\cli\ara.mjs doctor
node .\cli\ara.mjs list --json
node .\cli\ara.mjs route "Humanize my manuscript abstract while preserving citations and uncertainty"
node .\cli\ara.mjs read skills/academic-humanizer/SKILL.md
node .\cli\ara.mjs verify
```

Try a literature-review planning request, a research-gap question, or a request to edit a blog post in the author's own voice. Routing suggests instructions; it does not itself search a database, authenticate a service, run an experiment, or validate a research claim. The keyword router asks for clarification for some conflicting exclusions, but it cannot reliably interpret every negated instruction. Check suggestions against the complete request before using them, and use actual available tools and evidence.

## Installation and host compatibility

Export to a new directory; the CLI refuses to overwrite an existing target and does not change host settings. Use an absolute path appropriate for your machine. The export result prints the next steps.

```powershell
node .\cli\ara.mjs export --host codex --target "D:\ara-codex"
node .\cli\ara.mjs export --host claude --target "D:\ara-claude"
node .\cli\ara.mjs export --host antigravity --target "D:\ara-antigravity"
node .\cli\ara.mjs export --host generic --target "D:\ara-generic"
```

| Host | Supported route | Verification boundary |
|---|---|---|
| Codex | Local marketplace export, or a complete skill-directory export. | Codex CLI 0.163.0-alpha.10.2 installed the package in an isolated profile and app-server discovery found 118 skills and six MCP tools; no live assistant task was tested. |
| Claude Code | Native plugin export with persistent local-marketplace installation, session-only loading, or a complete skill-directory export. | Claude Code 2.1.311 previously validated the wrapper; the current machine has no `claude` command, and no live assistant task was tested. |
| Antigravity | Install the native wrapper from the app with `/plugin install <local-path>`, export a complete skill directory, or configure MCP manually. | Antigravity CLI 1.4.9 previously validated the wrapper in an isolated profile; the current machine has no `agy` command, and no live assistant task was tested. |
| Other compatible assistants | A portable skill directory, or a manually configured stdio MCP client. | Compatibility depends on the host's support for the relevant skill or MCP format. |

Keep the entire exported bundle together: nested methods use relative paths to shared resources. The server exposes read-only search, routing, resource access, environment status, and package verification. Its configuration does not install a host or connect external services. See [setup](docs/SETUP.md) for profile-specific commands, paths, and verification steps.

The GitHub release includes a tested npm-format tarball. In PowerShell, install and run the packaged CLI without an npm registry login:

```powershell
npx --yes --package=https://github.com/santanu-p/academic-research-assistant/releases/download/v4.0.0/academic-research-assistant-full-4.0.0.tgz academic-research-assistant-full doctor
npx --yes --package=https://github.com/santanu-p/academic-research-assistant/releases/download/v4.0.0/academic-research-assistant-full-4.0.0.tgz academic-research-assistant-full route "Compare these studies and identify evidence gaps"
```

Publishing to the npm registry is separate and may be added later by the maintainer. The earlier 3.2.0 release is a smaller package; this 4.0.0 release contains the complete reviewed collection.

## Contents and provenance

- [Skill mapping](audit/review-118/SKILL-MAPPING.md) and its [machine-readable details](audit/review-118/skill-mapping.json) describe all 118 entries and the two combined workflows.
- [File mapping](audit/review-118/file-mapping.json) records the destination and SHA-256 of 600 original payloads; adapted files retain originals under `audit/baseline/`.
- [Integration contract](docs/INTEGRATION.md), [ARMS dependencies](docs/ARMS.md), and [limitations](docs/LIMITATIONS.md) explain available behavior and missing components.
- [Build and validation](docs/BUILD.md) describes preservation, routing, protocol, and export checks. Historical research figures, scores, and logs are supplied examples, not newly reproduced findings.

## Optional standalone tools

The full collection keeps the standalone research utilities from version 3.2 alongside the 118 skills. They run separately; the MCP server does not launch them. Examples:

```powershell
python -X utf8 -B tools/workflow_runner.py examples/research-workflow.json --root .workflow-demo
python -X utf8 -B tools/rubric_score.py examples/rubric-review.json
python -X utf8 -B tools/presentation_builder.py --help
node tools/check_external_skills.mjs --help
```

These include local workflow planning/execution, checkpoint and evidence checks, rubric arithmetic, prose/table/figure QA, plotting (including paired, distribution, heatmap, and Pareto-frontier plots), text and LaTeX revision reports, basic editable PowerPoint generation, and external-skill preflight/handoff. Read the tool-specific guides in [`docs/`](docs/) before running a helper. Python packages are optional and listed in [`requirements-optional.txt`](requirements-optional.txt); LaTeX revision also requires separately installed `latexdiff` and Tectonic. Local commands run with your account's permissions, and workflow execution requires an explicit `--execute` flag.

For a simple UTF-8 CSV with a header and plain text cells, `python -X utf8 -B tools/csv_to_tex.py input.csv output.tex` creates a new LaTeX table fragment, escapes special characters, and refuses to overwrite. It does not interpret units, formulas, or missing-value meaning; inspect its documented limits before using it.

## Troubleshooting

- **An export target exists:** choose a new directory; exports do not overwrite files.
- **A host does not discover the plugin or skill:** check its documented installation path, reload the host, and inspect its own validation or plugin list. Export alone is not activation.
- **MCP does not start:** check that Node is on the host's PATH and the configured absolute `server/mcp.mjs` path points to the installed bundle. Regenerate configuration if the bundle moves.
- **A scientific tool is unavailable:** consult its source README and [dependencies](docs/DEPENDENCIES.md); the navigation server does not install optional research software.
- **Integrity verification fails:** run `node dev/build-index.mjs` after intentional runtime changes, then run `node cli/ara.mjs verify` and the applicable preservation checks in [build instructions](docs/BUILD.md). Investigate any original-file mismatch rather than replacing the recorded hash.

## Licenses and distribution

This is a mixed-license collection. The MIT notice applies only to the integration runtime and original material identified in [LICENSE](LICENSE); bundled source components retain their own terms and credits. The project maintainer reports that additional permission for this public distribution has been obtained. This does not replace or erase source notices. See [release rights and scope](docs/RELEASE-LICENSES.md) and [third-party notices](THIRD_PARTY_NOTICES.md) before redistributing or adapting individual components.
