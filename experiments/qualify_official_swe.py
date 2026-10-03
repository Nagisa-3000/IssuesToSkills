#!/usr/bin/env python3
"""Run official base/gold controls without exporting private solutions or test names."""

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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--instance-id", action="append", required=True)
    parser.add_argument("--harness-root", type=Path, required=True)
    parser.add_argument("--harness-commit", required=True)
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--docker-host", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--development-only", action="store_true")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args(argv)
    import docker

    verify_harness(args.harness_root, args.harness_commit)
    register = json.loads(args.register.read_text())
    client = docker.DockerClient(base_url=args.docker_host, timeout=args.timeout + 30)
    results = []
    for instance_id in args.instance_id:
        try:
            instance, provenance = load_private_registered_instance(
                register, args.variant, instance_id
            )
            result = qualify_official_instance(
                client,
                instance,
                provenance,
                args.output_dir / instance_id,
                namespace=args.namespace,
                harness_commit=args.harness_commit,
                timeout=args.timeout,
                development_only=args.development_only,
            )
            row = {
                "instance_id": instance_id,
                "qualified_official_oracle": result["qualified_official_oracle"],
                "fail_to_pass_count": result["fail_to_pass_count"],
                "pass_to_pass_count": result["pass_to_pass_count"],
                "formal_task_qualified": False,
                "formal_SWE_solver_runs": 0,
            }
        except Exception as error:  # noqa: BLE001 -- Population boundary retains failed requests for audit.
            row = {
                "instance_id": instance_id,
                "qualified_official_oracle": False,
                "failure_type": type(error).__name__,
                "native_private_output_suppressed": True,
                "failure_code": error.code if isinstance(error, QualificationFailure) else None,
                "formal_task_qualified": False,
                "formal_SWE_solver_runs": 0,
            }
        results.append(row)
        print(json.dumps(row), flush=True)
    write_json(
        args.output_dir / "qualification-inventory.json",
        {
            "schema": "official-swe-oracle-qualification-inventory-v1",
            "results": results,
            "source_register_sha256": fingerprint(register),
            "harness_commit": args.harness_commit,
            "development_only": args.development_only,
            "all_formal_qualifications_complete": False,
            "qualified_N": None,
            "formal_SWE_solver_runs": 0,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
