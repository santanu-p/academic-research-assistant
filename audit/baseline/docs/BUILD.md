# Rebuild and verify

The delivery workspace is `D:/PLUGIN`. Source folders/ZIPs remain unchanged at their supplied locations; `work/originals` is a hash-checked frozen copy and `work/expanded` contains safely expanded ZIP entries. `build_tools/` contains inspect_sources.py, build_plugin.py, component adapter modules, validate_package.py and release packaging utilities. `tests/` holds behavioral/regression tests. `docs/` records the design, plan and progress.

From that workspace:

```powershell
python .\build_tools\inspect_sources.py
python .\build_tools\build_plugin.py
python -m unittest discover -s tests
python .\build_tools\validate_package.py
```

The inspector checks all archive entries for traversal/collisions/symlinks, copies hidden files, parses all text/configuration/code/CSV content and extracts image/PDF metadata. The builder generates active skill metadata, full support trees, routing and exact source mapping, then runs recorded active-copy adapters. It retains authored integration files in the output directory; the release also includes their source template for reconstruction.

Validation uses PyYAML and jsonschema plus the official schemas saved under `work/schemas`. It checks both root manifests, compatibility metadata, all active skill definitions/agent YAML, JSON/JSONL/YAML/Python syntax, routing destinations, Markdown file references and every preserved file/directory. The core server uses Python stdlib only.

Development prerequisites are listed explicitly in `dev/requirements-dev.txt`: PyYAML, jsonschema, Pillow and pypdf (for source PDF inspection). Optional scientific packages enable additional integration tests. The release contains the complete authored `dev/integration` template, builder/adapter scripts, tests and fetched official schemas.

To reconstruct from the delivered package in a **new empty workspace**:

```powershell
python -m pip install -r .\dev\requirements-dev.txt
python .\dev\reconstruct.py --out D:\academic-plugin-rebuild
```

The reconstruction entrypoint copies the preserved original inputs and authoring sources, then inspects, builds and validates a fresh package without modifying the installed copy. It does not install scientific runtimes, run external models or create another account plugin. Test and release evidence from the original build are historical records; run the reconstructed tests to obtain a fresh receipt.

Release tooling packages **one plugin** and excludes runtime caches/bytecode and dependency installation directories. It verifies archive entry paths, exact file hashes against the package and preserved source hashes. The ZIP is written outside the plugin directory and a SHA-256 checksum is delivered beside it. Private Plugin Creator upload accepts that absolute ZIP path. The stored file inventory/component diagnostics are checked after saving.

See `audit/VERIFICATION.md` for the actual commands, receipts, unresolved dependencies and independent audit findings from this build. An environment-presence check is not an execution test; a representative numerical example is not full scientific reproduction.
