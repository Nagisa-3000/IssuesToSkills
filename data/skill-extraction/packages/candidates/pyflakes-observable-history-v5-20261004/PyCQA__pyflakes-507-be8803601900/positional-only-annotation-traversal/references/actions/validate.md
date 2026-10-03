# Validate annotation traversal

Bind commands to the current public checkout and render those commands before execution. The empty command arrays in this card are unbound source oracles, not runnable commands.

Run the focused regression on Python 3.8 or later, or a current runtime with equivalent positional-only AST support. Run the original mixed-parameter reproduction. Check that neither imported annotation name receives a false unused-import diagnostic.

Run relevant adjacent annotation tests and inspect the preservation of defaults and parameter binding. Review runtime guards and syntax-specific test isolation; execute older-runtime checks where the current support policy requires them and the environment permits. Record unavailable checks as UNKNOWN.

The historical evidence supplies a focused assertion and a local implementation change. It does not prove whole-project or cross-project safety. Broader current testing is a verification obligation, not an additional historical claim.

```arex-contract-v4
{
  "id": "workflow:verified-history:b95b785d6a29c4b04e9050af:validate",
  "intent": "Verify the target correction and preservation requirements after the edit.",
  "mechanism": "Execute public reproductions and the focused and adjacent tests, and review compatibility-sensitive collection logic.",
  "semantic_role": "verify-positional-only-annotation-repair",
  "owner_role": "annotation-regression-tests",
  "operation": "Run bound public checks and record observed results against the modified checkout.",
  "kind": "validate",
  "inputs": [
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
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "positional-only-repair-verification",
      "artifact_kind": "validation-report",
      "language": "Python",
      "scope": "current-checkout-function-signature-analysis",
      "phase": "validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "candidate-edit-present",
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
      "key": "validation-results-recorded",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "candidate-source-unmodified-by-validation",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "target-reproduction",
      "instruction": "Execute the public mixed positional-only/keyword-only reproduction against the current analyzer on a compatible runtime. Require no unused-import diagnostic for either annotation-only import.",
      "evidence_refs": [
        "PyCQA/pyflakes:507:body",
        "PyCQA/pyflakes:507:fix"
      ],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "focused-and-adjacent-tests",
      "instruction": "Execute the current focused positional-only annotation regression and relevant adjacent annotation tests. Require the focused no-diagnostic assertion to pass; check ordinary and keyword-only annotations, defaults and binding preservation, and supported-runtime guards or test skips. Report the actual scope and all unexecuted checks.",
      "evidence_refs": [
        "PyCQA/pyflakes:507:regression",
        "PyCQA/pyflakes:507:fix"
      ],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": [
    "PyCQA/pyflakes:507:repair:be8803601900"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:507:body",
    "PyCQA/pyflakes:507:fix",
    "PyCQA/pyflakes:507:regression"
  ],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:b95b785d6a29c4b04e9050af",
  "read_set": [
    "role:function-signature-collector",
    "role:python-runtime-compatibility-gate",
    "role:annotation-regression-tests",
    "role:public-analyzer-entry-point"
  ],
  "write_set": [],
  "validation_for": [
    "workflow:verified-history:b95b785d6a29c4b04e9050af:repair"
  ]
}
```
