# Validate changed and preserved behavior

Bind and render current public commands for the current regression harness. Execute invalid instance/constant cases, valid-class cases, uninferable exemptions, and relevant adjacent checker cases. Record outputs and metadata, not just exit status. Do not rewrite expectations to conceal failures.

When the current issue concerns the reported tuple-assignment symptom, run its reproduction separately and record crash/no-crash status. Neither this source nor a no-crash observation proves a parent-traversal repair.

This Action does not edit source or expectation files. Test artifacts are observations, not new historical evidence.

```arex-contract-v4
{
  "id": "workflow:verified-history:124787fcb0844f5e9acb613d:validate",
  "intent": "Observe diagnostic correctness and preservation assurances.",
  "mechanism": "Execute current public tests and review diagnostic text, metadata, and exemption behavior.",
  "semantic_role": "typed-diagnostic-validation",
  "owner_role": "special-class-assignment-regression-suite",
  "operation": "Render bound current Oracle commands, execute public regression checks, compare rejected-value diagnostics and metadata, check accepted and uninferable cases and adjacent behavior, and record tri-state results without concealing failures.",
  "kind": "validate",
  "inputs": [
    {
      "name": "diagnostic-change",
      "semantic_role": "inferred-kind-diagnostic-change",
      "artifact_kind": "checkout-diff",
      "language": "Python",
      "scope": "special-class-assignment",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "inferred-kind-diagnostic-validation",
      "artifact_kind": "test-observation",
      "language": "Python",
      "scope": "special-class-assignment",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "diagnostic-kind-included", "value": true, "evaluator": "evidence"},
    {"key": "assertions-match-diagnostic", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "acceptance-semantics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-metadata-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-checker-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-diagnostic-regressions",
      "instruction": "Run bound current public tests. Verify inferred-kind text for invalid instance and constant cases, unchanged symbol/source spans/object labels/confidence, valid-class acceptance, uninferable exemption, and adjacent behavior. Record argv, exit codes, outputs, and assurance checks. Any failure blocks a success claim.",
      "evidence_refs": ["pylint-dev/pylint:7467:fix", "pylint-dev/pylint:7467:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "check-public-reproduction",
      "instruction": "If relevant to the current public issue, execute the tuple-assignment reproduction through a bound current command and record crash/no-crash status separately. Otherwise record that it is inapplicable with public evidence. Do not infer an unsupported traversal mechanism.",
      "evidence_refs": ["pylint-dev/pylint:7467:body"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:124787fcb0844f5e9acb613d:edit"],
  "read_set": [
    "role:special-class-assignment-checker",
    "role:special-class-assignment-diagnostic",
    "role:special-class-assignment-regression-suite"
  ],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:7467:repair:b47aa3076ee0"],
  "evidence_refs": ["pylint-dev/pylint:7467:body", "pylint-dev/pylint:7467:fix", "pylint-dev/pylint:7467:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:124787fcb0844f5e9acb613d"
}
```
