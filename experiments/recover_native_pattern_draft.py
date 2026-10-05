#!/usr/bin/env python3
"""Recover one complete rejected native draft under its original reviewed authority."""

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from discover_native_history_patterns import load_reviewed_groups, prepare_groups

from arex_skill_graph.action_contracts import TemporalPolicy
from arex_skill_graph.adaptive_cli import read_references, transport_from_args
from arex_skill_graph.generation_context import generation_context_for_packages
from arex_skill_graph.historical_isolation import HistoricalIsolation
from arex_skill_graph.history_census import fingerprint, write_json
from arex_skill_graph.native_authoring_revision import NativeAuthoringDraft
from arex_skill_graph.native_pattern_revision import (
    prepare_native_pattern_revision,
    recover_native_pattern,
)
from arex_skill_graph.pattern_contracts import load_native_package
from arex_skill_graph.qualification_authority import load_source_qualifications


def prepare_session(args):
    policy = TemporalPolicy(args.cutoff)
    isolation = HistoricalIsolation.load(args.causal_isolation)
    packages = [load_native_package(ref, policy) for ref in read_references(args.references)]
    by_id = {package.reference["skill_id"]: package for package in packages}
    if len(by_id) != len(packages):
        raise ValueError("duplicate native source package")
    sources = {source.id: source for package in packages for source in package.sources}
    isolation.verify_sources(tuple(sources.values()))
    records = load_source_qualifications(args.verifications, tuple(sources.values()), policy)
    qualifications = {record.source_id: record for record in records}
    corpus = [
        {
            "package_id": package.reference["skill_id"],
            "package_sha256": package.reference["package_sha256"],
            "causal_source_group_ids": isolation.independent_source_groups(package.sources),
            "workflows": [workflow.to_dict() for workflow in package.workflows],
            "evidence_cards": {
                path.name: path.read_text()
                for path in (Path(package.root) / "references/evidence").glob("*.md")
            },
        }
        for package in packages
    ]
    previous = json.loads((args.discovery_audit / "discovery-input.json").read_text())
    if fingerprint(previous) != fingerprint(corpus):
        raise ValueError("recovery discovery differs from exact complete source corpus")
    context = generation_context_for_packages(packages, source_corpus_sha256=fingerprint(corpus))
    discovery = json.loads((args.discovery_audit / "discovery-response.json").read_text())
    prepared = prepare_groups(discovery["groups"], by_id, isolation)
    _reviews, accepted = load_reviewed_groups(
        args.reviewed_groups, args.mechanism_review, corpus, context, prepared
    )
    selected = [row for row in prepared if row[5] == args.package_id]
    if len(selected) != 1 or args.package_id not in accepted:
        raise ValueError("recovery must select exactly one independently accepted discovery group")
    _group, parents, support_sources, _key, kind, canonical = selected[0]
    review = accepted[canonical]
    original_request = json.loads(args.original_request.read_text())
    draft = NativeAuthoringDraft.from_bundle(args.draft.read_text())
    session = prepare_native_pattern_revision(
        draft,
        original_request,
        parents,
        policy,
        canonical_package_id=canonical,
        reviewed_mechanism=review["reviewed_mechanism"],
        mechanism_review=review,
        expected_kind=kind,
        generation_context=context,
        qualification_records=tuple(
            qualifications[sid] for sid in sorted({source.id for source in support_sources})
        ),
        seal_generation_context=args.seal_generation_context,
    )
    return session


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "references",
        "verifications",
        "causal-isolation",
        "discovery-audit",
        "reviewed-groups",
        "mechanism-review",
        "original-request",
        "draft",
        "output-dir",
        "audit-dir",
    ):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--package-id", required=True)
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    parser.add_argument("--seal-generation-context", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--base-url")
    parser.add_argument("--api-key-env", default="AREX_LLM_API_KEY")
    parser.add_argument("--replay", type=Path)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--max-output-tokens", type=int, default=60000)
    parser.add_argument("--authoring-timeout", type=float, default=1200)
    parser.add_argument("--stream-responses", action="store_true")
    parser.add_argument("--http-backend", choices=["native", "windows_pipe"], default="native")
    args = parser.parse_args(argv)
    if args.output_dir.exists() or args.audit_dir.exists():
        raise ValueError("recovery artifacts exist; preserve them and choose a new version")
    if (
        not 1 <= args.max_attempts <= 3
        or args.max_output_tokens <= 0
        or args.authoring_timeout <= 0
    ):
        raise ValueError("invalid native revision attempt or output/time budget")
    session = prepare_session(args)
    if args.preflight_only:
        args.audit_dir.mkdir(parents=True)
        proof = session.proof()
        write_json(args.audit_dir / "preflight.json", proof)
        print(
            json.dumps(
                {
                    "status": "source-bound-preflight-passed",
                    "canonical_package_id": args.package_id,
                    "actual_model_calls": 0,
                    "role_failures": len(proof["declared_role_diagnostics"].get("failures", [])),
                    "initial_full_publisher_rejection": proof["initial_full_publisher_rejection"],
                    "output_package_created": False,
                    "functional_evals_executed": False,
                }
            )
        )
        return proof
    transport = transport_from_args(args)
    if hasattr(transport, "config"):
        transport.config = replace(
            transport.config,
            max_output_tokens=args.max_output_tokens,
            timeout_seconds=args.authoring_timeout,
            stream_responses=args.stream_responses,
        )
    packages = recover_native_pattern(
        session, transport, args.output_dir, args.audit_dir, max_attempts=args.max_attempts
    )
    result = {
        "schema": "native-pattern-revision-result-v1",
        "canonical_package_id": args.package_id,
        "status": "candidate-package-published"
        if packages
        else "deferred-by-native-revision-author",
        "references": [package.reference for package in packages],
        "actual_model_calls": sum(
            not call.get("offline_replay", False) for call in getattr(transport, "calls", [])
        ),
        "offline_replay": bool(args.replay),
        "all_requests_serial": True,
        "functional_evals_executed": False,
        "formal_KB_admitted": False,
    }
    write_json(args.audit_dir / "result.json", result)
    print(json.dumps(result, ensure_ascii=False))
    return result


if __name__ == "__main__":
    main()
