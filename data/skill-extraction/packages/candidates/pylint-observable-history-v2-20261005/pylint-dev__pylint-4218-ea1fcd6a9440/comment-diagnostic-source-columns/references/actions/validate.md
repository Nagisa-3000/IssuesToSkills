# Validate columns and adjacent behavior

This Action is retained after the repair, including its expectation edits. Locate and bind the current public runner; do not copy an old command into an unrelated checkout.

Derive expected columns directly from the source token positions. For an ASCII reproduction using the report's layout, hash start columns are 0, 10, 4, and 8, so the supported rule yields columns 1, 11, 5, and 9. These derived checks are newly authored test definitions, not historical output.

Include spaced and unspaced hashes, case variation, configured notes or regexes where the current suite supports them, and unchanged diagnostics. Failure to execute leaves validation UNKNOWN, not PASS.

```arex-contract-v4
{
  "id": "workflow:verified-history:e90ff4df6c32dee9a7842f73:validate",
  "intent": "Obtain fresh public evidence that the coordinate repair works without changing adjacent diagnostic behavior.",
  "mechanism": "Check source-derived column expectations through the public diagnostic interface and run the bound regression and adjacent tests.",
  "semantic_role": "source-column-validation",
  "owner_role": "comment-note-regression-suite",
  "operation": "Bind and render current public oracle commands. Execute the reproduction and relevant regression tests, compare columns with token source start plus one, compare warning counts, lines, text, and recognition behavior with the baseline, and record outputs, exit codes, and PASS/FAIL/UNKNOWN checks. Do not rewrite expectations during validation.",
  "kind": "validate",
  "inputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "comment-column-candidate",
      "artifact_kind": "checkout-change-record",
      "language": "Python",
      "scope": "current-checkout-comment-note-diagnostics",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "comment-column-validation-result",
      "artifact_kind": "public-test-record",
      "language": "Python",
      "scope": "current-checkout-comment-note-diagnostics",
      "phase": "post-validation",
      "state": "checks-observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "comment-column-rule", "value": "token-source-start-plus-one", "evaluator": "evidence"},
    {"key": "public-column-expectations", "value": "source-anchored", "evaluator": "evidence"},
    {"key": "role:comment-note-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "note-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-content-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-public-source-columns",
      "instruction": "Execute a bound current public reproduction with standalone, inline, and nested indented comments. Verify columns equal hash source start plus one, including spaced and unspaced comments, and verify warning labels, lines, counts, and text.",
      "evidence_refs": ["pylint-dev/pylint:4218:body", "pylint-dev/pylint:4218:fix", "pylint-dev/pylint:4218:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-regression-and-adjacent-behavior",
      "instruction": "Run the bound current public regression runner for comment-note fixtures and available adjacent checks. Verify case and configurable note matching remain unchanged, inspect results rather than auto-updating expectations, and record any untested preservation claim as UNKNOWN.",
      "evidence_refs": ["pylint-dev/pylint:4218:fix", "pylint-dev/pylint:4218:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:e90ff4df6c32dee9a7842f73:repair"],
  "source_ids": ["pylint-dev/pylint:4218:repair:ea1fcd6a9440"],
  "evidence_refs": ["pylint-dev/pylint:4218:body", "pylint-dev/pylint:4218:fix", "pylint-dev/pylint:4218:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:e90ff4df6c32dee9a7842f73",
  "read_set": ["role:comment-note-emitter", "role:comment-note-regression-suite"],
  "write_set": []
}
```
