"""Synthetic native authored bundle; no real SWE labels or transfer claim."""

from dataclasses import asdict
import hashlib
import json
import subprocess

from arex_skill_graph.action_contracts import SourceRecord, TemporalPolicy, Port, Predicate
from arex_skill_graph.pattern_contracts import publish_v4_bundle
from arex_skill_graph.plan_validation import ResourcePolicy
from arex_skill_graph.task_context import (
    TaskContext,
    EvidenceAnchor,
    Binding,
    ObservedFact,
    SemanticCheck,
    CurrentOracle,
)

CUTOFF = "2024-01-01T00:00:00Z"
DATE = "2020-01-01T00:00:00Z"
MECHANISM = "Preserve runtime diagnostics while narrowing type-only context"


def fenced(marker, value):
    return "```" + marker + "\n" + json.dumps(value, ensure_ascii=False, indent=2) + "\n```\n"


def authored_bundle(
    *,
    pattern=True,
    duplicate=False,
    language="Python",
    bridge=False,
    alias=False,
    cleanup=False,
    optional=False,
):
    name = "type-context-pattern" if pattern else "type-context-workflow"
    pid = "pattern:type-context" if pattern else "workflow:a"
    records = [
        SourceRecord(
            "source:" + letter,
            "synthetic/" + letter,
            "bug:" + ("a" if duplicate else letter),
            "fix:" + letter,
            letter * 40,
            DATE,
            ("evidence:" + letter,),
            verified_resolution=True,
        )
        for letter in ("a", "b")
        if pattern or letter == "a"
    ]
    port = asdict(
        Port("context", "type_context", "ContextFacts", language, "module", "static", "resolved")
    )
    files = {}
    all_actions = []
    workflows = []
    for source in records:
        letter = source.id[-1]
        evidence = source.evidence_refs
        common = {
            "mechanism": MECHANISM,
            "source_ids": [source.id],
            "evidence_refs": list(evidence),
            "package_id": pid,
            "preserves": [asdict(Predicate("runtime_preserved", True))],
            "oracle": [
                {
                    "id": "oracle:" + letter,
                    "instruction": "Run public type-only and runtime boundary cases.",
                    "evidence_refs": list(evidence),
                    "kind": "repository_test",
                    "command": ["python", "checker.py"],
                }
            ],
        }
        probe = {
            **common,
            "id": "detect:" + letter,
            "intent": "Identify current type-only context",
            "semantic_role": "detect_context",
            "owner_role": "context_owner",
            "kind": "read",
            "operation": "Inspect the current context producer and distinguish static usage from runtime availability.",
            "inputs": [],
            "outputs": [port],
            "preconditions": [],
            "effects": [asdict(Predicate("context_known", True))],
            "read_set": ["context_owner"],
        }
        guard = {
            **common,
            "id": "guard:" + letter,
            "intent": "Narrow the actual diagnostic guard",
            "semantic_role": "narrow_guard",
            "owner_role": "diagnostic_owner",
            "kind": "edit",
            "operation": "At the current diagnostic owner, exempt only type-only usage; preserve runtime checking.",
            "inputs": [port],
            "outputs": [],
            "preconditions": [asdict(Predicate("context_known", True))],
            "effects": [asdict(Predicate("diagnostic_fixed", True))],
            "write_set": ["diagnostic_owner"],
        }
        check = {
            **common,
            "id": "validate:" + letter,
            "intent": "Check repaired and neighboring behavior",
            "semantic_role": "verify_behavior",
            "owner_role": "diagnostic_owner",
            "kind": "validate",
            "operation": "Run the public MRE and a runtime diagnostic that must remain active.",
            "inputs": [],
            "outputs": [],
            "preconditions": [asdict(Predicate("diagnostic_fixed", True))],
            "effects": [asdict(Predicate("validated", True))],
            "validation_for": [guard["id"]],
            "read_set": ["diagnostic_owner"],
        }
        if alias and letter == "b":
            guard["owner_role"] = "diagnostic_alias"
            guard["write_set"] = ["diagnostic_alias"]
            check["owner_role"] = "diagnostic_alias"
            check["read_set"] = ["diagnostic_alias"]
        actions = [probe, guard, check]
        if cleanup:
            restore = {
                **common,
                "id": "cleanup:" + letter,
                "intent": "Remove transient public reproduction artifact",
                "semantic_role": "cleanup_artifact",
                "owner_role": "diagnostic_owner",
                "kind": "cleanup",
                "operation": "Restore the temporary reproduction environment after focused verification.",
                "inputs": [],
                "outputs": [],
                "preconditions": [asdict(Predicate("diagnostic_fixed", True))],
                "effects": [asdict(Predicate("scratch_clean", True))],
                "cleanup_for": [guard["id"]],
                "write_set": ["temporary_artifact:" + letter],
            }
            restore_check = {
                **common,
                "id": "cleanup-check:" + letter,
                "intent": "Verify restored environment",
                "semantic_role": "verify_cleanup",
                "owner_role": "diagnostic_owner",
                "kind": "validate",
                "operation": "Check the temporary artifact is gone and normal diagnostics are retained.",
                "inputs": [],
                "outputs": [],
                "preconditions": [asdict(Predicate("scratch_clean", True))],
                "effects": [asdict(Predicate("cleanup_verified", True))],
                "validation_for": [restore["id"]],
            }
            actions.extend([restore, restore_check])
        if optional:
            actions.append(
                {
                    **common,
                    "id": "optional:" + letter,
                    "intent": "Inspect an optional feature",
                    "semantic_role": "optional_inspection",
                    "owner_role": "context_owner",
                    "kind": "read",
                    "operation": "Inspect plugin metadata only when that optional feature is enabled.",
                    "inputs": [],
                    "outputs": [],
                    "preconditions": [asdict(Predicate("plugin_available", True))],
                    "effects": [asdict(Predicate("optional_inspected", True))],
                }
            )
        if bridge and letter == "a":
            probe["outputs"] = [{**port, "phase": "parsed", "state": "unresolved"}]
            adapter = {
                **common,
                "id": "bridge:a",
                "intent": "Resolve parsed context facts",
                "semantic_role": "resolve_context",
                "owner_role": "context_owner",
                "kind": "bridge",
                "operation": "Use the current resolver to establish static context facts.",
                "inputs": [{**port, "phase": "parsed", "state": "unresolved"}],
                "outputs": [port],
                "preconditions": [],
                "effects": [asdict(Predicate("context_resolved", True))],
            }
            bridge_check = {
                **common,
                "id": "bridge-check:a",
                "intent": "Verify resolved context facts",
                "semantic_role": "verify_context",
                "owner_role": "context_owner",
                "kind": "validate",
                "operation": "Check resolved context boundaries before modifying the diagnostic.",
                "inputs": [],
                "outputs": [],
                "preconditions": [asdict(Predicate("context_resolved", True))],
                "effects": [asdict(Predicate("context_checked", True))],
                "validation_for": ["bridge:a"],
            }
            actions += [adapter, bridge_check]
        for action in actions:
            slug = action["id"].replace(":", "-")
            resource = "references/actions/" + slug + ".md"
            action["resource"] = resource
            files[resource] = "# " + action["intent"] + "\n\n" + fenced("arex-contract-v4", action)
        all_actions.extend(actions)
        wf = {
            "id": "workflow:" + letter,
            "goal": "Repair type-only diagnostic while preserving runtime behavior",
            "mechanism": MECHANISM,
            "action_ids": [a["id"] for a in actions],
            "source_ids": [source.id],
            "required_effects": [
                asdict(Predicate("diagnostic_fixed", True)),
                asdict(Predicate("validated", True)),
            ],
            "invariants": [asdict(Predicate("runtime_preserved", True))],
            "dependencies": [],
        }
        if optional:
            wf["optional_action_ids"] = ["optional:" + letter]
        if cleanup:
            wf["dependencies"] = [
                {
                    "before": "validate:" + letter,
                    "after": "cleanup:" + letter,
                    "reason": "Verify before restoring the transient reproducer",
                    "evidence_refs": list(evidence),
                }
            ]
        workflows.append(wf)
        path = (
            "references/workflow.md" if letter == "a" else "references/realizations/workflow-b.md"
        )
        files[path] = "# Historical realization\n\n" + fenced("arex-workflow-v4", wf)
        files["references/evidence/source-" + letter + ".md"] = "# Synthetic evidence\n\n" + fenced(
            "arex-evidence-v4",
            {
                "id": evidence[0],
                "source_id": source.id,
                "available_at": DATE,
                "kind": "resolution",
                "observation": "Synthetic independent historical fix and focused regression tests, used for protocol testing.",
            },
        )
    skill = (
        "---\nname: "
        + name
        + "\ndescription: "
        + json.dumps(
            "Repair type-only diagnostic guards when current context and runtime boundaries are evidenced."
        )
        + "\n---\n\n# Context-sensitive diagnostic repair\n\nInspect current owners, narrow the guard and verify public boundaries. Stop on a missing fact or failed oracle.\n"
    )
    skill += "\n[Historical workflow](references/workflow.md)\n"
    if pattern:
        roles = []
        for role, prefix, effect in [
            ("detect_context", "detect", "context_known"),
            ("narrow_guard", "guard", "diagnostic_fixed"),
            ("verify_behavior", "validate", "validated"),
        ]:
            roles.append(
                {
                    "id": role,
                    "effects": [asdict(Predicate(effect, True))],
                    "alternatives": [prefix + ":" + s.id[-1] for s in records],
                    "evidence_refs": [e for s in records for e in s.evidence_refs],
                    "required": True,
                }
            )
        skill += fenced(
            "arex-pattern-v4",
            {
                "id": pid,
                "mechanism": MECHANISM,
                "roles": roles,
                "required_effects": [
                    asdict(Predicate("diagnostic_fixed", True)),
                    asdict(Predicate("validated", True)),
                ],
                "invariants": [asdict(Predicate("runtime_preserved", True))],
                "applicability": [],
                "exclusions": [],
                "partial_order": [
                    {
                        "before": "detect_context",
                        "after": "narrow_guard",
                        "reason": "Context facts precede a narrow guard.",
                        "evidence_refs": ["evidence:a"],
                    }
                ],
                "supporting_workflow_ids": [w["id"] for w in workflows],
                "evidence_refs": [e for s in records for e in s.evidence_refs],
                "cross_project": True,
            },
        )
    files["SKILL.md"] = skill
    files["references/episode.md"] = (
        "# Synthetic source record\n\nIndependent synthetic fixtures; no SWE effectiveness claim.\n"
    )
    kind = "pattern" if pattern else "workflow"
    files["references/provenance.json"] = (
        json.dumps(
            {
                "schema_version": "arex-native-provenance-v4",
                "split": "train_candidate",
                "holdout_used": False,
                "package_kind": kind,
                "cutoff": CUTOFF,
                "sources": [asdict(x) for x in records],
                "source_episode_ids": sorted(s.id for s in records),
                "source_workflow_ids": [w["id"] for w in workflows],
                "package": {
                    "skill_id": pid,
                    "name": name,
                    "version": 1,
                    "level": kind,
                    "status": "candidate",
                },
            },
            indent=2,
        )
        + "\n"
    )
    for filename, values in [
        ("activation", ["activate", "clarify", "do_not_activate"]),
        ("applicability", ["applicable", "insufficient", "not_applicable"]),
    ]:
        files["evals/" + filename + "-cases.json"] = (
            json.dumps(
                {
                    "status": "not_executed",
                    "cases": [
                        {
                            "id": v,
                            "expected": v,
                            "setup": "Public diagnostic context",
                            "checks": ["Current fact boundaries"],
                        }
                        for v in values
                    ],
                }
            )
            + "\n"
        )
    files["evals/functional-cases.json"] = (
        json.dumps(
            {
                "status": "not_executed",
                "cases": [
                    {
                        "id": a["id"],
                        "action_id": a["id"],
                        "setup": "Current public checkout",
                        "checks": ["Expected observable state and preserved runtime behavior"],
                    }
                    for a in all_actions
                ],
            }
        )
        + "\n"
    )
    response = "AREX-SKILL-BUNDLE 1\n"
    for resource, content in files.items():
        response += (
            "<<<FILE "
            + name
            + "/"
            + resource
            + ">>>\n"
            + content.rstrip("\n")
            + "\n<<<END FILE>>>\n"
        )
    return response + "AREX-SKILL-BUNDLE-END\n", records


def make_fixture(tmp_path, **kwargs):
    response, sources = authored_bundle(**kwargs)
    (package,) = publish_v4_bundle(response, sources, TemporalPolicy(CUTOFF), tmp_path / "packages")
    root = tmp_path / "checkout"
    root.mkdir()
    (root / "context.py").write_text("def type_only(context):\n    return context == 'type'\n")
    (root / "checker.py").write_text(
        "def diagnostic(context):\n    return True\n\nif __name__ == '__main__':\n    assert diagnostic('type') is False\n    assert diagnostic('runtime') is True\n"
    )
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "Synthetic base",
        ],
        check=True,
    )
    sha = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    anchors = [
        EvidenceAnchor(
            "current:issue",
            "public_issue",
            "Type-only usage incorrectly reports a runtime diagnostic.",
            sha,
        )
    ]
    for name in ["context", "checker"]:
        path = root / (name + ".py")
        anchors.append(
            EvidenceAnchor(
                "current:" + name,
                "current_code",
                "Current semantic owner implementation",
                sha,
                path.name,
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
        )
    refs = ("current:context", "current:checker")
    checks = [
        SemanticCheck(
            "action:" + a.id, "PASS", "Synthetic reviewed applicability", refs, "fixture-review"
        )
        for a in package.actions
    ]
    owner_roles = sorted({a.owner_role for a in package.actions})
    checks += [
        SemanticCheck(
            "owner:" + role, "PASS", "Actual current function owner", refs, "fixture-review"
        )
        for role in owner_roles
    ]
    checks += [
        SemanticCheck(
            f"dependency:{d.before}:{d.after}",
            "PASS",
            "Current fixture still requires this dependency",
            refs,
            "fixture-review",
        )
        for w in package.workflows
        for d in w.dependencies
    ]
    checks += [
        SemanticCheck(
            f"oracle:{a.id}:{o.id}",
            "PASS",
            "Public current oracle checks this operation",
            refs,
            "fixture-review",
        )
        for a in package.actions
        for o in a.oracle
    ]
    if package.pattern:
        checks.append(
            SemanticCheck(
                "pattern:" + package.pattern.id,
                "PASS",
                "Current context matches the synthetic mechanism",
                refs,
                "fixture-review",
            )
        )
    for a in package.actions:
        for b in package.actions:
            if a.id != b.id:
                for port in b.inputs:
                    if any(out.compatible(port) for out in a.outputs):
                        checks.append(
                            SemanticCheck(
                                f"connect:{a.id}:{b.id}:{port.name}",
                                "PASS",
                                "Current facts have compatible semantic meaning",
                                refs,
                                "fixture-review",
                            )
                        )
    task = TaskContext(
        "query:public",
        "synthetic/current",
        sha,
        str(root),
        anchors[0].observation,
        "2024-02-01T00:00:00Z",
        tuple(anchors),
        facts=(ObservedFact("runtime_preserved", True, ("current:checker",)),),
        checks=tuple(checks),
        bindings=tuple(
            Binding(
                role,
                "current:context" if role == "context_owner" else "current:checker",
                "type_only" if role == "context_owner" else "diagnostic",
                "Python",
                "type_only(context)" if role == "context_owner" else "diagnostic(context)",
                ("current:context",) if role == "context_owner" else ("current:checker",),
            )
            for role in owner_roles
        ),
        oracles=tuple(
            CurrentOracle(
                a.id,
                o.id,
                "Check actual current public behavior",
                (
                    "python3",
                    "-c",
                    "from context import type_only; assert type_only('type') and not type_only('runtime')",
                )
                if a.kind == "read"
                else ("python3", "checker.py"),
                ("current:context",) if a.kind == "read" else ("current:checker",),
            )
            for a in package.actions
            for o in a.oracle
        ),
        goals=(Predicate("diagnostic_fixed", True), Predicate("validated", True)),
    )
    policy = ResourcePolicy(TemporalPolicy(CUTOFF), (package.reference,))
    return package, task, policy
