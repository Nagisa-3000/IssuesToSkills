# Validate target and adjacent behavior

Bind the current public reproduction and functional harness before execution. Inspect actual diagnostic identities as well as process status: a linter's nonzero status can represent expected unrelated diagnostics rather than the target crash.

Run the attribute-copy case and relevant existing simple-name dictionary, list, and set mutation cases. Review unchanged inference guards. Record commands, outputs, and PASS/FAIL/UNKNOWN outcomes without editing source. Missing or unexecuted checks do not establish success.

```arex-contract-v4
{
  "id": "workflow:verified-history:d4547bc8e3248f1130d70f73:validate",
  "intent": "Observe repaired copy behavior and preservation of adjacent checker behavior.",
  "mechanism": "Execute current public reproduction and regression oracles against the edited checker.",
  "semantic_role": "repair-validation",
  "owner_role": "iteration-functional-tests",
  "operation": "Run bound public checks, inspect crash and diagnostic outcomes, review guard preservation, and record observations without modifying checker or fixture source.",
  "kind": "validate",
  "inputs": [
    {
      "name": "repair",
      "semantic_role": "iterator-field-repair",
      "artifact_kind": "source-and-test-change",
      "language": "python",
      "scope": "iteration-checker-and-tests",
      "phase": "post-repair",
      "state": "edited",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "iterator-field-validation",
      "artifact_kind": "test-observation",
      "language": "python",
      "scope": "iteration-checker-and-tests",
      "phase": "post-repair",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "attribute-access-repaired", "value": true, "evaluator": "evidence"},
    {"key": "copy-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "simple-name-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inference-guards-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-mutation-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "attribute-copy-mre",
      "instruction": "Execute the current bound attribute-loop copy reproduction. Require no Attribute.name exception, no fatal astroid error, and no modified-iterating-dict diagnostic on assignment into the copied mapping.",
      "evidence_refs": ["pylint-dev/pylint:7461:body", "pylint-dev/pylint:7461:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "iteration-functional-regressions",
      "instruction": "Run the bound current functional harness including the copy regression and relevant existing simple-name dictionary, list, and set mutation cases. Require expected diagnostic identities and no unexpected messages. Review the diff to confirm inference guards remain unchanged.",
      "evidence_refs": ["pylint-dev/pylint:7461:fix", "pylint-dev/pylint:7461:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:d4547bc8e3248f1130d70f73:repair"],
  "source_ids": ["pylint-dev/pylint:7461:repair:fb30fe09d74d"],
  "evidence_refs": ["pylint-dev/pylint:7461:body", "pylint-dev/pylint:7461:fix", "pylint-dev/pylint:7461:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:d4547bc8e3248f1130d70f73",
  "read_set": ["role:iteration-checker", "role:iteration-functional-tests"],
  "write_set": []
}
```
