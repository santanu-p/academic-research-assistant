# Check a recorded workflow checkpoint

The optional standard-library tool `tools/pipeline_checkpoint.py` checks a local JSON record without running the workflow. It checks phase identifiers and dependencies, the presence of recorded successful checks for completed phases, and the SHA-256 hashes of explicitly listed artifacts. It reports effective states without changing the checkpoint, the artifacts or any host settings. A recorded `passed` value and its evidence description are author assertions: the tool does not run or authenticate the underlying check, verify scientific conclusions, or prove a workflow complete.

Save a checkpoint beside the artifacts it names. For example, this hypothetical checkpoint records one completed phase and one pending dependent phase. Replace the placeholder evidence and include actual artifact hashes only after independently checking the real files:

```json
{
  "phases": [
    {"id": "design", "state": "completed", "depends_on": [],
     "checks": [{"passed": true, "evidence": "Replace with the actual review record"}]},
    {"id": "analysis", "state": "pending", "depends_on": ["design"]}
  ]
}
```

Run `python -X utf8 -B tools/pipeline_checkpoint.py /path/to/checkpoint.json`. Optional `artifacts` are objects like `{"path":"results/table.csv","sha256":"<64 hexadecimal characters>"}`. Paths use forward slashes, must be relative to the checkpoint directory and may not escape it after link resolution. The path check and opening the file are separate operations, so use trusted directories that are not being concurrently modified; this is not a security boundary against hostile file replacement. Files over 256 MiB are reported unavailable; checkpoint input is limited to 1 MB and 500 phases. SHA-256 describes byte identity, not accuracy or authorship. Do not paste credentials or sensitive research data into evidence descriptions.

Phases may be `pending`, `in_progress`, `completed`, `failed`, or `blocked`. A completed phase with missing or failed recorded checks, changed or unavailable artifacts, or an incomplete dependency becomes `needs_recheck` in the report; its dependent phases are also marked for rechecking or blocked. Pending phases with completed dependencies remain pending. The process returns 0 when no phase is blocked, failed or needs rechecking, 1 when such a state exists, and 2 for invalid input or execution failure. Exit 0 does not mean that pending phases have been executed or that the scientific result is valid.

The lifecycle guide's human-readable **Active** corresponds to `in_progress` here; **Stopped** can be recorded as `failed` or `blocked` according to the reason. `needs_recheck` is an effective report state, not an accepted input state. Revise the checkpoint deliberately after addressing the reason; the checker never writes that transition for you.
