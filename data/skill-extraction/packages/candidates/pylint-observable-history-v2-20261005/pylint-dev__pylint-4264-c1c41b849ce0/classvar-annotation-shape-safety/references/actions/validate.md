# Validate shape safety and naming

Bind and render current public commands before execution. Test `ClassVar`, `ClassVar[int]`, `typing.ClassVar`, and `typing.ClassVar[int]`. Check class-constant naming classification, not just process survival. Preserve existing direct forms and neighboring diagnostics.

Probe non-annotated assignments, non-ClassVar Name and Attribute annotations, and unsupported normalized shapes. Require safe false results. Record actual outcomes without editing implementation or weakening expectations.

```arex-contract-v4
{
  "id": "workflow:verified-history:8196d401013577b7b429876a:validate",
  "intent": "Observe repaired recognition and preserved naming behavior through public checks.",
  "mechanism": "Execute current regression tests and negative-shape probes against the patched classifier.",
  "semantic_role": "annotation-repair-validation",
  "owner_role": "annotation-naming-regressions",
  "operation": "Run current bound public checks and record commands, anchors, diagnostics and outcomes without modifying implementation or expected behavior.",
  "kind": "validate",
  "inputs": [
    {"name": "patch", "semantic_role": "annotation-repair-candidate", "artifact_kind": "checkout-diff", "language": "python", "scope": "classvar-naming", "phase": "repair", "state": "unvalidated", "optional": false}
  ],
  "outputs": [
    {"name": "validation", "semantic_role": "annotation-validation-result", "artifact_kind": "test-report", "language": "python", "scope": "classvar-naming", "phase": "validation", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "qualified-classvar-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "direct-classvar-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-naming-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-naming-regressions",
      "instruction": "Run current public naming regressions and adjacent naming checks. Require no AttributeError for all four ClassVar spellings, class-constant invalid-name diagnostics for lowercase names, no corresponding violation for uppercase names, and preservation of existing diagnostics.",
      "evidence_refs": ["pylint-dev/pylint:4264:body", "pylint-dev/pylint:4264:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "verify-negative-shapes",
      "instruction": "Probe non-annotated assignments and annotations normalized to non-ClassVar Name, non-ClassVar Attribute or unsupported shapes. Record current AST shapes and require false without identifier-access exceptions.",
      "evidence_refs": ["pylint-dev/pylint:4264:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:8196d401013577b7b429876a:repair"],
  "source_ids": ["pylint-dev/pylint:4264:repair:c1c41b849ce0"],
  "evidence_refs": ["pylint-dev/pylint:4264:body", "pylint-dev/pylint:4264:fix", "pylint-dev/pylint:4264:regression"],
  "read_set": ["role:annotation-classifier", "role:class-constant-naming-consumer", "role:annotation-naming-regressions"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:8196d401013577b7b429876a"
}
```
