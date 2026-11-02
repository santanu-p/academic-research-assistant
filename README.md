# Academic Research Assistant

Reusable research workflows, scientific writing guidance, document helpers, and a local navigation server for AI assistants. The package contains skill instructions and optional tools; the assistant and its configured tools perform the research work.

**Release status:** Version 3.2.0 is distributed through the GitHub release assets. The npm manifest remains `private: true`, so npm registry publication is separate. This release contains 90 skills and does not claim to reproduce the separately preserved 118-entry reviewed collection.

The MCP server is local and read-only: it searches, routes to, and reads bundled instructions, and checks the installed bundle. It does not query scholarly databases, call models, run experiments, or compile documents by itself. External services and optional software are configured separately.

## Install the published release

The 3.2.0 tarball can be run directly from GitHub with Node.js 22 or newer and npm. This avoids assuming the package is available from the npm registry.

```sh
npx --yes --package=https://github.com/santanu-p/academic-research-assistant/releases/download/v3.2.0/academic-research-assistant-3.2.0.tgz academic-research-assistant verify
npx --yes --package=https://github.com/santanu-p/academic-research-assistant/releases/download/v3.2.0/academic-research-assistant-3.2.0.tgz academic-research-assistant route "plan a systematic literature review"
```

The release tarball was installed and checked offline before publication. The npm registry lookup returned E404, which does not distinguish an absent package from one inaccessible to the current account; the manifest is explicitly private, so a bare `npx academic-research-assistant` command is not documented as an install method.

To work from source, clone the repository and use the local CLI:

```sh
git clone https://github.com/santanu-p/academic-research-assistant.git
cd academic-research-assistant
node cli/ara.mjs --help
node cli/ara.mjs list
node cli/ara.mjs route "plan a systematic literature review"
node cli/ara.mjs verify
```

## Use with AI assistants

The CLI exports complete bundles to new directories and prints host-specific next steps. It refuses to overwrite an existing destination. From a source checkout, run each `node cli/ara.mjs` command from the repository root.

| Host | Supported installation route | Verification boundary |
| --- | --- | --- |
| Codex CLI / app | Export a local marketplace, register it, then install the plugin with Codex. The portable skill profile is also available. | The 3.2.0 tarball exported a Codex marketplace and its nested bundle passed `verify`; Codex CLI 0.163.0-alpha.10.2 exposes the marketplace/add commands. A separate 4.0.0-local.1 artifact passed isolated install and app-server discovery for 118 skill entries and six MCP tools; no live assistant task was tested. |
| Claude Code | Export a native plugin. Use `--plugin-dir` for one session, or register a marketplace and install by name. | The current machine has no `claude` command. Claude Code 2.1.311 validated a wrapper from the separate 4.0.0-local.1 artifact; no live task was tested. |
| Antigravity | Install the plugin from a GitHub repository or a local directory with `agy plugin install`; optional MCP configuration is separate. | The current machine has no `agy` command. Antigravity CLI 1.4.9 validated and installed the separate 4.0.0-local.1 artifact; no live assistant task or MCP discovery was tested. |
| Other compatible agents | Use the portable skill bundle where Agent Skills are supported, or configure the printed stdio MCP entry where MCP is supported. | There is no universal skill path. Check the target host's current documentation and verify discovery there. |

### Codex

```sh
npx --yes --package=https://github.com/santanu-p/academic-research-assistant/releases/download/v3.2.0/academic-research-assistant-3.2.0.tgz academic-research-assistant export --host codex --target ../ara-codex-marketplace
codex plugin marketplace add ../ara-codex-marketplace
codex plugin add academic-research-assistant@academic-research-assistant-local
```

The marketplace export and nested bundle verification were run from the actual 3.2.0 tarball. Codex's current [plugin guide](https://developers.openai.com/plugins/build/plugins) documents local marketplaces; `codex plugin marketplace add` registers a source and `codex plugin add` installs from it.

### Claude Code

```sh
npx --yes --package=https://github.com/santanu-p/academic-research-assistant/releases/download/v3.2.0/academic-research-assistant-3.2.0.tgz academic-research-assistant export --host claude --target ../ara-claude
claude plugin validate ../ara-claude
claude --plugin-dir ../ara-claude
```

`--plugin-dir` loads the plugin for one session. The 3.2.0 source also includes `.claude-plugin/marketplace.json` for persistent installation from a local checkout:

```sh
claude plugin marketplace add /absolute/path/to/academic-research-assistant
claude plugin install academic-research-assistant@academic-research-assistant --scope user
```

The persistent flow uses the marketplace manifest included in 3.2.0. See Anthropic's current [plugin installation](https://code.claude.com/docs/en/plugins/install) and [marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference). The manifest has structural checks but was not checked with the Claude CLI on this machine.

### Antigravity

```sh
agy plugin install https://github.com/santanu-p/academic-research-assistant
agy plugin list
```

The current official [Antigravity plugin guide](https://antigravity.google/docs/plugins?tab=cli) supports GitHub and local-directory plugin installation. A separate MCP connection is optional; see [Antigravity MCP setup](https://antigravity.google/docs/mcp). Verify the installed plugin in the host before relying on it.

### Portable skills and MCP

```sh
node cli/ara.mjs export --host generic --target ../ara-generic
node ../ara-generic/cli/ara.mjs config --host generic --root ../ara-generic
```

Use the emitted skill folder at a location supported by the target host. Add the printed stdio MCP configuration only where the host supports MCP. Agent Skills uses a `SKILL.md` file with required `name` and `description` frontmatter; see the [format specification](https://agentskills.io/specification). Keep the full exported bundle together because skills can refer to shared files.

## Capabilities and examples

The 90-skill release covers research planning and questions, evidence discovery and appraisal, literature reviews, study methods, quantitative and qualitative analysis, citations, academic writing, thesis and proposal work, LaTeX, scientific figures and tables, presentations, and research communication. The [catalog](catalog/skills.json) lists the installed methods. Start with [research-assistant](skills/research-assistant/SKILL.md) for stage-based routing and the [research contract](docs/RESEARCH-CONTRACT.md) for evidence and artifact checks.

Example local commands:

```sh
node cli/ara.mjs route "compare these studies and identify the evidence gaps"
node cli/ara.mjs read skills/systematic-review/SKILL.md
python -X utf8 -B tools/workflow_runner.py examples/research-workflow.json
python -X utf8 -B tools/rubric_score.py examples/rubric-review.json
```

Optional tools include descriptive prose and table checks, figures, editable PowerPoint output, text and LaTeX revision reports, evidence-tracked rubric arithmetic, and a dry-run-first local workflow runner. See [tool requirements and limits](docs/DEVELOPMENT.md) and the individual guides in `docs/`. Python 3.10+ is optional; some tools require separately installed libraries or programs.

## Requirements and troubleshooting

- Node.js 22 or newer for the CLI and MCP server. The Node runtime has no npm dependencies.
- Python 3.10 or newer only for optional Python tools and tests. Optional package dependencies are listed in [development notes](docs/DEVELOPMENT.md).
- GitHub download for the public release tarball; the host application and its account are installed and configured separately.

If an export says its target exists, choose a new path. If a host cannot find Node, use the absolute executable path reported by `node cli/ara.mjs doctor` in its MCP configuration. If the host does not show the plugin or skill, check the host's plugin list or skill browser and reload it. Exporting a bundle does not activate it. If a Python helper reports a missing module or executable, install its documented optional dependency; the core CLI does not install it.

## Verification and contribution

CI runs on Windows and Ubuntu with Node.js 22 and Python 3.11. From the source checkout, run:

```sh
npm run build
npm run validate
npm test
python -X utf8 -B -m unittest discover -s tests/python
python -X utf8 -B tests/test_package_release.py
npm pack
```

The pack preflight runs build, validation, and Node tests. Python tests and actual-artifact installation checks are separate. See [contributing](CONTRIBUTING.md) and [changelog](CHANGELOG.md). No CI badge is shown because no verified CI result is claimed here.

## Licensing and collection scope

The root [MIT license](LICENSE) covers this project's own code and text. The bundled Humanizer projects retain their separate MIT notices. The original complete reviewed collection is preserved separately and is not included in this 90-skill package; the full collection has mixed terms and unresolved redistribution permissions. Do not infer a new license from paraphrasing. See [release rights](docs/RELEASE-LICENSES.md), [source disposition](docs/SOURCE-DISPOSITION.md), and [third-party notices](THIRD_PARTY_NOTICES.md); credits and notices remain intact.
