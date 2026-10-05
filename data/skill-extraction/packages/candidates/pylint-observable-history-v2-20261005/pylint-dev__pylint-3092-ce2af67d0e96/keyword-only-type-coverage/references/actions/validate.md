# Validate publicly

Execute the bound focused regression and adjacent public suite. Record current revision/diff identity, commands, exit status, diagnostic output, and test outcomes.

Check ordinary annotated parameter behavior and genuinely missing type evidence. These are authored preservation checks, not claims that additional tests were committed historically. Where feasible, use a disposable public base checkout to confirm the focused regression fails before the collector repair for the affected names.

This Action changes no tracked code. A failure still produces a validation record, but does not establish the successful-validation effect. Refresh that effect only after target and preservation checks pass.

```arex-contract-v4
{
  "id": "workflow:verified-history:9458ec98dda8784befed789c:validate",
  "intent": "Observe repaired keyword-only behavior and preserved adjacent diagnostics.",
  "mechanism": "Run the focused no-message regression and adjacent public documentation checks.",
  "semantic_role": "public-validation",
  "owner_role": "parameter-documentation-test-suite",
  "operation": "Execute current bound public checks, record all outcomes, and refresh successful validation only when target and preservation checks pass.",
  "kind": "validate",
  "inputs": [
    {"name": "repair-candidate", "semantic_role": "repair-candidate", "artifact_kind": "checkout-change", "language": "Python", "scope": "parameter-documentation-checker", "phase": "repair", "state": "unvalidated"}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "validation-record", "artifact_kind": "test-result", "language": "Python", "scope": "parameter-documentation-checker", "phase": "validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "annotated-keyword-only-coverage", "value": true, "evaluator": "evidence"},
    {"key": "focused-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-annotation-credit-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-missing-type-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "target-and-adjacent-tests",
      "instruction": "Run the bound focused regression and adjacent suite. Require no warning for described annotated keyword-only parameters, unchanged ordinary annotation credit, and configured warnings for genuinely missing accepted type evidence. Record failures without marking successful validation.",
      "evidence_refs": ["pylint-dev/pylint:3092:body", "pylint-dev/pylint:3092:fix", "pylint-dev/pylint:3092:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:9458ec98dda8784befed789c:edit"],
  "source_ids": ["pylint-dev/pylint:3092:repair:ce2af67d0e96"],
  "evidence_refs": ["pylint-dev/pylint:3092:body", "pylint-dev/pylint:3092:fix", "pylint-dev/pylint:3092:regression"],
  "read_set": ["role:parameter-type-evidence-collector", "role:parameter-documentation-test-suite"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:9458ec98dda8784befed789c"
}
```
