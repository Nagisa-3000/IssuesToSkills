# Add the narrow exemption and regression

Bind the current AST call class and safe-inference API before implementing a predicate equivalent to:

```python
def released_by_recognized_parent(node):
    if not isinstance(node.parent, Call):
        return False
    func = safe_infer(node.parent.func)
    if not func:
        return False
    return func.qname() in {
        "contextlib._BaseExitStack.enter_context",
        "contextlib.ExitStack.enter_context",
    }
```

`Call` and `safe_infer` here are semantic placeholders, not imports to paste blindly. Preserve existing resource-candidate detection and existing context-manager exemptions. Emit the warning only when the candidate has neither existing exemption nor the supported inferred-registration exemption.

Add a public no-warning fixture with `open(...)` directly inside `stack.enter_context(...)` under a managed `ExitStack`. Do not broaden to arbitrary spelling matches, ancestors, custom wrappers, or asynchronous APIs. The implementation does not prove every ExitStack instance is closed.

The declared effects are intended effects pending current review and validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:556cefd05a1df4981665346d:repair",
  "intent": "Correct the directly registered resource false positive without suppressing unrelated warnings.",
  "mechanism": "Guard on an immediate call parent, safely infer its callable, and recognize an explicit standard-library qualified-name allowlist.",
  "semantic_role": "implement-cleanup-exemption",
  "owner_role": "resource-diagnostic-owner",
  "operation": "Edit the bound resource-diagnostic gate and helper; add a direct managed-registration no-warning fixture at the bound public diagnostic-test owner.",
  "kind": "edit",
  "inputs": [
    {
      "name": "binding",
      "semantic_role": "cleanup-diagnostic-binding",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "pre-edit",
      "state": "confirmed"
    }
  ],
  "outputs": [
    {
      "name": "candidate",
      "semantic_role": "cleanup-diagnostic-candidate",
      "artifact_kind": "source-and-test-change",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "preconditions": [
    {"key": "direct-registration-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:resource-diagnostic-owner", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:resource-diagnostic-test-owner", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "recognized-direct-registration-exempt", "value": true, "evaluator": "evidence"},
    {"key": "no-warning-regression-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-narrow-exemption",
      "instruction": "Review the public diff for immediate-call and failed-inference fallbacks, exact supported callable identities, retained candidate and context-manager checks, and a no-warning direct registration fixture. Do not treat the diff review as executed test success.",
      "evidence_refs": ["pylint-dev/pylint:4654:fix", "pylint-dev/pylint:4654:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4654:repair:c2d03c6b3881"],
  "evidence_refs": ["pylint-dev/pylint:4654:fix", "pylint-dev/pylint:4654:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:556cefd05a1df4981665346d",
  "read_set": ["role:resource-diagnostic-owner", "role:resource-diagnostic-test-owner"],
  "write_set": ["role:resource-diagnostic-owner", "role:resource-diagnostic-test-owner"],
  "invalidates": ["public-validation-observed"]
}
```
