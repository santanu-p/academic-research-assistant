# Current build and verification

Prerequisites: Node.js 22 or later, npm, Python 3.10 or later, and PyYAML for the preservation validator. Install PyYAML into the Python environment used for validation with `python -m pip install "PyYAML>=6.0"`. Other packages in `dev/requirements-dev.txt` support additional checks and are not required by the core pack lifecycle.

Host and generic exports omit package scripts and `tests/`. In an export, after intentional runtime changes run `node dev/build-index.mjs`, then `python -X utf8 -B dev/validate-full.py` (requires PyYAML) and `node cli/ara.mjs verify`. These checks cover local consistency and preservation, not host integration. The npm and test commands below require the original complete package.

A normal `npm pack` runs `prepack`, which rebuilds the runtime index, validates source preservation, and executes the Node suite. It does not bypass the collection’s mixed-license release restrictions. CI also rejects a committed runtime index that changes when rebuilt.

Run `python -X utf8 -B tests/test_package_artifact.py` separately for archive and offline installation checks. By default, this test rebuilds the runtime index and creates a fresh temporary tarball with lifecycle scripts disabled; it does not test a previously generated tarball. To check a specific existing tarball, run the following from the package root, replacing the placeholder with its path:

```powershell
$previousAraTarball = [Environment]::GetEnvironmentVariable('ARA_TEST_TARBALL', 'Process')
try {
    $env:ARA_TEST_TARBALL = (Resolve-Path -LiteralPath '<path-to-tarball.tgz>').Path
    python -X utf8 -B tests/test_package_artifact.py
} finally {
    [Environment]::SetEnvironmentVariable('ARA_TEST_TARBALL', $previousAraTarball, 'Process')
}
```

With `ARA_TEST_TARBALL` set, the test checks the selected archive's mapped payloads and internal integrity, installs it offline, and runs selected installed-package checks. It also performs a separate npm dry-run listing against the current source. Run normal `npm pack` or the checks below independently for the current source; selecting an existing archive does not run its `prepack` lifecycle.

From this full local package root:

```powershell
node dev/build-index.mjs
python -X utf8 -B dev/validate-full.py
npm.cmd test
python -X utf8 -B tests/test_python_server.py
node cli/ara.mjs verify
```

The index covers the complete runtime tree, including resources, shared agents, historical developer sources and source-preservation audits. The validator checks all 600 original file hashes and all 118 mapping rows, then compares every one of 114 unmerged complete source bodies against the preserved original plus only reviewed corrections. The two comprehensive merged methods have an independent semantic preservation review. These checks serve different requirements.

The Node suite exercises selection for original identifiers, natural-language near-neighbor routing, both Humanizers' support resources, compatibility aliases, path boundaries, stdio protocol behavior and host export formats. Full local exports are format-tested; an installed host session and external research/model services are not implied. `python -X utf8 -B tests/test_package_artifact.py` checks the npm artifact separately.

The maintained Python server is also checked against the current routing catalog and the 600-file review mapping. npm normalizes `.gitignore` files on installation: the two affected original files remain byte-exact in the source and are mapped to stable copies under `audit/review-118/preserved-ignore-files/` for packaged installations.

Original dev/build_tools, dev/reconstruct.py and dev/integration are preserved historical v1 sources. They can reconstruct the old build and are not the current catalog generator. Existing audit receipts describe earlier checks and should not be treated as proof of later edits; rerun the commands above. Scientific source scripts and cases were inspected, not reproduced.
