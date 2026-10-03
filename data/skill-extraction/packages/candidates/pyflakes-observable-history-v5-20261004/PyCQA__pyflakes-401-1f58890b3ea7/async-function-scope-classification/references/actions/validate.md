# Validate the changed classification and annotation behavior

Review the effective classifier and diff. Verify that async and ordinary definitions use function scope with the correct representation, unrelated entries remain intact, and access to unavailable AST classes remains protected.

Run the public reproduction, the regression, and surrounding current public annotation tests with bound current commands. Require no crash or unexpected diagnostics for the reproduction. Record actual exit statuses, failures, diagnostics, and skips.

Review compatibility guards and exercise supported-runtime checks where available. Unavailable runtime execution remains UNKNOWN; code review alone does not prove execution on those runtimes. Adjacent checks are preservation obligations, not claims of supplied historical outcomes.

```arex-contract-v4
{
  "id": "workflow:verified-history:76dfcbfcb074afe10f1cb891:validate",
  "intent": "Verify repaired async annotation behavior and preserve neighboring scope, annotation, and runtime behavior.",
  "mechanism": "Review the registry and guards, execute the public reproduction and annotation tests, and record current outcomes.",
  "semantic_role": "validate-async-scope-repair",
  "owner_role": "annotation-regression-tests",
  "operation": "Execute bound public checks and review current classifier, test, and compatibility invariants after modification.",
  "kind": "validate",
  "inputs": [
    {
      "name": "repair-change",
      "semantic_role": "async-scope-repair-change",
      "artifact_kind": "source-and-test-change",
      "language": "python",
      "scope": "scope-classifier-and-annotation-tests",
      "phase": "current",
      "state": "modified"
    }
  ],
  "outputs": [
    {
      "name": "validation-results",
      "semantic_role": "async-scope-repair-validation",
      "artifact_kind": "validation-record",
      "language": "python",
      "scope": "scope-classifier-and-annotation-tests",
      "phase": "current",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "role:python-ast-scope-classifier", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "current-public-validation-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-validation-results-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unchanged-by-validation", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-function-scope-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-scope-entries-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-annotation-tests-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-safety-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-classification-and-guards",
      "instruction": "Review and publicly probe async and ordinary function classification, registry value compatibility, unchanged unrelated entries, and import/test capability guards. Explicitly record unavailable runtime execution coverage.",
      "evidence_refs": ["PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
      "kind": "public_probe",
      "command": []
    },
    {
      "id": "verify-public-reproduction",
      "instruction": "Run the public class-and-same-name async parameter annotation reproduction, including a None return annotation; require no Module.parent crash and no unexpected diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-annotation-tests",
      "instruction": "Run the current regression and surrounding public annotation tests. Record actual exit statuses, failures, diagnostics, and skips, and check supported-runtime test safety.",
      "evidence_refs": ["PyCQA/pyflakes:401:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:76dfcbfcb074afe10f1cb891:repair"],
  "read_set": [
    "role:python-ast-scope-classifier",
    "role:python-runtime-capability-policy",
    "role:annotation-regression-tests"
  ],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
  "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:76dfcbfcb074afe10f1cb891"
}
```
