# Validate the repair and preserved behavior

Run the current regression against the patched checkout and record actual results. Where possible, establish the regression's fail-before/pass-after contrast using the pinned public base without overwriting the patch.

Run the relevant annotation test suite and public adjacent probes. Include genuine value-defining redefinitions, annotation expression analysis, and annotation-plus-assignment behavior. Those adjacent probes are current preservation checks, not additional historical test assertions.

The historical evidence provides the newly added no-diagnostics assertion. The contemporary attestation covers changed test files only. Neither authorizes claiming whole-project success.

```arex-contract-v4
{
  "id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:validate",
  "intent": "Verify the annotation-only repair and detect adjacent regressions.",
  "mechanism": "Execute the imported-name annotation regression and relevant current annotation and redefinition checks.",
  "semantic_role": "annotation-repair-validation",
  "owner_role": "annotation-regression-tests",
  "operation": "Run public current tests and record target and preservation results.",
  "kind": "validate",
  "inputs": [
    {
      "name": "patched-checkout",
      "semantic_role": "annotation-redefinition-checkout",
      "artifact_kind": "checkout-snapshot",
      "language": "python",
      "scope": "annotation-binding-and-regression",
      "phase": "post-repair",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-report",
      "semantic_role": "annotation-repair-results",
      "artifact_kind": "test-report",
      "language": "python",
      "scope": "annotation-binding-and-regression",
      "phase": "post-repair",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "annotation-import-regression-added",
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
      "key": "annotation-validation-results",
      "value": "recorded",
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "patched-source-content",
      "value": "unchanged",
      "evaluator": "evidence"
    },
    {
      "key": "value-defining-redefinition-analysis",
      "value": "preserved",
      "evaluator": "evidence"
    },
    {
      "key": "annotation-expression-analysis",
      "value": "preserved",
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "annotation-import-regression",
      "instruction": "Execute the public current equivalent of the historical no-diagnostics annotation-import regression; record interpreter compatibility, diagnostics, and exit status.",
      "evidence_refs": ["PyCQA/pyflakes:617:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-annotation-behavior",
      "instruction": "Run relevant existing annotation tests and public checks for true value-defining redefinitions and annotation-plus-assignment. Record results and do not claim preservation without current evidence.",
      "evidence_refs": ["PyCQA/pyflakes:617:fix", "PyCQA/pyflakes:617:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:617:repair:3de8e6120291"],
  "evidence_refs": ["PyCQA/pyflakes:617:fix", "PyCQA/pyflakes:617:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7",
  "read_set": ["role:annotation-binding-analysis", "role:redefinition-analysis", "role:annotation-regression-tests"],
  "write_set": [],
  "validation_for": ["workflow:verified-history:f7b7dad5578cfb8d7454d8e7:repair"]
}
```
