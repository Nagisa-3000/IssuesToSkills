import pytest

from arex_skill_graph.history_ranker_queries import pre_repair_problem


def record(*entries):
    return {"evidence": list(entries)}


def entry(identity, kind, at, text):
    return {"id": identity, "kind": kind, "available_at": at, "text": text}


def test_query_excludes_later_versions_discussion_and_repair_locators():
    data = record(
        entry("issue:title", "issue_title_as_of_cutoff", "2020-01-01T00:00:00Z", "Public symptom"),
        entry(
            "issue:body", "issue_body_as_of_cutoff", "2020-01-02T00:00:00Z", "Public reproduction"
        ),
        entry(
            "issue:comment",
            "issue_comment_as_of_cutoff",
            "2020-01-02T00:00:00Z",
            "Suggested historical patch",
        ),
        entry(
            "issue:fix",
            "historical_merged_implementation",
            "2020-01-04T00:00:00Z",
            "Historical implementation",
        ),
    )
    problem, at, refs = pre_repair_problem(data, "2020-01-04T00:00:00Z", "2020-01-03T00:00:00Z")
    assert problem == "Public symptom\n\nPublic reproduction"
    assert at == "2020-01-03T00:00:00Z" and refs == ("issue:title", "issue:body")


def test_query_body_edited_after_public_pr_cannot_be_backdated_to_issue_creation():
    data = record(
        entry("issue:body", "issue_body_as_of_cutoff", "2020-01-04T00:00:00Z", "Later edit")
    )
    # The PR opened on day 3 and merged on day 5. Day 4 is already too late.
    with pytest.raises(ValueError, match="pre-repair public issue body"):
        pre_repair_problem(data, "2020-01-03T00:00:00Z", "2020-01-01T00:00:00Z")


def test_base_newer_than_first_public_repair_is_not_a_training_query():
    data = record(
        entry(
            "issue:body",
            "issue_body_recovered_as_of_cutoff",
            "2020-01-01T00:00:00Z",
            "Recovered input",
        )
    )
    with pytest.raises(ValueError, match="chronology"):
        pre_repair_problem(data, "2020-01-03T00:00:00Z", "2020-01-04T00:00:00Z")
