# Probe annotation coverage

Read the bound collector and inspect the public reproduction through the current checker harness. Trace ordinary annotation credit and compare the separate keyword-only collections. Record policy, alignment, omission, diagnostic names, and owner anchors. Inspection must not change tracked files.

The review output records findings, including rejection or insufficient evidence. A produced review is not automatically a confirmed omission. Only evidence-backed PASS prerequisites authorize editing.

```arex-contract-v4
{
  "id": "workflow:verified-history:9458ec98dda8784befed789c:probe",
  "intent": "Determine whether omitted keyword-only annotation evidence explains the warning.",
  "mechanism": "Compare ordinary and keyword-only annotation coverage in the parameter-type collector.",
  "semantic_role": "coverage-diagnosis",
  "owner_role": "parameter-type-evidence-collector",
  "operation": "Inspect current code and a public reproduction without editing tracked files; record policy, alignment, omission findings, and current owner bindings.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "coverage-review", "semantic_role": "coverage-review", "artifact_kind": "review-record", "language": "Python", "scope": "parameter-documentation-checker", "phase": "diagnosis", "state": "recorded"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "coverage-review-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-annotation-credit-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-missing-type-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-omission",
      "instruction": "Record whether ordinary annotations count as type evidence, annotated keyword-only names are omitted, and keyword-only parameter/annotation indices align. Bind current collector and test owners and observe the public reproduction. Confirm inspection leaves tracked files unchanged; negative or unknown findings must not authorize editing.",
      "evidence_refs": ["pylint-dev/pylint:3092:body", "pylint-dev/pylint:3092:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3092:repair:ce2af67d0e96"],
  "evidence_refs": ["pylint-dev/pylint:3092:body", "pylint-dev/pylint:3092:fix"],
  "read_set": ["role:parameter-type-evidence-collector", "role:parameter-documentation-test-suite"],
  "write_set": [],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:9458ec98dda8784befed789c"
}
```
