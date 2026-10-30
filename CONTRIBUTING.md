# Contributing

Changes should preserve the distinction between project-authored material and third-party collections. Do not copy restricted instructions or remove their notices, and do not claim complete coverage from a matching skill name.

Use Node.js 22 or newer. After changing runtime files, run `npm run build`, `npm run validate`, `npm test`, and `python -X utf8 -B -m unittest discover -s tests/python`. The Node runtime has no npm dependencies. Optional Python tests may be skipped when their dependencies are absent; report those skips. Optional Python tools have separate dependencies described in [development](docs/DEVELOPMENT.md).

When changing a skill, keep its frontmatter name matched to its directory, identify when it applies, provide actionable instructions, and preserve evidence, citations and uncertainty. Test routing and affected resource links. Record actual tool execution separately from plans and static instructions. Update the import mapping if intentionally editing an imported draft, retaining the source provenance and describing the change.

Report a problem with a minimal sanitized example, expected and actual behavior, operating system, Node version and checks performed. Do not include credentials, private research data or unpublished reviewer correspondence in public reports. Live host activation and scientific accuracy require their own verification.

For host-related changes, use a fresh export target and record the host name and version, export command, validation or installation result, and installed bundle verification. If a live host session is available, separately check skill activation and MCP discovery and record the task and outcome. An export, manifest validation, or installation alone does not establish live activation or service connectivity. See [draft setup](docs/DRAFT-SETUP.md) for host-specific commands. Do not replace the separate source-coverage audit with a count of skill names.
