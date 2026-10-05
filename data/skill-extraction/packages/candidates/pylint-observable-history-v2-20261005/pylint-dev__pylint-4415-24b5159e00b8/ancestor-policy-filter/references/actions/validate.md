# Validate the candidate

Bind current public commands for the minimal reproduction, ancestry tests, and adjacent design checks. Execute after all repair edits and record diagnostics, counts, and exit status.

```arex-contract-v4
{
  "id": "workflow:verified-history:58d864f47bb516a028d64059:validate",
  "intent": "Establish current public evidence for the repaired metric and preserved adjacent behavior.",
  "mechanism": "Run negative and positive ancestry controls and adjacent design checks against the candidate.",
  "semantic_role": "ancestry-policy-validation",
  "owner_role": "ancestry-regression-owner",
  "operation": "Execute bound current public commands and record fresh results without editing implementation or assertions.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate-repair",
      "semantic_role": "ancestry-policy-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "ancestry-policy-validation",
      "artifact_kind": "test-result",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "negative-and-positive-regression-controls-added", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-regression-validated", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observation-fresh", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "user-defined-ancestry-warning-preserved", "value": true, "evaluator": "evidence"},
    {"key": "configured-threshold-comparison-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-design-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-minimal-sequence",
      "instruction": "Execute the bound current supported standard-library-derived reproduction. Confirm its ancestry warning is absent and record other diagnostics separately.",
      "evidence_refs": ["pylint-dev/pylint:4415:body", "pylint-dev/pylint:4415:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-ancestry-and-adjacent-tests",
      "instruction": "Execute bound current public ancestry and adjacent design-check tests. Confirm excessive nonexempt user-defined ancestry still warns, counts match the filtered metric, and adjacent tests pass. Review that the strict configured comparison remains unchanged. Stop on failed or unknown results.",
      "evidence_refs": ["pylint-dev/pylint:4415:fix", "pylint-dev/pylint:4415:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:58d864f47bb516a028d64059:repair"],
  "read_set": ["role:ancestor-counting-owner", "role:ancestry-regression-owner"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4415:repair:24b5159e00b8"],
  "evidence_refs": ["pylint-dev/pylint:4415:body", "pylint-dev/pylint:4415:fix", "pylint-dev/pylint:4415:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:58d864f47bb516a028d64059"
}
```

Empty commands require current binding. Historical paths and contemporary replay commands do not authorize automatic execution. Failed or unexecuted checks do not establish effects. Any subsequent edit requires refreshed validation.
