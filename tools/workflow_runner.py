"""Plan or explicitly execute caller-defined research workflow commands.

Commands run as argument arrays without a shell. They are not sandboxed and
run with the permissions of the current user; dry-run is the default.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

MAX_WORKFLOW_BYTES = 1_000_000
MAX_PHASES = 100
MAX_ARGS = 100
MAX_ARGUMENT_LENGTH = 4096
MAX_OUTPUT_BYTES = 256 * 1024 * 1024
DEFAULT_TIMEOUT_SECONDS = 600
MAX_TIMEOUT_SECONDS = 3600
PHASE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
RUNNER_NOTE = (
    "Commands are supplied by the caller, run sequentially without a shell, "
    "and are not sandboxed. A successful command and output hash do not validate research."
)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def _reject_constant(value: str):
    raise ValueError(f"invalid JSON number: {value}")


def _fields(value, required: set[str], optional: set[str], label: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    keys = set(value)
    missing = required - keys
    extra = keys - required - optional
    if missing:
        raise ValueError(f"{label} is missing fields: {', '.join(sorted(missing))}")
    if extra:
        raise ValueError(f"{label} has unknown fields: {', '.join(sorted(extra))}")
    return value


def _clean_text(value, label: str, *, allow_empty: bool = False, limit: int = 1000) -> str:
    if not isinstance(value, str) or len(value) > limit or "\x00" in value:
        raise ValueError(f"{label} must be text of at most {limit} characters")
    if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise ValueError(f"{label} must contain valid Unicode text")
    if not allow_empty and not value.strip():
        raise ValueError(f"{label} must not be empty")
    return value


def _relative_path(value, label: str, *, allow_dot: bool = False) -> str:
    value = _clean_text(value, label, limit=1024)
    if allow_dot and value == ".":
        return value
    parts = value.split("/")
    path = PurePosixPath(value)
    if (path.is_absolute() or "\\" in value or ":" in value or
            any(part in ("", ".", "..") for part in parts)):
        raise ValueError(f"{label} must be a safe relative path using '/' separators")
    return value


def validate_workflow(data: dict) -> tuple[dict, list[dict]]:
    document = _fields(data, {"version", "title", "phases"}, set(), "workflow")
    if type(document["version"]) is not int or document["version"] != 1:
        raise ValueError("workflow.version must be 1")
    title = _clean_text(document["title"], "workflow.title", limit=300).strip()
    phases = document["phases"]
    if not isinstance(phases, list) or not 1 <= len(phases) <= MAX_PHASES:
        raise ValueError(f"workflow.phases must contain 1 to {MAX_PHASES} entries")

    by_id = {}
    for index, item in enumerate(phases, 1):
        label = f"phases[{index}]"
        phase = _fields(item, {"id", "command"},
                        {"depends_on", "cwd", "outputs", "timeout_seconds"}, label)
        identifier = _clean_text(phase["id"], f"{label}.id", limit=80)
        if not PHASE_ID.fullmatch(identifier) or identifier in by_id:
            raise ValueError(f"{label}.id must be unique and use letters, digits, hyphens or underscores")

        command = phase["command"]
        if not isinstance(command, list) or not 1 <= len(command) <= MAX_ARGS:
            raise ValueError(f"{label}.command must be a list of 1 to {MAX_ARGS} arguments")
        args = [_clean_text(arg, f"{label}.command argument", allow_empty=True,
                            limit=MAX_ARGUMENT_LENGTH) for arg in command]
        if not args[0].strip():
            raise ValueError(f"{label}.command executable must not be empty")

        deps = phase.get("depends_on", [])
        if (not isinstance(deps, list) or not all(isinstance(dep, str) and PHASE_ID.fullmatch(dep)
                                                  for dep in deps) or
                len(set(deps)) != len(deps)):
            raise ValueError(f"{label}.depends_on must contain distinct phase IDs")
        if identifier in deps:
            raise ValueError(f"{label} cannot depend on itself")

        cwd = _relative_path(phase.get("cwd", "."), f"{label}.cwd", allow_dot=True)
        outputs = phase.get("outputs", [])
        if not isinstance(outputs, list) or len(outputs) > 100:
            raise ValueError(f"{label}.outputs must be a list of at most 100 paths")
        output_paths = [_relative_path(value, f"{label}.outputs[]") for value in outputs]
        if len(set(output_paths)) != len(output_paths):
            raise ValueError(f"{label}.outputs must not contain duplicate paths")

        timeout = phase.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)
        if type(timeout) is not int or not 1 <= timeout <= MAX_TIMEOUT_SECONDS:
            raise ValueError(f"{label}.timeout_seconds must be an integer from 1 to {MAX_TIMEOUT_SECONDS}")

        by_id[identifier] = {
            "id": identifier,
            "command": args,
            "depends_on": list(deps),
            "cwd": cwd,
            "outputs": output_paths,
            "timeout_seconds": timeout,
        }

    for phase in by_id.values():
        unknown = [dep for dep in phase["depends_on"] if dep not in by_id]
        if unknown:
            raise ValueError(f"{phase['id']}: unknown dependency: {unknown[0]}")

    ordered = []
    visiting = set()
    visited = set()

    def visit(identifier):
        if identifier in visiting:
            raise ValueError("workflow phases contain a dependency cycle")
        if identifier in visited:
            return
        visiting.add(identifier)
        for dependency in by_id[identifier]["depends_on"]:
            visit(dependency)
        visiting.remove(identifier)
        visited.add(identifier)
        ordered.append(by_id[identifier])

    for phase in by_id.values():
        visit(phase["id"])
    return {"version": 1, "title": title}, ordered


def _command_hash(command: list[str]) -> str:
    encoded = json.dumps(command, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _project_path(root: Path, relative: str, *, must_exist: bool) -> Path:
    target = root / relative
    if must_exist:
        target = target.resolve(strict=True)
    else:
        target = target.resolve(strict=False)
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes the workflow directory: {relative}") from exc
    return target


def _output_receipts(root: Path, outputs: list[str]) -> tuple[list[dict], list[str]]:
    receipts, problems = [], []
    for relative in outputs:
        try:
            target = _project_path(root, relative, must_exist=True)
            if not target.is_file() or target.stat().st_size > MAX_OUTPUT_BYTES:
                raise ValueError("not a regular file or larger than the output limit")
            digest = hashlib.sha256()
            count = 0
            with target.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    count += len(block)
                    if count > MAX_OUTPUT_BYTES:
                        raise ValueError("larger than the output limit")
                    digest.update(block)
            receipts.append({"path": relative, "bytes": count, "sha256": digest.hexdigest()})
        except (OSError, ValueError, RuntimeError):
            problems.append(f"declared output unavailable or outside workflow directory: {relative}")
    return receipts, problems


def _phase_record(phase: dict, status: str, *, exit_code=None, outputs=None, reason=None) -> dict:
    result = {
        "id": phase["id"],
        "status": status,
        "depends_on": phase["depends_on"],
        "cwd": phase["cwd"],
        "command_sha256": _command_hash(phase["command"]),
        "timeout_seconds": phase["timeout_seconds"],
        "exit_code": exit_code,
        "outputs": outputs or [],
    }
    if reason:
        result["reason"] = reason
    return result


def plan_workflow(metadata: dict, phases: list[dict]) -> dict:
    return {
        **metadata,
        "mode": "plan",
        "phases": [_phase_record(phase, "planned") for phase in phases],
        "note": RUNNER_NOTE,
    }


def execute_workflow(metadata: dict, phases: list[dict], root: Path) -> dict:
    root = root.resolve(strict=True)
    records = []
    status_by_id = {}
    for phase in phases:
        blocked_by = [dependency for dependency in phase["depends_on"]
                      if status_by_id.get(dependency) != "completed"]
        if blocked_by:
            record = _phase_record(phase, "blocked", reason="dependency did not complete: " + blocked_by[0])
            records.append(record)
            status_by_id[phase["id"]] = "blocked"
            continue

        try:
            cwd = _project_path(root, phase["cwd"], must_exist=True)
            if not cwd.is_dir():
                raise ValueError(f"working directory is not a directory: {phase['cwd']}")
            for relative in phase["outputs"]:
                target = _project_path(root, relative, must_exist=False)
                if target.exists() or target.is_symlink():
                    raise ValueError(f"declared output already exists: {relative}")
        except (OSError, ValueError, RuntimeError) as exc:
            record = _phase_record(phase, "failed", reason=str(exc))
            records.append(record)
            status_by_id[phase["id"]] = "failed"
            continue

        exit_code, status, reason = None, "failed", None
        try:
            completed = subprocess.run(
                phase["command"], cwd=cwd, timeout=phase["timeout_seconds"],
                check=False, shell=False, stdout=sys.stderr, stderr=sys.stderr,
            )
            exit_code = completed.returncode
            if exit_code == 0:
                status = "completed"
            else:
                reason = f"command exited with status {exit_code}"
        except subprocess.TimeoutExpired:
            status = "timed_out"
            reason = f"command exceeded {phase['timeout_seconds']} seconds"
        except OSError as exc:
            reason = f"could not start command: {exc}"

        receipts, output_problems = _output_receipts(root, phase["outputs"])
        if status == "completed" and output_problems:
            status = "failed"
            reason = output_problems[0]
        record = _phase_record(phase, status, exit_code=exit_code, outputs=receipts, reason=reason)
        records.append(record)
        status_by_id[phase["id"]] = status

    return {
        **metadata,
        "mode": "execute",
        "phases": records,
        "note": RUNNER_NOTE,
    }


def load_workflow(path: Path) -> tuple[dict, list[dict], Path]:
    raw = path.read_bytes()
    if len(raw) > MAX_WORKFLOW_BYTES:
        raise ValueError(f"workflow exceeds the {MAX_WORKFLOW_BYTES}-byte limit")
    try:
        data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_unique_object,
                          parse_constant=_reject_constant)
    except UnicodeError as exc:
        raise ValueError("workflow must be UTF-8 JSON") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}, column {exc.colno}") from exc
    metadata, phases = validate_workflow(data)
    return metadata, phases, path.resolve(strict=True).parent


def _preflight_report(path: Path, root: Path, phases: list[dict]) -> None:
    if path.exists() or path.is_symlink():
        raise ValueError(f"report output already exists: {path}")
    parent = path.parent if str(path.parent) else Path(".")
    if not parent.is_dir():
        raise ValueError("report output parent directory must already exist")
    report_target = path.resolve(strict=False)
    for phase in phases:
        for relative in phase["outputs"]:
            output_target = _project_path(root, relative, must_exist=False)
            if report_target == output_target:
                raise ValueError(f"report path conflicts with a declared phase output: {relative}")


def _write_report(report: dict, path: Path | None) -> None:
    rendered = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if path is None:
        sys.stdout.write(rendered)
        return
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(rendered)
    print(f"Wrote report to {path}", file=sys.stderr)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", type=Path, help="JSON manifest; relative paths are based at its directory")
    parser.add_argument("--execute", action="store_true", help="run the caller-supplied commands; default is plan only")
    parser.add_argument("--root", type=Path, help="project directory for relative working directories and outputs")
    parser.add_argument("--report", type=Path, help="write a new JSON report file; existing files are never overwritten")
    args = parser.parse_args(argv)
    try:
        metadata, phases, manifest_root = load_workflow(args.workflow)
        root = args.root.resolve(strict=True) if args.root is not None else manifest_root
        if not root.is_dir():
            raise ValueError("project root must be an existing directory")
        if args.report is not None:
            _preflight_report(args.report, root, phases)
        result = execute_workflow(metadata, phases, root) if args.execute else plan_workflow(metadata, phases)
        _write_report(result, args.report)
        if args.execute and any(phase["status"] in {"failed", "blocked", "timed_out"}
                                for phase in result["phases"]):
            return 1
        return 0
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
