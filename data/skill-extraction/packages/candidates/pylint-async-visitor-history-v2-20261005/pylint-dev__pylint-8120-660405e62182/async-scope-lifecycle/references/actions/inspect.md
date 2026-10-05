# Inspect the lifecycle mechanism

Read current owners and record bindings and hashed anchors. Compare synchronous and async visitor entry/exit and their assignment-state stack handling. Probe independent async scopes and synchronous equivalents. This operation does not edit tracked source; keep probe artifacts outside it.

Record mechanism facts separately from the fact that review occurred. Missing-hook and dispatch checks must explicitly PASS before repair; UNKNOWN permits further probes, and FAIL rejects this mechanism.

```arex-contract-v4
{
  "id": "workflow:verified-history:9a2315892fecfccf9d5c6c14:inspect",
  "intent": "Determine whether omitted async lifecycle registrations explain cross-scope diagnostics.",
  "mechanism": "Compare visitor dispatch and scope-state handling against synchronous isolation.",
  "semantic_role": "diagnose-scope-lifecycle",
  "owner_role": "assignment-type-checker",
  "operation": "Read current owners, bind public probes, and record mechanism observations without editing tracked code.",
  "kind": "probe",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "public-current-base-pinned", "value": true, "evaluator": "evidence"},
    {"key": "role:assignment-type-checker", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "scope-mechanism-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "current-owners-bound", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-lifecycle-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "within-scope-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-leakage-mechanism",
      "instruction": "Record async hook presence, dispatch semantics, assignment-state lifetime, and public async versus synchronous diagnostic output. Record missing-async-lifecycle-confirmed and async-dispatch-binding-confirmed as PASS, FAIL, or UNKNOWN. Confirm no tracked source edit.",
      "kind": "public_probe",
      "evidence_refs": ["pylint-dev/pylint:8120:body", "pylint-dev/pylint:8120:fix"]
    }
  ],
  "read_set": ["role:assignment-type-checker", "role:visitor-dispatch", "role:checker-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:8120:repair:660405e62182"],
  "evidence_refs": ["pylint-dev/pylint:8120:body", "pylint-dev/pylint:8120:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:9a2315892fecfccf9d5c6c14"
}
```
