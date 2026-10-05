# Validate target and adjacent behavior

Bind and render current public reproduction and fixture-runner commands. Execute them after all retained edits. Inspect actual outcomes, not matching predicate names.

Require no crash or false warning for the copy case, retained existing list/set/dictionary diagnostics, and the unchanged inference guard. Where feasible, an isolated original-base control with the added regression can confirm that it detects the original failure. Later qualification commands are not automatic bindings.

```arex-contract-v4
{
  "id": "workflow:verified-history:bc4129e7b226dfae4c87ca01:validate",
  "intent": "Observe target correctness and preserved adjacent diagnostics after edits.",
  "mechanism": "Execute public reproduction and iteration fixtures and review semantic preservation.",
  "semantic_role": "repair-validation",
  "owner_role": "iteration-test-runner-owner",
  "operation": "Run bound current public checks and record exit status, crash absence, copy-case diagnostics, retained expectations, and condition review without modifying tracked implementation or fixtures.",
  "kind": "validate",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "role:iteration-test-runner-owner", "value": true, "evaluator": "file_exists"},
    {"key": "iterable-identifier-selection", "value": "Attribute.attrname-or-Name.name", "evaluator": "evidence"},
    {"key": "attribute-copy-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": "PASS", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "inference-equality-guard-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-iteration-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "separate-copy-not-diagnosed-as-iterated-set", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "attribute-copy-analysis",
      "instruction": "Execute the bound public class-attribute-set reproduction. Require no Attribute.name exception or wrapped checker crash and no modified-iterating-set diagnostic for removal from the separate constructed copy.",
      "evidence_refs": ["pylint-dev/pylint:7528:body", "pylint-dev/pylint:7528:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "iteration-fixture-preservation",
      "instruction": "Execute the bound public iteration fixture runner. Require retained list, set, and dictionary diagnostics, no target warning for the added copy case, and only explained location changes. Review the unchanged inferred-object equality guard.",
      "evidence_refs": ["pylint-dev/pylint:7528:fix", "pylint-dev/pylint:7528:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:bc4129e7b226dfae4c87ca01:repair",
    "workflow:verified-history:bc4129e7b226dfae4c87ca01:regression"
  ],
  "read_set": ["role:iteration-condition-owner", "role:iteration-regression-owner", "role:iteration-test-runner-owner"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:7528:repair:aca8dd546e6e"],
  "evidence_refs": ["pylint-dev/pylint:7528:body", "pylint-dev/pylint:7528:fix", "pylint-dev/pylint:7528:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:bc4129e7b226dfae4c87ca01"
}
```

PASS is a required successful effect, not an existing result. Failed checks record FAIL; unavailable checks record UNKNOWN. Neither permits asserting successful validation.
