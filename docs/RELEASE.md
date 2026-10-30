# Release preparation

This is the historical v3 release preparation record. Version 3.1.0 has expanded capabilities; see the [changelog](../CHANGELOG.md), [host setup](DRAFT-SETUP.md), and [third-party notices](../THIRD_PARTY_NOTICES.md) for current details.

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

The v3 package was prepared for a possible npm release. Registry availability and package ownership must be checked separately; a local archive does not establish npm publication or universal host compatibility.

The project uses MIT for new text and implementations. No source collection has been relicensed by removing names. Recheck licenses and include required notices whenever adding third-party code, examples, artwork or templates.
