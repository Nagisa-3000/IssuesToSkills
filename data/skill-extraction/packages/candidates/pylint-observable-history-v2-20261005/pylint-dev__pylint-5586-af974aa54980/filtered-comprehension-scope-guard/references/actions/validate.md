# Validate the candidate and adjacent behavior

Bind public commands in the current checkout. No historical command is automatically executable, and no hidden-test-derived command belongs in this operation.

```arex-contract-v4
{
  "id": "workflow:verified-history:4d5404af23a33d07f9c8cd24:validate",
  "intent": "Observe target correction and preservation after both edits.",
  "mechanism": "Run the public reproduction and collected regression, then inspect and exercise adjacent variable-checker behavior.",
  "semantic_role": "public-candidate-validation",
  "owner_role": "python-public-validation-harness",
  "operation": "Run currently bound public checks after all edits. Confirm the filter reference no longer emits used-before-assignment, the added case is collected and passes, existing relevant used-before-assignment assertions still pass, and surrounding late-binding/loop-variable behavior remains intact. Record failures or unknown coverage rather than inferring success. Do not modify implementation or test expectations during this validation.",
  "kind": "validate",
  "inputs": [
    {"name": "regression-candidate", "semantic_role": "guard-and-public-regression", "artifact_kind": "checkout-code-and-tests", "language": "python", "scope": "current-checkout", "phase": "validation", "state": "ready"}
  ],
  "outputs": [
    {"name": "public-validation", "semantic_role": "candidate-validation-observations", "artifact_kind": "validation-record", "language": "python", "scope": "current-checkout", "phase": "validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "filter-homonym-guard-corrected", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-installed", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "nonfilter-homonym-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "late-binding-and-loop-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-target",
      "instruction": "Run the public reproduction and collected regression against the final candidate. Check that used-before-assignment is absent at the filter reference without disabling the diagnostic.",
      "evidence_refs": ["pylint-dev/pylint:5586:body", "pylint-dev/pylint:5586:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-adjacent",
      "instruction": "Run current public variable-analysis tests relevant to ordinary homonyms, actual used-before-assignment, late binding and loop variables; compare expected diagnostics and inspect retained dispatch calls. Report missing coverage as UNKNOWN.",
      "evidence_refs": ["pylint-dev/pylint:5586:fix"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:4d5404af23a33d07f9c8cd24:repair",
    "workflow:verified-history:4d5404af23a33d07f9c8cd24:regression"
  ],
  "read_set": ["role:python-variable-use-dispatch", "role:python-public-functional-tests", "role:python-public-validation-harness"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5586:repair:af974aa54980"],
  "evidence_refs": ["pylint-dev/pylint:5586:body", "pylint-dev/pylint:5586:fix", "pylint-dev/pylint:5586:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:4d5404af23a33d07f9c8cd24"
}
```

The desired effects and assurances remain conditional until observed. A successful focused check is not whole-project acceptance.
