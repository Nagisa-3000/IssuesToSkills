#!/usr/bin/env python3
"""Prepare native edit input boundaries by exactly reapplying a sealed inspection review."""

import argparse
import hashlib
import json
import shutil
import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import TemporalPolicy, digest
from arex_skill_graph.action_grounding import review_action_observation
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.adaptive_cli import read_references
from arex_skill_graph.execution_frontier import action_execution_checks
from arex_skill_graph.pattern_contracts import load_native_package
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.workspace_state import (
    public_workspace_execution_sha256,
    public_workspace_sha256,
)


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def exact_reapplication(task, action, record, observations, transcript, accepted_record_review):
    """No network request; original current evidence and semantic response must match."""
    if transcript["response"] != {
        "checks": [
            {k: v for k, v in check.items() if k != "reviewer"}
            for check in accepted_record_review["checks"]
        ]
    }:
        raise ValueError("reapplication response differs from the sealed accepted review")
    model = accepted_record_review["reviewer"].removeprefix("action-output-review:")

    class ExactReplay:
        calls = []
        config = SimpleNamespace(model=model, max_output_tokens=5000, retries=0)
        count = 0

        def complete(self, **request):
            if self.count:
                raise ValueError("one accepted response authorizes exactly one reapplication")
            if (
                request["system"] != transcript["system"]
                or json.loads(request["user"]) != json.loads(transcript["user"])
                or request["response_schema"] != transcript["response_schema"]
            ):
                raise ValueError("reapplication request differs from the original reviewed context")
            self.count += 1
            return transcript["response"]

    transport = ExactReplay()
    current, audit = review_action_observation(
        task,
        action,
        record,
        observations,
        transport,
        BudgetLedger(BudgetCaps(model_tokens=1000000, history_tokens=20000)),
    )
    if digest(audit) != digest(accepted_record_review) or transport.count != 1:
        raise ValueError("reapplication changed the sealed accepted Action verdict")
    return current, {
        "schema": "native-action-exact-review-reapplication-v1",
        "original_request_sha256": digest(
            {
                "system": transcript["system"],
                "user": json.loads(transcript["user"]),
                "response_schema": transcript["response_schema"],
            }
        ),
        "original_response_sha256": digest(transcript["response"]),
        "record_sha256": digest(record),
        "same_current_workspace": True,
        "new_actual_model_calls": 0,
        "new_independent_review": False,
        "repair_success_established": False,
        "formal_KB_admitted": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("inspection-manifest", "accepted-audit", "review-directory", "output-dir"):
        parser.add_argument("--" + option, type=Path, required=True)
    args = parser.parse_args(argv)
    if args.output_dir.exists():
        raise ValueError("preserve existing edit cases; use a new output directory")
    manifest = json.loads(args.inspection_manifest.read_text())
    case = next(c for c in manifest["cases"] if c["opaque_id"] == "q0")
    accepted = next(
        c for c in json.loads(args.accepted_audit.read_text())["cases"] if c["case"] == "q0"
    )
    review_path = args.review_directory / "reviews/q0-review.json"
    if hashlib.sha256(review_path.read_bytes()).hexdigest() != accepted["review_file_sha256"]:
        raise ValueError("independent inspection review changed after its accepted audit")
    task_path = Path(case["task_context"])
    if hashlib.sha256(task_path.read_bytes()).hexdigest() != case["task_context_sha256"]:
        raise ValueError("original inspection Task input changed")
    trajectory_path = Path(case["output_dir"]) / "trajectory.json"
    trajectory = json.loads(trajectory_path.read_text())
    review = json.loads(review_path.read_text())
    if digest(trajectory) != accepted["trajectory_sha256"] or review["trajectory_sha256"] != digest(
        trajectory
    ):
        raise ValueError("original inspection trajectory changed")
    if (
        review["policy_review"] != accepted["policy_review"]
        or review["policy_review"]["verdict"] != "PASS"
        or review["policy_review"]["behavior"] != "correct_confirmation"
    ):
        raise ValueError("edit input requires accepted independent inspection confirmation")
    transcripts_path = args.review_directory / "reviews/q0-review-transcript.json"
    transcripts = json.loads(transcripts_path.read_text())
    # A transcript alone never authorizes a verdict. The accepted audit above does.
    if (
        len(transcripts.get("calls", [])) != 2
        or len(transcripts.get("transcripts", [])) != 2
        or any(not call.get("successful") for call in transcripts["calls"])
        or any(
            call.get("response_id") != turn.get("response_id")
            for call, turn in zip(transcripts["calls"], transcripts["transcripts"], strict=True)
        )
    ):
        raise ValueError("accepted inspection review lacks its complete actual call transcript")
    if digest(json.loads(transcripts["transcripts"][1]["user"])) != review["review_input_sha256"]:
        raise ValueError("independent policy request changed")
    if transcripts["transcripts"][1]["response"] != review["policy_review"]:
        raise ValueError("independent policy response changed")
    (package,) = [
        p
        for r in read_references(Path(manifest["references"]))
        if (p := load_native_package(r, TemporalPolicy("2024-01-01T00:00:00Z"))).reference[
            "package_sha256"
        ]
        == manifest["package_sha256"]
    ]
    inspection = next(a for a in package.actions if a.id == manifest["action_id"])
    edit = next(a for a in package.actions if a.id.endswith(":overload-edit"))
    task = TaskContext.from_dict(json.loads(task_path.read_text()))
    observations = {
        o["observation_id"]: o for o in trajectory["public_observations"] if o.get("observation_id")
    }
    task = replace(
        task,
        revision=max(
            [task.revision, *[o.get("context_revision", 0) for o in observations.values()]]
        ),
    )
    if len(trajectory["action_observations"]) != 1 or len(review["record_reviews"]) != 1:
        raise ValueError("preparation requires one sealed inspection observation")
    current, replay_audit = exact_reapplication(
        task,
        inspection,
        trajectory["action_observations"][0],
        observations,
        transcripts["transcripts"][0],
        review["record_reviews"][0],
    )
    current.verify()
    args.output_dir.mkdir(parents=True)
    write_json(
        args.output_dir / "reapplication-audit.json",
        {
            **replay_audit,
            "original_files": {
                str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in [
                    args.inspection_manifest,
                    args.accepted_audit,
                    review_path,
                    task_path,
                    trajectory_path,
                    transcripts_path,
                ]
            },
            "package_sha256": edit.package_hash,
            "reapplied_fact_keys": [f.key for f in current.facts],
            "reapplied_ports": [v.port.name for v in current.port_values],
        },
    )
    cases = []
    instruction = (
        "Exercise only the supplied native overload-edit Action on this development checkout. "
        "Use the independently reviewed current overload-review only if its authored input "
        "phase/state and actual preconditions are present. Bind every declared owner and auxiliary "
        "role to current code and bind its public oracle. Apply the smallest supported function-node "
        "classification extension and add an asynchronous regression alongside retained ordinary "
        "overload and non-overload controls. Change only declared bound resources; do not change "
        "the supplied public probe or diagnostic expectations to conceal failure. "
        "If input evidence is missing, incompatible or stale, refuse modification and explain the "
        "unmet obligation. Record actual post-edit overload-change observations; do not claim "
        "validated repair or whole-project success. This is a definition development exercise."
    )
    for ident, boundary in [
        ("q0", "confirmed-inspection-input"),
        ("q1", "missing-inspection-input"),
        ("q2", "wrong-input-phase-and-state"),
        ("q3", "stale-workspace-evidence"),
    ]:
        checkout = args.output_dir / (ident + "-checkout")
        shutil.copytree(current.root, checkout, symlinks=True)
        if public_workspace_sha256(checkout) != public_workspace_sha256(
            current.root
        ) or public_workspace_execution_sha256(checkout) != public_workspace_execution_sha256(
            current.root
        ):
            raise ValueError("edit fixture clone changed inspection content or modes")
        public_anchor = next(a for a in current.anchors if a.kind == "public_issue")
        prepared = current.update(anchors=(replace(public_anchor, observation=instruction),))
        prepared = replace(
            prepared,
            task_id="native-action-edit-exercise:overload:" + ident,
            root=str(checkout.resolve()),
            public_problem=instruction,
        )
        if ident == "q1":
            prepared = replace(prepared, port_values=())
        elif ident == "q2":
            prepared = replace(
                prepared,
                port_values=tuple(
                    replace(v, port=replace(v.port, phase="post-edit", state="unvalidated"))
                    for v in prepared.port_values
                ),
            )
        prepared.verify()
        before = public_workspace_execution_sha256(checkout)
        if ident == "q3":
            (checkout / "public-stale-boundary.txt").write_text(
                "Controlled change after the reviewed input seal.\n"
            )
            try:
                prepared.verify()
            except ValueError as error:
                rejection = str(error)
            else:
                raise ValueError("stale reviewed workspace was accepted")
        else:
            rejection = None
        destination = args.output_dir / (ident + "-task.json")
        write_json(destination, prepared.to_dict())
        cases.append(
            {
                "opaque_id": ident,
                "boundary": boundary,
                "task_context": str(destination.resolve()),
                "task_context_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
                "base_commit": prepared.base_commit,
                "output_dir": str((args.output_dir / (ident + "-output")).resolve()),
                "workspace_execution_sha256_before_stale_mutation": before,
                "execution_frontier_before_fresh_grounding": action_execution_checks(
                    edit, prepared
                ),
                "deterministic_stale_rejection": rejection,
                "actual_LLM_calls": 0,
                "controlled_input_corruption": ident in {"q1", "q2", "q3"},
            }
        )
    write_json(
        args.output_dir / "dispatch-manifest.json",
        {
            "schema": "native-overload-edit-functional-dispatch-v1",
            "references": manifest["references"],
            "action_id": edit.id,
            "package_sha256": edit.package_hash,
            "dependency_root": manifest["dependency_root"],
            "cases": cases,
            "actual_LLM_calls": 0,
            "authored_Action_executed": False,
            "historical_source_definition_exercise": True,
            "same_model_family_limit": True,
            "source_project_count": 1,
            "formal_SWE_runs": 0,
            "formal_KB_admitted": False,
        },
    )
    print(
        json.dumps(
            {
                "prepared_cases": len(cases),
                "reapplied_inspection_reviews": 1,
                "actual_LLM_calls": 0,
                "authored_Action_executed": False,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
