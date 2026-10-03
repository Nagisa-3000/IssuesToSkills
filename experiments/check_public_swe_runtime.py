#!/usr/bin/env python3
"""Check the public Docker tool boundary on an exposed development environment."""

import argparse
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.docker_public_tools import DockerPublicTools
from arex_skill_graph.history_census import write_json
from arex_skill_graph.public_swe import prepare_public_swe_base


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qualification", type=Path, required=True)
    parser.add_argument("--docker-host", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    qualification = json.loads(args.qualification.read_text())
    if (
        not qualification["qualified_official_oracle"]
        or qualification["identity"]["development_only"] is not True
    ):
        raise ValueError("runtime smoke requires a qualified exposed development environment")
    import docker

    client = docker.DockerClient(base_url=args.docker_host, timeout=180)
    image = qualification["image"]
    prepared = prepare_public_swe_base(
        client,
        image["image_id"],
        image["repository_digest"],
        qualification["identity"]["base_commit"],
        args.output_dir / "public-base",
    )
    # Public tools receive a snapshot without .git, exactly as AdaptiveSolver does.
    from arex_skill_graph.history_verification import archive_revision

    with tempfile.TemporaryDirectory(prefix="arex-docker-smoke-") as scratch:
        archive_revision(
            Path(prepared["checkout"]) / ".git", prepared["base_commit"], Path(scratch) / "work"
        )
        tools = DockerPublicTools(
            Path(scratch) / "work",
            BudgetLedger(BudgetCaps(seconds=300)),
            client=client,
            image_id=image["image_id"],
            repository_digest=image["repository_digest"],
        )
        tools.preflight()
        probe = tools.run(
            [
                "python",
                "-c",
                "import pylint,sys; print('PUBLIC_PYLINT_IMPORTED'); print(sys.version_info[:3])",
            ]
        )
        result = {
            "schema": "public-swe-runtime-smoke-v1",
            "preflight": "passed",
            "probe_exit_code": probe["exit_code"],
            "probe_output": probe["output"],
            "runtime_sha256": tools.runtime_sha256,
            "isolation": tools.isolation,
            "public_base": prepared,
            "development_only": True,
            "formal_SWE_solver_runs": 0,
        }
    write_json(args.output_dir / "runtime-smoke.json", result)
    print(
        json.dumps(
            {
                "preflight": result["preflight"],
                "probe_exit_code": result["probe_exit_code"],
                "formal_SWE_solver_runs": 0,
            }
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
