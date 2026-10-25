# Explicit-command revision runner

The runner coordinates two caller-supplied reviewers and one reviser. It has no built-in model provider, credentials, Git actions or package installations. Start with ` python -X utf8 -B tools/revise.py --help ` for the authoritative options.

```text
python tools/revise.py manuscript.tex \
  --reviewer '["python","/absolute/path/review_technical.py"]' \
  --reviewer '["python","/absolute/path/review_argument.py"]' \
  --reviser '["python","/absolute/path/revise_draft.py"]' \
  --out new-run-directory \
  --source evidence.csv --rounds 3 --timeout 600
```

This example uses POSIX shell quoting; in PowerShell pass each JSON command array as one quoted string. Use absolute executable/script paths. Commands run with the manuscript's parent as their working directory. The default is preflight: validate paths and command declarations without launching them or creating the run directory. Add ` --execute ` only when ready to run the specified programs.

Each command receives a JSON request on stdin. Reviewers receive distinct technical and argument instructions plus the actual target text, hash and evidence context. They return JSON with ` decision ` equal to ` accept `, ` revise `, or ` stop ` and ` issues ` containing objects with ` id `, ` severity ` (` major ` or ` minor `), ` location `, and ` comment `. Acceptance cannot contain major issues. Reviewers must not edit the target. The reviser edits the actual target and returns ` changes ` and ` unresolved ` as arrays of strings. Follow-up reviews record dispositions for earlier issues. See the runner's request JSON and fixture tests when implementing adapters.

The runner snapshots the manuscript and sidecars, preserves supplied evidence bytes, and records command arrays, prompts, outputs, errors, timings and hashes in the new run directory. Binary evidence is identified as binary; the runner does not pretend to extract or interpret its contents. Receipts can contain sensitive manuscript data and source paths; store them according to the project's access requirements.

Command timeouts terminate the command's process tree using a Windows Job Object or a POSIX process group. Windows processes are assigned before execution starts. Input and output use receipt files so inherited pipes cannot hold the runner open. POSIX processes that deliberately detach can escape their group; this runner is not an operating-system sandbox. The POSIX branch has not been executed in this Windows release verification.

Optional `--check` command arrays perform project-specific checks. For execution, return code 0 means both reviewers accepted and configured checks succeeded; successful preflight also returns 0 without running any review. Code 3 means the round budget was exhausted; 4 means a scientific stop; 2 means an input, command or protocol failure. These are orchestration states, not proof that a manuscript is correct or publishable. Two reviewer commands may use the same system; independence of the underlying models or scientific judgment remains the caller's responsibility.
