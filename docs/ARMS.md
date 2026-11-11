# ARMS integration and execution

All 13 ARMS skills, their full instructions and support files are active under `skills/arms-*`. The entire 69-file supplied repository is preserved at `resources/upstream/ARMS-main`, including 23 CSVs, six PDF figures, manuscript/bibliography, five Python scripts, the Bash loop, methodology specification, brief templates, validation report and pipeline logs. These are supplied historical artifacts.

## Portable resources

From an active ARMS skill directory, resolve sibling skills under `../arms-<name>/` and repository assets under `../../resources/upstream/ARMS-main/`. Resolve paths to absolute paths before passing them to a shell from another working directory. Never assume `~/.claude/skills`, `~/.codex/skills`, `/Users/...` or `/home/...` exists on the user's machine. Active adapters replace resolvable private paths and document missing resources. Original instructions remain available for comparison.

## Missing upstream components

- `~/.claude/skills/_shared/scoring_rubric.md` was not supplied. The exact private scoring rubric cannot be restored from this snapshot. The full embedded grader/reviewer instructions remain usable, with any substitute criteria disclosed.
- `/failure-diagnoser`, `/consistency-auditor` and optional `/venue-compliance-gate` source folders were not supplied. The integration provides clearly identified procedural replacement roles in `agents/`. They specify inputs, operations, outputs and gates; they are not the missing original skills/tools.
- Private telemetry/auditor/apply/LaunchAgent and service infrastructure described in the pipeline README were not supplied. Their specifications are retained and their operational status is unavailable.
- The case-study manuscript refers to `neurips_2025.sty`, which is absent. No compiled manuscript PDF was supplied. These dependencies must be resolved before claiming a full manuscript build. The six figure PDFs remain inspectable.
- The disclaimer mentions a clinical `trials_data.csv`/ARMS-Biostat context not present in this snapshot. That claim is retained as historical source text and is not evidence of a bundled clinical dataset.

## Scientific Python

`method.py` uses NumPy and SciPy. Comparators/validation additionally use scikit-learn; the full validation and plotting use pandas/matplotlib and may retrieve benchmark data. The supplied `run_validation.py` is an expensive experiment suite and `generate_figures.py` can regenerate evidence files. Work on a task copy; do not overwrite preserved supplied results. A small deterministic method test is recorded in the audit; it does not reproduce all published/historical results or establish scientific validity/novelty.

## Optional critic/revisor loop

The active `skills/arms-critic-revisor/run_loop.sh` preserves the review/revise/build workflow with recorded safety/portability adaptations. The original is unchanged under resources. It requires Bash/WSL, authenticated Claude and Codex CLIs, Python, latexmk and latexdiff. It can spend model credits and edits the specified manuscript in place; invoke only when the user requests that loop and has authorized that manuscript work.

The active script checks dependencies before creating outputs. Automatic Git snapshotting is disabled by default. Explicit `ARMS_ENABLE_GIT_SNAPSHOT=1` opt-in enables scoped snapshots only when the index starts clean; unrelated staged work must not be included. The integration adapter and its tests record the exact behavior. No loop was executed during package construction. Model names in upstream examples express requirements and do not prove model access.

Example (in a configured Bash environment, from a task copy):

```bash
bash /absolute/plugin/skills/arms-critic-revisor/run_loop.sh /absolute/project/manuscript.tex 2 venue
```

Read the full skill before invoking. Do not run scripts inside provenance resources when an active adapted copy exists. Record failures and actual build/review receipts per round; never fill missing reviews with invented acceptance text.
