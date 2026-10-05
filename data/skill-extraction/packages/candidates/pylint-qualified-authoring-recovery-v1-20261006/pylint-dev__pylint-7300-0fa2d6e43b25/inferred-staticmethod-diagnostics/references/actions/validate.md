# Validate public diagnostic behavior

Bind commands to the current public harness and render those bindings before execution. Do not use the later qualification command as a current command merely because it appears in source audit data.

```arex-contract-v4
{
  "id": "workflow:verified-history:d64e04a769c8484780ab2708:validate",
  "intent": "Observe targeted correctness and preserved adjacent method diagnostics.",
  "mechanism": "Run targeted fixtures and adjacent public method-check tests, comparing exact diagnostics with retained expectations.",
  "semantic_role": "diagnostic-regression-validation",
  "owner_role": "method-argument-regressions",
  "operation": "Run the bound public fixture suite and adjacent argument/decorator checks; inspect diagnostic identities and locations; record command, exit status, output, and current code anchors. Do not edit tracked files.",
  "kind": "validate",
  "inputs": [
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
  "outputs": [
    {
      "name": "public-validation-record",
      "semantic_role": "static-method-diagnostic-validation",
      "artifact_kind": "public-test-observation-record",
      "language": "python",
      "scope": "method-argument-checking",
      "phase": "post-validation",
      "state": "observed-result"
    }
  ],
  "preconditions": [
    {"key": "inferred-staticmethod-exemption-installed", "value": true, "evaluator": "evidence"},
    {"key": "target-regressions-installed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-method-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "direct-staticmethod-handling-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-method-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "targeted-diagnostic-regressions",
      "instruction": "Run the current bound public functional harness. Require no receiver/argument diagnostics on direct, aliased and inferred-return staticmethod fixtures, retained diagnostics on malformed ordinary methods, and passing adjacent direct-staticmethod, classmethod and argument checks.",
      "evidence_refs": ["pylint-dev/pylint:7300:regression", "pylint-dev/pylint:7300:fix"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:d64e04a769c8484780ab2708:repair"],
  "read_set": ["role:method-argument-checker", "role:method-argument-regressions"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:7300:repair:0fa2d6e43b25"],
  "evidence_refs": ["pylint-dev/pylint:7300:regression", "pylint-dev/pylint:7300:fix"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:d64e04a769c8484780ab2708"
}
```

A completed run may establish that validation was observed while its checks still fail. Only passing target and preservation checks support acceptance. Unknown or failed checks require investigation or rejection, not a success claim.
