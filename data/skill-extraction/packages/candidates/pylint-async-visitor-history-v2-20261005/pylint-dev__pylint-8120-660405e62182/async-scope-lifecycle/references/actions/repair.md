# Restore async entry and exit parity

Use current role bindings, not historical paths. Register both async entry and async exit with the established synchronous scope lifecycle. Aliasing is appropriate only if current dispatch and handler semantics agree. Preserve synchronous, class, and module lifecycle behavior and diagnostic rules. Do not globally clear state or disable the warning.

The declared correction is an expected effect, not an execution result. This edit makes prior validation stale and retains [validation](validate.md).

```arex-contract-v4
{
  "id": "workflow:verified-history:9a2315892fecfccf9d5c6c14:repair",
  "intent": "Isolate assignment-type state within each async function scope.",
  "mechanism": "Register both async visitor lifecycle hooks with established scope handlers.",
  "semantic_role": "restore-async-lifecycle",
  "owner_role": "assignment-type-checker",
  "operation": "Edit the bound checker to provide equivalent async scope entry and exit without changing diagnostic rules.",
  "kind": "edit",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "current-owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "scope-mechanism-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "missing-async-lifecycle-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "async-dispatch-binding-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "async-lifecycle-parity", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-lifecycle-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "within-scope-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-hook-parity",
      "instruction": "Review the current diff and dispatch bindings. Both async entry and exit must invoke the established scope handlers; synchronous, class, module and diagnostic rules must remain intact. This review does not replace executable validation.",
      "kind": "public_probe",
      "evidence_refs": ["pylint-dev/pylint:8120:fix"]
    }
  ],
  "read_set": ["role:assignment-type-checker", "role:visitor-dispatch"],
  "write_set": ["role:assignment-type-checker"],
  "source_ids": ["pylint-dev/pylint:8120:repair:660405e62182"],
  "evidence_refs": ["pylint-dev/pylint:8120:fix"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:9a2315892fecfccf9d5c6c14"
}
```
