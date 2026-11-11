# Local setup and host connection

Use Node.js 22 or newer. From the collection root run `node cli/ara.mjs doctor`, then `node cli/ara.mjs verify`. Exports create a new directory and refuse to overwrite an existing target. They do not change host settings or authenticate external services. Replace the Windows examples with absolute paths for your system.

## Codex

```powershell
node .\cli\ara.mjs export --host codex --target "D:\ara-codex"
codex plugin marketplace add "D:\ara-codex"
codex plugin add academic-research-assistant-full@academic-research-assistant-full-local
```

Export does not install the plugin. Run a Codex plugin export from the original complete package: instruction-only exports and the bundles nested inside Claude or Antigravity wrappers omit plugin manifests and cannot be re-exported as a Codex plugin. The marketplace contains the complete bundle under `plugins/academic-research-assistant-full`. Codex CLI registered and installed the marketplace in an isolated profile and listed the plugin as enabled. The installed Node CLI verified its indexed files. Codex app-server discovery found all 118 skill entrypoints and the six bundled MCP tools in that profile; a live assistant task was not tested. See [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins).

Alternatively, export `--host codex-skill` to a new directory named `academic-research-assistant-full` under project `.agents/skills/` or user `~/.agents/skills/`. Reload the host and verify discovery. See [skill locations](https://learn.chatgpt.com/docs/build-skills).

## Claude Code

```powershell
node .\cli\ara.mjs export --host claude --target "D:\ara-claude"
claude plugin validate "D:\ara-claude"
claude plugin marketplace add "D:\ara-claude"
claude plugin install academic-research-assistant-full@academic-research-assistant-full-local --scope user
claude --plugin-dir "D:\ara-claude"
```

The wrapper contains one outer skill with the complete nested methods and resources, configures its local MCP server, and includes a marketplace manifest for persistent installation. `--plugin-dir` loads the plugin for one session. To install from this source checkout instead, add the collection directory as a marketplace and install `academic-research-assistant-full@academic-research-assistant`. Claude Code 2.1.311 previously validated an exported wrapper and noted an optional directory-listing icon; the current machine has no `claude` command, so the persistent flow has not been rechecked here and no live host task has been tested. See Anthropic's [plugin installation](https://code.claude.com/docs/en/plugins/install) and [marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference).

For instruction-only use, export `--host claude-skill` to a new folder named `academic-research-assistant-full` under project `.claude/skills/` or user `~/.claude/skills/`. See [Claude skills](https://code.claude.com/docs/en/skills).

## Antigravity

```powershell
node .\cli\ara.mjs export --host antigravity --target "D:\ara-antigravity"
```

In Antigravity's plugin manager, run `/plugin install "D:\ara-antigravity"` to install the local plugin. Then use the CLI to verify it:

```powershell
agy plugin list --json
```

The wrapper contains one outer skill and the complete nested resources. Its optional MCP connection is not registered automatically. After installation, locate the actual nested bundle and generate its absolute-path configuration:

```powershell
node "ABSOLUTE_INSTALLED_BUNDLE\cli\ara.mjs" config --host antigravity --root "ABSOLUTE_INSTALLED_BUNDLE"
```

Apply the printed JSON through the host's MCP configuration mechanism. If the bundle moves, regenerate the configuration. Antigravity CLI 1.4.9 previously validated and installed this wrapper in an isolated profile, and listed the outer skill as enabled; the current machine has no `agy` command. An assistant task and host MCP discovery remain untested. See the official [plugin](https://antigravity.google/docs/plugins?tab=cli), [skill](https://antigravity.google/docs/skills), and [MCP](https://antigravity.google/docs/mcp) documentation.

For instruction-only use, export `--host antigravity-skill` to a new folder named `academic-research-assistant-full`. Antigravity's workspace path is `.agents/skills/`; its app and CLI documentation list different global skill paths. Consult the applicable host documentation.

## Other compatible hosts

```powershell
node .\cli\ara.mjs export --host generic --target "D:\ara-generic"
node "D:\ara-generic\cli\ara.mjs" config --host generic --root "D:\ara-generic"
```

Use the printed JSON in a compatible stdio MCP client, or use the complete folder as a portable skill where supported. Do not copy isolated leaf methods: their relative links can refer to shared files. No generic installation path applies to every host.

The local server exposes read-only `search_capabilities`, `route_task`, `read_resource`, `environment_status`, `verify_package`, and `verify_sources`. For `read_resource`, offsets and lengths count Unicode code points; use the returned `next_offset` for the next page. The server navigates instructions; the host performs the task with actual tools. Binary resources need an appropriate viewer. Python scripts and scientific examples retain their optional dependencies in [dependencies](DEPENDENCIES.md), original READMEs and `requirements-optional.txt`. ARMS external model loops require explicit invocation and their own preflight. No scientific example, paid model loop or remote research service is exercised by exporting a bundle.
