# Validate target and adjacent behavior

Bind commands to the current public regression owner. Check target diagnostic identity rather than requiring silence from all lint messages. Capture commands, exit codes, and actual diagnostic output. Equivalent async probes are current supplemental checks where the visitor is shared; the historical fixture contains ordinary definitions only.

```arex-contract-v4
{
  "id": "workflow:verified-history:0b7e98c0346a9448ab645489:validate",
  "intent": "Observe removal of the false positive and preservation of supported warnings.",
  "mechanism": "Execute the positional-only negative cases, mixed-signature positive cases, and ordinary diagnostic controls.",
  "semantic_role": "public-diagnostic-validation",
  "owner_role": "signature-regression-owner",
  "operation": "Run bound current public checks without source edits, capture results, and refresh validation observations.",
  "kind": "validate",
  "inputs": [
    {"name": "candidate-repair", "semantic_role": "signature-diagnostic-candidate", "artifact_kind": "checkout-change", "language": "python", "scope": "signature-diagnostic", "phase": "post-edit", "state": "unvalidated"}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "signature-diagnostic-validation", "artifact_kind": "test-report", "language": "python", "scope": "signature-diagnostic", "phase": "post-validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "narrow-guard-and-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "mixed-signature-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "validation_for": ["workflow:verified-history:0b7e98c0346a9448ab645489:repair"],
  "oracle": [
    {
      "id": "run-signature-matrix",
      "instruction": "Execute the bound public harness. Require the target warning for the three mixed signatures and none for the five positional-only-prefix signatures in the regression evidence. Run existing ordinary diagnostic controls. Capture exit codes and failures; execution alone is not PASS.",
      "evidence_refs": ["pylint-dev/pylint:8570:regression", "pylint-dev/pylint:8570:body"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "read_set": ["role:signature-diagnostic-owner", "role:signature-regression-owner"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:8570:repair:56fa5dce747a"],
  "evidence_refs": ["pylint-dev/pylint:8570:fix", "pylint-dev/pylint:8570:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:0b7e98c0346a9448ab645489"
}
```
