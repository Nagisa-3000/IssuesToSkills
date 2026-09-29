#!/usr/bin/env python3
"""Build the first six-harness provider/endpoint resolution pilot manifest."""
from __future__ import annotations
import argparse, json, re, subprocess, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SEEDS = [
    ("earendil-works/pi", 5823),
    ("Aider-AI/aider", 2765),
    ("NousResearch/hermes-agent", 121359),
    ("openai/codex", 41095),
    ("google-gemini/gemini-cli", 15430),
    ("QwenLM/qwen-code", 9452),
]
CHECKOUTS = {
    "earendil-works/pi": "/home/chenyujia/tritonToLlvm/pi-agent",
    "Aider-AI/aider": "/home/chenyujia/tritonToLlvm/aider-agent",
    "NousResearch/hermes-agent": "/home/chenyujia/tritonToLlvm/hermes-agent",
    "openai/codex": "/home/chenyujia/tritonToLlvm/codex-agent",
    "google-gemini/gemini-cli": "/home/chenyujia/tritonToLlvm/gemini-cli",
    "QwenLM/qwen-code": "/home/chenyujia/tritonToLlvm/qwen-code",
}
CATEGORY = "provider-interface-adaptation"


def gh(url: str) -> Any:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "issues-to-skills-provider-pilot"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def git(checkout: str, *args: str) -> str:
    p = subprocess.run(["git", *args], cwd=checkout, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        return ""
    return p.stdout.strip()


def pr_numbers(value: Any) -> set[int]:
    text = json.dumps(value, ensure_ascii=False)
    return {int(x) for x in re.findall(r"/pull/(\d+)", text)}


def resolve_seed(repo: str, issue_number: int) -> dict[str, Any]:
    checkout = CHECKOUTS[repo]
    issue = gh(f"https://api.github.com/repos/{repo}/issues/{issue_number}")
    numbers = pr_numbers(issue)
    if isinstance(issue, dict) and issue.get("pull_request"):
        numbers.add(issue_number)
    for endpoint in ("timeline", "events"):
        try: numbers |= pr_numbers(gh(f"https://api.github.com/repos/{repo}/issues/{issue_number}/{endpoint}"))
        except Exception: pass
    prs=[]
    for number in sorted(numbers):
        try:
            pr=gh(f"https://api.github.com/repos/{repo}/pulls/{number}")
            if pr.get("merged") or pr.get("merged_at"):
                prs.append(pr)
        except Exception: pass
    pr=max(prs,key=lambda x: str(x.get("merged_at") or ""),default=None)
    ref=(pr or {}).get("merge_commit_sha") or (pr or {}).get("head",{}).get("sha")
    if not ref and issue.get("pull_request"):
        ref=issue.get("pull_request",{}).get("sha")
    files=[]; commits=[]
    if pr:
        try: files=gh(f"https://api.github.com/repos/{repo}/pulls/{pr['number']}/files?per_page=100")
        except Exception: files=[]
        try: commits=gh(f"https://api.github.com/repos/{repo}/pulls/{pr['number']}/commits?per_page=100")
        except Exception: commits=[]
    ref_exists=bool(ref and git(checkout,"cat-file","-e",f"{ref}^{{commit}}"))
    return {
        "case_id": f"{repo}#{issue_number}:{CATEGORY}:holdout_candidate",
        "repository": repo, "issue": issue_number,
        "issue_url": f"https://github.com/{repo}/issues/{issue_number}",
        "title": issue.get("title", ""), "body_present": bool(issue.get("body")),
        "category": CATEGORY, "theme": "model provider and endpoint resolution",
        "role": "holdout_candidate", "split": "holdout_candidate",
        "checkout": checkout, "ref": ref or "", "extraction_ref": ref or "",
        "pull_request": pr.get("number") if pr else None,
        "issue_relation": "linked-merged-pr" if pr else "no-merged-pr-resolved",
        "ref_exists_in_checkout": ref_exists,
        "file_sample": [x.get("filename") for x in files[:30] if isinstance(x,dict) and x.get("filename")],
        "commit_subjects": [((x.get("commit") or {}).get("message") or "").splitlines()[0] for x in commits[:20] if isinstance(x,dict)],
        "quality": {"merged_pr": bool(pr), "implementation_files": sum(1 for x in files if x.get("filename") and not any(s in x["filename"].lower() for s in ("test","spec","fixture"))), "test_files": sum(1 for x in files if any(s in (x.get("filename") or "").lower() for s in ("test","spec","fixture")))},
        "source": "user_seed_github_api",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=Path,required=True); ap.add_argument("--supplemental",type=Path,required=True); args=ap.parse_args()
    seeds=[resolve_seed(*item) for item in SEEDS]
    ready=json.loads(args.supplemental.read_text(encoding="utf-8"))["cases"]
    supplements=[]
    used={x["repository"] for x in seeds}
    for x in ready:
        if x.get("category") != CATEGORY or x.get("role") != "train_candidate": continue
        item=dict(x); item["source"]="existing_universal_train_candidate"; supplements.append(item)
    # One known-good supplemental training case per repository. Keep the user
    # supplied case as holdout so the first pilot has a clean paired arm.
    by_repo={}
    for x in supplements: by_repo.setdefault(x["repository"],x)
    cases=[]
    for seed in seeds:
        sup=by_repo.get(seed["repository"])
        if sup: cases.append(sup)
        cases.append(seed)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    payload={"schema_version":"provider-endpoint-resolution-pilot-v1","category":CATEGORY,"repositories":sorted({x["repository"] for x in cases}),"cases":cases,"policy":{"train_roles":["train_candidate"],"holdout_roles":["holdout_candidate"],"holdout_per_repository":1,"supplemental_per_repository":1}}
    args.output.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"cases":len(cases),"train":sum(x.get("role")=="train_candidate" for x in cases),"holdout":sum(x.get("role")=="holdout_candidate" for x in cases),"missing_refs":[f"{x['repository']}#{x['issue']}" for x in cases if not x.get('ref_exists_in_checkout',True)]},ensure_ascii=False))
    return 0
if __name__=="__main__": raise SystemExit(main())
