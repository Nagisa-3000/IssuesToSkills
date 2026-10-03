# Validate the edits and preserved behavior

Bind and render current public commands before execution. Run the new regression, the surrounding undefined-name tests, and the original annotated reproduction. Review the version gates and any changed asynchronous-loop branches.

Record interpreter versions, argv commands, exit statuses, and assertion outcomes. Unavailable older-version execution remains UNKNOWN; static truth-table review is a separate observation. A failing or unexecuted required check cannot establish the intended `public-validation: passed` effect.

Historical evidence supplies an assertion, not an executed command. This Action validates both modifying Actions.

```arex-contract-v4
{
  "id": "workflow:verified-history:4817630500584ee0981edde8:validate",
  "intent": "Validate the registry edit and regression using public behavior and preservation checks.",
  "mechanism": "Execute current bound public checks and review version-boundary and adjacent-branch semantics.",
  "semantic_role": "repair-validation",
  "owner_role": "undefined-name-regressions",
  "operation": "validate-registry-and-regression",
  "kind": "validate",
  "inputs": [
    {
      "name": "registry-edit",
      "semantic_role": "implicit-name-registration-change",
      "artifact_kind": "code-change",
      "language": "python",
      "scope": "module-name-checking",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    },
    {
      "name": "regression-edit",
      "semantic_role": "implicit-name-regression-change",
      "artifact_kind": "test-change",
      "language": "python",
      "scope": "module-name-checking",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "implicit-name-repair-validation",
      "artifact_kind": "public-check-record",
      "language": "python",
      "scope": "module-name-checking",
      "phase": "post-validation",
      "state": "outcomes-recorded",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "implicit-name-registration", "value": "version-gated", "evaluator": "evidence"},
    {"key": "module-annotations-regression", "value": "present", "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation", "value": "passed", "evaluator": "evidence", "description": "An intended successful result, established only by actual passing current public checks."}
  ],
  "preserves": [
    {"key": "existing-magic-names", "value": "preserved", "evaluator": "evidence"},
    {"key": "pre-3.6-registry-behavior", "value": "preserved", "evaluator": "evidence"},
    {"key": "async-loop-version-selection", "value": "preserved", "evaluator": "evidence"},
    {"key": "ordinary-undefined-name-behavior", "value": "preserved", "evaluator": "evidence"},
    {"key": "existing-undefined-name-tests", "value": "preserved", "evaluator": "evidence"},
    {"key": "older-interpreter-test-compatibility", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-public-regressions",
      "instruction": "Execute the bound current new regression and surrounding undefined-name suite. Record commands, interpreter versions, exit statuses, assertion outcomes, and unavailable checks.",
      "evidence_refs": ["PyCQA/pyflakes:395:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "check-public-reproduction",
      "instruction": "Run the current checker on module code a: int = 2 followed by print(__annotations__) and check for absence of the reported __annotations__ undefined-name diagnostic on a supported interpreter.",
      "evidence_refs": ["PyCQA/pyflakes:395:body"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "check-version-preservation",
      "instruction": "Review or publicly probe both sides of the Python 3.6 registry gate and every changed Python 3.5 loop-type branch. Confirm existing names and ordinary undefined-name checks remain intact; distinguish review from execution and record unavailable environments as UNKNOWN.",
      "evidence_refs": ["PyCQA/pyflakes:395:fix", "PyCQA/pyflakes:395:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:395:repair:066ba4a93c10"],
  "evidence_refs": ["PyCQA/pyflakes:395:body", "PyCQA/pyflakes:395:fix", "PyCQA/pyflakes:395:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:4817630500584ee0981edde8",
  "validation_for": [
    "workflow:verified-history:4817630500584ee0981edde8:register",
    "workflow:verified-history:4817630500584ee0981edde8:regression"
  ],
  "read_set": ["role:implicit-module-name-model", "role:interpreter-version-policy", "role:undefined-name-regressions"],
  "write_set": []
}
```
