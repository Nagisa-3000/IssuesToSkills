# Validate target and preserved behavior

Bind current public commands for the focused regression and relevant adjacent tests. Run them after the edit. Recheck the original match reproduction and its `if`/`else` comparison. Review unchanged `try` classification and run available neighboring branch/redefinition tests, including a legitimate same-branch redefinition control.

This last control is a preservation check for the narrow repair, not an additional historical regression claimed by the evidence. Record unavailable checks as UNKNOWN, never PASS. Broader test execution may be useful but is not historically verified by this package.

```arex-contract-v4
{
  "id": "workflow:verified-history:45a56eede77a20492da56a49:validate",
  "intent": "Observe that the repair removes the targeted false positive and preserves adjacent analysis.",
  "mechanism": "Execute the public regression and reproduction, then check existing branch behavior and legitimate diagnostics.",
  "semantic_role": "repair-validation",
  "owner_role": "binding-diagnostic-regression-tests",
  "operation": "Run current bound public checks and review preserved branch semantics.",
  "kind": "validate",
  "inputs": [
    {
      "name": "modified-checkout",
      "semantic_role": "branch-analysis-checkout",
      "artifact_kind": "source-tree",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "modified",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-report",
      "semantic_role": "branch-analysis-validation",
      "artifact_kind": "test-report",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "focused-match-binding-regression-added",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "current-public-oracles-bound",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "public-regression-validated",
      "value": true,
      "evaluator": "evidence",
      "description": "Expected only when executed checks pass; failures and unknowns must be recorded."
    }
  ],
  "preserves": [
    {
      "key": "existing-if-and-try-alternatives-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "legitimate-redefinition-diagnostics-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "supported-python-ast-availability-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "match-regression",
      "instruction": "Run the current test equivalent of two match cases defining y and returning y afterward. Require no diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:771:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "report-reproduction",
      "instruction": "Run the public match reproduction and if/else comparison in the current analyzer. Require no unused-name redefinition diagnostic between distinct alternatives.",
      "evidence_refs": ["PyCQA/pyflakes:771:body"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "adjacent-preservation",
      "instruction": "Review unchanged if/try alternative classification and AST availability handling; run available adjacent branch and legitimate same-branch redefinition checks. Record any unexecuted checks as UNKNOWN.",
      "evidence_refs": ["PyCQA/pyflakes:771:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:45a56eede77a20492da56a49:repair"],
  "source_ids": ["PyCQA/pyflakes:771:repair:f2671ffe1785"],
  "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix", "PyCQA/pyflakes:771:regression"],
  "read_set": ["role:alternative-branch-classifier", "role:binding-diagnostic-regression-tests"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:45a56eede77a20492da56a49"
}
```
