# Local workflow runner

`tools/workflow_runner.py` validates and optionally executes a user-maintained JSON manifest of local research phases. The default command prints a dependency-ordered plan and runs nothing. Add `--execute` only after reviewing the manifest's commands and paths.

Create an output directory so the example writes outside the source tree, inspect its plan, then explicitly execute it:

```sh
mkdir .workflow-demo
python -X utf8 -B tools/workflow_runner.py examples/research-workflow.json --root .workflow-demo
python -X utf8 -B tools/workflow_runner.py examples/research-workflow.json --root .workflow-demo --execute --report .workflow-demo/receipt.json
```

The sample commands create synthetic text files only. Replace the sample with commands, inputs, and checks appropriate to the project. `--root` must name an existing directory; without it, paths are based at the manifest's directory. Phase `cwd` and declared output paths are relative to that root and use `/` separators. A report path is relative to the process's current directory. Existing reports and declared phase outputs are refused rather than overwritten; choose a fresh output directory for each run.

Version 1 manifests have a title and 1–100 phases. Each phase contains a unique `id` and a `command` array. Optional fields are `depends_on`, `cwd`, `outputs`, and `timeout_seconds` (default 600; range 1–3600). Commands are ordered as an acyclic dependency graph; independent phases remain runnable when another phase fails, while its dependents are marked blocked. A command's stdout and stderr are forwarded to the terminal. The JSON report records phase status, exit code, command hash, declared output paths, byte sizes, and SHA-256 values; it does not copy command arguments into the report. Keep the manifest itself if the exact commands are needed later.

Commands are started as argument arrays without a shell, but they still run with the current user's permissions and are **not sandboxed**. They may access files or services outside `--root`, spawn other processes, or have external effects. Review every command, avoid putting credentials in arguments, and use the runner only for trusted commands. A timeout applies to the launched process; it does not provide process-tree isolation. A successful exit and file hash record execution facts only: they do not validate the method, data, results, or scientific conclusions.

Exit status is `0` for a valid plan or fully completed run, `1` when an executed phase fails, times out, or is blocked by a dependency, and `2` for an invalid manifest or report destination. This local tool does not discover host skills, invoke model agents, connect research services, or replace the read-only [checkpoint checker](../skills/research-workflow-coordination/references/checkpoint-checker.md).
