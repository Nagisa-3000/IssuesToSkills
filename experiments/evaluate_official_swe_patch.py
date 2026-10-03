#!/usr/bin/env python3
"""Independent official acceptance after the public solver has stopped."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.official_swe import (
    evaluate_official_solver_patch,
    load_private_registered_instance,
    verify_harness,
)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("register", "qualification", "patch", "output-dir", "harness-root"):
        parser.add_argument("--" + option, type=Path, required=True)
    parser.add_argument("--docker-host", required=True)
    args = parser.parse_args(argv)
    import docker

    qualification = json.loads(args.qualification.read_text())
    identity = qualification["identity"]
    verify_harness(args.harness_root, identity["harness_commit"])
    instance, provenance = load_private_registered_instance(
        json.loads(args.register.read_text()),
        identity["source"]["variant"],
        identity["instance_id"],
    )
    result = evaluate_official_solver_patch(
        docker.DockerClient(base_url=args.docker_host, timeout=660),
        instance,
        provenance,
        qualification,
        args.patch.read_text(),
        args.output_dir,
    )
    print(json.dumps(result), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
