#!/usr/bin/env python3
"""Use the real Codex CLI as the bounded semantic graph judge.

The judge receives only the already admitted training graph.  It may propose
semantic action merges and assess Pattern candidates, but it cannot rewrite
episodes or read holdout cases.  Raw prompt/response/stdout/stderr and the
execution metadata are retained beside the adjudication JSON.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import run_codex_issue_episode_extraction as codex_runner


def prompt_for(graph_path: str, schema_path: str, graph: dict) -> str:
    categories = sorted({str(item.get("category")) for item in graph.get("patterns", [])})
    return f"""You are the independent semantic judge for a universal ChangeAction -> IssueWorkflow -> Pattern graph.

Read ONLY this already-built training graph: {graph_path}
It contains admitted training episodes from six agent harness repositories. Do not search for,
read, or infer any holdout issue, repository solution, target test, or external episode. Do not
modify files. Return ONLY JSON matching the required schema.

Your two decisions are deliberately separate:

1. action_merges: propose a merge only when two or more action IDs describe the same reusable
   operation at the same semantic level, with the same meaningful postcondition and validation
   oracle. Paths, symbols, issue titles, provider names, and repository labels are not enough.
   If actions are merely in the same broad problem class but have different mechanisms or
   oracles, omit them or mark the relationship distinct/unknown. Preserve the most general
   existing action ID as canonical_action_id. Never merge actions from one episode merely
   because they occur in one workflow.

2. pattern_judgments: assess each graph Pattern candidate. Promote only if independent
   workflows from at least two repositories support a mandatory reusable action or an explicit
   equivalent-action cluster. Otherwise use defer or reject. This batch is a pilot, so it is
   acceptable and often correct to defer a broad category whose mechanisms do not align.
   A promoted candidate still needs an untouched holdout end-task repair and must not be called
   final here. List concrete missing probes whenever a candidate is deferred.

Use only evidence IDs already present in the graph's action/workflow payloads. Return grounded,
concise rationale. The graph currently contains these structural categories: {', '.join(categories)}.
Required schema: {schema_path}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--codex", required=True)
    parser.add_argument("--schema", type=Path, default=ROOT / "schemas" / "universal-resolution-adjudication-v1.schema.json")
    parser.add_argument("--checkout", type=Path, default=ROOT, help="isolated directory passed as Codex -C")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--codex-bypass-sandbox", action="store_true")
    args = parser.parse_args()

    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    if not isinstance(graph, dict):
        raise ValueError("graph must be an object")
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    graph_path = args.graph.expanduser().resolve()
    schema_path = args.schema.expanduser().resolve()
    prompt = prompt_for(codex_runner._external_path(args.codex, graph_path), codex_runner._external_path(args.codex, schema_path), graph)
    prompt_path = output / "prompt.txt"
    prompt_path.write_text(prompt, encoding="utf-8")
    response_path = output / "adjudication.json"
    command = {
        "executable": args.codex,
        "schema": str(schema_path),
        "graph": str(graph_path),
        "checkout": str(args.checkout.expanduser().resolve()),
        "timeout_seconds": args.timeout_seconds,
        "bypass_sandbox": args.codex_bypass_sandbox,
        "source": "training-only structural graph; holdout refused by prompt contract",
    }
    (output / "codex-command.json").write_text(json.dumps(command, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    codex_runner.SCHEMA = schema_path
    returncode = codex_runner.run_codex(
        args.codex,
        args.checkout.expanduser().resolve(),
        prompt,
        response_path,
        output / "codex-stdout.log",
        output / "codex-stderr.log",
        sandbox="read-only",
        timeout_seconds=max(1, args.timeout_seconds),
        bypass_sandbox=args.codex_bypass_sandbox,
    )
    valid = False
    errors: list[str] = []
    response: object = None
    if response_path.exists():
        try:
            response = json.loads(response_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"response is not JSON: {exc}")
    if isinstance(response, dict):
        for key in ("action_merges", "pattern_judgments", "unresolved"):
            if key not in response:
                errors.append(f"missing top-level key: {key}")
        valid = not errors
    else:
        errors.append("response is not an object")
    (output / "validation.json").write_text(json.dumps({"returncode": returncode, "valid": valid, "errors": errors}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "returncode": returncode, "valid": valid, "errors": errors}, ensure_ascii=False))
    return 0 if returncode == 0 and valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
