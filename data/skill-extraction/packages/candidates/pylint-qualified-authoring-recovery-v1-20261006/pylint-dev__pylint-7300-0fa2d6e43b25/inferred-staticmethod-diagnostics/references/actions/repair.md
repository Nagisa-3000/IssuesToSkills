# Repair the checker and targeted assertions

Apply a narrow qualified-identity exemption. Keep existing direct staticmethod behavior first. Add fixtures for direct and aliased zero-argument static methods and a decorator returning a staticmethod for a multi-argument function. Retain ordinary invalid instance-method expectations. Adapt expected line locations to current fixtures rather than copying historical offsets.

```arex-contract-v4
{
  "id": "workflow:verified-history:d64e04a769c8484780ab2708:repair",
  "intent": "Prevent false missing-receiver and missing-argument diagnostics for inferred static methods.",
  "mechanism": "An inferred builtins.staticmethod decorator identity short-circuits ordinary method-argument checks.",
  "semantic_role": "inferred-staticmethod-repair",
  "owner_role": "method-argument-checker",
  "operation": "In the current diagnostic decision chain, add an inferred builtins.staticmethod return branch after direct staticmethod handling and before ordinary argument checks. Update public method-argument fixtures and expected diagnostics with targeted staticmethod examples and retained instance-method controls.",
  "kind": "edit",
  "inputs": [
    {
      "name": "bound-diagnostic-context",
      "semantic_role": "static-method-diagnostic-context",
      "artifact_kind": "public-code-and-observation-record",
      "language": "python",
      "scope": "method-argument-checking",
      "phase": "pre-repair",
      "state": "identity-and-boundary-established"
    }
  ],
  "outputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "static-method-diagnostic-candidate",
      "artifact_kind": "code-and-regression-diff",
      "language": "python",
      "scope": "method-argument-checking",
      "phase": "post-repair",
      "state": "awaiting-public-validation"
    }
  ],
  "preconditions": [
    {"key": "role:method-argument-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:decorator-identity-provider", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:method-argument-regressions", "value": true, "evaluator": "file_exists"},
    {"key": "inferred-staticmethod-identity-established", "value": true, "evaluator": "evidence"},
    {"key": "target-false-diagnostic-observed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "inferred-staticmethod-exemption-installed", "value": true, "evaluator": "evidence"},
    {"key": "target-regressions-installed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-method-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "direct-staticmethod-handling-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-method-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "decorator-inference-needs-new-semantics", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-narrow-exemption",
      "instruction": "Review the current diff: require inferred qualified identity, placement after the existing direct branch and before ordinary method-argument checks, no diagnostic disabling, no unrelated bookkeeping changes, and targeted regression controls.",
      "evidence_refs": ["pylint-dev/pylint:7300:fix", "pylint-dev/pylint:7300:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:method-argument-checker", "role:decorator-identity-provider", "role:method-argument-regressions"],
  "write_set": ["role:method-argument-checker", "role:method-argument-regressions"],
  "source_ids": ["pylint-dev/pylint:7300:repair:0fa2d6e43b25"],
  "evidence_refs": ["pylint-dev/pylint:7300:fix", "pylint-dev/pylint:7300:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:d64e04a769c8484780ab2708"
}
```

Effects are intended outcomes of the edit, not observed correctness. This modifying Action must retain [validation](validate.md).
