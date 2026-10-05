# Add the conjunctive guard and controls

Use the currently bound predicate owners. Add an early return before member inference only when postponed evaluation **and** annotation context hold; import the context helper if needed.

Add public quoted and unquoted postponed annotation cases plus ordinary runtime access to the same actually absent member. Preserve existing generated-member expectations. Do not use OR or skip all member checks in a future-import module.

Effects are expected until public validation observes them. Retain the validation Action after this modification.

```arex-contract-v4
{
  "id": "workflow:verified-history:0c9590e0dcadfaf12ae0182b:edit",
  "intent": "Exclude postponed annotation attributes from runtime-oriented missing-member inference.",
  "mechanism": "Return before inference only when both postponed evaluation and annotation context hold.",
  "semantic_role": "context-specific-diagnostic-guard",
  "owner_role": "missing-member-attribute-visitor",
  "operation": "Edit the bound visitor and necessary imports; add public quoted/unquoted postponed annotations and a runtime missing-member control with explicit diagnostic expectations.",
  "kind": "edit",
  "inputs": [
    {
      "name": "repair-context",
      "semantic_role": "postponed-annotation-repair-context",
      "artifact_kind": "code-and-observation-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "applicability-established"
    }
  ],
  "outputs": [
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
  "preconditions": [
    {"key": "annotation-boundary-established", "value": true, "evaluator": "evidence"},
    {"key": "role:missing-member-attribute-visitor", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:postponed-evaluation-detector", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-context-detector", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:member-diagnostic-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "postponed-annotation-no-member-suppressed", "value": true, "evaluator": "evidence", "description": "Expected behavioral effect, requiring validation."},
    {"key": "annotation-runtime-regression-controls-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-runtime-no-member-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-generated-member-controls-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-conjunctive-guard",
      "instruction": "Review the current diff: both predicates are required, the return precedes inference, required imports resolve, and regression expectations distinguish annotation suppression from retained runtime and existing generated-member diagnostics.",
      "evidence_refs": ["pylint-dev/pylint:6594:fix", "pylint-dev/pylint:6594:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:6594:repair:f6479fd320e7"],
  "evidence_refs": ["pylint-dev/pylint:6594:fix", "pylint-dev/pylint:6594:regression"],
  "resource": "references/actions/edit.md",
  "package_id": "workflow:verified-history:0c9590e0dcadfaf12ae0182b",
  "read_set": ["role:postponed-evaluation-detector", "role:annotation-context-detector"],
  "write_set": ["role:missing-member-attribute-visitor", "role:member-diagnostic-regression-suite"],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "annotation-context-unresolved", "value": true, "evaluator": "evidence"},
    {"key": "equivalent-guard-already-effective", "value": true, "evaluator": "evidence"}
  ]
}
```
