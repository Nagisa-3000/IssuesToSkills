# Diagnose configuration ownership

Read current public code and trace option parsing, consumer construction, subsequent configuration writes, and runtime reads. Compare integrated and standalone construction. Run an isolated public reproduction without editing repository source or tests.

Record findings even when they reject the mechanism. Emit the diagnosed port only with concrete owner bindings; compatibility predicates become PASS only after evidence-backed review.

```arex-contract-v4
{
  "id": "workflow:verified-history:44cf4d12e6c9f03961fb6377:diagnose",
  "intent": "Determine whether runtime consumers read stale copies of authoritative configuration.",
  "mechanism": "Trace constructor snapshots, later host configuration updates, and runtime option reads.",
  "semantic_role": "configuration-lifecycle-diagnosis",
  "owner_role": "configuration-consumer",
  "operation": "Read current public code and run an isolated public reproduction; record configuration identity, update order, runtime reads, and construction modes without editing repository source or tests.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "diagnosed-consumer",
      "semantic_role": "configuration-consumer",
      "artifact_kind": "source-tree",
      "language": "python",
      "scope": "configuration-and-similarity",
      "phase": "repair",
      "state": "diagnosed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:configuration-consumer", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "ownership-diagnosis-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "standalone-option-semantics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "similarity-algorithm-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "trace-public-option",
      "instruction": "Capture the public option value, authoritative namespace identity, copied consumer values, configuration-write order, and runtime reads. Distinguish import-only duplicate-code from independent unused-import output. Record stale-copy, namespace-compatibility, and initialization-safety checks as PASS, FAIL, or UNKNOWN, and confirm repository source and tests were not edited.",
      "evidence_refs": ["pylint-dev/pylint:6350:body", "pylint-dev/pylint:6350:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:configuration-consumer", "role:configuration-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:6350:repair:cb37ae4fc24a"],
  "evidence_refs": ["pylint-dev/pylint:6350:body", "pylint-dev/pylint:6350:fix"],
  "resource": "references/actions/diagnose.md",
  "package_id": "workflow:verified-history:44cf4d12e6c9f03961fb6377"
}
```
