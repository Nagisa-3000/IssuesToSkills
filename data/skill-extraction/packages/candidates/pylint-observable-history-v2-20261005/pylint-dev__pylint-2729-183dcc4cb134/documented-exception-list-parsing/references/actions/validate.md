# Validate target and adjacent behavior

Execute freshly bound current public checks after the final edit. Independently cover each list member, singleton documentation, genuine missing exceptions, and supported syntax. Exercise shared parameter/property grammar consumers where present and retain Google's description handling.

This operation does not edit source or tests. Record FAIL and UNKNOWN explicitly. A fresh validation record does not imply passing checks; acceptance requires target behavior and all preserved assurances to pass.

```arex-contract-v4
{
  "id": "workflow:verified-history:659f8bc8e03e7014a22a5caa:validate",
  "intent": "Observe target and adjacent diagnostic behavior after edits.",
  "mechanism": "Execute public list regressions and adjacent syntax and missing-documentation controls.",
  "semantic_role": "validate-exception-list-repair",
  "owner_role": "raise-doc-tests",
  "operation": "Bind and execute public checker regressions, independent list-member probes, and adjacent controls; record commands, edited anchors, outputs, and tri-state results without editing source or tests.",
  "kind": "validate",
  "inputs": [
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
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "exception-list-public-validation",
      "artifact_kind": "test-record",
      "language": "python",
      "scope": "public-checkout-docstring-checker",
      "phase": "validated",
      "state": "public-results-recorded"
    }
  ],
  "preconditions": [
    {"key": "current-owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "public-list-regressions-added", "value": true, "evaluator": "evidence"},
    {"key": "role:raise-doc-tests", "value": true, "evaluator": "file_exists", "description": "Resolve the role to current public checker test files."}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "singleton-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-missing-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-type-forms-preserved", "value": true, "evaluator": "evidence"},
    {"key": "google-description-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "list-checker-regressions",
      "instruction": "Execute current public Sphinx and Google list regressions where supported. Independently check each documented member and the singleton for absence of false missing-raises warnings. An unvisited fixture raise is not independently verified.",
      "evidence_refs": ["pylint-dev/pylint:2729:body", "pylint-dev/pylint:2729:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-doc-behavior",
      "instruction": "Execute public controls proving genuinely undocumented exceptions still warn and supported singleton, or/container syntax and Google description handling retain baseline behavior. Exercise shared parameter/property consumers where present. Check that separator tokens cannot conceal genuine missing exceptions.",
      "evidence_refs": ["pylint-dev/pylint:2729:fix", "pylint-dev/pylint:2729:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:659f8bc8e03e7014a22a5caa:repair"],
  "source_ids": ["pylint-dev/pylint:2729:repair:183dcc4cb134"],
  "evidence_refs": ["pylint-dev/pylint:2729:fix", "pylint-dev/pylint:2729:regression"],
  "read_set": ["role:docstring-type-parser", "role:raise-doc-tests"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:659f8bc8e03e7014a22a5caa"
}
```

Any subsequent source or test edit requires renewed validation.
