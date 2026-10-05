# Guard satisfaction and encode the boundary

At the bound current accounting owner, prevent the supplied-state update when the matched name is positional-only and a keyword collector exists. Historically the correction was a no-op `elif` before the normal supplied-state assignment. Adapt to current metadata rather than assuming historical attributes.

Add public assertions for the failing call and four legal controls. Gate positional-only syntax on runtime support as required by the current harness. Do not change required/default checking or the no-collector rejection branch.

```arex-contract-v4
{
  "id": "workflow:verified-history:33b6359d2826e0cbb3dcbe89:repair",
  "intent": "Correct positional satisfaction and add regression coverage.",
  "mechanism": "Skip supplied-state marking only for positional-only keyword names accepted by **kwargs.",
  "semantic_role": "accounting-and-regression-edit",
  "owner_role": "call-argument-accounting",
  "operation": "Edit the bound call-accounting owner and public argument-regression harness to implement the guarded correction and five-call diagnostic matrix.",
  "kind": "edit",
  "inputs": [
    {
      "name": "bound-accounting",
      "semantic_role": "call-accounting-repair-context",
      "artifact_kind": "code-and-test-bindings",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-repair",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "modified-accounting",
      "semantic_role": "call-accounting-repair-context",
      "artifact_kind": "code-and-test-bindings",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-repair",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "accounting-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-test-harness-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:call-argument-accounting", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:argument-regression-harness", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {
      "key": "captured-keyword-does-not-satisfy-positional-only",
      "value": true,
      "evaluator": "evidence",
      "description": "Intended correction; public validation must establish the behavior."
    },
    {"key": "regression-matrix-authored", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {
      "key": "adjacent-binding-behavior-preserved",
      "value": true,
      "evaluator": "evidence",
      "description": "Preserve ordinary keyword binding, positional supply, mixed signatures, defaults, and existing no-collector rejection."
    }
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "inspect-guard-and-assertions",
      "instruction": "Review the public diff: satisfaction is skipped only with both positional-only membership and keyword collection. Verify the target assertion and all four legal controls, and that the no-collector branch is unchanged.",
      "evidence_refs": ["pylint-dev/pylint:8559:fix", "pylint-dev/pylint:8559:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:call-argument-accounting", "role:argument-regression-harness"],
  "write_set": ["role:call-argument-accounting", "role:argument-regression-harness"],
  "source_ids": ["pylint-dev/pylint:8559:repair:2db55f6a4896"],
  "evidence_refs": ["pylint-dev/pylint:8559:fix", "pylint-dev/pylint:8559:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:33b6359d2826e0cbb3dcbe89"
}
```

Effects describe requested outcomes, not observed execution. Retain [validate](validate.md) for both implementation and regression modifications. Empty command arrays are placeholders for public current bindings.
