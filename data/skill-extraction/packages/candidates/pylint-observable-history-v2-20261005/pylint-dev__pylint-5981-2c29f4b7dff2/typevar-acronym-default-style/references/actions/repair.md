# Repair the uppercase run

Only edit with current PASS evidence for the default policy and single-uppercase limitation.

Add `+` to the uppercase-start class inside the existing mixed-case branch. Retain Unicode-aware classes, leading underscore allowance, the all-uppercase branch, optional `T`, the `Type` exclusion, and variance suffix grammar.

Add accepted `HVACModeT` and `_IPAddress` and rejected `IPAddressU` assertions. Retain existing negatives and variance diagnostics; update positions only as required. Align relevant documentation and release notes.

```arex-contract-v4
{
  "id": "workflow:verified-history:23d822a5fcdadb4939406c43:repair",
  "intent": "Allow acronym-leading mixed-case TypeVar names without widening unrelated boundaries.",
  "mechanism": "Quantify the uppercase-start class inside the existing mixed-case branch rather than replace the grammar.",
  "semantic_role": "repair-default-typevar-grammar",
  "owner_role": "default-typevar-rule",
  "operation": "Edit the bound default rule, add positive and negative regression assertions, retain adjacent expectations, and align naming examples and release notes.",
  "kind": "edit",
  "inputs": [
    {
      "name": "located-rule-context",
      "semantic_role": "typevar-grammar-context",
      "artifact_kind": "binding-and-probe-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "diagnosed",
      "state": "observed"
    }
  ],
  "outputs": [
    {
      "name": "edited-rule-context",
      "semantic_role": "typevar-grammar-repair",
      "artifact_kind": "patch-and-test-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "edited",
      "state": "unvalidated"
    }
  ],
  "preconditions": [
    {"key": "role:default-typevar-rule", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:typevar-regressions", "value": true, "evaluator": "file_exists"},
    {"key": "role:naming-documentation", "value": true, "evaluator": "file_exists"},
    {"key": "single-uppercase-default-limitation-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "default-policy-active", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "acronym-default-rule-supported", "value": true, "evaluator": "evidence"},
    {"key": "boundary-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "naming-examples-aligned", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-naming-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "variance-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "custom-pattern-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-minimal-grammar-diff",
      "instruction": "Review the public diff: uppercase-run repetition is the only grammar relaxation; HVACModeT and _IPAddress are positive assertions and IPAddressU is negative; adjacent expectations survive; examples describe only the narrow relaxation. Confirm custom-policy selection and variance code remain unchanged. Retain behavioral validation.",
      "evidence_refs": ["pylint-dev/pylint:5981:fix", "pylint-dev/pylint:5981:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:default-typevar-rule", "role:typevar-regressions", "role:naming-documentation"],
  "write_set": ["role:default-typevar-rule", "role:typevar-regressions", "role:naming-documentation"],
  "source_ids": ["pylint-dev/pylint:5981:repair:2c29f4b7dff2"],
  "evidence_refs": ["pylint-dev/pylint:5981:fix", "pylint-dev/pylint:5981:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:23d822a5fcdadb4939406c43"
}
```

Effects are required outcomes, not observed execution. [Validate](validate.md) remains mandatory for every plan executing this edit. The freshness key invalidated here is distinct from the behavior assurances retained across the plan.
