import json

import pytest

from arex_skill_graph.benchmark_identity import (
    alias_union,
    classify_original_issue_group,
    dataset_issue_identities,
    project_issue_numbers,
    project_metadata,
    reconcile_dataset_issue_references,
    repository_identity,
)


def test_pinned_projection_excludes_solution_columns_and_preserves_variants(tmp_path):
    duckdb = pytest.importorskip("duckdb")
    connection = duckdb.connect(":memory:")
    connection.execute(
        "CREATE TABLE tasks(repo VARCHAR, instance_id VARCHAR, base_commit VARCHAR, version VARCHAR,"
        "patch VARCHAR, test_patch VARCHAR, problem_statement VARCHAR)"
    )
    private = "synthetic evaluator content"
    connection.executemany(
        "INSERT INTO tasks VALUES (?,?,?,?,?,?,?)",
        [
            (
                "pylint-dev/pylint",
                "pylint-dev__pylint-123",
                "a" * 40,
                "1",
                private,
                private,
                private,
            ),
            ("other/repo", "other__repo-2", "b" * 40, "1", private, private, private),
        ],
    )
    path = tmp_path / "tasks.parquet"
    connection.execute("COPY tasks TO ? (FORMAT PARQUET)", [str(path)])
    rows, audit = project_metadata(connection, str(path))
    assert len(rows) == 1 and rows[0]["pull_number"] == 123
    assert audit["raw_rows"] == 2
    assert not set(audit["projected_columns"]) & {"patch", "test_patch", "problem_statement"}
    assert private not in json.dumps(rows)
    memberships = [
        {**rows[0], "variant": "Full/test"},
        {**rows[0], "variant": "Verified/test", "base_commit": "c" * 40},
    ]
    union = alias_union(memberships)
    assert len(union) == 1 and len(union[0]["aliases"]) == 2
    assert union[0]["original_issue_mapping_verified"] is False
    assert union[0]["benchmark_qualification"] == "not-executed"
    connection.close()


def test_structured_repository_identity_and_missing_ownership():
    assert (
        repository_identity({"owner": {"login": "pylint-dev"}, "name": "pylint"})
        == "pylint-dev/pylint"
    )
    assert repository_identity("pylint", "pylint-dev") == "pylint-dev/pylint"
    with pytest.raises(ValueError):
        repository_identity("pylint")


def test_declared_issue_numbers_are_projected_from_live_arrays_without_solution_fields(tmp_path):
    duckdb = pytest.importorskip("duckdb")
    connection = duckdb.connect(":memory:")
    connection.execute(
        "CREATE TABLE tasks(repo VARCHAR, instance_id VARCHAR, issue_numbers VARCHAR[], patch VARCHAR)"
    )
    connection.execute(
        "INSERT INTO tasks VALUES ('pylint-dev/pylint','pylint-dev__pylint-7993',['7991'],'private solution fixture')"
    )
    path = tmp_path / "live.parquet"
    connection.execute("COPY tasks TO ? (FORMAT PARQUET)", [str(path)])
    rows, audit = project_metadata(connection, str(path))
    assert rows[0]["dataset_original_issue_numbers"] == [7991]
    assert rows[0]["original_issue_field_available"] is True
    assert "patch" not in audit["projected_columns"]
    assert "private solution fixture" not in json.dumps(rows)
    connection.close()


@pytest.mark.parametrize("value", ["1", "[true]", "[-1]", "[1.5]", '["../1"]', '["0001"]'])
def test_malformed_dataset_issue_identity_is_rejected(value):
    with pytest.raises(ValueError):
        project_issue_numbers(value)


def test_dataset_only_reference_restores_missing_mapping_and_conflict_blocks_qualification():
    issue = {
        "id": "issue-node",
        "number": 7991,
        "url": "https://github.com/example/repo/issues/7991",
        "createdAt": "2023-01-01T00:00:00Z",
        "repository": {"nameWithOwner": "example/repo"},
    }
    group = {
        "repository": "example/repo",
        "pull_number": 7993,
        "aliases": [
            {"original_issue_field_available": True, "dataset_original_issue_numbers": [7991]}
        ],
    }
    mapping = {"merged_at": "2023-02-01T00:00:00Z", "original_issues": []}
    reconciled = reconcile_dataset_issue_references(group, mapping, {7991: issue})
    result = classify_original_issue_group(group, reconciled, "2024-01-01T00:00:00Z")
    assert result["original_issue_mapping_verified"] is True
    assert result["temporal_classification"] == "pre-cutoff-historical-repair"
    assert reconciled["original_issue_reference_comparison"] == "dataset-reference-only"
    mapping["original_issues"] = [
        {"repository": "example/repo", "number": 7990, "created_at": "2023-01-01T00:00:00Z"}
    ]
    conflicting = reconcile_dataset_issue_references(group, mapping, {7991: issue})
    assert conflicting["original_issue_reference_comparison"] == "disagreement-review-required"
    assert not classify_original_issue_group(group, conflicting, "2024-01-01T00:00:00Z")[
        "original_issue_mapping_verified"
    ]
    missing = reconcile_dataset_issue_references(group, {**mapping, "original_issues": []}, {})
    assert missing["unavailable_dataset_issue_numbers"] == [7991]
    assert not classify_original_issue_group(group, missing, "2024-01-01T00:00:00Z")[
        "original_issue_mapping_verified"
    ]


def test_dataset_issue_lookup_requests_only_identity_fields():
    class API:
        def graphql(self, query, variables):
            assert "body" not in query and "patch" not in query and "title" not in query
            assert "issue(number:1)" in query
            return {"repository": {"i1": {"id": "node-1"}}}

    assert dataset_issue_identities(API(), "example/repo", [1]) == {1: {"id": "node-1"}}
    assert dataset_issue_identities(API(), "example/repo", []) == {}
