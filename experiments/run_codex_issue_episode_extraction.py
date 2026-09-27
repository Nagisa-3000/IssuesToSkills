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
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "codex-change-episode-v1.schema.json"

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


def issue_bundle(case: dict[str, Any], token: str | None, max_linked_prs: int) -> dict[str, Any]:
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
    return f"""You are extracting a training-quality ChangeEpisode from a real agent repository.

Repository checkout: {case['checkout']}
Issue number: {case['issue']}
GitHub evidence bundle: {bundle_path}
Required output schema: {SCHEMA}

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
"""


def run_codex(executable: str, checkout: Path, prompt: str, response_path: Path, stdout_path: Path, stderr_path: Path) -> int:
    command = [
        executable, "exec", "--ephemeral", "--sandbox", "read-only",
        "--output-schema", str(SCHEMA), "-o", str(response_path), "-C", str(checkout), prompt,
    ]
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(command, cwd=checkout, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_path.write_text(proc.stdout, encoding="utf-8")
    stderr_path.write_text(proc.stderr, encoding="utf-8")
    return proc.returncode


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
    episode["episode_id"] = str(episode.get("episode_id") or f"github:{case['repository']}#{case['issue']}")
    episode["repository"] = str(case["repository"])
    episode["revision"] = str(episode.get("revision") or "github-issue-" + str(case["issue"]))
    episode["evidence_ids"] = [str(unit["id"]) for unit in evidence if isinstance(unit, dict) and unit.get("id")]
    episode["metadata"] = {
        "source": "github_issue_pr_commit_codex",
        "repository": case["repository"],
        "issue": case["issue"],
        "checkout": case["checkout"],
        "github_bundle": bundle,
        "codex_response": response,
        "candidate_atomics": response.get("candidate_atomics", []),
        "candidate_workflows": response.get("candidate_workflows", []),
        "unresolved_questions": response.get("unresolved_questions", []),
    }
    episode.setdefault("call_sites", [u["claim"] for u in evidence if str(u.get("kind", "")).lower().replace("-", "_") == "call_site"])
    episode.setdefault("tests", [u["claim"] for u in evidence if "test" in str(u.get("kind", "")).lower()])
    return episode


def load_cases(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return list(DEFAULT_CASES)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("manifest must be a JSON array")
    return [dict(item) for item in data]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, help="JSON array of {repository, issue, checkout}")
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "skill-extraction" / "codex-runs" / now_id())
    parser.add_argument("--codex", default="codex", help="configured Codex CLI executable")
    parser.add_argument("--github-token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--max-cases", type=int, default=3, help="hard cap on Codex extraction calls")
    parser.add_argument("--max-linked-prs", type=int, default=2, help="hard cap on PR bundles fetched per issue")
    args = parser.parse_args()
    global SCHEMA
    cases = load_cases(args.manifest)[: max(0, args.max_cases)]
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
            (case_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
            response_path = case_dir / "codex-response.json"
            command_meta = {
                "executable": args.codex,
                "sandbox": "read-only",
                "schema": str(SCHEMA),
                "checkout": str(checkout),
                "source": "github issue/comments/timeline/linked PR files/commits + checkout",
                "max_linked_prs": args.max_linked_prs,
            }
            (case_dir / "codex-command.json").write_text(json.dumps(command_meta, indent=2), encoding="utf-8")
            returncode = run_codex(args.codex, checkout, prompt, response_path, case_dir / "codex-stdout.log", case_dir / "codex-stderr.log")
            record["codex_returncode"] = returncode
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
        "admitted_episodes": len(admitted),
        "insufficient_or_failed": sum(not bool(item.get("admitted")) for item in records),
        "records": records,
    }
    (args.output / "extraction-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "admitted_episodes": len(admitted), "total_cases": len(records)}, ensure_ascii=False))
    return 0 if all(item.get("admitted") or item.get("valid") is False for item in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())