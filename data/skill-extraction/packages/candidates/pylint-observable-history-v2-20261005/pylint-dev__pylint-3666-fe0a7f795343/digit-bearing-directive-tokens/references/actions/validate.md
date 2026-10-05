# Validate complete output and neighboring behavior

Bind current public commands. Execute the digit-bearing regression and exact-output probe, then adjacent parser tests. Require nonempty output, action `disable`, and the full original message list.

Check ordinary symbolic names, existing hyphen/underscore handling, multiple messages/directives, skip-file, missing assignment/message/keyword, unknown keywords, and unsupported assignments against current public expectations. Review token ordering and numeric-message rules. This current preservation obligation does not claim dedicated historical tests for every item.

This Action does not edit source or tests. Record failures and UNKNOWN checks honestly; emit success effects only after successful observation.

```arex-contract-v4
{
  "id": "workflow:verified-history:a4e1808f638c9a903d335608:validate",
  "intent": "Observe complete digit-bearing output and preserved adjacent parsing.",
  "mechanism": "Execute exact-output public probes and neighboring parser tests against the modified lexer.",
  "semantic_role": "validate-symbolic-token-repair",
  "owner_role": "directive-parser-tests",
  "operation": "Run currently bound public target and adjacent checks, inspect exact output and diff, and record commands, exit status, outcomes and current anchors without editing source/tests.",
  "kind": "validate",
  "inputs": [
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
  "outputs": [
    {
      "name": "validation-report",
      "semantic_role": "directive-parser-validation",
      "artifact_kind": "public-test-and-probe-results",
      "language": "Python",
      "scope": "current-directive-parser",
      "phase": "post-validation",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "symbolic-token-class-includes-ascii-digits", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertion-present", "value": true, "evaluator": "evidence"},
    {"key": "role:directive-parser-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "digit-bearing-symbol-preserved", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-directive-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-token-grammar-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "exact-disable-output",
      "instruction": "Run a current public digit-bearing disable fixture. Require nonempty parsed output, action disable, and a message list containing the complete original identifier without truncation.",
      "evidence_refs": ["pylint-dev/pylint:3666:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "adjacent-parser-tests",
      "instruction": "Run currently bound public directive-parser tests and inspect every failure. Check neighboring behavior and unchanged unrelated token rules. Record argv, exit status, outcomes and anchors; do not infer whole-project correctness.",
      "evidence_refs": ["pylint-dev/pylint:3666:fix", "pylint-dev/pylint:3666:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:a4e1808f638c9a903d335608:repair"],
  "read_set": ["role:directive-lexer", "role:directive-parser-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:3666:repair:fe0a7f795343"],
  "evidence_refs": ["pylint-dev/pylint:3666:fix", "pylint-dev/pylint:3666:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:a4e1808f638c9a903d335608"
}
```
