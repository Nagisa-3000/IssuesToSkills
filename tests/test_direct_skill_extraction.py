from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from arex_skill_graph.direct_skill_extraction import (
    END,
    FILE_END,
    START,
    direct_prompt,
    parse_bundle,
    project_episode_packages,
    publish_bundle,
    source_context,
    validate_graph_packages,
)
from arex_skill_graph.skill_packages import hydrate_package, validate_package
from arex_skill_graph.store import CatalogStore

ROOT = Path(__file__).resolve().parents[1]


def module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "experiments" / filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def wire(packages: dict[str, dict[str, str]]) -> str:
    return (
        START
        + "".join(
            f"<<<FILE {name}/{relative}>>>\n{content}{FILE_END}"
            for name, files in packages.items()
            for relative, content in files.items()
        )
        + END
    )


def authored_case():
    case = {
        "repository": "example/client",
        "issue": 17,
        "ref": "a" * 40,
        "role": "train_candidate",
        "split": "train_candidate",
        "category": "provider-interface-adaptation",
    }
    bundle = {"source": "local_git_pinned_ref", "resolved_commit": case["ref"]}
    context = source_context(case, bundle)
    name = "preserve-followup-selection-" + context["source_key"]
    files = {
        "SKILL.md": f"""---
name: {name}
description: "Preserve a selected endpoint when a successful initial request loses routing state in a follow-up request."
---

# Preserve endpoint selection across follow-up requests

## Purpose

Carry an explicit selection through the follow-up request boundary.

## When to use

- The initial request succeeds with a selected endpoint but the follow-up uses a default.

## Do not use / Anti-goals

- Do not replace global provider defaults or widen the patch to unrelated adapters.

## Not applicable when

- Initial selection itself fails or the caller intentionally requests a new endpoint.

## Applicability probes

- Trace the selected endpoint from the initial response to the follow-up constructor.

## Preconditions

A reproducible initial request succeeds and a focused routing oracle is available.

## Workflow

Read the [Workflow](references/workflow.md). First [locate the boundary](references/actions/locate-boundary.md),
then [propagate the selection](references/actions/propagate-selection.md).

## Validation ladder

- Run the focused follow-up routing regression, then the provider client regression suite.

## Failure modes

- Replacing a global default can accidentally change independent clients.

## Stop conditions

- Stop if the intended selected endpoint cannot be established from the caller.

## Evidence and provenance

See [historical source](references/episode.md), [diff](references/evidence/routing-diff.md)
and [provenance](references/provenance.json).

## Known limitations

- Eval definitions are not executed; the historical case alone does not prove transfer success.
""",
        "references/episode.md": """# Follow-up request drops the selected endpoint

## Before

The initial request selects an endpoint; its follow-up constructor falls back to a global default.

## After

The follow-up receives the caller's selected endpoint explicitly.

## Diff

Pass selected_endpoint across the request constructor and cover the follow-up case.

## Call sites

- The follow-up constructor consumes selected_endpoint from the previous request context.

## Tests

- The source diff adds a focused routing regression; this extraction has not run it.

## Known limitations

- The fixture is a synthetic protocol test, not a measured real-world repair result.
""",
        "references/evidence/routing-diff.md": f"""# Follow-up selection propagation

## Kind

diff

## Source

revision {case["ref"]}, src/client.py:10-30 and tests/test_client.py:20-45 (synthetic fixture).

## Observation

The caller passes its selected endpoint explicitly, and a focused regression checks the follow-up destination.
""",
        "references/workflow.md": """# Preserve endpoint selection across follow-up requests

## Goal

Every follow-up request preserves its caller's selected endpoint.

## Inputs

- A reproducible request, current checkout and focused routing test.

## Entry state

A valid initial request selects an endpoint and the follow-up loses it.

## Exit state

Follow-ups retain the selection and independent clients keep their defaults.

## Steps

| Action | Role | Required | Depends on | Condition | Validation |
| --- | --- | --- | --- | --- | --- |
| [locate-boundary](actions/locate-boundary.md) | diagnose | true | - | Always | Identify the producer and consumer of the selected endpoint |
| [propagate-selection](actions/propagate-selection.md) | implement | true | locate-boundary | Follow-up loses explicit selection | Focused routing and independent-client regressions pass |

## Evidence

- [routing diff](evidence/routing-diff.md)
""",
    }
    for slug, intent, change in [
        (
            "locate-boundary",
            "Locate the follow-up ownership boundary.",
            "Trace selection from the initial response to the follow-up constructor before editing.",
        ),
        (
            "propagate-selection",
            "Preserve explicit endpoint selection.",
            "Pass the selected endpoint through the boundary and add a focused regression without changing global defaults.",
        ),
    ]:
        files[f"references/actions/{slug}.md"] = f"""# {intent}

## Intent

{intent}

## Module role

Follow-up request adapter.

## Operation

propagate

## Preconditions

The initial request has a valid explicit endpoint selection.

## Invariants

Independent clients keep their configured defaults.

## Change

{change}

## Postconditions

The selected endpoint is established at the follow-up boundary.

## Validation

Run the focused follow-up routing regression and inspect the constructed destination.

## Regression checks

Run an independent-client request with its own default and compare its destination.

## Failure modes

Changing global defaults couples independent clients.

## Evidence

- [routing diff](../evidence/routing-diff.md)
"""
    workflow_id = f"workflow:{context['source_key']}:{name}"
    files["references/provenance.json"] = (
        json.dumps(
            {
                **context,
                "source_workflow_id": workflow_id,
                "package": {
                    "skill_id": workflow_id,
                    "name": name,
                    "version": 1,
                    "level": "workflow",
                    "status": "candidate",
                },
            },
            indent=2,
        )
        + "\n"
    )
    for filename, expected in [
        ("activation-cases.json", ["activate", "clarify", "do_not_activate"]),
        ("applicability-cases.json", ["applicable", "insufficient", "not_applicable"]),
    ]:
        files["evals/" + filename] = (
            json.dumps(
                {
                    "status": "not_executed",
                    "cases": [
                        {
                            "id": outcome,
                            "request": request,
                            "expected": outcome,
                            "rationale": "Verify the ownership boundary before activation.",
                        }
                        for outcome, request in zip(
                            expected,
                            [
                                "A valid initial selection is lost in follow-ups.",
                                "Routing fails but the boundary is unknown.",
                                "The initial selection fails.",
                            ],
                        )
                    ],
                },
                indent=2,
            )
            + "\n"
        )
    files["evals/functional-cases.json"] = (
        json.dumps(
            {
                "status": "not_executed",
                "cases": [
                    {
                        "id": slug,
                        "action_id": f"action:{context['source_key']}:{name}:{slug}",
                        "setup": "Initial request selects endpoint A; follow-up defaults to B.",
                        "checks": [
                            "Focused follow-up destination is A.",
                            "Independent client still uses B.",
                        ],
                    }
                    for slug in ("locate-boundary", "propagate-selection")
                ],
            },
            indent=2,
        )
        + "\n"
    )
    return case, bundle, {name: files}


def test_direct_authorship_survives_publication_catalog_and_context(tmp_path):
    case, bundle, authored = authored_case()
    report, episode = publish_bundle(wire(authored), case, bundle, tmp_path / "packages")
    assert report["extraction_success"] and report["workflows"] == 1 and report["actions"] == 2
    assert not any(key.startswith("candidate_") for key in episode["metadata"])
    reference = report["packages"][0]
    package = Path(reference["package_path"])
    for relative, content in authored[package.name].items():
        assert (package / relative).read_bytes() == content.encode()
    assert validate_package(package) == []
    manifest = json.loads((package / "manifest.json").read_text())
    assert manifest["authorship"] == "model_direct"
    subprocess.run([sys.executable, str(package / "scripts/verify_package.py")], check=True)
    graph_builder = module("direct_graph", "build_universal_resolution_graph.py")
    graph = graph_builder.build([episode], {"cases": [case]})
    assert validate_graph_packages(graph, [episode])["extraction_success"]
    hydrated = hydrate_package(graph["workflows"][0])
    assert authored[package.name]["SKILL.md"] in hydrated["rendered"]
    assert authored[package.name]["references/workflow.md"] in hydrated["rendered"]
    assert len(hydrated["hydrated_action_ids"]) == 2
    materializer = module("direct_materializer", "materialize_universal_resolution_graph.py")
    with CatalogStore(tmp_path / "catalog.sqlite") as store:
        store.initialize()
        counts = materializer.materialize(graph, store)
        assert counts["workflows"] == 1
        stored = store.get_node(reference["skill_id"])
        assert hydrate_package(stored.payload)["package_sha256"] == hydrated["package_sha256"]
    second, _ = publish_bundle(wire(authored), case, bundle, tmp_path / "packages")
    assert second["packages"] == report["packages"]
    (package / "SKILL.md").write_text("Manual changes must survive.\n")
    with pytest.raises(ValueError, match="refusing to overwrite"):
        publish_bundle(wire(authored), case, bundle, tmp_path / "packages")
    assert (package / "SKILL.md").read_text() == "Manual changes must survive.\n"


def test_multiple_packages_and_all_or_nothing_validation(tmp_path):
    case, bundle, authored = authored_case()
    first = next(iter(authored))
    second = "repair-request-boundary-" + source_context(case, bundle)["source_key"]
    authored[second] = {
        relative: text.replace(first, second) for relative, text in authored[first].items()
    }
    report, episode = publish_bundle(wire(authored), case, bundle, tmp_path / "packages")
    assert report["materialized_skill_packages"] == 2
    assert len(project_episode_packages(episode)["workflows"]) == 2
    del authored[second]["evals/functional-cases.json"]
    with pytest.raises(ValueError, match="incomplete"):
        publish_bundle(wire(authored), case, bundle, tmp_path / "rejected")
    assert not list((tmp_path / "rejected").glob("*/SKILL.md"))


@pytest.mark.parametrize(
    "mutation",
    ["cycle", "dangling", "missing-oracle", "false-eval-pass", "source", "missing-evidence"],
)
def test_malformed_contract_never_admits_packages(tmp_path, mutation):
    case, bundle, authored = authored_case()
    files = next(iter(authored.values()))
    if mutation == "cycle":
        files["references/workflow.md"] = files["references/workflow.md"].replace(
            "true | - |", "true | propagate-selection |"
        )
    elif mutation == "dangling":
        files["references/workflow.md"] = files["references/workflow.md"].replace(
            "true | locate-boundary |", "true | absent |"
        )
    elif mutation == "missing-oracle":
        files["references/actions/locate-boundary.md"] = files[
            "references/actions/locate-boundary.md"
        ].replace("## Validation", "## Missing oracle")
    elif mutation == "false-eval-pass":
        files["evals/activation-cases.json"] = files["evals/activation-cases.json"].replace(
            "not_executed", "passed"
        )
    elif mutation == "source":
        files["references/provenance.json"] = files["references/provenance.json"].replace(
            "example/client", "other/client"
        )
    else:
        del files["references/evidence/routing-diff.md"]
    with pytest.raises(ValueError):
        publish_bundle(wire(authored), case, bundle, tmp_path / "packages")
    assert not list((tmp_path / "packages").glob("*/SKILL.md"))


def test_safe_wire_paths_partial_responses_credentials_and_abstention(tmp_path):
    case, bundle, authored = authored_case()
    name = next(iter(authored))
    valid = wire(authored)
    for bad in [
        valid[: -len(END)],
        START + END,
        json.dumps({"candidate_workflows": []}),
        valid.replace(name + "/SKILL.md", "../SKILL.md", 1),
        valid.replace(name + "/SKILL.md", name + "/C:\\unsafe", 1),
        valid.replace("# Preserve endpoint", "# " + "ghp_" + "z" * 32, 1),
    ]:
        with pytest.raises(ValueError):
            parse_bundle(bad)
    duplicate = valid.replace(END, valid[len(START) :])
    with pytest.raises(ValueError, match="duplicate"):
        parse_bundle(duplicate)
    deferred = "AREX-SKILL-DEFERRED 1\nNo implementation-bearing diff is available; inspect a pinned resolution first.\nAREX-SKILL-DEFERRED-END\n"
    report, episode = publish_bundle(deferred, case, bundle, tmp_path / "deferred")
    assert report["valid"] and not report["extraction_success"] and episode is None
    assert not (tmp_path / "deferred").exists()
    with pytest.raises(ValueError, match="holdout"):
        publish_bundle(valid, {**case, "role": "holdout_candidate"}, bundle, tmp_path / "holdout")
    assert not (tmp_path / "holdout").exists()


def test_stale_graph_and_package_tampering_are_rejected(tmp_path):
    case, bundle, authored = authored_case()
    report, episode = publish_bundle(wire(authored), case, bundle, tmp_path / "packages")
    workflow = project_episode_packages(episode)["workflows"][0]
    stale = deepcopy(workflow)
    stale["anti_goals"] = ["Change every provider default."]
    with pytest.raises(ValueError, match="stale package"):
        hydrate_package(stale)
    bad_episode = deepcopy(episode)
    bad_episode["revision"] = "other-revision"
    with pytest.raises(ValueError, match="source boundary"):
        project_episode_packages(bad_episode)
    package = Path(report["packages"][0]["package_path"])
    (package / "references/evidence/routing-diff.md").write_text("Forged evidence.\n")
    with pytest.raises(ValueError, match="validation failed"):
        hydrate_package(workflow)


def test_default_codex_transport_has_no_semantic_json_schema_or_renderer(tmp_path, monkeypatch):
    runner = module("direct_runner", "run_codex_issue_episode_extraction.py")
    case, bundle, authored = authored_case()
    bundle_path = tmp_path / "bundle.json"
    bundle_path.write_text(json.dumps(bundle))
    prompt = runner.prompt_for(bundle_path, {**case, "checkout": str(tmp_path)})
    assert "AREX-SKILL-BUNDLE 1" in prompt and "Return ONLY JSON" not in prompt
    captured = []

    def run(command, **kwargs):
        captured.extend(command)
        return SimpleNamespace(
            returncode=0,
            stdout=json.dumps(
                {
                    "type": "item.completed",
                    "item": {"type": "agent_message", "text": wire(authored)},
                }
            )
            + "\n",
            stderr="",
        )

    monkeypatch.setattr(runner.subprocess, "run", run)
    response = tmp_path / "response.skill.md"
    assert (
        runner.run_codex(
            "codex", tmp_path, prompt, response, tmp_path / "stdout", tmp_path / "stderr"
        )
        == 0
    )
    assert "--output-schema" not in captured and "-o" not in captured
    assert response.read_bytes() == wire(authored).encode()
    monkeypatch.setattr(
        runner,
        "compile_workflow_graph",
        lambda *a, **k: pytest.fail("default path invoked JSON renderer"),
    )
    report, episode = runner.finalize_extraction(
        response.read_text(), bundle, case, tmp_path / "packages"
    )
    assert report["extraction_success"] and episode is not None


def test_http_direct_transport_does_not_force_json(tmp_path, monkeypatch):
    from arex_skill_graph.llm_http import OpenAICompatibleConfig, OpenAICompatibleTransport

    case, bundle, authored = authored_case()
    transport = OpenAICompatibleTransport(
        OpenAICompatibleConfig(
            api_key="stubkey",
            base_url="https://example.invalid/v1",
            model="test-model",
        )
    )
    sent = []

    def request(body):
        sent.append(body)
        return {"choices": [{"finish_reason": "stop", "message": {"content": wire(authored)}}]}

    monkeypatch.setattr(transport, "_request", request)
    prompt = direct_prompt(case, bundle, "synthetic implementation evidence")
    result = transport.complete_text(system="Author a Skill.", user=prompt)
    assert result == wire(authored)
    assert "response_format" not in sent[0] and "response_schema" not in transport.transcripts[0]
    monkeypatch.setattr(
        transport,
        "_request",
        lambda body: {"choices": [{"finish_reason": "length", "message": {"content": result}}]},
    )
    with pytest.raises(ValueError, match="complete"):
        transport.complete_text(system="Author a Skill.", user=prompt)


def test_catalog_rebuild_and_inventory_use_authored_packages(tmp_path, monkeypatch):
    case, bundle, authored = authored_case()
    case["case_id"] = "example-client-17"
    _report, episode = publish_bundle(wire(authored), case, bundle, tmp_path / "packages")
    before = {p: p.read_bytes() for p in (tmp_path / "packages").rglob("*") if p.is_file()}
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    manifest = manifests / "01-provider-interface-adaptation.json"
    manifest.write_text(json.dumps({"cases": [case]}))
    holdout = {
        "repository": "other/client",
        "issue": 18,
        "case_id": "other-client-18",
        "category": case["category"],
        "role": "holdout_candidate",
        "split": "holdout_candidate",
        "issue_url": "https://example.invalid/other/18",
        "evidence_status": "intentionally_not_extracted",
        "extraction_forbidden": True,
    }
    (manifests / "holdouts.json").write_text(json.dumps({"cases": [holdout]}))
    episodes_path = tmp_path / "episodes.json"
    episodes_path.write_text(json.dumps([episode]))
    catalog = module("direct_catalog_cli", "build_agent_core_catalog.py")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_agent_core_catalog",
            "--manifest",
            str(manifest),
            "--episodes",
            str(episodes_path),
            "--output-dir",
            str(tmp_path / "catalog"),
        ],
    )
    assert catalog.main() == 0
    assert before == {p: p.read_bytes() for p in before}
    run = tmp_path / "run"
    category = run / manifest.stem
    output = category / "example__client__17"
    output.mkdir(parents=True)
    for relative, value in {
        "codex-response.skill.md": wire(authored),
        "validation.json": json.dumps({"valid": True, "errors": []}),
        "codex-command.json": json.dumps(
            {"model": "test-model", "profile": None, "sandbox": "read-only"}
        ),
        "issue-bundle.json": json.dumps(bundle),
        "prompt.txt": "Synthetic protocol fixture.\n",
    }.items():
        (output / relative).write_text(value)
    (category / "episodes.json").write_text(json.dumps([episode]))
    (category / "extraction-summary.json").write_text(
        json.dumps({"total_cases": 1, "admitted_episodes": 1})
    )
    summarizer = module("direct_summary", "summarize_issue_episode_extraction.py")
    inventory, _, errors = summarizer.summarize(
        run, manifests, ROOT / "schemas/codex-change-episode-v3.schema.json"
    )
    assert errors == [] and inventory["counts"]["direct_package_extractions"] == 1
    inventory_path = run / "extraction-inventory.json"
    inventory_path.write_text(json.dumps(inventory))
    spec = importlib.util.spec_from_file_location(
        "direct_inventory",
        ROOT
        / "data/skill-extraction/packages/universal-resolution-distiller/scripts/validate_extraction_inventory.py",
    )
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    result = validator.validate_inventory(
        inventory_path, repository_root=tmp_path, require_packages=True
    )
    assert result["valid"], result["errors"]
    assert result["materialized_skill_packages"] == 1
    (output / "codex-response.skill.md").write_text(
        wire(authored).replace("Carry an explicit", "Contradict the explicit")
    )
    result = validator.validate_inventory(
        inventory_path, repository_root=tmp_path, require_packages=True
    )
    assert not result["valid"]


def test_direct_governance_records_keep_real_package_identity(tmp_path):
    from arex_skill_graph.episodes import ChangeEpisode

    case, bundle, authored = authored_case()
    report, episode = publish_bundle(wire(authored), case, bundle, tmp_path / "packages")
    admission = module("direct_record_admission", "admit_preextracted_candidates.py")
    change = ChangeEpisode.from_mapping(episode)
    atomics = admission.atomic_records(change)
    workflows = admission.workflow_records(change, atomics)
    assert len(atomics) == 2 and len(workflows) == 1
    assert workflows[0].skill_id == report["packages"][0]["skill_id"]
    assert hydrate_package(workflows[0].payload)["skill_id"] == workflows[0].skill_id


def test_prepared_evidence_identity_is_not_fabricated_github_issue(tmp_path):
    case, bundle, authored = authored_case()
    original = source_context(case, bundle)
    prepared_case = {**case, "issue": None, "artifact_id": "bounded-routing-case"}
    prepared = source_context(prepared_case, bundle)
    old_name = next(iter(authored))
    new_name = old_name.replace(original["source_key"], prepared["source_key"])
    files = {
        relative: content.replace(original["source_key"], prepared["source_key"])
        for relative, content in authored[old_name].items()
    }
    identity = f"workflow:{prepared['source_key']}:{new_name}"
    files["references/provenance.json"] = (
        json.dumps(
            {
                **prepared,
                "source_workflow_id": identity,
                "package": {
                    "skill_id": identity,
                    "name": new_name,
                    "version": 1,
                    "level": "workflow",
                    "status": "candidate",
                },
            }
        )
        + "\n"
    )
    report, episode = publish_bundle(
        wire({new_name: files}).rstrip("\n"), prepared_case, bundle, tmp_path / "packages"
    )
    assert report["extraction_success"]
    assert episode["episode_id"].startswith("prepared:") and episode["metadata"]["issue"] is None
    assert project_episode_packages(episode)["workflows"][0]["issue"] is None
