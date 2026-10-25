# Release preparation

This folder is the public source project for [santanu-p/academic-research-assistant](https://github.com/santanu-p/academic-research-assistant). The parent workspace's private recovery archive is not part of the project. The npm package name and ownership remain to be verified before registry publication.

Before publishing, choose and verify the npm package name, set the actual repository URL in package.json, and check version consistency in all three manifests. Regenerate catalogs after any runtime edit.

```sh
npm run build
npm run validate
npm test
python -X utf8 -B -m unittest discover -s tests/python
npm pack --dry-run
npm pack
```

Inspect the real tarball and run it locally using the command in [installation](INSTALLATION.md). The prepack hook reruns Node validation and tests; it does not run optional Python tests. Publish only after those separate results and package contents are satisfactory.

The intended public entry point is ` npx academic-research-assistant@3.0.0 ` if that name is available and this release is published under it. The prepared archive is a local artifact; no npm release, GitHub repository, cloud deployment, or universal host compatibility is implied.

The project uses MIT for new text and implementations. No source collection has been relicensed by removing names. Recheck licenses and include required notices whenever adding third-party code, examples, artwork or templates.
