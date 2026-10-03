# Validate target and adjacent behavior

Bind and render current public commands for the regression and relevant test suite. Run the assignment-to-function regression and the motivating class-body reproduction. Compare the new diagnostic to the current analyzer's existing unused-redefinition message and location conventions.

Run the current equivalent of the changed test file and inspect adjacent cases:

- Previously recognized definition-to-definition collisions still report.
- Same-name assignment-to-definition produces the intended diagnostic.
- Different-name bindings do not become collisions.
- Assignment-to-assignment rebinding retains its previous behavior.
- Existing unusedness, scope, and special-name rules retain their current behavior.

These adjacent probes are current preservation obligations, not a claim that the supplied historical diff individually tested every item. Broader public tests are useful when available, but the supplied qualification proves only changed-test-file behavior.

```arex-contract-v4
{
  "id": "workflow:verified-history:ee79eebf2283561900232caf:validate",
  "intent": "Determine whether the candidate restores the target diagnostic without breaking adjacent behavior.",
  "mechanism": "Execute the public target regression, class-body reproduction, and current adjacent redefinition tests after the edit.",
  "semantic_role": "assignment-definition-repair-validation",
  "owner_role": "python-unused-redefinition-tests",
  "operation": "Bind public test commands, execute them, refresh observations, and record PASS, FAIL, or UNKNOWN.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate",
      "semantic_role": "assignment-definition-repair-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-repair",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation_report",
      "semantic_role": "assignment-definition-validation-report",
      "artifact_kind": "test-report",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:python-unused-redefinition-tests",
      "value": true,
      "evaluator": "file_exists"
    },
    {
      "key": "candidate-anchors-current",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "current-public-oracles-bound",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "post-edit-validation-result",
      "value": "recorded",
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "checkout-source",
      "value": "unchanged",
      "evaluator": "evidence"
    },
    {
      "key": "inherited-redefinition-rule",
      "value": "preserved",
      "evaluator": "evidence"
    },
    {
      "key": "ordinary-assignment-rebinding-policy",
      "value": "unchanged",
      "evaluator": "evidence"
    },
    {
      "key": "existing-unused-scope-policy",
      "value": "unchanged",
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "assignment-function-regression",
      "instruction": "Run the current public regression for x = 1 followed by def x(): pass and verify the existing unused-redefinition diagnostic.",
      "evidence_refs": [
        "PyCQA/pyflakes:760:regression"
      ],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "class-body-reproduction",
      "instruction": "Run the public class-body attribute-followed-by-method reproduction and compare it with repeated method definitions, recording diagnostic presence and current message/location conventions.",
      "evidence_refs": [
        "PyCQA/pyflakes:760:body"
      ],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "adjacent-redefinition-preservation",
      "instruction": "Run the current changed-test-file equivalent and public adjacent probes for definition redefinition, different names, assignment rebinding, and existing scope/unusedness/special-name rules. Record failures and unexecuted checks explicitly.",
      "evidence_refs": [
        "PyCQA/pyflakes:760:body",
        "PyCQA/pyflakes:760:fix",
        "PyCQA/pyflakes:760:regression"
      ],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:ee79eebf2283561900232caf:repair"
  ],
  "source_ids": [
    "PyCQA/pyflakes:760:repair:e9324649874a"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:760:body",
    "PyCQA/pyflakes:760:fix",
    "PyCQA/pyflakes:760:regression"
  ],
  "read_set": [
    "role:python-definition-binding-predicate",
    "role:python-unused-redefinition-tests"
  ],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:ee79eebf2283561900232caf"
}
```

A report must distinguish passed checks, failed checks, and checks not executed. The Workflow's required `current-public-validation = passed` effect is satisfied only by actual successful current execution, not by this contract or the later historical qualification attestation.
