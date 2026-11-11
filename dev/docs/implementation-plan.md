# Academic research plugin implementation plan

**Goal:** faithfully integrate the supplied collection and deliver a validated private plugin with complete provenance.
**Spec:** docs/design.md and the supplied goal-objective.md.
**Architecture:** immutable provenance, namespaced active skills, routing catalog, read-only local MCP server, reproducible builder and verification.
**Tech stack:** Python 3.10+, stdlib runtime; PyYAML/jsonschema for development checks; optional upstream scientific packages.

## Global constraints

- Preserve every supplied file and archive member; no source edits.
- Distinguish active, preserved, external, verified and untested components.
- No credential bundles, fabricated tools, external endpoints, scientific results or installation claims.
- Work in D:/PLUGIN; no Git repository was supplied and no commit is required.
- Proceed through implementation under the user's explicit instruction; no additional design approval gate is needed.

## Review focus

Name collisions, missing ARMS frontmatter, relocated relative paths, global activation/affiliate behavior, absent external execution backends.

## Tasks

- [x] 1. Freeze originals, safely inspect ZIP entries, read/parse all source files and binary metadata. Produce work/original-inventory.json, archive-inventory.json, inspection.json.
- [ ] 2. Build package and complete source mapping. Preserve all source/support files and adapt all 117 active skill definitions. Generate catalog, routing, docs, dependency registry and change log.
- [ ] 3. Write behavior tests for routing, resource containment, dependency reporting, provenance tamper detection and MCP subprocess protocol. Run failing checks, implement server, then pass checks.
- [ ] 4. Validate package against official schemas and components; audit every source hash and relative reference; test upstream runnable scripts and representative workflows. Record independent review and resolve issues.
- [ ] 5. Build and inspect one-plugin archive, save with Plugin Creator, inspect stored component inventory and report install/activation status accurately. Deliver package and linked audit documents.
