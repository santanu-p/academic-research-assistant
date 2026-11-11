# Install, connect and use

## Private account plugin

Open the Plugin Creator link in the delivery message and use the host's installation/select controls. Creation saves the package privately to the authenticated account/workspace; it does not by itself prove installation, local executor availability or service authentication. Start/select the installed plugin in a **local** Codex chat if the host requires a fresh chat for skill/tool discovery.

## Local portable package

Extract the delivered ZIP to a stable folder. The single plugin root contains `plugin.json`, `mcp.json`, `skills/` and `server/`. Register/install it through the host's supported local plugin or marketplace flow. The `.codex-plugin/plugin.json` overlay is provided for local Codex compatibility. Do not install nested manifests from `resources/` as extra plugins.

The stdio server configuration is:

```json
{"type":"stdio","command":"python","args":["-u","${PLUGIN_ROOT}/server/assistant_server.py"],"cwd":"${PLUGIN_ROOT}"}
```

If the host's local server configuration does not expand `${PLUGIN_ROOT}`, replace it with the actual extracted absolute directory in that host configuration. Use the correct Python executable for the desired optional environment. Never launch this server as an HTTP service; it reads MCP JSON-RPC on stdin and writes only MCP responses on stdout.

## Verify activation

1. Confirm the host discovered **118 skills** and the `academic-research-local` server.
2. Call `environment_status` and inspect what is available.
3. Call `verify_sources`; it should verify **273 files** and **179 directory entries**, with no missing or mismatched files.
4. Call `route_task` with `{"task":"Plan a PRISMA systematic review"}`; read the returned skill files using `read_resource` or the host file tools.
5. Confirm no external service is presented as connected until separately configured and tested.

If tools have not loaded, refresh/reselect the plugin or use a new local chat according to host behavior. The receipt's saved component inventory verifies ingestion; it does not substitute for these activation checks.

## Direct inspection without host activation

```powershell
'{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python -u .\server\assistant_server.py
```

The server ends cleanly on stdin EOF. This checks subprocess tool discovery only.

## Useful requests

- “Identify a defensible research gap using verified sources; distinguish hypotheses from established findings.”
- “Plan a mixed-methods study, draft the interview guide and align the analysis with the research question.”
- “Audit the claims in this manuscript against my actual data and derivations.”
- “Create readable conference slides from this paper and retain the references and uncertainty.”
- “Use the supplied house style on my LaTeX draft without changing numbers, meaning or citations.”
- “Show every source file and confirm preservation hashes.”
