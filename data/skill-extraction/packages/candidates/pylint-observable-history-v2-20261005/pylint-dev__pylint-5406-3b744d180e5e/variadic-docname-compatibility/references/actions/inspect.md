# Inspect the mismatch

Locate current parser, comparator, and public test owners. Record signature names and parsed documentation names separately. Reproduce exact diagnostics using current configuration.

Use raw docstrings or doubled source backslashes when isolating documentation parsing from Python string-literal warnings. Read/probe only: do not change tracked code or fixtures. Return incomplete bindings if ownership or supported grammar is unknown.

```arex-contract-v4
{
  "id": "workflow:verified-history:8f01015f3fde403e97d30645:inspect",
  "intent": "Localize a supported variadic documentation-name mismatch.",
  "mechanism": "Observe extraction and signature comparison independently.",
  "semantic_role": "mismatch-localization",
  "owner_role": "documentation-name-analysis",
  "operation": "Read current owners and run non-modifying public reproductions; record style, configuration, names, diagnostics, pinned anchors, and role bindings.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "localized-mismatch", "semantic_role": "variadic-documentation-repair-context", "artifact_kind": "public-code-analysis", "language": "python", "scope": "documentation-parameter-checker", "phase": "pre-edit", "state": "bound-and-observed"}
  ],
  "preconditions": [
    {"key": "public-python-reproduction-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "repair-owners-and-style-bound", "value": true, "evaluator": "evidence"},
    {"key": "supported-variadic-name-mismatch-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-parameters-and-exemptions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "string-literal-warning-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "observe-name-mismatch",
      "instruction": "Record current style, configuration, signature names, parsed names, exact diagnostics, and current owner anchors. Distinguish literal warnings from documentation-name mismatch; confirm tracked files are unchanged.",
      "evidence_refs": ["pylint-dev/pylint:5406:body", "pylint-dev/pylint:5406:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:documentation-name-parser", "role:documentation-parameter-comparator", "role:documentation-checker-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5406:repair:3b744d180e5e"],
  "evidence_refs": ["pylint-dev/pylint:5406:body", "pylint-dev/pylint:5406:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:8f01015f3fde403e97d30645"
}
```
