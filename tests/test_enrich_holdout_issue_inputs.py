from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "enrich_holdout_issue_inputs.py"
SPEC = importlib.util.spec_from_file_location("enrich_holdout_issue_inputs", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_enrichment_keeps_holdout_forbidden_and_redacts_public_secret() -> None:
    secret = "sk-" + "abcdefghijklmnopqrstuvwxyz123456"
    case = {
        "case_id": "org/repo#1",
        "repository": "org/repo",
        "issue": 1,
        "role": "holdout_candidate",
        "extraction_forbidden": True,
    }
    issue = {
        "title": "Credential failure",
        "body": f"accidentally pasted {secret}",
        "state": "closed",
        "labels": [{"name": "bug"}],
        "url": "https://api.github.com/repos/org/repo/issues/1",
        "html_url": "https://github.com/org/repo/issues/1",
    }

    result = MODULE.enrich_case(case, issue)

    assert result["extraction_forbidden"] is True
    assert result["public_issue_secret_redactions"] == 1
    assert secret not in result["issue_body"]
    assert result["evaluation_input_source"]["kind"] == "github_issue_title_and_body_only"
