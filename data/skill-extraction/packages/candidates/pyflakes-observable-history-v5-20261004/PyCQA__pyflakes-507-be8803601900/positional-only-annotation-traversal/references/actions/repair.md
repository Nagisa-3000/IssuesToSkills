# Include positional-only annotations

After applicability is confirmed, collect each positional-only parameter's name and annotation through the same accumulation path used for ordinary and keyword-only parameters. Respect the current runtime-support policy: the historical implementation guarded access with `PY38_PLUS`.

Add a focused regression in the current annotation test owner. Use an import referenced only by a positional-only parameter annotation and require no unused-import diagnostic. Isolate or skip the syntax on runtimes predating its support.

Keep the existing ordinary/keyword-only loop, defaults processing, and legacy branches intact unless current evidence requires a separate repair. Historical implementation paths are recorded in the episode, not assumed to be current bindings.

All effects below are expected edit outcomes, not observed test results. The validation Action is mandatory after this modifying Action.

```arex-contract-v4
{
  "id": "workflow:verified-history:b95b785d6a29c4b04e9050af:repair",
  "intent": "Extend annotation collection to positional-only parameters and add a focused regression.",
  "mechanism": "Append positional-only names and annotations before the existing ordinary/keyword-only collection, using an appropriate runtime guard.",
  "semantic_role": "repair-positional-only-collection",
  "owner_role": "function-signature-collector",
  "operation": "Edit the collector and its annotation regression tests using the confirmed current bindings.",
  "kind": "edit",
  "inputs": [
    {
      "name": "assessment",
      "semantic_role": "positional-only-omission-assessment",
      "artifact_kind": "inspection-record",
      "language": "Python",
      "scope": "current-checkout-function-signature-analysis",
      "phase": "diagnosis",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate",
      "semantic_role": "positional-only-annotation-repair",
      "artifact_kind": "checkout-change",
      "language": "Python",
      "scope": "current-checkout-function-signature-analysis",
      "phase": "repair",
      "state": "edited-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "positional-only-annotation-omission-confirmed",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "role:function-signature-collector",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:annotation-regression-tests",
      "value": true,
      "evaluator": "file_exists"
    },
    {
      "key": "supported-runtime-policy-established",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "positional-only-annotations-collected",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "focused-regression-present",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "ordinary-and-keyword-only-collection-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "supported-runtime-compatibility-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "existing-defaults-and-binding-behavior-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "review-collection-edit",
      "instruction": "Review the current diff for collection of positional-only names and annotations, preservation of existing argument/default handling, appropriate runtime gating, and a syntax-aware focused regression. This review does not substitute for executing validation.",
      "evidence_refs": [
        "PyCQA/pyflakes:507:fix",
        "PyCQA/pyflakes:507:regression"
      ],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": [
    "PyCQA/pyflakes:507:repair:be8803601900"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:507:fix",
    "PyCQA/pyflakes:507:regression"
  ],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:b95b785d6a29c4b04e9050af",
  "read_set": [
    "role:function-signature-collector",
    "role:python-runtime-compatibility-gate",
    "role:annotation-regression-tests"
  ],
  "write_set": [
    "role:function-signature-collector",
    "role:annotation-regression-tests"
  ],
  "invalidates": [
    "current-unused-import-diagnostic-result",
    "current-annotation-test-results",
    "current-runtime-compatibility-result"
  ]
}
```
