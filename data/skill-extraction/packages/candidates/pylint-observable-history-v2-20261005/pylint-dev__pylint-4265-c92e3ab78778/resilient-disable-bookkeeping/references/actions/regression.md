# Retain a mixed-ID suppression regression

Add a public configuration regression with an unresolved numeric advisory identifier before a valid disabled identifier, and source code that would emit the latter diagnostic without disabling it. Resolve identifiers against the current registry; historical names are not portable bindings.

The historical fixture used `C0111,C0326,W0703` and an `except Exception` example. It contained no annotation expecting `broad-except`. Reuse the behavioral shape, not an assumption about current identifier validity.

```arex-contract-v4
{
  "id": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:regression",
  "intent": "Retain a public assertion that missing advisory IDs do not block subsequent valid disables.",
  "mechanism": "Combine numeric disable entries and a diagnostic-triggering fixture in the configuration test harness.",
  "semantic_role": "configuration-regression-addition",
  "owner_role": "configuration-regression",
  "operation": "Add or extend a source fixture and its disable configuration to exercise missing lookup followed by valid suppression, without weakening existing expected diagnostics.",
  "kind": "edit",
  "inputs": [
    {
      "name": "mechanism-evidence",
      "semantic_role": "advisory-disable-mechanism",
      "artifact_kind": "evidence-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-repair",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [],
  "preconditions": [
    {"key": "role:configuration-regression", "value": true, "evaluator": "file_exists"},
    {"key": "advisory-keyerror-interrupts-disable", "value": true, "evaluator": "evidence"},
    {"key": "current-regression-identifiers-resolved", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "mixed-id-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "known-numeric-registration-preserved", "value": true, "evaluator": "evidence"},
    {"key": "symbolic-disable-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-errors-not-suppressed", "value": true, "evaluator": "evidence"},
    {"key": "existing-test-expectations-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-regression-shape",
      "instruction": "Inspect the new public fixture and configuration. Confirm the unresolved advisory identifier precedes a valid disable, the source triggers that diagnostic when enabled, and existing assertions were not weakened.",
      "evidence_refs": ["pylint-dev/pylint:4265:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:configuration-regression", "role:message-registry"],
  "write_set": ["role:configuration-regression"],
  "source_ids": ["pylint-dev/pylint:4265:repair:c92e3ab78778"],
  "evidence_refs": ["pylint-dev/pylint:4265:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b"
}
```
