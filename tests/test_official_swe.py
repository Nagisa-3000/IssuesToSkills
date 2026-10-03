"""Exercise qualification boundaries using synthetic evaluator controls."""

import io
import json
import sys
import tarfile
from types import SimpleNamespace

import pytest

from arex_skill_graph.official_swe import (
    QualificationFailure,
    memory_tar,
    qualify_official_instance,
)


def official_fixture(monkeypatch):
    spec = SimpleNamespace(
        FAIL_TO_PASS=["synthetic-f2p"],
        PASS_TO_PASS=["synthetic-p2p"],
        instance_image_key="example/synthetic-image",
    )
    monkeypatch.setitem(
        sys.modules,
        "swebench.harness.test_spec.test_spec",
        SimpleNamespace(make_test_spec=lambda *a, **k: spec),
    )
    image = SimpleNamespace(
        id="sha256:synthetic", attrs={"RepoDigests": ["example/image@sha256:synthetic"]}
    )
    client = SimpleNamespace(images=SimpleNamespace(get=lambda _: image))
    instance = {
        "instance_id": "synthetic-1",
        "repo": "synthetic/project",
        "base_commit": "a" * 40,
        "test_patch": "synthetic hidden tests",
        "patch": "synthetic repair",
    }
    return client, instance, spec, image


def control(*, fixed):
    return {
        "parsed_official_test_output": True,
        "command_exit_code": 0 if fixed else 1,
        "observed_test_count": 2,
        "required_test_count": 2,
        "missing_required_test_count": 0,
        "fail_to_pass_passed": int(fixed),
        "fail_to_pass_failed": int(not fixed),
        "pass_to_pass_passed": 1,
        "pass_to_pass_failed": 0,
        "private_log_sha256": "b" * 64,
    }


def test_memory_transfer_has_contained_private_permissions():
    raw = memory_tar("repair.diff", "synthetic repair")
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        (member,) = archive.getmembers()
        assert member.name == "repair.diff" and member.mode == 0o600
        assert archive.extractfile(member).read() == b"synthetic repair"
    with pytest.raises(ValueError):
        memory_tar("../outside", "synthetic")


@pytest.mark.parametrize(
    "mutation", [None, "missing", "base_pass", "gold_failure", "p2p_failure", "count_change"]
)
def test_qualification_requires_both_official_controls(monkeypatch, tmp_path, mutation):
    client, instance, _, _ = official_fixture(monkeypatch)

    def evaluate(client, image, instance, spec, patch, output, **kwargs):
        result = control(fixed=bool(patch))
        if mutation == "missing":
            result["missing_required_test_count"] = 1
        elif mutation == "base_pass" and not patch:
            result["fail_to_pass_failed"] = 0
        elif mutation == "gold_failure" and patch:
            result["command_exit_code"] = 1
        elif mutation == "p2p_failure" and patch:
            result["pass_to_pass_passed"] = 0
        elif mutation == "count_change" and patch:
            result["observed_test_count"] = 3
        return result

    monkeypatch.setattr("arex_skill_graph.official_swe.evaluator_control", evaluate)
    result = qualify_official_instance(
        client,
        instance,
        {"source": "synthetic"},
        tmp_path,
        namespace="example",
        harness_commit="c" * 40,
    )
    assert result["qualified_official_oracle"] is (mutation is None)
    assert result["formal_task_qualified"] is False
    assert result["formal_SWE_solver_runs"] == 0
    exported = json.dumps(result)
    assert "synthetic hidden tests" not in exported
    assert "synthetic repair" not in exported
    assert "synthetic-f2p" not in exported


def test_qualification_rejects_ambiguous_image_digest(monkeypatch, tmp_path):
    client, instance, _, image = official_fixture(monkeypatch)
    image.attrs["RepoDigests"].append("example/other@sha256:different")
    with pytest.raises(QualificationFailure, match="digest_not_unique"):
        qualify_official_instance(
            client, instance, {}, tmp_path, namespace="example", harness_commit="c" * 40
        )


def test_qualification_checkpoint_rejects_control_tampering(monkeypatch, tmp_path):
    client, instance, _, _ = official_fixture(monkeypatch)
    monkeypatch.setattr(
        "arex_skill_graph.official_swe.evaluator_control", lambda *a, **k: control(fixed=bool(a[4]))
    )
    qualify_official_instance(
        client, instance, {}, tmp_path, namespace="example", harness_commit="c" * 40
    )
    path = tmp_path / "qualification.json"
    saved = json.loads(path.read_text())
    saved["controls"]["historical_gold_control"]["fail_to_pass_passed"] = 0
    path.write_text(json.dumps(saved))
    with pytest.raises(ValueError, match="control record changed"):
        qualify_official_instance(
            client, instance, {}, tmp_path, namespace="example", harness_commit="c" * 40
        )
