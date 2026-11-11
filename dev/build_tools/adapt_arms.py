"""Adapt active ARMS copies without modifying the preserved upstream archive."""
from pathlib import Path
import hashlib
import re


SKILLS = (
    "brief-expander", "critic-revisor", "house-style", "literature-lead",
    "methodology-architect", "paper-critic", "paper-fixer", "paper-grader",
    "paper-modeler", "paper-writer", "research-pipeline", "validate-method",
    "write-manuscript",
)
REPLACEMENT_ROLES = ("failure-diagnoser", "consistency-auditor", "venue-compliance-gate")
MARKER = "<!-- ARMS_PORTABLE_ADAPTER_V1 -->"


def _portable_markdown(text: str, skill: str, is_skill: bool) -> str:
    # The root brief has the newer author-exemplar and contribution fields.
    text = re.sub(
        r"(?:~/)?\.claude/skills/(?:arms-)?research-pipeline/research_brief_template\.md",
        "../../resources/upstream/ARMS-main/research_brief_template.md", text)
    text = re.sub(r"(?:~/)?\.claude/skills/_shared/scoring_rubric\.md",
                  "UNAVAILABLE_UPSTREAM_SCORING_RUBRIC", text)
    for name in SKILLS:
        target = "../arms-" + name
        text = re.sub(r"(?:~/)?\.claude/skills/(?:arms-)?" + re.escape(name)
                      + r"(?=/|[`\s\"'])", target, text)
        text = re.sub(r"(?<![\w./-])skills/(?:arms-)?" + re.escape(name)
                      + r"(?=/)", target, text)
        text = text.replace("../" + name + "/", target + "/")
        text = re.sub(r"(?<![\w./-])(?:arms-)?" + re.escape(name) + r"/SKILL\.md",
                      target + "/SKILL.md", text)
        text = re.sub(r"(?<![\w./-])/" + re.escape(name) + r"(?![\w-])",
                      "/arms-" + name, text)
    for name in REPLACEMENT_ROLES:
        text = text.replace("/" + name + " ",
                            "Read ../../agents/" + name + ".md; apply this separately authored local replacement role to ")
        text = text.replace("`/" + name + "`", "`../../agents/" + name + ".md`")
    if skill != "house-style":
        text = re.sub(r"(?<![\w./-])examples/(abstract-reader-first|dense-results-paragraph)\.md",
                      r"../arms-house-style/examples/\1.md", text)
    text = text.replace("/skill-auditor", "UNAVAILABLE_UPSTREAM_SKILL_AUDITOR")
    text = text.replace("~/Library/LaunchAgents/com.yuanj.skill-auditor.plist",
                        "UNAVAILABLE_UPSTREAM_MACOS_LAUNCH_AGENT")
    text = re.sub(r"(?:~/)?\.claude/[^`\s\"')]+",
                  "UNAVAILABLE_UPSTREAM_PRIVATE_DEPENDENCY", text)
    if not is_skill or MARKER in text:
        return text
    notice = (
        MARKER + "\n## Portable ARMS execution\n\n"
        "Bundled relative paths below resolve from the directory holding this SKILL.md, "
        "not from the research project's working directory. Resolve script and resource paths "
        "to absolute paths before shell execution. Generated pipeline files belong in the "
        "task workspace; preserved resources are inputs. Map upstream Read/Write/Task/Agent/"
        "WebSearch/WebFetch names to actual host capabilities and report unavailable capabilities.\n\n"
    )
    if "UNAVAILABLE_UPSTREAM_SCORING_RUBRIC" in text:
        notice += (
            "The upstream shared scoring rubric is absent "
            "(UNAVAILABLE_UPSTREAM_SCORING_RUBRIC). Do not invent it or claim its checks passed. "
            "The embedded paper-grader rubric remains supplied guidance, with this limitation "
            "reported separately.\n\n"
        )
    if skill == "research-pipeline":
        notice += (
            "Upstream helper skills failure-diagnoser, consistency-auditor and venue-compliance-gate "
            "are not supplied. This package may provide separately authored replacement roles at "
            "`../../agents/failure-diagnoser.md`, `../../agents/consistency-auditor.md` and "
            "`../../agents/venue-compliance-gate.md`. Check each file exists before dispatch; if "
            "absent, report the required gate unavailable. These are local replacements, not "
            "upstream ARMS implementations. Private telemetry, skill-auditor, proposal application "
            "and macOS scheduling described in the historical README are unavailable.\n\n"
        )
    if skill == "critic-revisor":
        notice += (
            "Run the adapted script's `--preflight` first; it checks prerequisites without "
            "creating outputs or invoking model CLIs. Git snapshots are disabled by default. "
            "`ARMS_ENABLE_GIT_SNAPSHOT=1` explicitly enables bounded snapshots only when the Git "
            "index is clean. Only the manuscript and current run directory may enter those "
            "commits. The manuscript is still revised in place; work from a preserved baseline "
            "in the task workspace. No model family is enforced by the supplied CLI commands.\n\n"
        )
    if text.startswith("---"):
        parts = text.split("---", 2)
        return "---" + parts[1] + "---\n\n" + notice + parts[2].lstrip("\r\n")
    return notice + text


PREREQUISITES = r'''
# ARMS_PORTABLE_SCRIPT_V1: check everything before logs, edits or model calls.
if [[ ! "$MAX_ROUNDS" =~ ^[1-9][0-9]*$ ]]; then
  echo "ERROR: max_rounds must be a positive integer" >&2
  exit 2
fi
[[ "$MANUSCRIPT" == *.tex ]] || { echo "ERROR: expected a .tex manuscript" >&2; exit 2; }
_missing=()
for _tool in claude codex latexmk latexdiff dirname basename date mkdir cp find xargs grep tail seq cat awk rm sleep; do
  command -v "$_tool" >/dev/null 2>&1 || _missing+=("$_tool")
done
if ! command -v md5 >/dev/null 2>&1 && ! command -v md5sum >/dev/null 2>&1; then
  _missing+=("md5 or md5sum")
fi
if [[ "${ARMS_ENABLE_GIT_SNAPSHOT:-0}" == "1" ]] && ! command -v git >/dev/null 2>&1; then
  _missing+=("git (snapshot opt-in)")
fi
if [[ ${#_missing[@]} -gt 0 ]]; then
  printf 'ERROR: missing prerequisite: %s\n' "${_missing[@]}" >&2
  exit 2
fi
'''


GIT_PREFLIGHT = r'''
USE_GIT=0
if [[ "${ARMS_ENABLE_GIT_SNAPSHOT:-0}" == "1" ]]; then
  if ! git -C "$WORK_DIR" rev-parse --git-dir >/dev/null 2>&1; then
    echo "ERROR: Git snapshots require an existing repository" >&2
    exit 2
  fi
  if ! git -C "$WORK_DIR" diff --cached --quiet --exit-code; then
    echo "ERROR: Git snapshot requires a clean index; existing staged changes preserved" >&2
    exit 2
  fi
  USE_GIT=1
fi
if [[ "$PREFLIGHT_ONLY" == "1" ]]; then
  echo "Preflight passed; no outputs created or model CLIs invoked. Git snapshots: $USE_GIT"
  exit 0
fi
'''


GIT_SNAPSHOT = r'''
# Optional, narrowly scoped snapshots. No automatic commit of user work.
git_snapshot_round() {
  [[ "${ARMS_ENABLE_GIT_SNAPSHOT:-0}" == "1" && "${USE_GIT:-0}" == "1" ]] || return 0
  if ! git -C "$WORK_DIR" diff --cached --quiet --exit-code; then
    echo "ERROR: Git index changed; snapshot skipped without staging or committing" >&2
    return 2
  fi
  git -C "$WORK_DIR" add -- "$MANU_FILE" "$RUN_DIR" || return 2
  if git -C "$WORK_DIR" diff --cached --quiet --exit-code -- "$MANU_FILE" "$RUN_DIR"; then
    return 0
  fi
  git -C "$WORK_DIR" commit --only --quiet -m "critic-revisor round $1" -- "$MANU_FILE" "$RUN_DIR"
}

'''


def _adapt_loop(text: str) -> str:
    if "# ARMS_PORTABLE_SCRIPT_V1:" in text:
        return text
    replacements = [
        ('SOURCE_SPEC=""\n', 'PREFLIGHT_ONLY=0\nSOURCE_SPEC=""\n'),
        ('  case "$1" in\n', '  case "$1" in\n    --preflight) PREFLIGHT_ONLY=1; shift ;;\n'),
        ('VENUE="${POSITIONAL[2]:-}"\n', 'VENUE="${POSITIONAL[2]:-}"\n' + PREREQUISITES),
        ('cd "$WORK_DIR" || exit 2\n', 'cd "$WORK_DIR" || exit 2\n' + GIT_PREFLIGHT),
        ('USE_GIT=0\nif git -C "$WORK_DIR" rev-parse --git-dir >/dev/null 2>&1; then\n  USE_GIT=1\nfi\n', ''),
        ('# ---- Main loop -------------------------------------------------------------',
         GIT_SNAPSHOT + '# ---- Main loop -------------------------------------------------------------'),
        ('  if [[ $USE_GIT -eq 1 ]]; then\n    git -C "$WORK_DIR" add -A 2>/dev/null\n'
         '    git -C "$WORK_DIR" commit -m "critic-revisor round $r" --quiet 2>/dev/null || true\n  fi\n',
         '  if ! git_snapshot_round "$r"; then\n    EXIT_REASON="Git snapshot failed; user index preserved"\n    break\n  fi\n'),
    ]
    for old, new in replacements:
        if old not in text:
            raise ValueError("Unrecognized upstream ARMS loop; expected anchor missing: " + old[:75])
        text = text.replace(old, new, 1)
    text = text.replace('[--sources <paths>]', '[--sources <paths>] [--preflight]', 1)
    return text


def adapt_arms(package_root: Path) -> list[dict]:
    """Adapt only active ARMS skill files and return per-file provenance changes."""
    package_root = Path(package_root).resolve()
    upstream = package_root / "resources/upstream/ARMS-main"
    if not (upstream / "LICENSE").is_file():
        raise ValueError("Preserved ARMS resource tree is required before adaptation")
    changes = []
    for name in SKILLS:
        active = package_root / "skills" / ("arms-" + name)
        if not (active / "SKILL.md").is_file():
            raise ValueError("Active ARMS skill is missing: " + str(active))
        for path in sorted(active.rglob("*")):
            if not path.is_file():
                continue
            before = path.read_bytes()
            if path.suffix == ".md":
                text = _portable_markdown(before.decode("utf-8-sig"), name, path.name == "SKILL.md")
            elif name == "critic-revisor" and path.name == "run_loop.sh":
                text = _adapt_loop(before.decode("utf-8-sig"))
            else:
                continue
            after = text.replace("\r\n", "\n").encode("utf-8")
            if after == before:
                continue
            path.write_bytes(after)
            changes.append({
                "path": path.relative_to(package_root).as_posix(),
                "source_sha256": hashlib.sha256(before).hexdigest(),
                "adapted_sha256": hashlib.sha256(after).hexdigest(),
                "changes": (["Prerequisite preflight before outputs/model CLIs", "Git snapshots opt-in; clean index; manuscript and current run only"]
                            if path.name == "run_loop.sh" else
                            ["Portable package-relative paths and host capability resolution", "Absent upstream dependencies explicitly marked; local replacement roles labelled"]),
            })
    return changes
