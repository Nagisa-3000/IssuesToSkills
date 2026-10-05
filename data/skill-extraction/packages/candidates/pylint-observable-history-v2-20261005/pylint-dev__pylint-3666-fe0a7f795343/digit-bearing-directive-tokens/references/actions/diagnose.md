# Diagnose symbolic token loss

Locate the current Python directive lexer and public parser tests. Trace input through comment extraction, tokenization, parsing, and lookup. Inspect the symbolic character class, minimum length, and precedence.

This probe does not edit source or tests. Successful outputs below are conditional: emit a confirmed diagnosis only after current public evidence establishes the cause and valid digit-bearing grammar. Otherwise record contrary or unknown observations and stop the edit branch.

```arex-contract-v4
{
  "id": "workflow:verified-history:a4e1808f638c9a903d335608:diagnose",
  "intent": "Confirm whether digit exclusion causes symbolic directive token loss.",
  "mechanism": "Inspect a Python regex lexer and trace exact public directive output.",
  "semantic_role": "diagnose-symbolic-token-loss",
  "owner_role": "directive-lexer",
  "operation": "Read and bind current lexer/tests; inspect grammar and precedence; run a non-editing public reproduction and record exact input, action and messages.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
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
  "preconditions": [],
  "effects": [
    {"key": "lexical-digit-exclusion-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "digits-valid-in-symbolic-identifiers", "value": true, "evaluator": "evidence"},
    {"key": "role:directive-lexer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:directive-parser-tests", "value": true, "evaluator": "file_exists"}
  ],
  "preserves": [
    {"key": "adjacent-directive-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-token-grammar-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "trace-digit-loss",
      "instruction": "Record exact public digit-bearing disable input and parsed output. Inspect the bound symbolic regex and establish loss during tokenization rather than rejection of an intact name at lookup. Establish that digits are valid symbolic characters and confirm source/tests were not edited.",
      "evidence_refs": ["pylint-dev/pylint:3666:body", "pylint-dev/pylint:3666:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:directive-lexer", "role:directive-parser-tests"],
  "write_set": [],
  "exclusions": [
    {"key": "identifier-reaches-lookup-intact", "value": true, "evaluator": "evidence"},
    {"key": "digits-forbidden-by-public-grammar", "value": true, "evaluator": "evidence"}
  ],
  "source_ids": ["pylint-dev/pylint:3666:repair:fe0a7f795343"],
  "evidence_refs": ["pylint-dev/pylint:3666:body", "pylint-dev/pylint:3666:fix"],
  "resource": "references/actions/diagnose.md",
  "package_id": "workflow:verified-history:a4e1808f638c9a903d335608"
}
```
