# Observe correction and preservation

Bind current public analyzer and repository test commands. Compare before/after diagnostics and inspect actual emitted messages. Run target fixtures and ordinary unused-local, unused-argument, undefined-name, and used-before-assignment controls.

Do not edit expectations during validation. An expectation removal alone is not evidence of correction. Retain command output, exit status, and current anchors; on failure or UNKNOWN, do not assert successful validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:d24c4831d73f4eeb9d623f2b:validate",
  "intent": "Observe target diagnostic correction and preserved adjacent behavior.",
  "mechanism": "Run bound public reproductions and the current diagnostic fixture harness after the edit.",
  "semantic_role": "repair-validation",
  "owner_role": "diagnostic-validation",
  "operation": "Execute bound checks, compare actual diagnostic output, and retain logs tied to current anchors without modifying source or expected diagnostics.",
  "kind": "validate",
  "inputs": [
    {"name": "candidate-change", "semantic_role": "unused-name-repair-candidate", "artifact_kind": "checkout-diff", "language": "python", "scope": "current-checkout", "phase": "post-edit", "state": "unvalidated"}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "unused-name-validation", "artifact_kind": "test-record", "language": "python", "scope": "current-checkout", "phase": "post-edit", "state": "observed"}
  ],
  "preconditions": [
    {"key": "shared-target-exclusion", "value": true, "evaluator": "evidence"},
    {"key": "homonym-regression-covered", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-unused-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-name-errors-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-homonym",
      "instruction": "Run bound generator and list-comprehension homonym analyzer probes. Observe no unused-variable for the outer iterable and record emitted diagnostics, not application assertion outcomes.",
      "evidence_refs": ["pylint-dev/pylint:6136:body", "pylint-dev/pylint:6136:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-adjacent",
      "instruction": "Run bound current repository tests for the annotation-comprehension expectation and ordinary unused-local, unused-argument, undefined-name, and used-before-assignment controls. Verify actual outputs and confirm no adjacent expectations were weakened.",
      "evidence_refs": ["pylint-dev/pylint:6136:fix", "pylint-dev/pylint:6136:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:d24c4831d73f4eeb9d623f2b:repair"],
  "read_set": ["role:unused-name-dispatch", "role:diagnostic-fixtures", "role:diagnostic-validation"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:6136:repair:50ad118bd21a"],
  "evidence_refs": ["pylint-dev/pylint:6136:body", "pylint-dev/pylint:6136:fix", "pylint-dev/pylint:6136:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:d24c4831d73f4eeb9d623f2b"
}
```
