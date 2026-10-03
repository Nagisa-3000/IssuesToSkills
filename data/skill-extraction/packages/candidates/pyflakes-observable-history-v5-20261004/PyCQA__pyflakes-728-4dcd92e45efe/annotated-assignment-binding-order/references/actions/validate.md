# Validate the target diagnostic and adjacent behavior

Bind and run the current public regression test and the relevant annotation test suite. Re-run the public ordinary/annotated self-reference comparison.

Review and test preservation of annotation processing and existing initializer branches using the current suite. A passing narrow regression does not by itself establish those preservation claims. Report test scope, commands, exit statuses, diagnostics, and unknown coverage explicitly.

Where practical, run the new regression against the pinned original base to establish that it detects the reported defect. This is a current validation procedure, not a claim of supplied historical execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:88cc33218756cccdf2ac071b:validate",
  "intent": "Check that the repair restores the undefined-name diagnostic without breaking adjacent annotation behavior.",
  "mechanism": "Execute the focused regression and adjacent public annotation tests, compare public reproductions, and review preserved handler branches.",
  "semantic_role": "verify-binding-order-repair",
  "owner_role": "annotation-regression-suite",
  "operation": "Run current bound public checks after both modifications and record the observed result and coverage limits.",
  "kind": "validate",
  "inputs": [
    {
      "name": "corrected-handler",
      "semantic_role": "annotated-assignment-handler",
      "artifact_kind": "source-code",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "target-visit-delayed"
    },
    {
      "name": "extended-regression-suite",
      "semantic_role": "annotation-regression-suite",
      "artifact_kind": "test-code",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "self-reference-assertion-added"
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "binding-order-validation",
      "artifact_kind": "validation-report",
      "language": "text",
      "scope": "current-checkout",
      "phase": "validation",
      "state": "observations-recorded"
    }
  ],
  "preconditions": [
    {
      "key": "initializer-analyzed-before-new-target-binding",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "undefined-self-reference-regression-present",
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
      "key": "target-and-adjacent-checks-pass",
      "value": true,
      "evaluator": "evidence",
      "description": "Expected acceptance effect, established only by recorded successful current execution."
    }
  ],
  "preserves": [
    {
      "key": "annotation-processing-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "initializer-special-branches-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "adjacent-annotation-behavior-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "self-reference-diagnostic",
      "instruction": "Execute current public checks showing that both x = x and x: int = x report an undefined x in fresh scopes. Record diagnostic identity and location where the public harness exposes them.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:body",
        "PyCQA/pyflakes:728:regression"
      ],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "annotation-regressions",
      "instruction": "Execute the new regression assertion and the relevant current public annotation suite. Review preserved annotation and initializer branches; record any uncovered preservation claim as UNKNOWN and do not claim full acceptance.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:fix",
        "PyCQA/pyflakes:728:regression"
      ],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:88cc33218756cccdf2ac071b:reorder",
    "workflow:verified-history:88cc33218756cccdf2ac071b:regression"
  ],
  "read_set": [
    "role:annotated-assignment-handler",
    "role:annotation-regression-suite"
  ],
  "write_set": [],
  "source_ids": [
    "PyCQA/pyflakes:728:repair:4dcd92e45efe"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:728:body",
    "PyCQA/pyflakes:728:fix",
    "PyCQA/pyflakes:728:regression"
  ],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:88cc33218756cccdf2ac071b"
}
```
