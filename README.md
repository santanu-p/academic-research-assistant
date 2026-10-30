# Academic Research Assistant

A toolkit for research planning, literature work, scientific reasoning, writing, figures, and academic documents. Version 3.1.0 combines 38 skills from the existing public v3 source, 50 additional skills, and the separately credited MIT Humanizer and Academic Humanizer projects, plus a local MCP server and optional Python tools.

Skills are methods that a host assistant reads and follows. The MCP server discovers and reads these methods; it does not search scholarly databases, generate research results, compile documents, or call models by itself. External research tools remain separately configured host capabilities. Routing is advisory and recognizes only some explicit exclusions; check suggestions against the full request.

This incremental release contains 90 skills. It is not yet demonstrated to reproduce all 118 workflows in the separately preserved full collection. [Import mapping](docs/independent-skill-import.json) records how the 50 additional skills were included, including two renamed to avoid replacing existing skills; [Humanizer mapping](docs/humanizer-source-map.json) records the upstream source files.

The separately preserved full collection has different license terms and is not part of this package. This release does not claim complete functional parity or redistribution rights for that collection.

## Quick start

Requires Node.js 22 or later. No Node dependencies or account setup are needed for the local CLI.

```sh
git clone https://github.com/santanu-p/academic-research-assistant.git
cd academic-research-assistant
node cli/ara.mjs --help
node cli/ara.mjs list
node cli/ara.mjs route "plan a systematic literature review"
node cli/ara.mjs verify
```

You can also use the downloadable release archive after extracting it. Registry installation depends on publication to npm; check the registry before relying on an `npx` command.

## Use with a host

Run exports from this project directory. Choose a new destination: existing folders are refused. Export/install copy the complete runtime bundle and print the next steps. They do not change host settings or install host applications.

| Host/profile | Command |
| --- | --- |
| Codex local marketplace | ` node cli/ara.mjs export --host codex --target ../ara-codex-marketplace ` |
| Claude Code plugin | ` node cli/ara.mjs export --host claude --target ../ara-claude-plugin ` |
| Antigravity plugin | ` node cli/ara.mjs export --host antigravity --target ../ara-antigravity-plugin ` |
| Codex single entry skill | ` node cli/ara.mjs export --host codex-skill --target ../ara-codex-skill ` |
| Claude single entry skill | ` node cli/ara.mjs export --host claude-skill --target ../ara-claude-skill ` |
| Antigravity single entry skill | ` node cli/ara.mjs export --host antigravity-skill --target ../ara-antigravity-skill ` |
| Other assistant / local MCP | ` node cli/ara.mjs export --host generic --target ../ara-generic ` |

The profiles emit local files only. A local export does not establish activation in Codex, Claude, or Antigravity. Claude and Antigravity wrappers contain the complete nested bundle as one outer skill; keep that bundle intact. Antigravity MCP configuration is optional and uses the installed bundle's absolute path. Generic compatibility depends on the host supporting local files, Agent Skills, or stdio MCP.

See [host setup](docs/DRAFT-SETUP.md) for registration commands and verification limits. The historical [v3 installation guide](docs/INSTALLATION.md) is retained as a reference. Each export prints its own follow-up steps.

For separately installed skills, the setup guide also describes an opt-in local preflight that checks only user-specified paths. Actual registration and invocation depend on the host; the preflight does not connect external services or establish permission to use third-party material.

## Research coverage

The [skill catalog](catalog/skills.json) lists all methods. Start with [research-assistant](skills/research-assistant/SKILL.md), which routes by research stage. Every skill shares the [research contract](docs/RESEARCH-CONTRACT.md): preserve evidence, identify assumptions, distinguish completed work from proposals, and verify artifacts before claiming completion.

Coverage includes research questions, methods, literature searching and appraisal, systematic reviews, meta-analysis, quantitative and qualitative analysis, citations, research integrity, proposals and planning, scientific models and validation, manuscript preparation and revision, LaTeX production and repair, conversion, figures and tables, slides, posters, theses, professional documents, teaching materials, and public communication.

## Executable tools

Python 3.10+ is optional and separate from the Node runtime.

| Tool | Purpose | Additional libraries |
| --- | --- | --- |
| ` tools/prose_metrics.py ` | Descriptive prose counts and optional exemplar comparison | None |
| ` tools/table_qa.py ` | Inspect delimited numerical tables and uncertainty notation | None |
| ` tools/visual_qa.py ` | Inspect SVG, raster, or PDF artifacts | Pillow for raster; PyMuPDF for PDF |
| ` tools/scientific_visuals.py ` | Plot comparisons, intervals, grouped observations, paired data, grids and Pareto frontiers; calculate opaque color contrast | NumPy, Matplotlib for plotting; contrast calculation needs none |
| ` tools/presentation_builder.py ` | Create a simple slide deck with editable text and optional supplied images | python-pptx |
| ` tools/text_revision_report.py ` | Create a text-level HTML comparison of two saved versions | None |
| ` tools/pipeline_checkpoint.py ` | Check recorded phase dependencies and artifact hashes | None |
| ` tools/revise.py ` | Run two reviewers and a reviser supplied as explicit command arrays | None; caller supplies commands |

```sh
python -X utf8 -B tools/prose_metrics.py draft.md --json
python -X utf8 -B tools/table_qa.py results.tsv --json
python -X utf8 -B tools/presentation_builder.py --help
python -X utf8 -B tools/text_revision_report.py --help
python -X utf8 -B tools/pipeline_checkpoint.py --help
python -X utf8 -B examples/scientific_figures.py --out outputs/synthetic
python -X utf8 -B tools/revise.py --help
```

See the [scientific helper API](skills/scientific-visuals/references/api.md), [presentation guidance](skills/presentations-posters/SKILL.md), and [revision runner](docs/REVISION-RUNNER.md). The PowerPoint helper creates basic editable text and shapes and can embed supplied images; inspect each resulting slide for fit and meaning. The revision report compares plain text approximately; it does not interpret LaTeX or produce tracked PDFs. Inspection reports are aids to review, not scientific or stylistic certificates. No plagiarism or AI-authorship detector is included.

For a synthetic PowerPoint example, install the optional `python-pptx` library in your Python environment and run `python -X utf8 -B tools/presentation_builder.py examples/presentation.json example.pptx`. Choose a new output path; the builder refuses to overwrite an existing file. The sample contains placeholders, not research results.

## Develop and package

```sh
npm run build
npm run validate
npm test
python -X utf8 -B -m unittest discover -s tests/python
npm pack
```

No ` npm install ` is required for the Node runtime. Python tests involving optional libraries report skips when those libraries are absent. Developer tests, generated outputs, and private recovery material are excluded from the npm tarball. See [development](docs/DEVELOPMENT.md), the historical [v3 release record](docs/RELEASE.md), and the historical [v3 source disposition](docs/SOURCE-DISPOSITION.md).

The two MIT Humanizer sources are included with their notices. Other supplied source collections and previous private integrations are not vendored here. [LICENSE](LICENSE) covers this project's newly authored code and text; [third-party notices](THIRD_PARTY_NOTICES.md) describe the separate source licenses. Rewriting existing third-party material would not remove its license conditions.
