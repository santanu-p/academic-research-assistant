# Release rights and scope

Reviewed 2026-11-02 against the supplied source files, their included license and attribution records, and the linked author terms. Current upstream pages for ARMS, Fasih's terms, and Academic PPTX were also rechecked on that date. This is a release-readiness record, not a claim that every adaptation has been legally cleared.

## Current GitHub package

The 3.2.0 release contains 90 skills. Its npm manifest has `private: true`; this version is distributed through GitHub release assets, while npm publication is deferred. It retains the MIT notices for Humanizer and Academic Humanizer. The separately preserved full collection is not included in this 90-skill package.

The root [MIT license](../LICENSE) covers project-authored material. It does not relicense third-party material. The import and source-disposition records explain the provenance of the additional skill drafts; those engineering records do not establish legal permission or complete functional parity.

## Separately preserved full collection

The full review ledger maps 118 skill entrypoints (117 from the supplied source families plus the existing `research-assistant` baseline) to 116 canonical methods and two compatibility entries. Its preservation audit accounts for 600 original payload files. Those preservation and test results do not establish a redistribution grant.

| Source family | Evidence retained | Release consequence |
| --- | --- | --- |
| ARMS | The supplied `LICENSE` and the current upstream [`LICENSE`](https://github.com/koaeraser/ARMS/blob/main/LICENSE) state CC BY-NC 4.0. The [license deed](https://creativecommons.org/licenses/by-nc/4.0/) permits sharing and adaptation with attribution and change notices, and prohibits commercial use. | Keep its own terms and attribution. It cannot be represented as covered by the project's MIT license or as unrestricted commercial-use material. The Open Source Definition excludes licenses that restrict fields of endeavor; see [criterion 6](https://opensource.org/osd#6-no-discrimination-against-fields-of-endeavor). A compatible additional grant is required for an unrestricted open-source release. |
| Humanizer | Supplied MIT `LICENSE`, with copyright and upstream acknowledgment retained. | Redistribution is allowed under that license when its notices remain. |
| Academic Humanizer | Supplied MIT `LICENSE` and acknowledgments to Humanizer and ARMS. | Preserve its MIT notices. Its grant does not replace or extend the separate ARMS license. |
| Academic PPTX | The exact supplied archive contains an MIT `LICENSE` and `SKILL.md` metadata that says `Proprietary. LICENSE.txt has complete terms`; the archive contains no `LICENSE.txt`. The current upstream [`LICENSE`](https://github.com/Gabberflast/academic-pptx-skill/blob/main/LICENSE) and [`SKILL.md`](https://github.com/Gabberflast/academic-pptx-skill/blob/main/SKILL.md) still show these conflicting signals. The upstream [issue #6](https://github.com/Gabberflast/academic-pptx-skill/issues/6) asking which terms govern was still open on 2026-11-02. | Resolve the conflicting upstream terms for the exact files before treating the full component as cleared. The MIT file is evidence of a grant, but the unresolved proprietary metadata prevents this review from claiming the scope is settled. |
| LaTeX Document Maker, Research Evidence Finder, Scholar Research | No license file was supplied. Each original `.codex-plugin/plugin.json` names Fasih and links to [Fasih's terms](https://github.com/Fasih38/plugin-pages/blob/main/terms.md). The current terms page, effective September 20, 2026, says the plugin materials belong to the author and does not grant copying, modification, resale, or republication. | Do not redistribute these source materials or their adaptations as cleared MIT material without a separate grant. |
| Research Writing Guardrails | The supplied 1.0.0 bundle's manifests name ANDONG HUANG and contain no license field or license file. No grant is established by the supplied files. This check does not establish that no separate grant exists. | Obtain a grant before redistributing the source material or any adaptation whose rights depend on it. |
| Scientific Visuals & Tables | The supplied 2.2.0 bundle's manifest names Navish Kumar and links to [his homepage](https://kumarnavish.github.io/); no license field or license file was supplied. The homepage publishes a contact address, but does not provide a redistribution license. The source collection includes artwork and other assets. | Obtain rights for the material and assets before redistributing them. |

No attribution, notice, source file, or license was removed from the preserved collection. Rewording or changing a source's surface wording does not itself grant redistribution rights or erase provenance. The project will not present the full mixed-license collection as a single MIT-licensed work while these terms remain unresolved.

## Conditions before full public distribution

Resolve the missing and conflicting grants with the relevant rights holders, or keep affected materials private and create independently authored replacements with a traceable, honest provenance record. Any release that omits components must say so and cannot be described as the complete reviewed collection. Preserve all applicable credits, license texts, and change notices in every permitted distribution.
