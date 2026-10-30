# Host setup

This release has 90 methods, including two separately credited MIT Humanizer skills. It does not establish complete coverage of the separately preserved 118-entry source collection. Node.js 22 or newer is required for the CLI and navigation MCP server; optional scientific tools have their own dependencies. The host checks described below used earlier snapshots of this release; live assistant activation has not been established.

From the project root, run `node cli/ara.mjs verify` and `node cli/ara.mjs route "plan a systematic review protocol"`. Export to a new path; the CLI checks source integrity, refuses existing targets and prints the appropriate next steps. It does not change account settings.

## Codex

```sh
node cli/ara.mjs export --host codex --target /absolute/new/ara-marketplace
codex plugin marketplace add /absolute/new/ara-marketplace
codex plugin add academic-research-assistant@academic-research-assistant-local
```

The two `codex` commands registered and installed this local marketplace plugin in an isolated Codex profile; the installed CLI verified its indexed files. A live assistant task and MCP discovery in a Codex session have not been tested. Alternatively use `--host codex-skill` and place the complete exported folder at the host's documented skills location.

## Claude Code

```sh
node cli/ara.mjs export --host claude --target /absolute/new/ara-claude
claude plugin validate /absolute/new/ara-claude
claude --plugin-dir /absolute/new/ara-claude
```

The wrapper contains one outer skill with the complete nested bundle and its local MCP configuration. `--plugin-dir` loads for a session. Claude Code 2.1.311 validated the exported wrapper; a live assistant session remains untested. `--host claude-skill` produces an instruction-only folder instead.

## Antigravity

```sh
node cli/ara.mjs export --host antigravity --target /absolute/new/ara-antigravity
agy plugin install /absolute/new/ara-antigravity
agy plugin list --json
```

The plugin wrapper contains one outer skill. MCP is optional and not automatically configured: after installation, use `node INSTALLED_BUNDLE/cli/ara.mjs config --host antigravity --root INSTALLED_BUNDLE` with the actual absolute nested bundle path, then apply the printed configuration in the host. Regenerate it if the bundle moves. `--host antigravity-skill` is an instruction-only option. Antigravity CLI 1.4.8 validated and installed this wrapper in an isolated profile. A live assistant task and host MCP discovery remain untested.

## Generic hosts

Use `node cli/ara.mjs export --host generic --target /absolute/new/ara-generic`, then run its `config --host generic --root /absolute/new/ara-generic` command for a stdio MCP configuration. A generic skill or MCP setup depends on the host's supported mechanism. Keep exported resources together; individual methods may use relative links.

## Separately installed skills and services

Register separately installed skills and MCP servers through your host's own settings and permissions. Their instructions, code, licenses and credentials are not included or copied by this release. The host decides whether it can discover and invoke them; this plugin's advisory router does not automatically select them. Consult the provider's terms and the host's instructions before use. Never put credentials in the reference file below.

For an optional local filesystem preflight, make a private JSON file outside the exported bundle, with only the skill directories you choose to check:

```json
{"version":1,"skills":[{"name":"example","path":"/absolute/path/to/installed-skill"}]}
```

On Windows use a JSON-escaped absolute path (for example `C:\\skills\\example`). Run `node tools/check_external_skills.mjs /absolute/path/to/references.json`. It checks the supplied directory and its immediate `SKILL.md` for accessibility; it does not read their contents, traverse a collection, copy files, execute instructions, or modify host configuration. It refuses symbolic links for the final directory and file, and reports unavailable entries with a nonzero exit code. Intermediate path components are resolved by the operating system. A readable file is not proof of host registration, activation, functional compatibility, or permission to use its contents. The report includes the paths you supplied, so treat it as potentially sensitive. External services require separate configuration and an actual authorized connection test; this preflight does not contact them.

### Optional external workflow handoff

To coordinate a sequence involving separately installed capabilities, maintain a private JSON record outside the bundle. Identify the actual host and use its supported interface to discover and invoke each capability. Record observations and completed work only after they happen. The following is an illustrative record, not a claim about an installed service:

```json
{
  "version": 1,
  "capabilities": [
    {"id":"search", "kind":"mcp-tool", "host":"your host", "status":"unverified"},
    {"id":"appraisal", "kind":"skill", "host":"your host", "status":"unverified"}
  ],
  "steps": [
    {"id":"find", "action":"Search through the host", "dependsOn":[], "requires":["search"], "status":"pending"},
    {"id":"assess", "action":"Appraise retrieved sources", "dependsOn":["find"], "requires":["appraisal"], "status":"pending"}
  ]
}
```

Run `node tools/external_handoff.mjs /absolute/path/to/handoff.json`. Set a capability to `available` only with a nonempty `evidence` field describing the relevant observation; supported statuses also include `unavailable` and `unverified`. Set a step to `completed` only with an `evidence` field identifying the result. The checker reports pending steps as blocked or ready for host action, and flags completed steps whose recorded prerequisites are unmet, including downstream inconsistencies. It rejects unknown references and cycles. `ready-for-host` does not invoke anything or establish authorization. A completed step that needs review produces a nonzero exit code; blocked pending work is a valid handoff. All observations and evidence are user-supplied and unverified by the checker. It neither reads external skill content nor calls services, and it does not register tools, verify credentials, or perform research. Keep credentials and sensitive material out of the record and report. Check provider terms, permissions, host access, and actual outputs independently.

Check actual host documentation and installed versions before registration: [Codex plugins](https://developers.openai.com/plugins/build/plugins), [Claude plugins](https://code.claude.com/docs/en/plugins-reference), [Antigravity plugins](https://antigravity.google/docs/plugins?tab=cli), [Antigravity MCP](https://antigravity.google/docs/mcp), and the [Agent Skills specification](https://agentskills.io/specification). None of these exported formats proves that a live host has loaded the plugin or that an external research service is connected.
