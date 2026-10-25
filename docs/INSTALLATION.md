# Installation and host support

Use Node.js 22+ on a host with a local filesystem. Keep exported bundles intact because skill links refer to shared methods, documents, and optional tools. None of the exports edits global host configuration. Install/export means filesystem copying.

## Codex plugin marketplace

From the source directory:

```sh
node cli/ara.mjs export --host codex --target ../ara-marketplace
codex plugin marketplace add ../ara-marketplace
codex plugin add academic-research-assistant@academic-research-assistant-local
```

The export creates a local marketplace at ` .agents/plugins/marketplace.json ` and the plugin at ` plugins/academic-research-assistant `. These locations follow the [Codex plugin format](https://developers.openai.com/plugins/build/plugins). Registration is a separate explicit host operation. A compatible installed Codex version and its plugin permissions are required.

## Claude Code plugin

```sh
node cli/ara.mjs export --host claude --target ../ara-claude
claude --plugin-dir ../ara-claude
```

The export contains ` .claude-plugin/plugin.json `, root ` skills/ ` and ` .mcp.json ` with the Claude plugin-root placeholder. See the [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference). Commands and behavior depend on the installed Claude Code version. Configure trust and local server permissions within that host.

## Single-entry Agent Skills

Export ` --host codex-skill ` or ` --host claude-skill `. Place the complete exported folder in that host's supported skill location. Only the outer ` academic-research-assistant ` skill is the entry point; it loads nested canonical methods. Do not copy just the root SKILL.md. Do not assume a host recursively discovers every nested skill.

## Other local MCP hosts

```sh
node cli/ara.mjs config --host generic --root /absolute/path/to/bundle
```

This prints MCP JSON containing ` command: "node" ` and an absolute server path. ` --host codex ` prints a TOML fragment. For a desktop host without Node on its PATH, use the absolute executable reported by ` node cli/ara.mjs doctor `. Add the printed configuration using that host's documented settings.

The server reads newline-delimited JSON-RPC on stdin/stdout, supports MCP protocol versions 2025-06-18 and 2025-11-25, and exposes five read-only tools: capability search, task routing, resource reading, environment reporting, and local package consistency checks. It has no network, shell, or model-execution tool.

## Before npm publication

Use ` node cli/ara.mjs ` in the source tree. To test the actual archive, use:

```sh
npm exec --yes --package /absolute/path/academic-research-assistant-3.0.0.tgz -- academic-research-assistant --help
```

Keep an npm cache writable if using npm in a restricted environment. A local tarball avoids relying on an unpublished registry name.

## Verified boundary

Automated checks exercise actual bundle export for all five profiles, path containment, refused overwrites, direct server launch, JSON-RPC tool calls, and tarball execution. Manifest formats were checked against the linked official documentation. Account-level installation, host discovery UI, external search services, subscriptions, TeX/office backends, and paid model commands are not configured or certified by these tests.
