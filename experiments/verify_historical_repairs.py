#!/usr/bin/env python3
"""Causally qualify a registered historical development subset in isolated namespaces."""

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.adaptive_runner import TOOL_BACKENDS
from arex_skill_graph.history_census import redact_history, write_json
from arex_skill_graph.history_verification import verify_historical_repair


def canonical_repair_requests(requests):
    """Collapse PR/commit aliases while retaining every original request for audit."""
    groups = {}
    for request in requests:
        key = (
            request["issue_id"],
            request["repository_path"],
            request["metadata"]["mergeCommit"]["oid"],
        )
        groups.setdefault(key, []).append(request)
    priorities = {"direct_closure": 0, "closing_reference": 1}
    result = []
    for rows in groups.values():
        chosen = min(
            rows,
            key=lambda row: (
                priorities.get(row["metadata"].get("resolution_relationship"), 2),
                row["metadata"].get("number") is None,
                row["metadata"].get("fix_id", ""),
            ),
        )
        result.append(
            (
                chosen,
                [
                    {
                        "fix_id": row["metadata"].get("fix_id"),
                        "locator": row.get("locator"),
                        "relationship": row["metadata"].get("resolution_relationship"),
                    }
                    for row in rows
                ],
            )
        )
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    parser.add_argument("--population-register", type=Path)
    parser.add_argument(
        "--dependency-root",
        type=Path,
        help="Prepared runtime override; original requests remain immutable",
    )
    parser.add_argument("--sandbox-backend", choices=TOOL_BACKENDS, default="namespace-bind")
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args(argv)
    requests = json.loads(args.requests.read_text())
    if args.population_register:
        from arex_skill_graph.history_census import fingerprint

        register = json.loads(args.population_register.read_text())
        if (
            register["requests_sha256"] != fingerprint(requests)
            or register["cutoff_exclusive"] != args.cutoff
        ):
            raise ValueError("historical verification population integrity changed")
    results = []
    scheduled = canonical_repair_requests(requests)
    if args.workers < 1:
        raise ValueError("historical verification workers must be positive")

    def run_request(request, aliases):
        relative = request["issue_id"].replace("/", "__").replace(":", "-")
        if args.population_register:
            relative += "-" + request["metadata"]["mergeCommit"]["oid"][:12]
        try:
            result = verify_historical_repair(
                request["repository_path"],
                request["metadata"],
                request["issue_id"],
                args.cutoff,
                args.output_dir / relative,
                args.dependency_root or request["dependency_root"],
                request.get("command"),
                sandbox_backend=args.sandbox_backend,
            )
            result_row = {
                "issue_id": request["issue_id"],
                "verified_resolution": result["verified_resolution"],
                "verification_path": str(args.output_dir / relative / "verification.json"),
                "fix_id": request["metadata"].get("fix_id"),
                "request_aliases": aliases,
                "fail_to_pass_count": len(result["fail_to_pass"]),
                "pass_to_pass_count": len(result["pass_to_pass"]),
            }
        except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as error:
            result_row = {
                "issue_id": request["issue_id"],
                "verified_resolution": False,
                "fix_id": request["metadata"].get("fix_id"),
                "request_aliases": aliases,
                "reason": (
                    "historical source command failed"
                    if isinstance(error, subprocess.CalledProcessError)
                    else redact_history(str(error))
                ),
            }
            write_json(args.output_dir / relative / "verification-failure.json", result_row)
        print(json.dumps(result_row), flush=True)
        return result_row

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        pending = [executor.submit(run_request, request, aliases) for request, aliases in scheduled]
        for future in as_completed(pending):
            results.append(future.result())
            write_json(
                args.output_dir / "verification-progress.json",
                {
                    "completed_count": len(results),
                    "canonical_requested_count": len(scheduled),
                    "results": results,
                    "full_history_qualified": False,
                    "formal_SWE_runs": 0,
                },
            )
    write_json(
        args.output_dir / "verification-inventory.json",
        {
            "schema": "historical-development-verification-inventory-v1",
            "results": results,
            "development_subset": args.population_register is None,
            "population_register": str(args.population_register)
            if args.population_register
            else None,
            "requested_count": len(requests),
            "canonical_requested_count": len(scheduled),
            "alias_policy": "same issue/repository/merge SHA; strongest observed closure then PR metadata; no independent-source multiplication",
            "runtime_override": str(args.dependency_root) if args.dependency_root else None,
            "sandbox_backend": args.sandbox_backend,
            "full_history_qualified": False,
            "formal_SWE_runs": 0,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
