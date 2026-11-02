# Release status and checklist

Reviewed 2026-11-02. This record distinguishes the 90-skill GitHub release from the separately preserved full collection and from npm registry publication.

## Current GitHub release

- The configured repository is [santanu-p/academic-research-assistant](https://github.com/santanu-p/academic-research-assistant); see its [release assets](https://github.com/santanu-p/academic-research-assistant/releases).
- Version `3.2.0` contains 90 skills, the local navigation MCP server, and optional research workflow tools. The four package/plugin manifests use `3.2.0`.
- The npm manifest remains `private: true`. The GitHub release tarball and portable ZIP are separate from npm registry publication. npm sign-in and publication are deferred; the current registry E404 does not distinguish an absent package from access denial.
- The separate local full candidate records 118 reviewed entries and 600 preserved source payloads. It remains private and is not included in the 90-skill release.

## Distribution scope

The 3.2.0 release contains the project-authored 90-skill package and the two MIT-licensed Humanizer components with their notices. It does not contain the other source collections from the separately preserved full candidate. See [release rights](RELEASE-LICENSES.md), [source disposition](SOURCE-DISPOSITION.md), and [third-party notices](../THIRD_PARTY_NOTICES.md). The full collection has mixed source terms and unresolved redistribution permissions. Preserve its source files, credits, and license notices. Rewording does not create permission. Do not describe the 90-skill release as complete coverage of the 118-entry review ledger.

## Checks for a future release

1. Choose the version and verify it across all package/plugin manifests. Confirm npm package ownership and registry access separately; change `private` only for an intentional, authorized npm release.
2. Run `npm run build`, `npm run validate`, `npm test`, `python -X utf8 -B -m unittest discover -s tests/python`, and `python -X utf8 -B tests/test_package_release.py` from a clean checkout.
3. Build the actual tarball with `npm pack`. Install it offline in a temporary project and run `tests/test_draft_artifact.py` with `ARA_DRAFT_TARBALL` set to that archive. Verify the portable ZIP with `dev/package-release.py`; retain both archives, verification records, and SHA-256 checksums.
4. Inspect the artifact inventory and confirm it contains exactly the licensed and documented scope, required notices, and host manifests. Validate current Codex, Claude Code, and Antigravity commands against their target versions. Distinguish format checks from live host activation.
5. Commit and push the reviewed source, create a version tag and GitHub release, attach the verified tarball, ZIP, and checksums, then verify each public asset. Publish to npm only if the package name, ownership, authentication, and release terms are confirmed; install and verify it independently.

## Verification recorded for 3.2.0

On 2026-11-02, `npm run build` indexed 90 skills. `npm run validate` reported 179 runtime files, 198 local links, 715 checks, and zero failures. The Node suite passed 39 tests; one Windows symlink test was skipped because the environment returned `EPERM`. The Python suite passed 89 tests with 12 skips; `tests/test_package_release.py` and the offline `tests/test_draft_artifact.py` each passed.

The actual 3.2.0 tarball was installed offline and checked for package inventory, routes, resources, and exports. The portable ZIP was checked for source/archive byte equality and exclusion of private/developer files. These are local package checks, not live assistant tasks. Exact artifact checksums are published alongside the GitHub release assets.

The separately preserved full candidate validated 600 source payloads, all 118 map entries, all 118 active skill headers, and 427 active links. Its Node suite passed 227 tests; two Windows symlink tests skipped because the environment returned `EPERM`. This verifies package structure and tested behavior, not permission to redistribute.

The previous 3.1.0 GitHub tarball was rerun with `npx`: its verifier found 169 indexed files, zero failures, and zero unindexed files; the documented systematic-review route returned review skills. Codex CLI `0.163.0-alpha.10.2` exposes the documented marketplace and plugin commands. Claude Code and Antigravity CLIs are not installed in the current environment; their live host integrations are not certified here.
