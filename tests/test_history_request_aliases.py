import importlib.util
from pathlib import Path


def test_same_repair_aliases_prefer_closure_and_keep_audit():
    source = Path(__file__).resolve().parents[1] / "experiments/verify_historical_repairs.py"
    spec = importlib.util.spec_from_file_location("repair_requests", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def request(issue, fix, relation, number):
        return {
            "issue_id": issue,
            "repository_path": "/source/repo.git",
            "metadata": {
                "mergeCommit": {"oid": "a" * 40},
                "fix_id": fix,
                "resolution_relationship": relation,
                "number": number,
            },
        }

    requests = [
        request("issue:1", "commit:a", "mention_only_not_verified_resolution", None),
        request("issue:1", "pr:1", "direct_closure", 1),
        request("issue:2", "pr:1", "closing_reference", 1),
    ]
    collapsed = module.canonical_repair_requests(requests)
    assert len(collapsed) == 2
    chosen, aliases = collapsed[0]
    assert chosen["metadata"]["fix_id"] == "pr:1"
    assert {a["fix_id"] for a in aliases} == {"commit:a", "pr:1"}
    assert collapsed[1][0]["issue_id"] == "issue:2"
