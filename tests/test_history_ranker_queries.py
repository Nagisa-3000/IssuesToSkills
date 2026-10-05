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


@pytest.mark.parametrize("repository", ["pylint-dev/pylint", "PyCQA/pyflakes"])
@pytest.mark.parametrize("environment", [(), ("Observed interpreter 3.8.3 in isolated replay",)])
def test_generic_query_does_not_invent_a_pyflakes_runtime(tmp_path, repository, environment):
    import subprocess

    from arex_skill_graph.history_ranker_queries import prepare_historical_query

    source = tmp_path / "source"
    source.mkdir()
    subprocess.run(["git", "init", "-q", str(source)], check=True)
    (source / "module.py").write_text("value = 1\n")
    subprocess.run(["git", "-C", str(source), "add", "."], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(source),
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.invalid",
            "commit",
            "-qm",
            "Public base",
        ],
        check=True,
        env={
            **__import__("os").environ,
            "GIT_AUTHOR_DATE": "2020-01-01T00:00:00Z",
            "GIT_COMMITTER_DATE": "2020-01-01T00:00:00Z",
        },
    )
    base = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    qid, fix_id = repository + ":7", repository + ":pr:8"
    data = {
        "issue_id": qid,
        "identity": {"repository": repository},
        "evidence": [
            entry("issue:body", "issue_body_as_of_cutoff", "2020-01-02T00:00:00Z", "Public symptom")
        ],
    }
    verification = {
        "verified_resolution": True,
        "issue_relationship_verified": True,
        "identity": {
            "issue_id": qid,
            "fix_id": fix_id,
            "base_commit": base,
            "repair_available_at": "2020-01-04T00:00:00Z",
        },
    }
    request = {
        "repository_path": str(source / ".git"),
        "metadata": {
            "fix_id": fix_id,
            "first_possible_public_repair_at": "2020-01-03T00:00:00Z",
            "first_possible_public_repair_time_basis": "Public PR opening",
        },
    }
    if environment:
        task, audit = prepare_historical_query(
            data, verification, request, tmp_path / "replay", environment=environment
        )
    else:
        task, audit = prepare_historical_query(data, verification, request, tmp_path / "replay")
    assert task.repository == repository
    assert task.environment == environment
    assert audit["runtime_environment"] == list(environment)
    assert audit["runtime_environment_inferred_from_repository"] is False
    assert "Pyflakes" not in " ".join(task.environment)
