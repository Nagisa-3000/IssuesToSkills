# Guard missing advisory lookup

Only after the probe establishes the mechanism, add a local `KeyError` guard around numeric-ID advisory registration. An unresolved lookup produces no advisory tuple and must not interrupt later configuration entries. Keep successful tuple construction and append behavior intact.

Do not catch `Exception`, guard the entire configuration parser, or change message emission policy. The historical change guarded the numeric test, lookup, tuple construction, and append within the helper; choose the corresponding narrow boundary in current code.

```arex-contract-v4
{
  "id": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:guard",
  "intent": "Allow disable processing to continue after missing advisory identifier lookup.",
  "mechanism": "Catch KeyError locally in numeric-message advisory registration.",
  "semantic_role": "advisory-lookup-repair",
  "owner_role": "disable-bookkeeping",
  "operation": "Modify only the advisory registration boundary to tolerate missing numeric ID lookup, preserving successful registration and all non-KeyError propagation.",
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
    {"key": "role:disable-bookkeeping", "value": true, "evaluator": "symbol_exists"},
    {"key": "advisory-keyerror-interrupts-disable", "value": true, "evaluator": "evidence"},
    {"key": "continuation-compatible-with-required-policy", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "missing-advisory-id-tolerated", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "known-numeric-registration-preserved", "value": true, "evaluator": "evidence"},
    {"key": "symbolic-disable-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-errors-not-suppressed", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-exception-boundary",
      "instruction": "Review the public diff: only advisory numeric-ID registration tolerates KeyError; known IDs retain tuple contents and append behavior; non-KeyError failures are not newly caught.",
      "evidence_refs": ["pylint-dev/pylint:4265:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:disable-bookkeeping", "role:message-registry"],
  "write_set": ["role:disable-bookkeeping"],
  "source_ids": ["pylint-dev/pylint:4265:repair:c92e3ab78778"],
  "evidence_refs": ["pylint-dev/pylint:4265:fix"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b"
}
```
