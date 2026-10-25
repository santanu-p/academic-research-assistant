# Portable public package implementation plan

Goal: ship newly authored research instructions and implementations under MIT, ready for later GitHub/npm publication, without a cloud account dependency.

Architecture: one editable research plugin, a dependency-free Node CLI and read-only stdio MCP server, with optional Python scientific helpers. Host exports preserve the whole relative resource tree. Historical supplied material and previous releases are retained only in an excluded local backup.

Decisions: Node 22+, Python 3.10+ for optional helpers; version 3.0.0 for the changed runtime/package and distribution scope. No install hooks, credentials, hidden downloads or automated public publishing. A package archive is not evidence of a host session or registry publication.

Approaches considered: retaining mixed-license inputs cannot meet unrestricted public distribution; hiding credits or superficial paraphrasing cannot fix that. This release uses new general-purpose prose/code instead, excluding the source collection, its graphics, corpora, case studies, copied recipes and restricted helper implementations. Required notices remain if any third-party material is retained.

1. Test public behavior before implementation: local command help/catalog, contained reads, MCP initialization/tool discovery, target installation preserving references, refusal to overwrite and host export structure.
2. Implement a Node catalog reader and strict JSON-RPC transport without external dependencies or research/network execution.
3. Implement CLI list/route/read/doctor/mcp/config/export/install, explicit target paths and profile-specific metadata. Test fresh installs and package-root discovery after npm extraction.
4. Author research/artifact methods and scientific Python tools independently in disjoint paths. Run actual tests and inspect generated figures.
5. Validate every skill, local link, manifest, catalog entry and runtime allowlist. Build npm/ZIP artifacts; inspect their full contents for excluded/private files.
6. Verify preserved historical files before removing redundant workspace copies. Retain one excluded recovery archive and new final deliverables.
7. Document actual compatibility and limits. Do not claim npm name ownership, live host testing, scholarly connectivity or public release.
