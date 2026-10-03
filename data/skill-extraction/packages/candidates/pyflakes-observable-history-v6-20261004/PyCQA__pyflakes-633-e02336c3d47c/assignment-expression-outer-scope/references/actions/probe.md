# Probe assignment-expression binding ownership

Locate the current binding classifier, insertion owner, comprehension-scope model, and public regression-test owner. Analyze a public generator-expression reproduction followed by an enclosing target use. Record diagnostics and actual scope ownership.

This operation reads code and runs a diagnostic probe without editing source. The output is a review artifact containing observations; it need not conclude that repair is applicable. Unknown or failed applicability checks do not authorize editing.

```arex-contract-v4
{
  "id": "workflow:verified-history:fd9457af9cbbabf21f89fac4:probe",
  "intent": "Determine whether the current analyzer has the evidenced assignment-expression scope mismatch.",
  "mechanism": "Compare a public false undefined-name reproduction with current target classification and scope insertion.",
  "semantic_role": "scope-routing-diagnosis",
  "owner_role": "assignment-binding-router",
  "operation": "Inspect public source and run a current-bound diagnostic probe without modifying source; record current owner bindings, code anchors, runtime support, diagnostics, and routing observations.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "reviewed-routing",
      "semantic_role": "assignment-expression-routing-state",
      "artifact_kind": "source-and-probe-record",
      "language": "python",
      "scope": "analyzer-binding-and-regressions",
      "phase": "pre-repair",
      "state": "reviewed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "routing-review-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-assignment-scope-preserved", "value": true, "evaluator": "evidence"},
    {"key": "iteration-variable-isolation-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-binding-bookkeeping-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-routing-mismatch",
      "instruction": "Analyze a public walrus-generator case followed by an enclosing target use and inspect current binding classification and insertion. Record whether the false diagnostic is caused by comprehension-local insertion, whether syntax is supported, and which current symbols own the mechanism. Confirm the probe did not edit source.",
      "evidence_refs": ["PyCQA/pyflakes:633:body", "PyCQA/pyflakes:633:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:633:repair:e02336c3d47c"],
  "evidence_refs": ["PyCQA/pyflakes:633:body", "PyCQA/pyflakes:633:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:fd9457af9cbbabf21f89fac4",
  "read_set": [
    "role:assignment-binding-router",
    "role:comprehension-scope-model",
    "role:scope-regression-tests"
  ],
  "write_set": []
}
```
