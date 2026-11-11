# Contributing

This collection is developed for private local use. Before sharing a copy, fork,
archive, or release publicly, resolve the permissions described in
[LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The full
collection includes noncommercial material and source families without supplied
redistribution licenses. A successful check does not grant distribution rights.

## Set up and check a change

Work from this directory, containing `package.json`. Use Node.js 22 or newer and
Python 3.10 or newer available as `python`. The current core JavaScript runtime
has no npm dependencies. The preservation validator needs PyYAML 6 or newer:

```sh
python -m pip install "PyYAML>=6.0"
npm run build
npm run validate
npm test
python -X utf8 -B tests/test_python_server.py
node cli/ara.mjs verify
python -X utf8 -B tests/test_package_artifact.py
```

In PowerShell, use `npm.cmd` if your execution policy blocks `npm.ps1`.
Alternatively, install development dependencies from `dev/requirements-dev.txt`
in a virtual environment. Scientific examples and older development tests may
need the separate packages in `requirements-optional.txt`; they are outside the
core checks above. See [dependencies](docs/DEPENDENCIES.md) and
[current build scope](docs/BUILD.md).

The build refreshes `catalog/files.json` after runtime changes. Run it before
validation and verification, inspect the generated changes, and retain only
intentional updates. No API key, paid account, host installation, or external
research service is required for these checks.

The root `.gitattributes` disables Git text conversion for every file. Preserved
payloads contain original mixed line endings and must remain byte-exact across
checkouts. Keep this rule and do not normalize source line endings. The package
artifact test checks the actual npm archive for preservation and exclusions.

## Keep changes reviewable

- Describe the problem, the resulting behavior, and the checks actually run.
- Add a focused regression case for changed routing or runtime behavior. Include
  a failing example and nearby requests that should keep their existing route.
- Preserve scientific claims, citations, uncertainty, numbers, and authorship.
  Distinguish instructions, proposals, historical evidence, and executed results.
- Keep preserved originals under `resources/` and their notices intact. Active
  adaptations must remain traceable through the catalog and preservation audit;
  document intended corrections instead of changing baseline hashes to hide a
  mismatch. Coordinate source additions or updates with the maintainer.
- Do not add credentials, private manuscripts, personal data, machine-specific
  paths, generated exports, or unreviewed upstream changes.

The automated checks cover local package preservation, routing, resource access,
stdio protocol behavior, and export formats. They do not establish a live
Codex/Claude connection, verify a research finding, or reproduce the supplied
scientific examples. Report any additional manual integration checks with the
host/version, exact procedure, and observed result.

## Report a problem or propose an improvement

Use the issue forms in the repository hosting this collection. For a bug, supply
a minimal sanitized command or request, expected behavior, actual behavior, and
runtime versions. For an improvement, describe the user problem and an observable
acceptance criterion. If an issue could disclose credentials, private research,
or an exploitable vulnerability, contact the repository owner privately through
an established channel instead of posting sensitive details in an issue.

Keep `private: true` in `package.json`. Public distribution of the full collection
requires a separate permissions review; this workflow does not publish packages,
upload bundles, or approve a release.
