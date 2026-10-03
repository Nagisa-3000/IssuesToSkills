# Inspect current identity-comparison owners

Read the current analyzer and public tests without modifying them. Bind semantic owners and inspect supported AST representations. Look for a classifier limited to string/number/bytes nodes, an identity operator visitor, and existing singleton behavior.

Determine applicability from current evidence; owner existence alone does not prove semantic compatibility. The intended output is a reviewed binding record, not a claim that repair has succeeded.

```arex-contract-v4
{
  "id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:inspect",
  "intent": "Establish whether the constant-tuple identity-diagnostic repair applies to current Python AST code.",
  "mechanism": "Inspect comparison traversal, AST compatibility branches, singleton handling, diagnostic ownership, and public regression coverage.",
  "semantic_role": "applicability-inspection",
  "owner_role": "comparison-classifier",
  "operation": "Read current owners and tests; collect public AST observations for empty tuples, recursive constants, singleton values, and variable-containing tuples. Make no source edits.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "reviewed-target",
      "semantic_role": "identity-diagnostic-target",
      "artifact_kind": "binding-and-observation-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "repair",
      "state": "reviewed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-python-ast-analyzer-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-owner-bindings-observed", "value": true, "evaluator": "evidence"},
    {"key": "repair-applicability-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "singleton-exemptions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nonconstant-tuple-exclusion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-literal-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nonidentity-comparison-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-current-owners",
      "instruction": "Confirm the current Python AST comparison visitor, literal diagnostic, public tests, supported runtime representations, and whether constant tuples are omitted. Record semantic findings and owner bindings. Verify inspection has not changed source files.",
      "evidence_refs": ["PyCQA/pyflakes:483:body", "PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:483:repair:0af480e3351a"],
  "evidence_refs": ["PyCQA/pyflakes:483:body", "PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f",
  "read_set": ["role:comparison-classifier", "role:literal-diagnostic", "role:comparison-regressions"],
  "write_set": [],
  "exclusions": [
    {"key": "non-python-ast-target", "value": true, "evaluator": "evidence"},
    {"key": "runtime-identity-rewrite-requested", "value": true, "evaluator": "evidence"}
  ]
}
```

An empty oracle command means no current command has been bound. It is not an executable validation or a PASS result. Use a current public probe to resolve UNKNOWN facts before considering an edit.
