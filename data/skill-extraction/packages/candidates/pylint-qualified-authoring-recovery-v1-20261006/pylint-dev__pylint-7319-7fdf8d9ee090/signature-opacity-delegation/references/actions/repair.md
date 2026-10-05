# Install the narrow guard and regression

At the current diagnostic owner, extend the existing early-return condition with the conjunction of unavailable inherited arguments and an override argument-name list different from `["self"]`.

The historical expression was:

```python
or (meth_node.args.args is None and function.argnames() != ["self"])
```

Use it literally only if current probes establish the same representation. Retain existing parameter/default comparisons. Do not suppress all builtin delegation diagnostics.

At the regression owner, add the default-message exception constructor without an expected useless-delegation diagnostic. Review the diff for unrelated changes. Retain the [validate Action](validate.md) after editing.

```arex-contract-v4
{
  "id": "workflow:verified-history:79391484ce4048a1c8e1217a:repair",
  "intent": "Repair conservative handling of uninspectable inherited signatures.",
  "mechanism": "Add the unavailable-arguments/non-self-only guard and the default-message exception regression.",
  "semantic_role": "signature-opacity-repair",
  "owner_role": "delegation-diagnostic-owner",
  "operation": "Edit the current diagnostic early-return condition and public regression fixture while retaining existing comparisons and expectations.",
  "kind": "edit",
  "inputs": [
    {
      "name": "signature-analysis",
      "semantic_role": "opaque-parent-delegation-analysis",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "delegation-diagnostic",
      "phase": "pre-edit",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate-repair",
      "semantic_role": "opaque-parent-delegation-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "delegation-diagnostic",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:delegation-diagnostic-owner", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:delegation-regression-owner", "value": true, "evaluator": "file_exists"},
    {"key": "opaque-parent-nonself-override-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "target-false-positive-observed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "opaque-signature-guard-installed", "value": true, "evaluator": "evidence"},
    {"key": "default-message-regression-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "inspectable-signature-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "self-only-guard-boundary-preserved", "value": true, "evaluator": "evidence"},
    {"key": "fixture-interface-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-narrow-guard",
      "instruction": "Review the public diff for the conjunction of unavailable inherited arguments and non-self-only override. Confirm existing comparisons remain, the fixture expects no warning, and explicit post-edit validation is retained.",
      "evidence_refs": ["pylint-dev/pylint:7319:fix", "pylint-dev/pylint:7319:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:7319:repair:7fdf8d9ee090"],
  "evidence_refs": ["pylint-dev/pylint:7319:fix", "pylint-dev/pylint:7319:regression"],
  "read_set": ["role:delegation-diagnostic-owner", "role:delegation-regression-owner"],
  "write_set": ["role:delegation-diagnostic-owner", "role:delegation-regression-owner"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:79391484ce4048a1c8e1217a"
}
```

Effects describe intended edit outcomes, not observed repair success. Any subsequent edit requires fresh validation.
