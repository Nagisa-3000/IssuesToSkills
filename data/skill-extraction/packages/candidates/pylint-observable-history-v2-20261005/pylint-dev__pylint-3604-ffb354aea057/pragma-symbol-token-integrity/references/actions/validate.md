# Observe exact token integrity and adjacent grammar

Bind current public test and reproduction commands. Render and execute them after editing; record actual argv, exit status, exact output, and coverage. Do not edit source during this Action.

Require action `disable` and exactly one complete underscore-containing message. Check ordinary and hyphenated names, numeric IDs, multiple messages, and existing missing/invalid assignment, keyword, and message cases using current documented expectations.

If a public registered-message fixture is available, check actual symbolic disabling too. Without it, explicitly report parser-only validation. Environment failures are UNKNOWN; failed assertions are FAIL. Emit success effects only after passing observed checks, not merely after command invocation.

```arex-contract-v4
{
  "id": "workflow:verified-history:69a4d4302a9cbe21cf4cdae8:validate",
  "intent": "Observe corrected token integrity and preserved adjacent grammar.",
  "mechanism": "Execute exact-output regression and neighboring parser checks in the current checkout.",
  "semantic_role": "verify-pragma-token-repair",
  "owner_role": "pragma-parser-tests",
  "operation": "Run bound current public parser regression and adjacent checks without source edits; record actual results, validation freshness and coverage limits.",
  "kind": "validate",
  "inputs": [
    {"name": "patched-checkout", "semantic_role": "pragma-token-repair-candidate", "artifact_kind": "checkout", "language": "python", "scope": "current-public-checkout", "phase": "repair", "state": "underscore-enabled-with-exact-regression"}
  ],
  "outputs": [
    {"name": "validation-report", "semantic_role": "observed-pragma-repair-results", "artifact_kind": "test-report", "language": "python", "scope": "current-public-checkout", "phase": "validation", "state": "observed-public-results"}
  ],
  "preconditions": [
    {"key": "underscore-token-class-enabled", "value": true, "evaluator": "evidence"},
    {"key": "exact-symbol-regression-authored", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "underscore-symbol-intact", "value": true, "evaluator": "evidence"},
    {"key": "current-public-validation-passed", "value": true, "evaluator": "evidence"},
    {"key": "current-public-validation-observation", "value": "fresh", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-pragma-grammar-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "exact-symbol-and-adjacent-tests",
      "instruction": "Execute the bound parser regression and adjacent suite. Require disable plus a singleton complete underscore-containing name, and preserved results for ordinary/hyphenated names, numeric IDs, multiple messages and malformed pragmas. Record actual exits/output and whether registered-message integration was checked.",
      "evidence_refs": ["pylint-dev/pylint:3604:body", "pylint-dev/pylint:3604:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:69a4d4302a9cbe21cf4cdae8:repair"],
  "source_ids": ["pylint-dev/pylint:3604:repair:ffb354aea057"],
  "evidence_refs": ["pylint-dev/pylint:3604:body", "pylint-dev/pylint:3604:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:69a4d4302a9cbe21cf4cdae8",
  "read_set": ["role:pragma-parser", "role:pragma-parser-tests"],
  "write_set": []
}
```
