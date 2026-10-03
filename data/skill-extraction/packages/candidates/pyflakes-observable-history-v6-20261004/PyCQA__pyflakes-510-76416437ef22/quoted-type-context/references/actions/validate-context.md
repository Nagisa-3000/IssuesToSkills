# Validate quoted contexts and adjacent behavior

Bind public test commands to the current checkout. Run target assertions and relevant existing annotation tests. Record commands, results, and remaining coverage gaps. Do not claim whole-project success from a narrow annotation-test run.

Required checks include quoted casts and renamed imports; partially quoted and nested typing subscriptions; a second cast argument such as `'Optional[int]'` remaining an ordinary string; context restoration; and unchanged special Literal handling. In the original report, the unrelated undefined `reveal_type` diagnostic remains legitimate.

```arex-contract-v4
{
  "id": "workflow:verified-history:3f957b40be188975fdc11a7e:validate",
  "intent": "Observe corrected quoted-type diagnostics and preserved adjacent semantics.",
  "mechanism": "Public reproduction, regression assertions and annotation-neighbor tests.",
  "semantic_role": "context-validation",
  "owner_role": "annotation-regression-tests",
  "operation": "Execute currently bound public checks and inspect diagnostic results after repair, without further source edits.",
  "kind": "validate",
  "inputs": [
    {
      "name": "patched-analyzer",
      "semantic_role": "annotation-context-repair",
      "artifact_kind": "source-tree",
      "language": "python",
      "scope": "annotation-analyzer",
      "phase": "repair",
      "state": "modified"
    }
  ],
  "outputs": [
    {
      "name": "validation-report",
      "semantic_role": "annotation-validation-observation",
      "artifact_kind": "test-report",
      "language": "python",
      "scope": "annotation-analyzer",
      "phase": "validation",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "runtime-string-semantics", "value": "preserved", "evaluator": "evidence"},
    {"key": "annotation-state-restoration", "value": "preserved", "evaluator": "evidence"},
    {"key": "typing-literal-semantics", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "quoted-context-regressions",
      "instruction": "Run public checks corresponding to all five supplied regression assertions, the original diagnostic reproduction, and current annotation neighbors covering restoration and Literal semantics. Record PASS/FAIL/UNKNOWN and exact coverage; tests must demonstrate no unused import for quoted type references and no interpretation of runtime cast values as type names.",
      "evidence_refs": ["PyCQA/pyflakes:510:body", "PyCQA/pyflakes:510:fix", "PyCQA/pyflakes:510:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:3f957b40be188975fdc11a7e:repair"],
  "read_set": ["role:python-annotation-analyzer", "role:annotation-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:510:repair:76416437ef22"],
  "evidence_refs": ["PyCQA/pyflakes:510:body", "PyCQA/pyflakes:510:fix", "PyCQA/pyflakes:510:regression"],
  "resource": "references/actions/validate-context.md",
  "package_id": "workflow:verified-history:3f957b40be188975fdc11a7e"
}
```

An observed report can contain failures. Validation observation is not synonymous with validation success; stop on failures or unknown required assurances.
