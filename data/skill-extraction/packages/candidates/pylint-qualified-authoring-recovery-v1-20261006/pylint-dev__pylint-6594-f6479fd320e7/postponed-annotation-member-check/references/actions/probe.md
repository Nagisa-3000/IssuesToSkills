# Inspect the annotation boundary

Read current public code without modifying files. Establish both predicates semantically, not by helper names. Locate the attribute-inference boundary and public regression harness. An effective equivalent guard or a runtime-only target excludes this repair.

```arex-contract-v4
{
  "id": "workflow:verified-history:0c9590e0dcadfaf12ae0182b:probe",
  "intent": "Establish applicability and current semantic owner bindings.",
  "mechanism": "Inspect the public target, postponed-evaluation predicate, annotation-context predicate, and attribute-inference boundary.",
  "semantic_role": "annotation-boundary-inspection",
  "owner_role": "missing-member-attribute-visitor",
  "operation": "Read the pinned public checkout without editing files; record hashed anchors and evidence-backed owner bindings. Emit an applicability-established context only when the mechanism is confirmed.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
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
  "preconditions": [],
  "effects": [
    {"key": "annotation-boundary-established", "value": true, "evaluator": "evidence"},
    {"key": "role:missing-member-attribute-visitor", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:postponed-evaluation-detector", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-context-detector", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:member-diagnostic-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "preserves": [
    {"key": "ordinary-runtime-no-member-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-generated-member-controls-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-context",
      "instruction": "Inspect current public anchors and the reproduction. Confirm postponed evaluation, annotation classification of the target, runtime classification of the control, and absence of an effective equivalent guard. Confirm inspection did not edit files. Unresolved prerequisites remain UNKNOWN and do not authorize editing.",
      "evidence_refs": ["pylint-dev/pylint:6594:body", "pylint-dev/pylint:6594:fix", "pylint-dev/pylint:6594:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:6594:repair:f6479fd320e7"],
  "evidence_refs": ["pylint-dev/pylint:6594:body", "pylint-dev/pylint:6594:fix", "pylint-dev/pylint:6594:regression"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:0c9590e0dcadfaf12ae0182b",
  "read_set": [
    "role:missing-member-attribute-visitor",
    "role:postponed-evaluation-detector",
    "role:annotation-context-detector",
    "role:member-diagnostic-regression-suite"
  ],
  "write_set": [],
  "exclusions": [
    {"key": "runtime-only-failure", "value": true, "evaluator": "evidence"},
    {"key": "equivalent-guard-already-effective", "value": true, "evaluator": "evidence"}
  ]
}
```
