# Repair the proven character omission and author exact assertions

Bind the current symbolic-message token specification and parser test owner. Add underscore to the existing permitted class, without changing token precedence, minimum length, numeric syntax, assignment syntax, or keyword recognition.

Add a regression through the current public parser interface. The historical assertion used `raw_input-builtin`; the reported symptom used `found-_-in-module-class`. Assert the complete symbol as a singleton message list and action `disable`. Merely asserting absence of an exception is insufficient.

This Action combines implementation and regression edits. Its effects describe an authored repair candidate, not observed repair success. Invalidate the old validation observation and retain the following public validate Action.

```arex-contract-v4
{
  "id": "workflow:verified-history:69a4d4302a9cbe21cf4cdae8:repair",
  "intent": "Restore supported underscore-containing message names as single tokens.",
  "mechanism": "Add underscore to the existing symbolic-message character class and author exact-output regression assertions.",
  "semantic_role": "repair-identifier-token-class",
  "owner_role": "pragma-message-token-specification",
  "operation": "Edit the bound symbolic-message token class to admit only the established missing underscore and add an exact action/messages regression in the bound parser tests.",
  "kind": "edit",
  "inputs": [
    {"name": "diagnosed-checkout", "semantic_role": "bound-pragma-repair-target", "artifact_kind": "checkout-evidence", "language": "python", "scope": "current-public-checkout", "phase": "diagnosis", "state": "owners-bound-and-omission-established"}
  ],
  "outputs": [
    {"name": "patched-checkout", "semantic_role": "pragma-token-repair-candidate", "artifact_kind": "checkout", "language": "python", "scope": "current-public-checkout", "phase": "repair", "state": "underscore-enabled-with-exact-regression"}
  ],
  "preconditions": [
    {"key": "repair-owner-bound", "value": true, "evaluator": "evidence"},
    {"key": "underscore-omission-established", "value": true, "evaluator": "evidence"},
    {"key": "role:pragma-message-token-specification", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:pragma-parser-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "underscore-token-class-enabled", "value": true, "evaluator": "evidence"},
    {"key": "exact-symbol-regression-authored", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-pragma-grammar-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["current-public-validation-observation"],
  "oracle": [
    {
      "id": "review-localized-edit",
      "instruction": "Review the current diff: underscore is the only grammar expansion; ordering, minimum length, numeric syntax, assignment and keywords remain unchanged. Confirm exact disable action and singleton complete message assertions. Do not treat review as executed validation.",
      "evidence_refs": ["pylint-dev/pylint:3604:fix", "pylint-dev/pylint:3604:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3604:repair:ffb354aea057"],
  "evidence_refs": ["pylint-dev/pylint:3604:fix", "pylint-dev/pylint:3604:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:69a4d4302a9cbe21cf4cdae8",
  "read_set": ["role:pragma-message-token-specification", "role:pragma-parser-tests"],
  "write_set": ["role:pragma-message-token-specification", "role:pragma-parser-tests"]
}
```
