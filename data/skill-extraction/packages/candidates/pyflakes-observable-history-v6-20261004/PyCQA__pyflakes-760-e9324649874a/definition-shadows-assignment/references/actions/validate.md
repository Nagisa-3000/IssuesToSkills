# Validate the candidate and adjacent behavior

Execute public current checks after the edit. The historical assertion supplies the target behavior, while the retained superclass branch and the report's ordinary-rebinding distinction supply adjacent preservation requirements.

```arex-contract-v4
{
  "id": "workflow:verified-history:ee79eebf2283561900232caf:validate",
  "intent": "Observe target correction and required adjacent behavior after the edit.",
  "mechanism": "Run public regression tests and diagnostic reproductions against the current candidate.",
  "semantic_role": "definition-assignment-public-validation",
  "owner_role": "unused-redefinition-tests-owner",
  "operation": "Bind and execute public current test commands, record diagnostic results and exit status, and refresh validation evidence without modifying source or tests.",
  "kind": "validate",
  "inputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "definition-assignment-redefinition-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "post-edit",
      "state": "awaiting-public-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "definition-assignment-public-validation-result",
      "artifact_kind": "test-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "post-validation",
      "state": "observed-public-results",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "definition-assignment-rule-present", "value": true, "evaluator": "evidence"},
    {"key": "target-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "regression-owner-located", "value": true, "evaluator": "file_exists", "description": "Resolve role:unused-redefinition-tests-owner."}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence", "description": "Fresh public results are recorded; acceptance additionally requires all required oracle checks to PASS."}
  ],
  "preserves": [
    {"key": "superclass-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-assignment-rebinding-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "target-and-adjacent-tests",
      "instruction": "Run the current public assignment-to-function regression and relevant binding/unused-redefinition tests. Verify the class assignment-to-method reproduction and existing definition-to-definition diagnostic. Verify ordinary assignment rebinding remains permitted and review or probe current exemptions and different-name classification. Record command argv, outputs, exit status, and PASS/FAIL/UNKNOWN checks. A failure rejects acceptance.",
      "evidence_refs": ["PyCQA/pyflakes:760:body", "PyCQA/pyflakes:760:fix", "PyCQA/pyflakes:760:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:ee79eebf2283561900232caf:extend-and-cover"],
  "source_ids": ["PyCQA/pyflakes:760:repair:e9324649874a"],
  "evidence_refs": ["PyCQA/pyflakes:760:body", "PyCQA/pyflakes:760:fix", "PyCQA/pyflakes:760:regression"],
  "read_set": ["role:binding-redefinition-owner", "role:assignment-binding-owner", "role:unused-redefinition-tests-owner"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:ee79eebf2283561900232caf"
}
```

Recording a failed run makes an observation fresh, not successful. Acceptance requires passing target and preservation checks. No current or historical execution is asserted by this card.
