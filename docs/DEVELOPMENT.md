# Development

The Node runtime uses only standard libraries. ` cli/ara.mjs ` handles discovery, export and configuration printing; ` lib/core.mjs ` enforces resource boundaries; ` server/mcp.mjs ` serves MCP over stdio. Python tools run separately and are never launched by the MCP server.

Canonical skill folders live under ` skills/ `. Each has a YAML name matching its directory, a concise description, substantive methods and a link to the research contract. The outer SKILL.md supports hosts that discover only one directory. The catalog contains searchable descriptions and keywords; it is not an autonomous scientific decision system.

After editing runtime files:

```sh
npm run build
npm run validate
npm test
python -X utf8 -B -m unittest discover -s tests/python
```

Build regenerates the capability catalog and SHA-256 file inventory. Validation checks skill coverage, metadata, local links, manifests and inventory consistency. Hashes detect local changes; a locally editable inventory is not publisher authentication. Tests execute the actual CLI and subprocess protocols. The revision fixture commands are local test programs, not language models.

Optional plotting tests require NumPy and Matplotlib; raster tests require Pillow; PDF checks require PyMuPDF. Install these into a virtual environment you control. Library APIs use stable basic operations but this release does not pin or vendor optional Python libraries. Keep temporary outputs inside a writable working directory in restricted environments.

To add a skill, define its stage and distinct deliverable before adding code. Add its keyword entry in ` dev/build-catalog.mjs `, update coverage checks, and regenerate catalogs. Do not split duplicate synonyms into competing skills. Preserve attribution and license terms for any future imported material.

Runtime package contents use an explicit whitelist in package.json and core.mjs. Keep these lists aligned. Tests and dev files remain in the public source repository but outside runtime distributions.
