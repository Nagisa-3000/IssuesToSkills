# Validate behavior and preservation

Bind current public test commands. Check diagnostic identities and affected names, not exit status alone. Variance diagnostics are distinct from `invalid-name`; use consistent variance settings for names such as `_T_co`.

Do not rewrite source or expectations to conceal failures. Empty command arrays require current binding before execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:23d822a5fcdadb4939406c43:validate",
  "intent": "Observe the repaired default naming rule and preservation of adjacent behavior.",
  "mechanism": "Run public positive and negative checks after the edit and compare adjacent policies against current baseline observations.",
  "semantic_role": "validate-default-typevar-repair",
  "owner_role": "typevar-regressions",
  "operation": "Execute current bound public tests and diagnostic probes, review documentation consistency, and record statuses, diagnostic comparisons, and scope without modifying source or expectations.",
  "kind": "validate",
  "inputs": [
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
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "typevar-grammar-validation",
      "artifact_kind": "public-check-results",
      "language": "python",
      "scope": "current-checkout",
      "phase": "validated",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "boundary-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "repair-checks-pass", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-naming-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "variance-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "custom-pattern-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-default-boundaries",
      "instruction": "Run current default-style tests and public probes. Require no invalid-name for HVACModeT, IPAddressT, and _IPAddress; retain rejection of IPAddressU, DeviceType, CALLABLE_T, DICT_T, ENUM_T, and camelCase negatives. Retain accepted T, _CallableT, _T_co, AnyStr, and DeviceTypeT with consistent variance settings. Review underscore and suffix boundaries.",
      "evidence_refs": ["pylint-dev/pylint:5981:body", "pylint-dev/pylint:5981:fix", "pylint-dev/pylint:5981:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "verify-adjacent-policy",
      "instruction": "Check current custom-pattern selection and incorrect-variance behavior against the observed baseline; review unchanged selection and variance code and documentation consistency. Record unavailable checks as UNKNOWN rather than success.",
      "evidence_refs": ["pylint-dev/pylint:5981:fix", "pylint-dev/pylint:5981:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:23d822a5fcdadb4939406c43:repair"],
  "read_set": ["role:default-typevar-rule", "role:typevar-regressions", "role:naming-documentation"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5981:repair:2c29f4b7dff2"],
  "evidence_refs": ["pylint-dev/pylint:5981:fix", "pylint-dev/pylint:5981:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:23d822a5fcdadb4939406c43"
}
```

A validation record may contain failures. Only actual passing observations establish `repair-checks-pass`; failures or UNKNOWN preservation checks block success.
