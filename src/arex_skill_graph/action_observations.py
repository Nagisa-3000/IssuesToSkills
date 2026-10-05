"""Record witnessed Action outputs without promoting model claims to current facts.

The broker supplies actual tool results. Declared port states remain unreviewed;
an independent functional evaluator must judge effects and preservation.
"""

from __future__ import annotations

import hashlib
from dataclasses import asdict
from pathlib import Path

from .action_contracts import digest
from .skill_packages import _resolve
from .task_context import PortValue, assert_public
from .workspace_state import public_workspace_execution_sha256, public_workspace_sha256

MAX_ARTIFACT_BYTES = 16 * 1024 * 1024
WITNESS_OPERATIONS = frozenset({"read_file", "write_file", "run_public_command"})


def _record_witnesses(observation_ids, paths, task, broker_observations, record_id, witnesses):
    if any(
        not isinstance(v, list)
        or any(not isinstance(s, str) or not s for s in v)
        or len(set(v)) != len(v)
        for v in (observation_ids, paths)
    ):
        raise ValueError("Output witnesses must be unique nonempty string arrays")
    if not observation_ids and not paths:
        raise ValueError("Expected output without an actual witness is not an observation")
    refs = []
    for identity in observation_ids:
        observation = broker_observations.get(identity)
        if (
            not isinstance(observation, dict)
            or observation.get("operation") not in WITNESS_OPERATIONS
            or observation.get("observation_id") != identity
        ):
            raise ValueError("Output refers to an unobserved or non-tool result")
        assert_public(observation)
        ref = record_id + ":tool:" + identity
        witnesses[ref] = {
            "id": ref,
            "kind": "broker_observation",
            "record_sha256": digest(observation),
            "record": observation,
        }
        refs.append(ref)
    for relative in paths:
        if relative == ".git" or relative.startswith(".git/"):
            raise ValueError("Version history cannot witness a public Action output")
        path = _resolve(Path(task.root), relative)
        if not path.is_file() or path.stat().st_size > MAX_ARTIFACT_BYTES:
            raise ValueError("Action artifact is missing or exceeds the public file limit")
        ref = record_id + ":artifact:" + relative
        witnesses[ref] = {
            "id": ref,
            "kind": "current_artifact",
            "path": relative,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "context_revision": task.revision,
        }
        refs.append(ref)
    return refs


def record_action_observation(action, request, task, broker_observations, *, record_id):
    """Record real execution evidence; declared artifact ports remain optional.

    Actions with no declared ports use v4 explicit top-level observation_ids and
    artifact_paths, with outputs=[]; actions with ports retain the v3 protocol.

    This does not mutate TaskContext, confirm semantic predicates, establish
    prerequisites, authorize an edit, or turn a failed Oracle into a pass.
    """
    assert_public(request)
    portless = not action.outputs
    fields = {"action_id", "context_revision", "outputs", "summary"}
    if portless:
        fields |= {"observation_ids", "artifact_paths"}
    if not isinstance(request, dict) or set(request) != fields:
        raise ValueError("Action observation requires exact documented fields")
    if request["action_id"] != action.id:
        raise ValueError("Action observation changed the approved Action identity")
    if type(request["context_revision"]) is not int or request["context_revision"] != task.revision:
        raise ValueError("Action observation must name the current context revision")
    if not isinstance(request["summary"], str) or not request["summary"].strip():
        raise ValueError("Action observation needs a nonempty account of performed work")
    items = request["outputs"]
    if not isinstance(items, list) or (not portless and not items):
        raise ValueError("Action observation needs actual witnessed outputs")
    expected = {port.name: port for port in action.outputs}
    emitted, witnesses, seen = [], {}, set()
    execution_refs = []
    if portless:
        if items:
            raise ValueError("Action without declared ports cannot invent an output")
        execution_refs = _record_witnesses(
            request["observation_ids"],
            request["artifact_paths"],
            task,
            broker_observations,
            record_id,
            witnesses,
        )
    for item in items:
        if not isinstance(item, dict) or set(item) != {
            "port_name",
            "observation_ids",
            "artifact_paths",
        }:
            raise ValueError("Output needs an exact port name and explicit witnesses")
        name = item["port_name"]
        if not isinstance(name, str) or name not in expected or name in seen:
            raise ValueError("Output port is unknown or duplicated")
        seen.add(name)
        observation_ids, paths = item["observation_ids"], item["artifact_paths"]
        refs = _record_witnesses(
            observation_ids, paths, task, broker_observations, record_id, witnesses
        )
        emitted.append(asdict(PortValue(expected[name], tuple(refs))))
    if {p.name for p in action.outputs if not p.optional} - seen:
        raise ValueError("Action observation is missing a required output")
    if any(not set(value["evidence_refs"]).issubset(witnesses) for value in emitted):
        raise ValueError("Action observation witness references are not closed")
    result = {
        "schema": "arex-action-observation-v4" if portless else "arex-action-observation-v3",
        "workspace_execution_sha256": public_workspace_execution_sha256(task.root),
        "workspace_sha256": public_workspace_sha256(task.root),
        "id": record_id,
        "action_id": action.id,
        "package_id": action.package_id,
        "package_sha256": action.package_hash,
        "action_contract_sha256": digest(action.to_dict()),
        "action_resource": action.resource,
        "task_id": task.task_id,
        "base_commit": task.base_commit,
        "context_revision": task.revision,
        "summary": request["summary"],
        "outputs": emitted,
        "witnesses": list(witnesses.values()),
        "semantic_validation": "unreviewed",
        "current_facts_promoted": False,
        "current_ports_promoted": False,
        "repair_success_established": False,
    }
    if portless:
        result["execution_evidence_refs"] = execution_refs
    assert_public(result)
    return result
