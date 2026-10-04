"""Formal input qualification rejects late answers and keeps older body versions."""

from copy import deepcopy

import pytest

from arex_skill_graph.benchmark_public_inputs import compose_public_problem, recover_issue_input

CREATED = "2024-02-01T00:00:00Z"
REPAIR = "2024-02-03T00:00:00Z"
LATE = "2024-02-04T00:00:00Z"
CUTOFF = "2024-01-01T00:00:00Z"


class API:
    def graphql(self, query, variables):
        if "repository(owner" in query:
            return {
                "repository": {
                    "issue": {
                        "id": "issue-node",
                        "number": 1,
                        "url": "https://github.com/owner/repo/issues/1",
                        "title": "Later renamed title",
                        "body": "Later repaired answer",
                        "createdAt": CREATED,
                        "updatedAt": LATE,
                        "lastEditedAt": LATE,
                        "state": "CLOSED",
                        "closedAt": LATE,
                        "comments": {"totalCount": 0},
                        "timelineItems": {
                            "nodes": [
                                {
                                    "__typename": "RenamedTitleEvent",
                                    "createdAt": LATE,
                                    "previousTitle": "Original defect",
                                    "currentTitle": "Later renamed title",
                                }
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        },
                    }
                }
            }
        return {
            "node": {
                "id": "issue-node",
                "body": "Later repaired answer",
                "createdAt": CREATED,
                "lastEditedAt": LATE,
                "userContentEdits": {
                    "nodes": [
                        {"id": "late-edit", "editedAt": LATE, "diff": "Later repaired answer"},
                        {"id": "early-edit", "editedAt": CREATED, "diff": "Original reproduction"},
                    ],
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                },
            }
        }


def test_original_input_recovers_past_title_and_body_without_later_answer():
    issue = recover_issue_input(API(), "owner/repo", 1, REPAIR)
    public = compose_public_problem(
        [issue], base_committed_at=CREATED, repair_before=REPAIR, main_cutoff=CUTOFF
    )
    assert public["public_problem"] == "Original defect\n\nOriginal reproduction"
    assert "Later" not in str(issue)
    assert public["input_available_at"] == CREATED


@pytest.mark.parametrize("field", ["created_at", "title_available_at", "body_available_at"])
def test_late_input_cannot_pass_composition(field):
    issue = deepcopy(recover_issue_input(API(), "owner/repo", 1, REPAIR))
    issue[field] = REPAIR
    with pytest.raises(ValueError):
        compose_public_problem(
            [issue], base_committed_at=CREATED, repair_before=REPAIR, main_cutoff=CUTOFF
        )


def test_future_base_and_pre_cutoff_backlog_are_rejected():
    issue = recover_issue_input(API(), "owner/repo", 1, REPAIR)
    with pytest.raises(ValueError, match="base/input chronology"):
        compose_public_problem(
            [issue], base_committed_at=LATE, repair_before=REPAIR, main_cutoff=CUTOFF
        )
    issue["created_at"] = "2023-12-31T00:00:00Z"
    with pytest.raises(ValueError, match="backlog"):
        compose_public_problem(
            [issue], base_committed_at=CREATED, repair_before=REPAIR, main_cutoff=CUTOFF
        )
