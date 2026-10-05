# Repair extraction and comparison

Apply only necessary changes at current bound owners.

The historical Sphinx expression changes the escaped-asterisk repetition allowance from `{1,2}` to `{0,2}`, retaining a plain-word alternative. The Google expression permits an optional escape before asterisks, and extracted Google parameter names have backslashes removed. This does not establish that every unescaped Sphinx spelling is valid.

For missing names, the historical code computes unmatched expected names, then skips a missing diagnostic when the expected name with `*` removed occurs among documented names.

For differing names, it conditionally substitutes a bare expected name when that bare name occurs in documentation, otherwise retaining the starred name. It then retains the existing symmetric-difference and exemption calculation. Repair both halves of paired diagnostics.

Preserve ordinary identifiers, not-needed names, ignored arguments, and genuine mismatch reporting. Do not change type-documentation policy. Add public style-specific assertions using raw strings or doubled source backslashes where needed.

```arex-contract-v4
{
  "id": "workflow:verified-history:8f01015f3fde403e97d30645:repair",
  "intent": "Correct supported variadic extraction and bare-name equivalence.",
  "mechanism": "Style-bounded escape handling and conditional equivalence from starred expected names to documented bare names.",
  "semantic_role": "variadic-name-compatibility-edit",
  "owner_role": "documentation-parameter-checker",
  "operation": "Edit bound parser and comparator where mismatch is observed; add public regression assertions without suppressing genuine diagnostics.",
  "kind": "edit",
  "inputs": [
    {"name": "localized-mismatch", "semantic_role": "variadic-documentation-repair-context", "artifact_kind": "public-code-analysis", "language": "python", "scope": "documentation-parameter-checker", "phase": "pre-edit", "state": "bound-and-observed"}
  ],
  "outputs": [
    {"name": "repair-candidate", "semantic_role": "variadic-documentation-repair-candidate", "artifact_kind": "checkout-change", "language": "python", "scope": "documentation-parameter-checker", "phase": "post-edit", "state": "awaiting-public-validation"}
  ],
  "preconditions": [
    {"key": "repair-owners-and-style-bound", "value": true, "evaluator": "evidence"},
    {"key": "supported-variadic-name-mismatch-observed", "value": true, "evaluator": "evidence"},
    {"key": "role:documentation-name-parser", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:documentation-parameter-comparator", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:documentation-checker-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "variadic-documentation-name-compatibility", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-parameters-and-exemptions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "string-literal-warning-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["current-public-validation-observed", "current-parsed-name-observation"],
  "oracle": [
    {
      "id": "review-bounded-name-repair",
      "instruction": "Review the current diff for supported style-bounded escape handling, conditional bare-name equivalence in both comparisons, preserved exemptions, and public regression assertions. Review alone is not behavioral execution.",
      "evidence_refs": ["pylint-dev/pylint:5406:fix", "pylint-dev/pylint:5406:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:documentation-name-parser", "role:documentation-parameter-comparator", "role:documentation-checker-tests"],
  "write_set": ["role:documentation-name-parser", "role:documentation-parameter-comparator", "role:documentation-checker-tests"],
  "source_ids": ["pylint-dev/pylint:5406:repair:3b744d180e5e"],
  "evidence_refs": ["pylint-dev/pylint:5406:fix", "pylint-dev/pylint:5406:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:8f01015f3fde403e97d30645"
}
```
