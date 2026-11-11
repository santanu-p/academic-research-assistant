# Academic Research Assistant

A unified academic, scientific and research assistant built from the entire supplied collection: **117 source skills plus one unified routing skill**, with a local MCP navigation server, complete source preservation, research workflows and reproducible verification.

Start with [installation and onboarding](docs/SETUP.md), [capability inventory](docs/INVENTORY.md), [integration rules](docs/INTEGRATION.md), and [verification results](audit/VERIFICATION.md).

All **174 original files** and **99 expanded archive files** are retained with SHA-256 provenance. The [source map](audit/source-map.csv) accounts for files, directories and ZIP entries. Every supplied source skill has an active namespaced copy; overlapping skills remain separately invocable. Complete supporting resources and upstream configurations are retained. Some workflows need separately installed software, authenticated research services or host tools. See [dependencies](docs/DEPENDENCIES.md) and [limitations](docs/LIMITATIONS.md).

## Use

Ask: “Plan a systematic review,” “Audit my research claims,” “Write an NIH Specific Aims draft from this evidence,” “Create an academic presentation,” or “Prepare my LaTeX manuscript.” The router selects the skill files to read before executing the task. It can combine specialists and apply evidence and artifact QA gates.

The MCP tools `route_task`, `search_capabilities`, `read_resource`, `environment_status`, and `verify_sources` operate locally. They provide real catalog lookup, contained text reads, runtime presence checks and provenance auditing. They do not perform scholarly search, execute experiments or author documents independently of the host assistant.

## Contents

- `skills/`: 118 discoverable skills and every skill's supporting files.
- `catalog/`: complete skill records and deterministic routing rules.
- `server/`: stdlib-only read-only MCP server (Python 3.10+).
- `workflows/` and `agents/`: research stage handoffs and reusable role instructions.
- `resources/originals/`: exact input files, including all four ZIP containers and hidden source metadata.
- `resources/upstream/`: complete extracted archive trees.
- `audit/`: mapping, source inspection, adaptations, independent reviews and test evidence.
- `docs/`: setup, dependencies, licensing, integration and known limitations.

Preserved upstream manifests and marketplace files are reference material. Only the root manifest, compatibility overlay, root MCP configuration and top-level `skills/` register this unified plugin.

## Reproduce

From the supplied build workspace, run the inspection and builder scripts, validation and tests described in `docs/BUILD.md`. Runtime Python uses no third-party packages. Validation and optional upstream workflows have their own documented dependencies.

This private collection retains mixed upstream terms. ARMS is CC BY-NC 4.0; three standalone skills carry MIT notices; the five supplied installed-plugin trees contain no license text. See [third-party notices](THIRD_PARTY_NOTICES.md). No blanket redistribution license is asserted.
