# Dependencies and connection requirements

## Core plugin

Node.js **22+** runs the configured local MCP server without npm dependencies or API keys. Python 3.10+ is optional for the alternate Python server and supplied Python tools. A compatible local Codex/agent host provides the model, skill discovery, file access, process execution and permission enforcement. Cloud/mobile clients cannot run the local process by account saving alone.

## Optional supplied functionality

| Component | Requirement | Connection/execution status |
|---|---|---|
| Literature/evidence skills | Host search/browser or authenticated scholarly connector; database access for subscription material | No search MCP endpoint/configuration or credentials supplied; not bundled or automatically connected |
| LaTeX documents | TeX Live/MiKTeX/Tectonic or host compiler; latexmk, biber/BibTeX when used | Detect locally; package supplies instructions/templates, not a TeX distribution |
| LaTeX revision comparison | `latexdiff` and Tectonic | `tools/latex_revision.py` invokes them only when explicitly run; both are installed separately |
| Conversion | Pandoc/LaTeXML/make4ht as selected; optional Word/Docs backend | Install separately; original sources explain format limitations |
| Academic PPTX | Host presentation skill/backend; optional `python-pptx`; LibreOffice and PDF renderer for rendering | Content and structure skill supplied. `tools/presentation_builder.py` creates basic editable decks; it does not replace a full presentation authoring backend |
| Visual plotting templates | numpy, matplotlib; optional pandas for data workflows | Actual source templates and example retained; install into the Python used to run them |
| Raster QA | Pillow; PyMuPDF (`fitz`) for PDF rendering | `visual_qa.py` requires relevant renderer; other checks remain available |
| Standalone workflow, rubric, checkpoint, and revision helpers | Python standard library; `python-pptx` for slide generation; optional plotting and QA packages | Tools run directly when invoked; the MCP server does not execute them |
| External-skill preflight and handoff | Node.js 22+ | Local filesystem checks only; does not install, register, or activate external skills |
| Reference selection / table QA | Python stdlib | `select_references.py`, `table_qa.py`; no external service |
| ARMS mathematical method | numpy, scipy | Small deterministic smoke calculation tested; full empirical validation is separate |
| ARMS validation/figures | numpy, scipy, pandas, scikit-learn, matplotlib; dataset access for fetched benchmarks | Historical outputs retained; original experiments not automatically rerun |
| ARMS style metrics | Python stdlib | Supplied script with advisory metrics and `--ref` for a user exemplar |
| ARMS critic/revisor | Bash/WSL, Claude CLI, Codex CLI, their authenticated model access; python, latexmk, latexdiff, optional Git | Never activated automatically; see ARMS.md and active script preflight |
| Statistical/meta-analysis advice | R/metafor/meta, Python stats packages, RevMan or other user-selected software as described upstream | Method guidance retained; no implementation is implied for every named software package |
| Citation managers and academic services | User's Zotero/Mendeley/EndNote/Paperpal/Overleaf/etc. installation/account | Links and workflow specifications retained; not bundled, authenticated or verified integrations |

The configured Node server’s `environment_status` reports executable presence on its PATH and probes module presence in the Python interpreter it finds there. If Python is unavailable or its probe fails, module status is unknown rather than absent. Presence does not establish full compatibility, successful execution, licenses or authentication. The verification report records which commands were actually exercised here.

## Setup examples

Use a project virtual environment; choose only the optional dependencies needed for the task:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-optional.txt
```

This is a documented user setup command; it is not run by installation. To use a virtual environment for optional Python tools, activate it or configure those tools to use its Python. The default MCP server remains Node; its Python module probe uses the interpreter on the server’s PATH. Do not put credentials in plugin files.

For an external MCP service: use the service's verified official endpoint, transport, authentication and scopes in a host-managed connection; make a harmless read/query and record the receipt. No external MCP service configuration was present in the nine supplied top-level items, so this package registers only its implemented local server. Source plugin install IDs identify upstream packages and are not MCP server URLs or connection authorizations.
