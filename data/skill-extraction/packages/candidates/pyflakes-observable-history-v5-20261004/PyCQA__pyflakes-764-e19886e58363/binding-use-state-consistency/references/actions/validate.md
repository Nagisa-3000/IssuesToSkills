# Validate final metadata and diagnostic behavior

Bind public current commands to the reproduction and current test suite. Execute against the final edits and retain actual outputs. Review the annotation guard and continuation in addition to checking test results.

The supplied historical record contains assertions, not an executable historical command. Empty source command arrays require current binding; they do not authorize skipping execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9020121b14a346d4f659c0e:validate",
  "intent": "Verify both modifications and required adjacent behavior.",
  "mechanism": "Execute the public interaction regression and adjacent annotation tests, and review representation and guard preservation.",
  "semantic_role": "repair-validation",
  "owner_role": "annotation-regression-tests",
  "operation": "Validate the final producer edit and regression using bound public probes and repository tests.",
  "kind": "validate",
  "inputs": [
    {"name": "repaired-producer", "semantic_role": "binding-use-implementation", "artifact_kind": "source-code", "language": "Python", "scope": "binding-use-analysis", "phase": "current", "state": "edited", "optional": false},
    {"name": "interaction-test", "semantic_role": "annotation-interaction-regression", "artifact_kind": "test-code", "language": "Python", "scope": "binding-use-analysis", "phase": "current", "state": "authored", "optional": false}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "binding-use-validation", "artifact_kind": "test-result", "language": "Python", "scope": "binding-use-analysis", "phase": "current", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "annotation-use-metadata", "value": "scope-and-node", "evaluator": "evidence"},
    {"key": "interaction-regression", "value": "present", "evaluator": "evidence"},
    {"key": "current-public-oracles", "value": "bound", "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "validation-observations", "value": "recorded", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "annotation-read-remains-undefined", "value": true, "evaluator": "evidence"},
    {"key": "unused-local-remains-reported", "value": true, "evaluator": "evidence"},
    {"key": "postponed-annotation-branch-preserved", "value": true, "evaluator": "evidence"},
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "interaction-diagnostics",
      "instruction": "Run the public reproduction through the checker and confirm no exception plus undefined-name and unused-local diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:764:body", "PyCQA/pyflakes:764:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "annotation-suite",
      "instruction": "Execute the focused regression and adjacent public annotation tests, including relevant postponed-annotation tests; review the unchanged guard and continuation. Record scope and failures.",
      "evidence_refs": ["PyCQA/pyflakes:764:fix", "PyCQA/pyflakes:764:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:764:repair:e19886e58363"],
  "evidence_refs": ["PyCQA/pyflakes:764:body", "PyCQA/pyflakes:764:fix", "PyCQA/pyflakes:764:regression"],
  "validation_for": [
    "workflow:verified-history:a9020121b14a346d4f659c0e:repair",
    "workflow:verified-history:a9020121b14a346d4f659c0e:regression"
  ],
  "read_set": ["role:binding-use-producer", "role:binding-use-consumer", "role:annotation-regression-tests"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:a9020121b14a346d4f659c0e"
}
```

A recorded failure or unknown result is not success. Refresh observations after any further edit. Do not infer whole-project safety from passing one changed test file.
