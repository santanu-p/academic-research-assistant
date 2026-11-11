# Dependencies and connection requirements

## Core plugin

Python **3.10+** on PATH as `python`, with its standard library, runs the local MCP server. No packages or API keys are required for its five tools. A compatible local Codex/agent host provides the model, skill discovery, file access, process execution and permission enforcement. Cloud/mobile clients cannot run the local process by account saving alone. The root `requires_local_executor` flag states this requirement.

## Optional supplied functionality

| Component | Requirement | Connection/execution status |
|---|---|---|
| Literature/evidence skills | Host search/browser or authenticated scholarly connector; database access for subscription material | No search MCP endpoint/configuration or credentials supplied; not bundled or automatically connected |
| LaTeX documents | TeX Live/MiKTeX/Tectonic or host compiler; latexmk, biber/BibTeX when used | Detect locally; package supplies instructions/templates, not a TeX distribution |
| Conversion | Pandoc/LaTeXML/make4ht as selected; optional Word/Docs backend | Install separately; original sources explain format limitations |
| Academic PPTX | Host presentation skill/backend, or python-pptx/PptxGenJS; LibreOffice and PDF renderer for rendering | Content and structure skill supplied; upstream `pptx` authoring skill and its docs are absent |
| Visual plotting templates | numpy, matplotlib; optional pandas for data workflows | Actual source templates and example retained; install into the Python used to run them |
| Raster QA | Pillow; PyMuPDF (`fitz`) for PDF rendering | `visual_qa.py` requires relevant renderer; other checks remain available |
| Reference selection / table QA | Python stdlib | `select_references.py`, `table_qa.py`; no external service |
| ARMS mathematical method | numpy, scipy | Small deterministic smoke calculation tested; full empirical validation is separate |
| ARMS validation/figures | numpy, scipy, pandas, scikit-learn, matplotlib; dataset access for fetched benchmarks | Historical outputs retained; original experiments not automatically rerun |
| ARMS style metrics | Python stdlib | Supplied script with advisory metrics and `--ref` for a user exemplar |
| ARMS critic/revisor | Bash/WSL, Claude CLI, Codex CLI, their authenticated model access; python, latexmk, latexdiff, optional Git | Never activated automatically; see ARMS.md and active script preflight |
| Statistical/meta-analysis advice | R/metafor/meta, Python stats packages, RevMan or other user-selected software as described upstream | Method guidance retained; no implementation is implied for every named software package |
| Citation managers and academic services | User's Zotero/Mendeley/EndNote/Paperpal/Overleaf/etc. installation/account | Links and workflow specifications retained; not bundled, authenticated or verified integrations |

`environment_status` reports executable/module **presence in the server's Python environment only**, not full compatibility, successful execution, licenses or authentication. The verification report records which commands were actually exercised here.

## Setup examples

Use a project virtual environment; choose only the optional dependencies needed for the task:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-optional.txt
```

This is a documented user setup command; it is not run by installation. To use a virtual environment for MCP, configure the host's command to that environment's Python while preserving the packaged script argument. Do not put credentials in plugin files.

For an external MCP service: use the service's verified official endpoint, transport, authentication and scopes in a host-managed connection; make a harmless read/query and record the receipt. No external MCP service configuration was present in the nine supplied top-level items, so this package registers only its implemented local server. Source plugin install IDs identify upstream packages and are not MCP server URLs or connection authorizations.
