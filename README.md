# Academic Research Assistant

An MIT-licensed toolkit for research planning, literature work, scientific reasoning, writing, figures, and academic documents. It contains 38 research skills, a dependency-free local MCP server, optional Python inspection/plotting tools, and an explicit-command revision runner.

Skills are methods that a host assistant reads and follows. The MCP server discovers and reads these methods; it does not search scholarly databases, generate research results, compile documents, or call models by itself. External research tools remain separately configured host capabilities.

## Install from GitHub

Download the npm tarball from [GitHub Releases](https://github.com/santanu-p/academic-research-assistant/releases), or clone the editable source:

```sh
git clone https://github.com/santanu-p/academic-research-assistant.git
cd academic-research-assistant
```

The release also includes a portable plugin ZIP and SHA-256 checksums. For local tarball installation, see [installation](docs/INSTALLATION.md#before-npm-publication).

## Try the local source

Requires Node.js 22 or later. No Node dependencies or account setup are needed.

```sh
node cli/ara.mjs --help
node cli/ara.mjs list
node cli/ara.mjs route "plan a systematic literature review"
node cli/ara.mjs verify
```

Before npm publication, use the local source or the release tarball. After publication the equivalent entry point will be ` npx academic-research-assistant@3.0.0 --help `. The npm name is proposed; availability and publication have not been verified.

## Use with a host

Run exports from this project directory. Choose a new destination: existing folders are refused. Export/install copy the complete runtime bundle and print the next steps. They do not change host settings or install host applications.

| Host/profile | Command |
| --- | --- |
| Codex local marketplace | ` node cli/ara.mjs export --host codex --target ../ara-codex-marketplace ` |
| Claude Code plugin | ` node cli/ara.mjs export --host claude --target ../ara-claude-plugin ` |
| Codex single entry skill | ` node cli/ara.mjs export --host codex-skill --target ../ara-codex-skill ` |
| Claude single entry skill | ` node cli/ara.mjs export --host claude-skill --target ../ara-claude-skill ` |
| Other assistant / local MCP | ` node cli/ara.mjs export --host generic --target ../ara-generic ` |

The plugin profiles expose individual skills. The single-entry profiles use the root [SKILL.md](SKILL.md) to route to nested methods; keep the entire directory together. Generic compatibility depends on the host supporting local files, Agent Skills, or stdio MCP. There is no claim that every CLI or app supports these interfaces.

See [installation and host support](docs/INSTALLATION.md) for registration commands and the verification boundary.

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
| ` tools/scientific_visuals.py ` | Plot comparisons, intervals, trends and Pareto frontiers | NumPy, Matplotlib |
| ` tools/revise.py ` | Run two reviewers and a reviser supplied as explicit command arrays | None; caller supplies commands |

```sh
python -X utf8 -B tools/prose_metrics.py draft.md --json
python -X utf8 -B tools/table_qa.py results.tsv --json
python -X utf8 -B examples/scientific_figures.py --out outputs/synthetic
python -X utf8 -B tools/revise.py --help
```

See the [scientific helper API](skills/scientific-visuals/references/api.md) and [revision runner](docs/REVISION-RUNNER.md). Inspection reports are aids to review, not scientific or stylistic certificates. No plagiarism or AI-authorship detector is included.

## Develop and package

```sh
npm run build
npm run validate
npm test
python -X utf8 -B -m unittest discover -s tests/python
npm pack
```

No ` npm install ` is required for the Node runtime. Python tests involving optional libraries report skips when those libraries are absent. Developer tests, generated outputs, and private recovery material are excluded from the npm tarball. See [development](docs/DEVELOPMENT.md), [release preparation](docs/RELEASE.md), and [source disposition](docs/SOURCE-DISPOSITION.md).

Version 3 is newly authored public source. Supplied source collections and previous private integrations are not vendored. [LICENSE](LICENSE) covers this project's new code and text; [third-party notices](THIRD_PARTY_NOTICES.md) describe the boundary. Rewriting existing third-party material would not remove its license conditions.
