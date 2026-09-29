#!/usr/bin/env python3
"""Extract evidence-backed ChangeEpisodes with the configured Codex CLI.

This runner deliberately starts from live GitHub issue/PR/commit metadata and an
actual agent checkout. Prepared evidence.md/case.json files are never read. The
Codex process is invoked inside each checkout with read-only sandboxing and a
strict JSON output schema; insufficiently grounded issues remain audit records
and are excluded from downstream admission.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "codex-change-episode-v1.schema.json"
META_SKILL = ROOT / "data" / "skill-extraction" / "packages" / "universal-resolution-distiller" / "SKILL.md"

DEFAULT_CASES = [
    # Small pilot: two implementation-bearing cases plus one negative control.
    # Keep this list intentionally bounded; expand only after reviewing cost and
    # extraction quality from the first run.
    {"repository": "Aider-AI/aider", "issue": 3941, "checkout": "/home/chenyujia/tritonToLlvm/aider-agent"},
    {"repository": "NousResearch/hermes-agent", "issue": 122513, "checkout": "/home/chenyujia/tritonToLlvm/hermes-agent"},
    {"repository": "earendil-works/pi", "issue": 10092, "checkout": "/home/chenyujia/tritonToLlvm/pi-agent"},
]

QUALIFYING_EVIDENCE_KINDS = {
    "implementation", "implementation_change", "diff", "commit", "call-site",
    "call_site", "test", "validation", "benchmark", "code_review",
}


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def gh_json(url: str, token: str | None) -> Any:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "arex-skill-graph-codex-extractor"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def paged(url: str, token: str | None) -> list[Any]:
    values: list[Any] = []
    page = 1
    while page <= 10:
        separator = "&" if "?" in url else "?"
        batch = gh_json(f"{url}{separator}per_page=100&page={page}", token)
        if not isinstance(batch, list):
            return values
        values.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return values


def extract_pr_numbers(value: Any) -> set[int]:
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    return {int(number) for number in re.findall(r"/pull/(\d+)", text)}


def _git(checkout: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=checkout, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def _git_best_effort(checkout: Path, *args: str) -> tuple[str, str | None]:
    try:
        return _git(checkout, *args), None
    except RuntimeError as exc:
        return "", str(exc)


def local_issue_bundle(case: dict[str, Any]) -> dict[str, Any]:
    """Build a bounded, truthful bundle from the pinned local implementation ref."""
    checkout = Path(str(case["checkout"])).expanduser().resolve()
    # `extraction_ref` is the enriched-manifest field.  Keep `ref` as an
    # explicit override so small hand-written pilot manifests remain valid.
    ref = str(case.get("ref") or case.get("extraction_ref") or "").strip()
    if not ref:
        raise RuntimeError("offline fallback requires manifest ref")
    commit = _git(checkout, "rev-parse", f"{ref}^{{commit}}").strip()
    parents = _git(checkout, "rev-list", "--parents", "-n", "1", commit).strip().split()[1:]
    parent = parents[0] if parents else ""
    show, show_error = _git_best_effort(checkout, "show", "--no-ext-diff", "--format=fuller", "--stat", commit)
    if not show:
        show, _ = _git_best_effort(checkout, "cat-file", "-p", commit)
    names, names_error = _git_best_effort(checkout, "diff-tree", "-m", "--no-commit-id", "--name-status", "-r", commit)
    if not names:
        names = "\n".join(f"M\t{path}" for path in case.get("file_sample", []))
    limitations = ["No fabricated GitHub discussion metadata; implementation evidence must come from local git and checkout."]
    if show_error:
        limitations.append("git show --stat was unavailable because this checkout is a promisor/partial clone; commit metadata and manifest file samples are retained.")
    if names_error:
        limitations.append("git diff-tree was unavailable; changed-file evidence is limited to manifest file samples.")
    return {
        "source": "local_git_pinned_ref",
        "repository": str(case["repository"]),
        "issue_number": int(case["issue"]),
        "issue": {"number": int(case["issue"]), "title": case.get("title", ""), "body": None,
                  "metadata_unavailable": ["issue body", "comments", "timeline", "author/review discussion"]},
        "comments": [], "timeline": [],
        "linked_pull_requests": [{
            "pull_request": {"number": int(case.get("pull_request", 0) or 0), "title": case.get("title", ""),
                              "metadata_unavailable": ["PR body", "reviews", "status checks"]},
            "files": [{"status_line": line} for line in names.splitlines() if line.strip()],
            "commits": [{"sha": commit, "subject": subject} for subject in case.get("commit_subjects", [])],
        }] if case.get("pull_request") else [],
        "checkout": str(checkout), "pinned_ref": ref, "resolved_commit": commit, "parent_commit": parent,
        "commit_show_stat": show, "changed_files_name_status": names,
        "linked_issue_numbers": case.get("linked_issue_numbers", [int(case["issue"])]),
        "manifest_metadata": {k: case[k] for k in ("category", "theme", "module_families", "file_sample", "quality") if k in case},
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "limitations": limitations,
    }


def issue_bundle(case: dict[str, Any], token: str | None, max_linked_prs: int) -> dict[str, Any]:
    if os.environ.get("GITHUB_OFFLINE_FALLBACK") == "1" or os.environ.get("GITHUB_CACHE_ONLY") == "1":
        return local_issue_bundle(case)
    repo = str(case["repository"])
    issue_number = int(case["issue"])
    api = f"https://api.github.com/repos/{repo}"
    issue = gh_json(f"{api}/issues/{issue_number}", token)
    comments = paged(f"{api}/issues/{issue_number}/comments", token)
    timeline = paged(f"{api}/issues/{issue_number}/timeline", token)
    pr_numbers = set(extract_pr_numbers(issue)) | set(extract_pr_numbers(comments)) | set(extract_pr_numbers(timeline))
    if isinstance(issue, dict) and issue.get("pull_request"):
        pr_numbers.add(issue_number)
    pull_requests: list[dict[str, Any]] = []
    for number in sorted(pr_numbers)[:max_linked_prs]:
        try:
            pr = gh_json(f"{api}/pulls/{number}", token)
            files = paged(f"{api}/pulls/{number}/files", token)
            commits = paged(f"{api}/pulls/{number}/commits", token)
            pull_requests.append({"pull_request": pr, "files": files, "commits": commits})
        except urllib.error.HTTPError:
            continue
    return {
        "source": "github_api",
        "repository": repo,
        "issue_number": issue_number,
        "issue": issue,
        "comments": comments,
        "timeline": timeline,
        "linked_pull_requests": pull_requests,
        "checkout": str(case["checkout"]),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def prompt_for(bundle_path: Path, case: dict[str, Any]) -> str:
    ref = str(case.get("ref") or case.get("extraction_ref") or "(not supplied)")
    category = str(case.get("category") or case.get("theme") or "universal-functional-problem")
    meta_skill = META_SKILL.read_text(encoding="utf-8") if META_SKILL.exists() else ""
    ref_instruction = f"Pinned implementation ref: {ref}\nUse git show {ref} and inspect its parent, changed files, implementation, call sites, and tests."
    return f"""You are extracting a training-quality ChangeEpisode from a real agent repository.

Repository checkout: {case["checkout"]}
Issue number: {case["issue"]}
Universal problem class: {category}
{ref_instruction}
GitHub evidence bundle: {bundle_path}
Required output schema: {SCHEMA}

Use the following corrected meta-skill as the extraction contract. It is a
semantic role specification, not evidence about this repository:

{meta_skill}

Read the issue bundle and inspect the actual checkout. Use git history, the issue/PR
references, changed files, implementation code, call sites, and tests. Do not read
or use any prepared evidence.md or case.json artifact. Do not invent a before/after
change from an issue title, an automatic close, or a PR link alone.

Return ONLY JSON matching the required schema. The episode must contain a precise
before state, after state, and implementation diff summary. Every evidence unit must
have a stable id, kind, claim, and source. Evidence kinds implementation, diff,
commit, call_site/call-site, test, or validation require direct support from the
checkout or GitHub bundle. If no implementation-bearing change can be established,
return empty candidate arrays, put the reason in unresolved_questions, and do not
claim a usable episode. Candidate atomics and workflows must be grounded in the
returned episode evidence, not generic repository knowledge.

For every candidate_atomic, fill semantic_action when the evidence supports it:
intent, semantic module_role, finite operation, pre_state, post_state,
validation, and parameter slots; if it is not supportable, return null rather
than inventing values. Keep paths, symbols, commit ids, and provider names in
evidence or parameters; do not use them as the abstraction. For every
candidate_workflow, fill workflow_graph as a partial-order resolution chain
when supportable, otherwise return null.
Use requires/enables/validates/repairs edges based on code and tests rather than
commit timestamp alone. Keep unresolved_or_deferred explicit. The universal
problem class is a routing hypothesis, not permission to invent a match.
"""


def _external_path(executable: str, path: Path) -> str:
    """Translate WSL paths for a Windows Codex executable when needed."""
    if not executable.lower().endswith((".exe", ".cmd", ".ps1")):
        return str(path)
    try:
        converted = subprocess.check_output(["wslpath", "-w", str(path)], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        converted = ""
    return converted or str(path)


def _powershell_literal(value: str) -> str:
    """Encode one argument as a PowerShell single-quoted string literal."""
    return "'" + value.replace("'", "''") + "'"


def _windows_codex_command(executable: str, arguments: list[str]) -> list[str]:
    """Run a Windows Codex binary through PowerShell from the WSL host.

    A Windows binary launched directly by a WSL subprocess inherits WSL path
    and terminal semantics.  PowerShell is the stable bridge for UNC checkout
    paths and for the CLI's non-interactive JSON mode.  EncodedCommand avoids
    corrupting the prompt/schema paths when the prompt contains quotes or
    non-ASCII text.
    """
    executable_path = _external_path(executable, Path(executable))
    ps_arguments = ",".join(_powershell_literal(item) for item in arguments)
    script = (
        "$ErrorActionPreference='Stop'; "
        f"$exe={_powershell_literal(executable_path)}; "
        f"$codexArgs=@({ps_arguments}); "
        "& $exe @codexArgs; exit $LASTEXITCODE"
    )
    encoded = base64.b64encode(script.encode("utf-16le")).decode("ascii")
    powershell = shutil.which("powershell.exe") or "powershell.exe"
    return [powershell, "-NoLogo", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded]


def run_codex(executable: str, checkout: Path, prompt: str, response_path: Path, stdout_path: Path, stderr_path: Path, profile: str | None = None, model: str | None = None, sandbox: str = "read-only", timeout_seconds: int = 900, bypass_sandbox: bool = False) -> int:
    codex_arguments: list[str] = []
    if profile:
        codex_arguments += ["--profile", profile]
    if model:
        codex_arguments += ["--model", model]
    codex_arguments += [
        "exec", "--ephemeral", "--skip-git-repo-check", "--json", "--sandbox", sandbox,
        "--output-schema", _external_path(executable, SCHEMA),
        "-o", _external_path(executable, response_path),
        "-C", _external_path(executable, checkout), "-",
    ]
    if bypass_sandbox:
        codex_arguments.insert(0, "--dangerously-bypass-approvals-and-sandbox")
    windows_executable = executable.lower().endswith((".exe", ".cmd", ".ps1"))
    command = _windows_codex_command(executable, codex_arguments) if windows_executable else [executable, *codex_arguments]
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        process_cwd = Path("/mnt/c/Users/W") if windows_executable and Path("/mnt/c/Users/W").exists() else checkout
        # Feed the prompt through stdin.  Besides avoiding Windows command-line
        # length/quoting limits, this is the stable non-interactive path used by
        # the direct JSONL pilot.  The final structured response is still
        # written by Codex to response_path via -o.
        proc = subprocess.run(command, cwd=process_cwd, input=prompt, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout_seconds)
        stdout, stderr, returncode = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        stderr += f"\nCodex extraction timed out after {timeout_seconds} seconds.\n"
        returncode = 124
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    return returncode


def validate_response(value: Any) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return False, ["response is not an object"]
    for key in ("episode", "evidence_units", "candidate_atomics", "candidate_workflows", "unresolved_questions"):
        if key not in value:
            errors.append(f"missing top-level key: {key}")
    episode = value.get("episode")
    if not isinstance(episode, dict):
        errors.append("episode is not an object")
    else:
        for key in ("episode_id", "title", "before", "after", "diff"):
            if not str(episode.get(key, "")).strip():
                errors.append(f"episode.{key} is empty")
    evidence = value.get("evidence_units")
    if not isinstance(evidence, list):
        errors.append("evidence_units is not an array")
        evidence = []
    ids: set[str] = set()
    qualifying = False
    for index, unit in enumerate(evidence):
        if not isinstance(unit, dict):
            errors.append(f"evidence_units[{index}] is not an object")
            continue
        for key in ("id", "kind", "claim", "source"):
            if not str(unit.get(key, "")).strip():
                errors.append(f"evidence_units[{index}].{key} is empty")
        unit_id = str(unit.get("id", ""))
        if unit_id in ids and unit_id:
            errors.append(f"duplicate evidence id: {unit_id}")
        ids.add(unit_id)
        kind = str(unit.get("kind", "")).strip().lower().replace(" ", "_")
        qualifying |= kind in QUALIFYING_EVIDENCE_KINDS
    if not qualifying:
        errors.append("no implementation-bearing evidence kind")
    if not isinstance(value.get("candidate_atomics"), list):
        errors.append("candidate_atomics is not an array")
    if not isinstance(value.get("candidate_workflows"), list):
        errors.append("candidate_workflows is not an array")
    if not isinstance(value.get("unresolved_questions"), list):
        errors.append("unresolved_questions is not an array")
    return not errors, errors


def canonical_episode(response: dict[str, Any], bundle: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    episode = dict(response["episode"])
    evidence = response["evidence_units"]
    supplied_id = str(episode.get("episode_id") or "").strip()
    if not supplied_id or supplied_id == str(case["issue"]):
        supplied_id = f"github:{case['repository']}#{case['issue']}"
    episode["episode_id"] = supplied_id
    episode["repository"] = str(case["repository"])
    episode["revision"] = str(episode.get("revision") or "github-issue-" + str(case["issue"]))
    episode["evidence_ids"] = [str(unit["id"]) for unit in evidence if isinstance(unit, dict) and unit.get("id")]
    episode["metadata"] = {
        "source": "github_issue_pr_commit_codex",
        "repository": case["repository"],
        "issue": case["issue"],
        "checkout": case["checkout"],
        "manifest_metadata": {
            "category": case.get("category") or case.get("theme"),
            "role": case.get("role") or case.get("split"),
            "case_id": case.get("case_id"),
        },
        "github_bundle": bundle,
        "codex_response": response,
        "candidate_atomics": response.get("candidate_atomics", []),
        "candidate_workflows": response.get("candidate_workflows", []),
        "unresolved_questions": response.get("unresolved_questions", []),
    }
    episode.setdefault("call_sites", [u["claim"] for u in evidence if str(u.get("kind", "")).lower().replace("-", "_") == "call_site"])
    episode.setdefault("tests", [u["claim"] for u in evidence if "test" in str(u.get("kind", "")).lower()])
    return episode


def load_cases(path: Path | None, role: str = "all") -> list[dict[str, Any]]:
    if path is None:
        return list(DEFAULT_CASES)
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("cases")
    if not isinstance(data, list):
        raise ValueError("manifest must be a JSON array or an object with a cases array")
    cases = [dict(item) for item in data]
    if role != "all":
        cases = [
            item for item in cases
            if str(item.get("role") or item.get("split") or "") == role
        ]
    return cases


def main() -> int:
    global SCHEMA
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, help="JSON array of {repository, issue, checkout}")
    parser.add_argument("--schema", type=Path, default=SCHEMA, help="schema path visible to the Codex process")
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "skill-extraction" / "codex-runs" / now_id())
    parser.add_argument("--codex", default="codex", help="configured Codex CLI executable")
    parser.add_argument("--codex-profile", default=os.environ.get("CODEX_PROFILE"), help="Codex profile layered onto user config")
    parser.add_argument("--codex-model", default=os.environ.get("CODEX_MODEL"), help="Codex model override")
    parser.add_argument("--codex-sandbox", default=os.environ.get("CODEX_SANDBOX", "read-only"), choices=("read-only", "workspace-write", "danger-full-access"), help="Codex sandbox policy")
    parser.add_argument("--codex-bypass-sandbox", action="store_true", help="explicitly bypass Codex approvals/sandbox; use only with an isolated staging checkout")
    parser.add_argument("--github-token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--role", default="all", choices=("all", "train_candidate", "holdout_candidate"), help="optional manifest role filter")
    parser.add_argument("--max-cases", type=int, default=3, help="hard cap on Codex extraction calls")
    parser.add_argument("--max-linked-prs", type=int, default=2, help="hard cap on PR bundles fetched per issue")
    parser.add_argument("--codex-timeout-seconds", type=int, default=900, help="per-episode Codex timeout")
    args = parser.parse_args()
    args.output = args.output.expanduser().resolve()
    SCHEMA = args.schema.expanduser().resolve()
    cases = load_cases(args.manifest, args.role)[: max(0, args.max_cases)]
    args.output.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    admitted: list[dict[str, Any]] = []
    for case in cases:
        repo_slug = str(case["repository"]).replace("/", "__")
        case_dir = args.output / f"{repo_slug}__{case['issue']}"
        case_dir.mkdir(parents=True, exist_ok=True)
        checkout = Path(str(case["checkout"])).expanduser().resolve()
        record: dict[str, Any] = {"repository": case["repository"], "issue": case["issue"], "checkout": str(checkout)}
        try:
            if not (checkout / ".git").exists():
                raise RuntimeError(f"checkout is not a git repository: {checkout}")
            bundle = issue_bundle(case, args.github_token, max(0, args.max_linked_prs))
            bundle_path = case_dir / "issue-bundle.json"
            bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
            prompt = prompt_for(bundle_path, case)
            if args.codex.lower().endswith((".exe", ".cmd", ".ps1")):
                prompt = prompt.replace(str(bundle_path), _external_path(args.codex, bundle_path))
                prompt = prompt.replace(str(checkout), _external_path(args.codex, checkout))
                prompt = prompt.replace(str(SCHEMA), _external_path(args.codex, SCHEMA))
            (case_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
            response_path = case_dir / "codex-response.json"
            command_meta = {
                "executable": args.codex,
                "sandbox": args.codex_sandbox,
                "bypass_sandbox": args.codex_bypass_sandbox,
                "schema": str(SCHEMA),
                "checkout": str(checkout),
                "source": "github issue/comments/timeline/linked PR files/commits + checkout",
                "max_linked_prs": args.max_linked_prs,
                "timeout_seconds": args.codex_timeout_seconds,
            }
            (case_dir / "codex-command.json").write_text(json.dumps(command_meta, indent=2), encoding="utf-8")
            returncode = run_codex(args.codex, checkout, prompt, response_path, case_dir / "codex-stdout.log", case_dir / "codex-stderr.log", args.codex_profile, args.codex_model, args.codex_sandbox, max(1, args.codex_timeout_seconds), args.codex_bypass_sandbox)
            record["codex_returncode"] = returncode
            record["execution_status"] = "completed" if returncode == 0 else "failed_or_timed_out"
            response = json.loads(response_path.read_text(encoding="utf-8")) if response_path.exists() else None
            ok, errors = validate_response(response)
            (case_dir / "validation.json").write_text(json.dumps({"valid": ok, "errors": errors}, indent=2), encoding="utf-8")
            record["valid"] = ok
            record["validation_errors"] = errors
            if ok:
                episode = canonical_episode(response, bundle, case)
                record["episode_id"] = episode["episode_id"]
                record["admitted"] = True
                admitted.append(episode)
            else:
                record["admitted"] = False
        except Exception as exc:
            record["valid"] = False
            record["admitted"] = False
            record["error"] = f"{type(exc).__name__}: {exc}"
        records.append(record)
    (args.output / "episodes.json").write_text(json.dumps(admitted, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.output / "extraction-records.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {
        "source": "server_codex_cli",
        "prepared_fixtures_used": False,
        "run_id": args.output.name,
        "total_cases": len(records),
        "max_cases": args.max_cases,
        "max_linked_prs": args.max_linked_prs,
        "codex_timeout_seconds": args.codex_timeout_seconds,
        "admitted_episodes": len(admitted),
        "insufficient_or_failed": sum(not bool(item.get("admitted")) for item in records),
        "records": records,
    }
    (args.output / "extraction-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "admitted_episodes": len(admitted), "total_cases": len(records)}, ensure_ascii=False))
    return 0 if all(item.get("admitted") or item.get("valid") is False for item in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
