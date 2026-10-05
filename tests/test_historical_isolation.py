import copy
import json
from dataclasses import replace
from pathlib import Path

import pytest
from adaptive_fixture import CUTOFF, make_fixture

from arex_skill_graph.action_contracts import SourceRecord
from arex_skill_graph.historical_isolation import HistoricalIsolation, reconcile_cluster_reviews
from arex_skill_graph.history_census import fingerprint
from arex_skill_graph.temporal_ranker_data import HistoricalQuery, build_examples, eligible_catalog


def source(number, issue=None):
    issue = issue or "historical:issue:" + str(number)
    return SourceRecord(
        "historical:source:" + str(number),
        "fixture/repo",
        issue,
        "historical:fix:" + str(number),
        str(number) * 40,
        "2020-01-01T00:00:00Z",
        (issue + ":body",),
        aliases=("https://example.invalid/" + issue,),
        verified_resolution=True,
    )


def review_directory(tmp_path, sources, *, duplicates=(), uncertain=(), version=1):
    directory = tmp_path / "review"
    directory.mkdir()
    records = [
        {
            "issue_id": s.bug_cluster_id,
            "source_id": s.id,
            "fix_id": s.fix_id,
            "revision": s.revision,
            "entries": [
                {
                    "id": s.id + ":body",
                    "available_at": s.available_at,
                    "text": "Fixture source evidence",
                    "kind": "public_issue",
                }
            ],
        }
        for s in sources
    ]
    by_issue = {}
    for record in records:
        by_issue.setdefault(record["issue_id"], []).extend(record["entries"])
    payload = {"cutoff_exclusive": CUTOFF, "historical_records": records, "queries": []}
    response = {
        "reviews": [
            {
                "issue_id": issue,
                "mechanism": "Offline TARGET REPAIR mechanism",
                "reason": "OFFLINE_REPAIR_REASON must stay outside actor features",
                "evidence_refs": [e["id"] for e in entries],
            }
            for issue, entries in by_issue.items()
        ],
        "duplicate_groups": [],
        "uncertain_groups": [],
    }
    for kind, groups in (("duplicate_groups", duplicates), ("uncertain_groups", uncertain)):
        response[kind] = [
            {
                "members": list(group),
                "reason": "Evidence-based fixture relation",
                "evidence_refs": [by_issue[member][0]["id"] for member in group],
            }
            for group in groups
        ]
    receipt = {
        "schema": "historical-causal-cluster-review-v" + str(version),
        "input_sha256": fingerprint(payload),
        "response_sha256": fingerprint(response),
        "review": response,
        "issue_count": len(by_issue),
        "query_count": 0,
    }
    if version == 2:
        receipt["source_count"] = len(records)
    for name, contents in (
        ("review-input.json", payload),
        ("review-response.json", response),
        ("cluster-review.json", receipt),
    ):
        (directory / name).write_text(json.dumps(contents))
    return directory


def test_reviewed_causal_relation_excludes_previously_eligible_immutable_package(tmp_path):
    package, task, _ = make_fixture(tmp_path / "package")
    donor = package.sources[0]
    query = HistoricalQuery(
        replace(task, task_id="historical:new-issue", input_available_at="2022-01-01T00:00:00Z"),
        "declared-independent",
        "new-query-fix",
    )
    current = source(3, query.task.task_id)
    directory = review_directory(
        tmp_path, (donor, current), duplicates=((donor.bug_cluster_id, current.bug_cluster_id),)
    )
    index = reconcile_cluster_reviews((directory,), tuple(package.sources))
    before = {p: p.read_bytes() for p in Path(package.root).rglob("*") if p.is_file()}
    reference = copy.deepcopy(package.reference)
    legacy = eligible_catalog(
        query, (reference,), training_cutoff="2023-01-01T00:00:00Z", main_cutoff=CUTOFF
    )
    reconciled = eligible_catalog(
        query,
        (reference,),
        training_cutoff="2023-01-01T00:00:00Z",
        main_cutoff=CUTOFF,
        isolation=index,
    )
    assert len(legacy[1]) == 1 and reconciled[1] == ()
    assert "excluded identity/bug cluster/fix" in reconciled[3][0]["reason"]
    assert donor.id in reconciled[0].excluded_ids and donor.fix_id in reconciled[0].excluded_fixes
    assert reference == package.reference
    assert before == {p: p.read_bytes() for p in Path(package.root).rglob("*") if p.is_file()}
    serialized = json.dumps(index.to_dict())
    assert "OFFLINE_REPAIR_REASON" not in serialized and "TARGET REPAIR" not in serialized
    assert HistoricalIsolation.from_dict(index.to_dict()) == index


def test_uncertain_transitive_relations_are_conservative_exclusions(tmp_path):
    a, b, c = source(1), source(2), source(3)
    directory = review_directory(
        tmp_path,
        (a, b, c),
        duplicates=((a.bug_cluster_id, b.bug_cluster_id),),
        uncertain=((b.bug_cluster_id, c.bug_cluster_id),),
    )
    index = reconcile_cluster_reviews((directory,), (a, b, c))
    assert len(index.components) == 1 and index.components[0].conservative_uncertainty
    assert len(index.independent_source_groups((a, c))) == 1
    assert index.full_corpus_causal_review_complete


def test_reviewed_cluster_cannot_cross_train_development_split(tmp_path):
    _, task, _ = make_fixture(tmp_path / "package")
    a, b = source(1), source(2)
    directory = review_directory(
        tmp_path, (a, b), duplicates=((a.bug_cluster_id, b.bug_cluster_id),)
    )
    index = reconcile_cluster_reviews((directory,), (a, b))
    queries = [
        HistoricalQuery(
            replace(task, task_id=s.bug_cluster_id, input_available_at=date),
            "unreconciled:" + str(n),
            s.fix_id,
        )
        for n, (s, date) in enumerate(((a, "2020-06-01T00:00:00Z"), (b, "2022-06-01T00:00:00Z")))
    ]
    provider = lambda *args: []
    legacy, _ = build_examples(
        queries, (), (), provider, training_cutoff="2021-01-01T00:00:00Z", main_cutoff=CUTOFF
    )
    assert legacy == ()
    with pytest.raises(ValueError, match="bug cluster crosses"):
        build_examples(
            queries,
            (),
            (),
            provider,
            training_cutoff="2021-01-01T00:00:00Z",
            main_cutoff=CUTOFF,
            isolation=index,
        )


def test_native_alias_copy_and_same_commit_closure_does_not_inflate_support(tmp_path):
    a, b, c = source(1), source(2), source(3)
    b = replace(b, copied_from=(a.id,))
    c = replace(c, revision=a.revision)
    other = source(4)
    directory = review_directory(tmp_path, (a, other))
    index = reconcile_cluster_reviews((directory,), (a, b, c, other))
    assert len(index.independent_source_groups((a, b, c))) == 1
    assert len(index.independent_source_groups((a, other))) == 2
    assert not index.full_corpus_causal_review_complete


@pytest.mark.parametrize(
    "mutation", ("input", "response", "unaccepted", "foreign_citation", "cutoff")
)
def test_review_receipt_and_owned_evidence_are_required(tmp_path, mutation):
    a, b = source(1), source(2)
    directory = review_directory(tmp_path, (a, b))
    payload = json.loads((directory / "review-input.json").read_text())
    response = json.loads((directory / "review-response.json").read_text())
    receipt = json.loads((directory / "cluster-review.json").read_text())
    if mutation == "input":
        payload["historical_records"][0]["entries"][0]["text"] = "Changed observation"
    elif mutation == "response":
        response["reviews"][0]["reason"] = "Changed response"
    elif mutation == "unaccepted":
        receipt["schema"] = "raw-unaccepted-response"
    elif mutation == "foreign_citation":
        response["reviews"][0]["evidence_refs"] = response["reviews"][1]["evidence_refs"]
        receipt["response_sha256"] = fingerprint(response)
        receipt["review"] = response
    else:
        payload["historical_records"][0]["entries"][0]["available_at"] = CUTOFF
        receipt["input_sha256"] = fingerprint(payload)
    for name, contents in (
        ("review-input.json", payload),
        ("review-response.json", response),
        ("cluster-review.json", receipt),
    ):
        (directory / name).write_text(json.dumps(contents))
    with pytest.raises(ValueError):
        reconcile_cluster_reviews((directory,), (a, b))


def test_source_identity_and_index_tampering_are_rejected(tmp_path):
    a, b = source(1), source(2)
    directory = review_directory(tmp_path, (a, b))
    index = reconcile_cluster_reviews((directory,), (a, b))
    with pytest.raises(ValueError, match="native source differs"):
        index.verify_sources((replace(a, aliases=("changed-alias",)),))
    with pytest.raises(ValueError, match="absent"):
        index.verify_sources((source(3),))
    payload = index.to_dict()
    payload["components"][0]["id"] = "edited-component"
    with pytest.raises(ValueError, match="hash"):
        HistoricalIsolation.from_dict(payload)
    with pytest.raises(ValueError, match="native authority"):
        reconcile_cluster_reviews((directory,), (replace(a, revision="9" * 40), b))


def test_review_coverage_must_not_be_overclaimed(tmp_path):
    a, b = source(1), source(2)
    directory = review_directory(tmp_path, (a,))
    index = reconcile_cluster_reviews((directory,), (a, b))
    payload = index.to_dict()
    payload["full_corpus_causal_review_complete"] = True
    with pytest.raises(ValueError, match="overclaimed"):
        HistoricalIsolation.from_dict(payload)


def test_multiple_repairs_of_one_issue_retain_per_source_evidence_and_coverage(tmp_path):
    a, b = source(1), source(2, "historical:issue:1")
    directory = review_directory(tmp_path, (a, b), version=2)
    index = reconcile_cluster_reviews((directory,), (a, b))
    assert len(index.sources) == 2 and len(index.reviewed_source_ids) == 2
    assert len(index.components) == 1 and index.full_corpus_causal_review_complete
    receipt = json.loads((directory / "cluster-review.json").read_text())
    receipt["source_count"] = 1
    (directory / "cluster-review.json").write_text(json.dumps(receipt))
    with pytest.raises(ValueError, match="receipt"):
        reconcile_cluster_reviews((directory,), (a, b))
