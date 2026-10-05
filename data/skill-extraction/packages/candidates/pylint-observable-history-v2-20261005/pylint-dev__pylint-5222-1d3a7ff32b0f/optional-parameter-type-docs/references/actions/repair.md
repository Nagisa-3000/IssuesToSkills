# Edit the parser and regression

This modifying Action covers both production parsing and public regression assertions. Retain its explicit validation Action.

```arex-contract-v4
{
  "id": "workflow:verified-history:00bdb5de0892c0cbbab00de9:repair",
  "package_id": "workflow:verified-history:00bdb5de0892c0cbbab00de9",
  "resource": "references/actions/repair.md",
  "kind": "edit",
  "intent": "Recognize described name-only entries without inventing inline type information.",
  "mechanism": "Accept colon or newline after an optionally starred identifier and separately accumulate documentation and docstring-type membership.",
  "semantic_role": "repair-optional-inline-types",
  "owner_role": "numpy-parameter-parser",
  "operation": "Adapt the NumPy-specific matcher and collector to accept newline-delimited names and preserve explicit type parsing. Retain ordinary and keyword section handling. Update a public mixed-entry regression with an explicitly typed entry, annotated and unannotated description-only entries, and a starred description entry. Require exactly missing-type-doc for the unannotated parameter. Review current captures; do not introduce the historical debug print or use a delimiter as proof of description content.",
  "inputs": [
    {"name": "diagnosis", "semantic_role": "optional-type-diagnosis", "artifact_kind": "inspection-report", "language": "python", "scope": "parameter-documentation-checker", "phase": "diagnosis", "state": "bound-and-observed", "optional": false}
  ],
  "outputs": [
    {"name": "candidate", "semantic_role": "optional-type-repair", "artifact_kind": "checkout-change", "language": "python", "scope": "parameter-documentation-checker", "phase": "repair", "state": "edited-unvalidated", "optional": false}
  ],
  "preconditions": [
    {"key": "owner-bindings-observed", "value": true, "evaluator": "evidence"},
    {"key": "entry-rejection-observed", "value": true, "evaluator": "evidence"},
    {"key": "role:numpy-parameter-parser", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:documentation-checker-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "description-only-recognition", "value": true, "evaluator": "evidence"},
    {"key": "mixed-regression-authored", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "legitimate-type-diagnostics", "value": "preserved", "evaluator": "evidence"},
    {"key": "adjacent-docstring-behavior", "value": "preserved", "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-parser-and-test-diff",
      "instruction": "Review both production and regression changes. Confirm documentation membership is independent of docstring type presence, explicit types remain meaningful, and the exact regression expects only the legitimate unannotated missing-type diagnostic. Review actual description capture and avoid changing unrelated shared grammars.",
      "evidence_refs": ["pylint-dev/pylint:5222:fix", "pylint-dev/pylint:5222:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:numpy-parameter-parser", "role:parameter-documentation-checker", "role:documentation-checker-tests"],
  "write_set": ["role:numpy-parameter-parser", "role:documentation-checker-tests"],
  "source_ids": ["pylint-dev/pylint:5222:repair:1d3a7ff32b0f"],
  "evidence_refs": ["pylint-dev/pylint:5222:fix", "pylint-dev/pylint:5222:regression"]
}
```

Effects describe intended behavior until public validation observes it. Empty descriptions, malformed entries, and return documentation need separate current evidence; the historical targeted regression does not settle them.
