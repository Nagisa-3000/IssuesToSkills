# Repair the symbolic character class

Consume a confirmed diagnosis. Add ASCII `0-9` while retaining letters, hyphens, underscores, minimum length, precedence, and unrelated rules. Do not replace the class with a wildcard or change registration.

Add a public regression asserting the full original identifier and disable action. Include a nonempty-result guard as a current safety check; the historical regression only asserted values inside a loop.

Effects below are expected patch properties, not observed behavioral success. Retain the [validation Action](validate.md) after this modification.

```arex-contract-v4
{
  "id": "workflow:verified-history:a4e1808f638c9a903d335608:repair",
  "intent": "Restore full digit-bearing symbolic identifiers with a narrow lexer and test edit.",
  "mechanism": "Add ASCII digits to the symbolic identifier regex character class.",
  "semantic_role": "repair-symbolic-token-class",
  "owner_role": "directive-lexer",
  "operation": "Edit the bound symbolic token class to include ASCII digits without changing existing characters, minimum length, ordering or unrelated rules; add a complete-output disable regression.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosis",
      "semantic_role": "digit-exclusion-diagnosis",
      "artifact_kind": "code-and-probe-evidence",
      "language": "Python",
      "scope": "current-directive-parser",
      "phase": "pre-edit",
      "state": "confirmed"
    }
  ],
  "outputs": [
    {
      "name": "parser-patch",
      "semantic_role": "digit-inclusive-parser-patch",
      "artifact_kind": "source-and-test-diff",
      "language": "Python",
      "scope": "current-directive-parser",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "preconditions": [
    {"key": "lexical-digit-exclusion-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "digits-valid-in-symbolic-identifiers", "value": true, "evaluator": "evidence"},
    {"key": "role:directive-lexer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:directive-parser-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "symbolic-token-class-includes-ascii-digits", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertion-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-directive-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-token-grammar-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-narrow-diff",
      "instruction": "Review the current source/test diff. Verify ASCII digit inclusion, retention of existing characters, minimum length and token order, unchanged keyword/assignment/numeric rules, and regression assertions for complete disable output.",
      "evidence_refs": ["pylint-dev/pylint:3666:fix", "pylint-dev/pylint:3666:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:directive-lexer", "role:directive-parser-tests"],
  "write_set": ["role:directive-lexer", "role:directive-parser-tests"],
  "source_ids": ["pylint-dev/pylint:3666:repair:fe0a7f795343"],
  "evidence_refs": ["pylint-dev/pylint:3666:fix", "pylint-dev/pylint:3666:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:a4e1808f638c9a903d335608"
}
```
