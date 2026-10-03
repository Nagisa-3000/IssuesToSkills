"""Pinned official SWE controls, confined to the independent evaluator process.

The caller receives only identity, environment and aggregate oracle qualification.
Raw solutions stay in anonymous input memory and isolated evaluator containers.
This module is never imported into a solver's public tool namespace.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import tarfile
import time
from pathlib import Path

from .benchmark_identity import public_file_in_memory
from .history_census import fingerprint, now, redact_history, write_json


class QualificationFailure(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__("official qualification failed: " + code)


def load_private_registered_instance(register, variant_name, instance_id):
    import duckdb

    variants = [v for v in register["variants_with_target"] if v["variant"] == variant_name]
    if len(variants) != 1:
        raise QualificationFailure("registered_variant_not_unique")
    variant = variants[0]
    found, source_files = [], []
    for source in variant["files"]:
        with public_file_in_memory(source["source_url"], source["sha256"]) as (memory, size):
            connection = duckdb.connect(":memory:")
            try:
                reader = (
                    "read_parquet(?)"
                    if source["file"].endswith(".parquet")
                    else "read_json_auto(?,format='newline_delimited',union_by_name=true)"
                )
                cursor = connection.execute(
                    f"SELECT * FROM {reader} WHERE instance_id=?", [memory, instance_id]
                )
                columns = [item[0] for item in cursor.description]
                found.extend(dict(zip(columns, row)) for row in cursor.fetchall())
            finally:
                connection.close()
        source_files.append({"file": source["file"], "sha256": source["sha256"], "bytes": size})
    if len(found) != 1 or found[0]["repo"].lower() not in {"pylint-dev/pylint", "pycqa/pylint"}:
        raise QualificationFailure("registered_instance_unavailable_or_ambiguous")
    return found[0], {
        "variant": variant["variant"],
        "dataset_id": variant["dataset_id"],
        "revision": variant["revision"],
        "files": source_files,
        "raw_dataset_persisted": False,
        "solution_fields_exported": False,
    }


def memory_tar(name, text):
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+", name):
        raise ValueError("evaluator resource name must be local")
    payload = text.encode()
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        item = tarfile.TarInfo(name)
        item.size, item.mode = len(payload), 0o600
        archive.addfile(item, io.BytesIO(payload))
    return stream.getvalue()


def verify_harness(root, commit):
    import swebench

    root = Path(root).resolve()
    if not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise ValueError("official harness must be pinned")
    git = ["git", "-c", "safe.directory=" + str(root), "-C", str(root)]
    current = subprocess.check_output([*git, "rev-parse", "HEAD"], text=True).strip()
    if current != commit or Path(swebench.__file__).resolve().parents[1] != root:
        raise ValueError("loaded official harness differs from its pinned checkout")
    dirty = subprocess.check_output([*git, "diff", "--name-only", "HEAD"], text=True)
    if dirty.strip():
        raise ValueError("pinned official harness has modified source files")


def evaluator_control(client, image, instance, spec, patch, output, *, timeout=600):
    from docker.errors import DockerException
    from requests.exceptions import RequestException
    from swebench.harness.constants import FAIL_TO_PASS, PASS_TO_PASS
    from swebench.harness.grading import get_eval_tests_report, get_logs_eval

    output = Path(output)
    output.mkdir(parents=True, exist_ok=True, mode=0o700)
    output.chmod(0o700)
    # The official script and patches enter only this evaluator container. No
    # host mount, credential environment, Docker socket, or external network.
    container = client.containers.create(
        image.id,
        ["sleep", "infinity"],
        network_disabled=True,
        cap_drop=["ALL"],
        security_opt=["no-new-privileges:true"],
        mem_limit="4g",
        nano_cpus=2_000_000_000,
        pids_limit=256,
        environment={"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1"},
    )
    started = time.monotonic()
    try:
        container.start()
        reset = container.exec_run(
            [
                "git",
                "-c",
                "safe.directory=/testbed",
                "-C",
                "/testbed",
                "reset",
                "--hard",
                instance["base_commit"],
            ]
        )
        if reset.exit_code:
            raise QualificationFailure("registered_base_reset_failed")
        if patch:
            # This private file is transferred directly to the container, never
            # exported as an artifact or passed to a model/controller input.
            container.put_archive("/", memory_tar("repair.diff", patch))
            applied = container.exec_run(
                ["bash", "-c", "cd /testbed && git apply --whitespace=nowarn /repair.diff"]
            )
            if applied.exit_code:
                raise QualificationFailure("historical_gold_control_apply_failed")
        container.put_archive("/", memory_tar("eval.sh", spec.eval_script))
        # A shell timeout also bounds the Docker exec's descendants inside this
        # isolated container; finally always removes the complete container.
        result = container.exec_run(["timeout", str(timeout), "bash", "/eval.sh"])
        raw = result.output.decode("utf-8", errors="replace")
        log = output / "private-test-output.txt"
        log.write_text(redact_history(raw))
        log.chmod(0o600)
        status, parsed = get_logs_eval(spec, str(log))
        expected = {FAIL_TO_PASS: spec.FAIL_TO_PASS, PASS_TO_PASS: spec.PASS_TO_PASS}
        report = get_eval_tests_report(status, expected)
        required = set(spec.FAIL_TO_PASS) | set(spec.PASS_TO_PASS)
        return {
            "parsed_official_test_output": parsed,
            "command_exit_code": result.exit_code,
            "observed_test_count": len(status),
            "required_test_count": len(required),
            "missing_required_test_count": len(required - set(status)),
            "fail_to_pass_passed": len(report[FAIL_TO_PASS]["success"]),
            "fail_to_pass_failed": len(report[FAIL_TO_PASS]["failure"]),
            "pass_to_pass_passed": len(report[PASS_TO_PASS]["success"]),
            "pass_to_pass_failed": len(report[PASS_TO_PASS]["failure"]),
            "elapsed_seconds": time.monotonic() - started,
            "private_log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
            "test_names_exported": False,
            "solution_exported": False,
        }
    except (DockerException, RequestException) as error:
        # Native Docker/network messages may include private command output.
        raise RuntimeError(
            f"official evaluator infrastructure failed ({type(error).__name__})"
        ) from None
    finally:
        container.remove(force=True)


def qualify_official_instance(
    client,
    instance,
    provenance,
    output,
    *,
    namespace,
    harness_commit,
    timeout=600,
    development_only=False,
):
    from swebench.harness.test_spec.test_spec import make_test_spec

    output = Path(output)
    identity = {
        "instance_id": instance["instance_id"],
        "repository": instance["repo"],
        "base_commit": instance["base_commit"],
        "source": provenance,
        "harness_commit": harness_commit,
        "namespace": namespace,
        "test_patch_sha256": hashlib.sha256(instance["test_patch"].encode()).hexdigest(),
        "repair_patch_sha256": hashlib.sha256(instance["patch"].encode()).hexdigest(),
        "timeout_seconds": timeout,
        "development_only": development_only,
    }
    checkpoint = output / "qualification.json"
    if checkpoint.exists():
        saved = json.loads(checkpoint.read_text())
        if saved["identity"] != identity or saved["controls_sha256"] != fingerprint(
            saved["controls"]
        ):
            raise ValueError("official qualification identity/control record changed")
        client.images.get(saved["image"]["image_id"])
        return saved
    spec = make_test_spec(instance, namespace=namespace)
    image = client.images.get(spec.instance_image_key)
    digests = [
        value for value in image.attrs.get("RepoDigests", []) if value.startswith(namespace + "/")
    ]
    if len(digests) != 1:
        raise QualificationFailure("official_image_repository_digest_not_unique")
    controls = {
        "base_with_hidden_regression": evaluator_control(
            client, image, instance, spec, "", output / "base", timeout=timeout
        ),
        "historical_gold_control": evaluator_control(
            client, image, instance, spec, instance["patch"], output / "gold", timeout=timeout
        ),
    }
    before, after = controls.values()
    nf, np = len(spec.FAIL_TO_PASS), len(spec.PASS_TO_PASS)
    qualified = (
        bool(nf)
        and bool(np)
        and before["parsed_official_test_output"]
        and after["parsed_official_test_output"]
        and not before["missing_required_test_count"]
        and not after["missing_required_test_count"]
        and before["fail_to_pass_failed"] == nf
        and before["pass_to_pass_passed"] == np
        and after["fail_to_pass_passed"] == nf
        and after["pass_to_pass_passed"] == np
        and before["observed_test_count"] == after["observed_test_count"]
        and after["command_exit_code"] == 0
    )
    result = {
        "schema": "official-swe-oracle-qualification-v1",
        "checked_at": now(),
        "identity": identity,
        "image": {"image_id": image.id, "repository_digest": digests[0]},
        "qualified_official_oracle": qualified,
        "controls": controls,
        "controls_sha256": fingerprint(controls),
        "fail_to_pass_count": nf,
        "pass_to_pass_count": np,
        "neighbor_regression_qualification": "not-executed",
        "formal_task_qualified": False,
        "formal_SWE_solver_runs": 0,
        "public_solver_received_hidden_material": False,
    }
    write_json(checkpoint, result)
    return result


def evaluate_official_solver_patch(
    client, instance, provenance, qualification, patch, output, *, timeout=600
):
    """Run only after solver termination; export aggregate acceptance, never tests."""
    from swebench.harness.test_spec.test_spec import make_test_spec

    identity = qualification["identity"]
    if (
        not qualification["qualified_official_oracle"]
        or identity["instance_id"] != instance["instance_id"]
        or identity["base_commit"] != instance["base_commit"]
        or identity["source"] != provenance
        or identity["test_patch_sha256"]
        != hashlib.sha256(instance["test_patch"].encode()).hexdigest()
    ):
        raise QualificationFailure("solver_evaluator_qualification_identity_changed")
    image = client.images.get(qualification["image"]["image_id"])
    if qualification["image"]["repository_digest"] not in image.attrs.get("RepoDigests", []):
        raise QualificationFailure("solver_evaluator_image_digest_changed")
    spec = make_test_spec(instance, namespace=identity["namespace"])
    observation = evaluator_control(client, image, instance, spec, patch, output, timeout=timeout)
    nf, np = len(spec.FAIL_TO_PASS), len(spec.PASS_TO_PASS)
    resolved = (
        observation["parsed_official_test_output"]
        and observation["command_exit_code"] == 0
        and not observation["missing_required_test_count"]
        and observation["fail_to_pass_passed"] == nf
        and observation["pass_to_pass_passed"] == np
    )
    return {
        "benchmark_resolved": resolved,
        "validated_resolved": False,
        "neighbor_regression_qualification": "not-executed",
        "official_observation": observation,
        "evaluator_version": "official-swe:" + identity["harness_commit"],
        "evaluation_spec_sha256": fingerprint(identity),
        "official_regression_pass": observation["pass_to_pass_passed"] == np,
        "regression_exit_codes": [0 if observation["pass_to_pass_passed"] == np else 1],
        "solution_exported": False,
        "hidden_results_returned_to_solver": False,
    }
