# Validate suppression and retained diagnostics

Bind a current public regression command before execution. Inspect actual diagnostics, not just exit status. Confirm the member used in controls is genuinely absent.

Quoted and unquoted postponed annotations must be accepted while ordinary runtime access still reports missing-member. Retained generated-member expectations must pass. Validation does not edit source or expectations to hide failures.

An eager-annotation control may additionally probe the current boundary, but is not a historical committed assertion from this repair.

```arex-contract-v4
{
  "id": "workflow:verified-history:0c9590e0dcadfaf12ae0182b:validate",
  "intent": "Observe target suppression and preserved adjacent behavior.",
  "mechanism": "Compare actual diagnostics with annotation, runtime, and generated-member expectations.",
  "semantic_role": "annotation-runtime-control-validation",
  "owner_role": "member-diagnostic-regression-suite",
  "operation": "Run the bound current public regression command without modifying source or expectations; record actual diagnostics, exit status, and tested candidate anchors.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate",
      "semantic_role": "postponed-annotation-repair-candidate",
      "artifact_kind": "code-and-regression-diff",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "awaiting-validation"
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "postponed-annotation-validation-record",
      "artifact_kind": "public-test-observation-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-validation",
      "state": "checks-recorded"
    }
  ],
  "preconditions": [
    {"key": "annotation-runtime-regression-controls-present", "value": true, "evaluator": "evidence"},
    {"key": "public-oracle-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence", "description": "Establish only after all required public checks pass; otherwise record FAIL or UNKNOWN and stop."}
  ],
  "preserves": [
    {"key": "ordinary-runtime-no-member-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-generated-member-controls-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "annotation-runtime-regressions",
      "instruction": "Execute the current bound public harness. Assert no missing-member diagnostic for quoted or unquoted postponed annotations, an explicit missing-member diagnostic for runtime access, and satisfaction of retained generated-member expectations. Record argv, exit status, actual output, and candidate anchors.",
      "evidence_refs": ["pylint-dev/pylint:6594:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:6594:repair:f6479fd320e7"],
  "evidence_refs": ["pylint-dev/pylint:6594:body", "pylint-dev/pylint:6594:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:0c9590e0dcadfaf12ae0182b",
  "read_set": ["role:missing-member-attribute-visitor", "role:member-diagnostic-regression-suite"],
  "write_set": [],
  "validation_for": ["workflow:verified-history:0c9590e0dcadfaf12ae0182b:edit"]
}
```
