# Align recognition and extraction

Edit current semantic owners, not presumed historical paths. Recognize supported multiple-type declarations and expose individual exception names to the checker comparison. Retain existing type forms and Google's description gate; do not replace the grammar with unrestricted matching.

Add public singleton-plus-list regressions for supported Sphinx and Google styles. Historical assertions directly visit `NameError`; broader per-member validation is a new requirement. The historical splitter can return separators as well as names, so do not claim a names-only exact set.

Existence predicates identify roles in their keys and use boolean values. Resolve roles to actual current files/symbols before evaluation.

```arex-contract-v4
{
  "id": "workflow:verified-history:659f8bc8e03e7014a22a5caa:repair",
  "intent": "Expose individually documented list members to missing-raises comparison.",
  "mechanism": "Coordinate list-capable grammar recognition and per-name collection with public regression assertions.",
  "semantic_role": "repair-exception-list-parser",
  "owner_role": "docstring-type-parser",
  "operation": "Edit bound Python recognition and raises collection to handle supported lists; preserve supported forms and Google description handling; add public singleton-plus-list checker regressions.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosis",
      "semantic_role": "exception-list-diagnosis",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "public-checkout-docstring-checker",
      "phase": "diagnosed",
      "state": "owners-bound-and-mismatch-confirmed"
    }
  ],
  "outputs": [
    {
      "name": "candidate",
      "semantic_role": "exception-list-repair-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "public-checkout-docstring-checker",
      "phase": "edited",
      "state": "parser-and-public-regressions-updated"
    }
  ],
  "preconditions": [
    {"key": "current-owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "list-parsing-mismatch-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:docstring-type-parser", "value": true, "evaluator": "symbol_exists", "description": "Resolve the role to current Python recognition and exception-collection symbols."},
    {"key": "role:raise-doc-tests", "value": true, "evaluator": "file_exists", "description": "Resolve the role to current public checker test files."}
  ],
  "effects": [
    {"key": "documented-list-members-recognized", "value": true, "evaluator": "evidence"},
    {"key": "public-list-regressions-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "singleton-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-missing-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-type-forms-preserved", "value": true, "evaluator": "evidence"},
    {"key": "google-description-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-list-change",
      "instruction": "Review coordinated recognition and collection edits and public regressions. Confirm supported forms and Google description handling remain intact. Reject blanket warning suppression or unrelated inference workarounds. Retain the validate Action before acceptance.",
      "evidence_refs": ["pylint-dev/pylint:2729:fix", "pylint-dev/pylint:2729:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:2729:repair:183dcc4cb134"],
  "evidence_refs": ["pylint-dev/pylint:2729:fix", "pylint-dev/pylint:2729:regression"],
  "read_set": ["role:docstring-type-parser", "role:raise-doc-tests"],
  "write_set": ["role:docstring-type-parser", "role:raise-doc-tests"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:659f8bc8e03e7014a22a5caa"
}
```

Effects describe intended outcomes, not observed execution success. Subsequent validation must show that incidental separator tokens cannot mask real missing names.
