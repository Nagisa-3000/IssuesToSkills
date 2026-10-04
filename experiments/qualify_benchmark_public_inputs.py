#!/usr/bin/env python3
"""Qualify original public inputs for every pre-registered SWE union representative."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from build_history_verification_requests import cached_repair_metadata

from arex_skill_graph.benchmark_public_inputs import compose_public_problem, recover_issue_input
from arex_skill_graph.history_census import GitHubCLI, fingerprint, redact_history, write_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("scheduling", "repository", "output-dir"):
        parser.add_argument("--" + option, type=Path, required=True)
    parser.add_argument("--gh-executable", default="gh")
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    args = parser.parse_args(argv)
    scheduling = json.loads(args.scheduling.read_text())
    config = {
        "scheduling_sha256": fingerprint(scheduling),
        "cutoff": args.cutoff,
        "input_policy": "original-title-body-before-earliest-possible-repair-v1",
    }
    api, results = GitHubCLI(args.gh_executable), []
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for row in scheduling["scheduled"]:
        path = args.output_dir / row["instance_id"] / "public-input.json"
        identity = {"config": config, "representative": row}
        if path.exists():
            result = json.loads(path.read_text())
            if result["identity"] != identity or result["result_sha256"] != fingerprint(
                {k: v for k, v in result.items() if k != "result_sha256"}
            ):
                raise ValueError("public benchmark input checkpoint changed")
        else:
            try:
                metadata = cached_repair_metadata(
                    api,
                    {"repository": "pylint-dev/pylint", "pull_number": row["pull_number"]},
                    args.output_dir / "metadata-cache",
                )
                repair_before = metadata["first_possible_public_repair_at"]
                issues = []
                for issue_id in row["original_issue_ids"]:
                    repository, raw_number = issue_id.rsplit(":", 1)
                    cache = (
                        args.output_dir
                        / "issue-cache"
                        / (fingerprint([issue_id, repair_before]) + ".json")
                    )
                    if cache.exists():
                        saved_issue = json.loads(cache.read_text())
                        issue = saved_issue["snapshot"]
                        if saved_issue["snapshot_sha256"] != fingerprint(issue):
                            raise ValueError("public issue snapshot cache integrity changed")
                        if (
                            issue["issue_id"] != issue_id
                            or issue["repair_exclusion_before"] != repair_before
                        ):
                            raise ValueError("public issue snapshot cache identity changed")
                    else:
                        issue = recover_issue_input(api, repository, int(raw_number), repair_before)
                        write_json(
                            cache, {"snapshot": issue, "snapshot_sha256": fingerprint(issue)}
                        )
                    issues.append(issue)
                base_at = subprocess.check_output(
                    [
                        "git",
                        "--git-dir",
                        str(args.repository),
                        "show",
                        "-s",
                        "--format=%cI",
                        row["base_commit"],
                    ],
                    text=True,
                ).strip()
                public = compose_public_problem(
                    issues,
                    base_committed_at=base_at,
                    repair_before=repair_before,
                    main_cutoff=args.cutoff,
                )
                result = {
                    "identity": identity,
                    "public_input_qualified": True,
                    "public": public,
                    "original_inputs": issues,
                    "repair_time_basis": metadata["first_possible_public_repair_time_basis"],
                    "formal_task_qualified": False,
                    "formal_SWE_solver_runs": 0,
                }
            except (
                ValueError,
                RuntimeError,
                OSError,
                KeyError,
                subprocess.CalledProcessError,
            ) as error:
                result = {
                    "identity": identity,
                    "public_input_qualified": False,
                    "failure_type": type(error).__name__,
                    "reason": "public base metadata command failed"
                    if isinstance(error, subprocess.CalledProcessError)
                    else redact_history(str(error)),
                    "formal_task_qualified": False,
                    "formal_SWE_solver_runs": 0,
                }
            result["result_sha256"] = fingerprint(result)
            write_json(path, result)
        results.append(
            {
                "instance_id": row["instance_id"],
                "pull_number": row["pull_number"],
                "qualified": result["public_input_qualified"],
                "path": str(path),
                "result_sha256": result["result_sha256"],
            }
        )
        write_json(
            args.output_dir / "input-qualification-inventory.json",
            {
                "config": config,
                "results": results,
                "scheduled_count": len(scheduling["scheduled"]),
                "completed_count": len(results),
                "qualified_input_count": sum(r["qualified"] for r in results),
                "api_calls": api.calls,
                "semantic_duplicate_review_complete": False,
                "formal_task_qualified": False,
                "formal_SWE_solver_runs": 0,
            },
        )
        print(json.dumps(results[-1]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
