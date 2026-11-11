# ARMS integration audit

Audited 25 October 2026. Upstream root: `D:/PLUGIN/work/expanded/ARMS-main`. Only this report and its JSON evidence file were created during the audit. Source originals remain immutable.

Coverage: **69 files, 932,413 bytes, 13 skills, 23 CSVs (322 data rows), 6 one-page PDF figures, 5 Python scripts and one Bash script**. Every file was hashed; all text/data read; code, references and PDF metadata inspected. No expensive experiments, external model loops, source downloading, manuscript compilation or scientific sign-off were performed.

## Integration verdict

Preserve the complete source at `resources/upstream/ARMS-main` and create namespaced active copies. The supplied pipeline is not self-contained without the adaptations below. Only 4 of 13 SKILL files have YAML metadata; the other nine need host registration metadata.

## Required fixes

### ARMS-01: Three invoked helper skills are absent (blocker)

failure-diagnoser, venue-compliance-gate, consistency-auditor are invoked but not shipped. Venue gate defaults off in SKILL (README example says on). Consistency audit is a required final gate.

**Locations:** `skills/research-pipeline/SKILL.md:530`, `skills/research-pipeline/SKILL.md:688`, `skills/research-pipeline/SKILL.md:762`

**Adaptation:** Use separately labelled local replacement role documents with explicit provenance and existence checks, or report gate unavailable. Do not claim these are supplied upstream skills.

### ARMS-02: Canonical shared scoring rubric is not shipped (blocker)

References ~/.claude/skills/_shared/scoring_rubric.md, absent. Embedded paper-grader scoring text exists, but is not proof of the absent canonical severity/escalation document.

**Locations:** `skills/paper-critic/SKILL.md:107`, `skills/paper-critic/SKILL.md:130`, `skills/paper-critic/SKILL.md:205`, `skills/paper-grader/SKILL.md:543`, `skills/research-pipeline/README.md:124`

**Adaptation:** Mark unavailable explicitly; retain embedded rubric as supplied, never fabricate the canonical document.

### ARMS-03: Critic loop edits in place and automatically commits unrelated repository state (high)

Automatic git add -A and commit run on any enclosing Git repository. Snapshots protect main .tex/.pdf only; revisor may edit in place and failed builds do not roll back. Model processes have no wall-clock timeout.

**Locations:** `skills/critic-revisor/run_loop.sh:120`, `skills/critic-revisor/run_loop.sh:469`, `skills/critic-revisor/run_loop.sh:490`, `skills/critic-revisor/run_loop.sh:491`

**Adaptation:** Default Git snapshots off; explicit opt-in, clean-index precondition, bounded manuscript/run paths only. Check all prerequisites before outputs/models. Never run against preserved resources.

### ARMS-04: Private installation paths and Claude APIs require adaptation (high)

Claude Read/Glob/Grep/Bash/Task/Agent/WebSearch/WebFetch and general-purpose subagent_type are host-specific. Private telemetry hook, skill-auditor, apply-proposal script, snapshots and macOS LaunchAgent are absent.

**Locations:** `skills/brief-expander/SKILL.md:61`, `skills/critic-revisor/SKILL.md:21`, `skills/house-style/SKILL.md:53`, `skills/research-pipeline/README.md:151`

**Adaptation:** Resolve bundled skills relative to SKILL directory; execute from resolved absolute paths. Use host equivalents honestly; mark private services unavailable. Project pipeline outputs remain task-local.

### ARMS-05: Case-study executable package is incomplete (high)

Scripts expect/create sibling validated_results, but shipped results are data/mve_production.csv and data/stress_all.csv, not mve_results.csv/stress_tests_combined.csv. Production/sensitivity/real-data/ablation/significance/conditional-coverage generators and raw Housing/Wine inputs are absent. NeurIPS 2025 style and compiled manuscript are absent.

**Locations:** `case-studies/conformal-prediction/code/run_validation.py:30`, `case-studies/conformal-prediction/code/run_validation.py:31`, `case-studies/conformal-prediction/code/generate_figures.py:19`, `case-studies/conformal-prediction/code/generate_figures.py:60`, `case-studies/conformal-prediction/manuscript.tex:4`

**Adaptation:** Preserve as historical example. For a rerun copy full case to writable task workspace and configure output/input directories. Do not equate production data with 500-rep validation simply by renaming. Obtain missing official style/data and rebuild generators separately if reproduction is requested.

### ARMS-06: Conflicting templates and historical narrative (medium)

Root template has author exemplars/manuscript shape/contribution fields missing from skill-local template; skill template has statistics-specific defaults. DISCLAIMER describes absent clinical data/trials_data.csv and two biostatistics case studies. README markets domain-agnostic pipeline; pipeline scope is statistical/biostatistical methodology. Six historic validation iterations exceed present max-three instructions.

**Locations:** `research_brief_template.md`, `skills/research-pipeline/research_brief_template.md`, `DISCLAIMER.md`, `case-studies/conformal-prediction/pipeline_log.md`

**Adaptation:** Use richer root template for new briefs while preserving both originals. Mark clinical disclaimer cross-repo provenance and historic results; do not advertise general-domain autonomous scientific validation.

### ARMS-07: Numerical implementation assumptions must remain visible (medium)

generate_mve_data accepts K but always creates five sources and assumes d>=4. Base model is fitted on the same source observations scored for calibration. Oracle label says test/ground-truth selection but caller supplies target calibration scores. Report CONDITIONAL GO accepts min coverage 0.840 while code marks min<0.85 NO-GO. Method validation of empty/nonfinite/negative input and alpha bounds is absent; RandomState(0) search fixed.

**Locations:** `case-studies/conformal-prediction/code/run_validation.py:41`, `case-studies/conformal-prediction/code/run_validation.py:283`, `case-studies/conformal-prediction/code/run_validation.py:288`, `case-studies/conformal-prediction/code/run_validation.py:763`, `case-studies/conformal-prediction/code/comparators.py:293`, `case-studies/conformal-prediction/code/method.py:105`

**Adaptation:** Treat code as demonstration, not general validated conformal library; document parameter domain and compare exact scripts/data before any new scientific claim. Formal deployed data-dependent-weight guarantee is acknowledged missing in manuscript.

### ARMS-08: Style metrics are portable diagnostics with parser limits (medium)

Stdlib only. Ignores paragraphs <=40 tokens, uses regex rather than TeX parser, does not follow input/include, locale-default decoding errors ignored. include-appendix still stops at bibliography, so appendices after bibliography are not included. --ref/--genre missing arguments can IndexError; unknown genre is unchecked; successful --gate always exits zero by design. Default full exemplar is not distributed.

**Locations:** `skills/house-style/scripts/style_metrics.py:46`, `skills/house-style/scripts/style_metrics.py:127`, `skills/house-style/scripts/style_metrics.py:165`, `skills/house-style/scripts/style_metrics.py:200`, `skills/house-style/scripts/style_metrics.py:244`

**Adaptation:** Keep advisory. Supply accessible user exemplar with --ref. Do not interpret metric CLI success as manuscript, style or scientific approval.

## Dependencies and external access

No pinned or minimum dependency versions are supplied. The style-metrics utility is Python standard library only. Numerical scripts require **NumPy, SciPy, pandas, Matplotlib and scikit-learn**. README omits scikit-learn. The bundled Codex Python has NumPy 2.3.5/pandas 3.0.1/pypdf 6.10.0, but lacks SciPy/Matplotlib/scikit-learn. System Python 3.14 has NumPy 2.4.2, SciPy 1.17.1, pandas 3.0.1 and Matplotlib 3.10.8; scikit-learn remains unavailable. No installation was performed.

Critic-loop dependencies: `Bash`, `claude (authenticated)`, `codex (authenticated)`, `latexmk`, `latexdiff`, `pdflatex/TeX engine`, `md5 or md5sum`, `dirname`, `basename`, `date`, `mkdir`, `cp`, `find`, `xargs`, `grep`, `tail`, `seq`, `cat`, `awk`, `rm`, `sleep`, `kill`, `timeout or gtimeout optional; shell watchdog fallback`, `git optional; original enabled automatically`.

LaTeX dependencies: `article`, `neurips_2025 (missing)`, `inputenc`, `fontenc`, `hyperref`, `url`, `booktabs`, `amsfonts`, `amsmath`, `amssymb`, `amsthm`, `nicefrac`, `microtype`, `xcolor`, `graphicx`, `algorithm`, `algorithmic`, `natbib`, `multirow`, `subcaption`, `tikz (shapes.geometric, arrows.meta, positioning, fit, calc, decorations.pathreplacing)`, `plainnat.bst`, `BibTeX`.

The script delegates network access to authenticated Claude/Codex CLIs and to host WebSearch/WebFetch. It does not directly call HTTP APIs. Two reviews are labelled Opus but no `--model` is passed, so the configured Claude default actually decides the model. `codex` similarly uses configured settings. Reviewer non-editing and source-claim checks are prompt rules, not filesystem enforcement; Write is enabled. Source-pack directory discovery stops at depth two, accepts `.tex/.pdf/.md/.txt`, excludes CSV/Bib files, resolves relative source paths after changing to manuscript CWD, and trims through `xargs` (problematic quoting/backslashes).

## License and provenance

Upstream `LICENSE` states CC BY-NC 4.0: retain attribution and license link, mark modifications, preserve noncommercial terms and do not impose additional restrictions. License copyright is 2026 with no named holder. Retain README/DISCLAIMER and verified archive-origin attribution. No separate licenses for code, data or PDFs were found. ARMS must not be relabelled MIT or commercially unrestricted.

## Data and PDF checks

All 23 CSVs parsed, with no empty/nonfinite cells and no observed coverage/p-value values outside [0,1]. These are schema/range checks, not scientific validation. Most core production/stress rows report 2,000 replicates; sensitivity/real-world/high-dimensional rows report 500. The 322 records are summary results, not per-replicate raw data. CSV schemas, methods, scenarios and counts are recorded in JSON.

All six PDFs parse without encryption; each has one page. Five were generated by Matplotlib 3.9.4 on 24 March 2026, +08:00; method_overview.pdf was generated by pdfTeX 1.40.26 / TeX Live 2024. Exact metadata, dimensions and extracted text are in JSON. These are figure PDFs, not the compiled paper. Four includegraphics paths in manuscript.tex resolve; method overview is inline TikZ, and two supplied PDFs are not external includegraphics targets.

The manuscript has 17 bibliography entries, 16 cited keys, no missing citation keys, no duplicate labels or unresolved static refs. One uncited key is `diakonikolas2019algorithmic`. References were parsed but not independently verified against publishers.

## Safe representative checks

- Five Python files parse via ast.parse.
- Bash syntax check passes (`bash -n`); first Git Bash invocation was sandbox-blocked and a read-only approved retry passed.
- style_metrics.py CLI passes with compare/sections/JSON and with legacy gate alias plus a supplied reference. Measurements remain advisory.
- A tiny deterministic DISCOMCP fit/predict and five comparator fits pass on system NumPy/SciPy. The arbitrary test scores were used for API/invariant checks, not a coverage experiment.
- WeightedConformal/full run_validation were not run: scikit-learn is absent, and importing run_validation creates validated_results at module scope.
- No plotting was run: generate_figures performs 200 fits for weight analysis and does not recreate the shipped publication PDFs.

## Preservation check

Recomputed all 69 source SHA-256 hashes at audit closure: no changed files and no extra upstream files. Per-file hashes and evidence are in `arms-audit.json`.

## Namespaced active skills

`arms-brief-expander`, `arms-critic-revisor`, `arms-house-style`, `arms-literature-lead`, `arms-methodology-architect`, `arms-paper-critic`, `arms-paper-fixer`, `arms-paper-grader`, `arms-paper-modeler`, `arms-paper-writer`, `arms-research-pipeline`, `arms-validate-method`, `arms-write-manuscript`.

## Active adapter implementation

`build_tools/adapt_arms.py` exports `adapt_arms(package_root: Path) -> list[dict]` and returns changed active paths, before/after hashes and adaptation notes. It changes active ARMS markdown and the critic loop only. Missing upstream rubric/private features stay visibly unavailable; helper calls refer to separately authored agents/failure-diagnoser.md, agents/consistency-auditor.md and agents/venue-compliance-gate.md with existence checks.

Critic changes: dependency preflight before outputs/models, safe --preflight exit, positive round-count/.tex validation, Git snapshots off unless ARMS_ENABLE_GIT_SNAPSHOT=1, existing repository and clean index required, index rechecked before snapshots, and stage/commit pathspecs restricted to the manuscript and current run directory. No automatic add -A remains in the adapted script.

Six adapter tests pass. Full current acceptance suite: 28 tests pass with 3 environment-dependent skips. Bash syntax/preflight and snapshot helper tests use copied fixtures/stub CLIs and temporary repositories; no model loop was run. Git Bash required approved escalation due sandbox MSYS named-object denial. Upstream hashes were rechecked after tests: all 69 unchanged, no extra files.

Residual limitations: missing canonical rubric and third-party setup cannot be fabricated; actual scholarly connections/model credentials are separate; production case-study reproduction and parser limitations remain as documented. The critic still revises task manuscripts in place and uses configured model defaults.
