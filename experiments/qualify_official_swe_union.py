#!/usr/bin/env python3
"""Pre-register representatives and qualify official controls for the full new-issue union.

This is independent environment/oracle preparation. It does not qualify public
inputs or semantic bug clusters, freeze a cohort, or run a repair solver.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.history_census import fingerprint, write_json
from arex_skill_graph.official_swe import (
    QualificationFailure,
    load_private_registered_instance,
    qualify_official_instance,
    verify_harness,
)

PRIORITY = {"Live/verified": 0, "Live/test": 1, "Live/full": 2, "Live/lite": 3}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--union", type=Path, required=True)
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--harness-root", type=Path, required=True)
    parser.add_argument("--harness-commit", required=True)
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--docker-host", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args(argv)
    import docker

    verify_harness(args.harness_root, args.harness_commit)
    union = json.loads(args.union.read_text())
    register = json.loads(args.register.read_text())
    client = docker.DockerClient(base_url=args.docker_host, timeout=args.timeout + 120)
    scheduled, excluded = [], []
    for record in union["records"]:
        if record["temporal_classification"] != "post-cutoff-new-issue-candidate":
            continue
        if record["exposed_gold_development_only"] or record["mapping_reference_conflict"]:
            excluded.append(
                {
                    "pull_number": record["pull_number"],
                    "reason": "exposed-development"
                    if record["exposed_gold_development_only"]
                    else "identity-reference-conflict-pending",
                }
            )
            continue
        candidates = [a for a in record["aliases"] if a["variant"] in PRIORITY]
        if not candidates:
            excluded.append(
                {
                    "pull_number": record["pull_number"],
                    "reason": "registered-official-runtime-not-supported",
                }
            )
            continue
        alias = min(candidates, key=lambda a: (PRIORITY[a["variant"]], a["instance_id"]))
        scheduled.append(
            {
                "pull_number": record["pull_number"],
                "variant": alias["variant"],
                "instance_id": alias["instance_id"],
                "base_commit": alias["base_commit"],
                "issue_alias_cluster_id": record["issue_alias_cluster_id"],
                "original_issue_ids": record["cluster_original_issue_ids"],
            }
        )
    scheduling = {
        "schema": "official-oracle-union-pre-registration-v1",
        "scheduled": scheduled,
        "excluded": excluded,
        "union_sha256": fingerprint(union),
        "source_register_sha256": fingerprint(register),
        "priority": PRIORITY,
        "selection_uses_solver_or_oracle_results": False,
    }
    schedule_path = args.output_dir / "scheduling.json"
    if schedule_path.exists() and json.loads(schedule_path.read_text()) != scheduling:
        raise ValueError("official control population changed; preserve it and use a new version")
    write_json(schedule_path, scheduling)
    results = []
    for row in scheduled:
        try:
            instance, provenance = load_private_registered_instance(
                register, row["variant"], row["instance_id"]
            )
            if instance["base_commit"] != row["base_commit"]:
                raise QualificationFailure("registered_representative_base_changed")
            image_name = (
                args.namespace + "/sweb.eval.x86_64." + row["instance_id"].replace("__", "_1776_")
            )
            try:
                client.images.get(image_name)
            except docker.errors.ImageNotFound:
                client.images.pull(image_name)
            result = qualify_official_instance(
                client,
                instance,
                provenance,
                args.output_dir / row["instance_id"],
                namespace=args.namespace,
                harness_commit=args.harness_commit,
                timeout=args.timeout,
            )
            summary = {
                **row,
                "qualified_official_oracle": result["qualified_official_oracle"],
                "fail_to_pass_count": result["fail_to_pass_count"],
                "pass_to_pass_count": result["pass_to_pass_count"],
                "formal_task_qualified": False,
                "formal_SWE_solver_runs": 0,
            }
        except Exception as error:  # noqa: BLE001 -- Population boundary retains failed requests for audit.
            summary = {
                **row,
                "qualified_official_oracle": False,
                "failure_type": type(error).__name__,
                "failure_code": error.code if isinstance(error, QualificationFailure) else None,
                "native_private_output_suppressed": True,
                "formal_task_qualified": False,
                "formal_SWE_solver_runs": 0,
            }
        results.append(summary)
        write_json(
            args.output_dir / "qualification-inventory.json",
            {
                "schema": "official-swe-union-control-inventory-v1",
                "results": results,
                "scheduled_count": len(scheduled),
                "completed_count": len(results),
                "scheduling_sha256": fingerprint(scheduling),
                "qualified_N": None,
                "all_formal_qualifications_complete": False,
                "formal_SWE_solver_runs": 0,
            },
        )
        print(json.dumps(summary), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
