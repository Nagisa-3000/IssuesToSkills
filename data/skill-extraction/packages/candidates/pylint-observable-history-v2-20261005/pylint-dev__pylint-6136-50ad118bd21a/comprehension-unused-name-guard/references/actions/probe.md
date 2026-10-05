# Confirm the dispatch mechanism

Read current owners and run a bound public reproduction without modifying checkout files. Trace the iterable use and target binding separately. Confirm that target-name exclusion currently protects only arguments, not the shared local-variable dispatch.

Emit a confirmed context only when evidence supports this mechanism. Already-shared guards or materially different target-set semantics make the repair inapplicable.

```arex-contract-v4
{
  "id": "workflow:verified-history:d24c4831d73f4eeb9d623f2b:probe",
  "intent": "Establish the current symptom and supported dispatch boundary.",
  "mechanism": "Compare public homonym diagnostic output with anchored target-name exclusion placement.",
  "semantic_role": "mechanism-confirmation",
  "owner_role": "unused-name-dispatch",
  "operation": "Read dispatch and target collection, run a bound public analyzer probe, and record anchors and output without editing checkout files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "confirmed-context", "semantic_role": "confirmed-unused-name-mechanism", "artifact_kind": "evidence-record", "language": "python", "scope": "current-checkout", "phase": "pre-edit", "state": "confirmed"}
  ],
  "preconditions": [
    {"key": "public-base-pinned", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "dispatch-mechanism-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-unused-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-name-errors-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-dispatch",
      "instruction": "Bind a current public reproduction command. Capture the outer container's false unused-variable diagnostic, inspect anchored argument-only target exclusion and target-set semantics, and verify the probe made no checkout edits.",
      "evidence_refs": ["pylint-dev/pylint:6136:body", "pylint-dev/pylint:6136:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:unused-name-dispatch", "role:comprehension-target-collection"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:6136:repair:50ad118bd21a"],
  "evidence_refs": ["pylint-dev/pylint:6136:body", "pylint-dev/pylint:6136:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:d24c4831d73f4eeb9d623f2b"
}
```
