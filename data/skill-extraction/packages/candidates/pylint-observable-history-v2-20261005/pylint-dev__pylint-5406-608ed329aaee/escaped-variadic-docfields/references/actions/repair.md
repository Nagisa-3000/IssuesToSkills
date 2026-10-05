# Repair the Sphinx-specific boundary

Accept ordinary word names or one backslash followed by one or two stars and a word name. The historical two-star form is `\**kwargs`, not separately escaped stars. Keep capture groups aligned with extraction and remove the escape only from recognized Sphinx parameter names before signature comparison.

Add public positive and negative assertions. Preserve ordinary fields, missing-documentation checks, and unrelated diagnostics. If an applicable production example exists, make its docstring raw and use the escaped variadic field. Do not create unrelated production code to imitate history or alter other styles.

```arex-contract-v4
{
  "id": "workflow:verified-history:f2490b7f20db2a942170750b:repair",
  "intent": "Correct escaped Sphinx variadic recognition and signature matching.",
  "mechanism": "Constrain the parameter-name grammar, normalize its recognized escape, and align raw examples and regression assertions.",
  "semantic_role": "sphinx-escape-repair",
  "owner_role": "sphinx-parameter-parser",
  "operation": "Edit the bound Sphinx recognizer and extractor, update public diagnostic fixtures, and correct applicable production docstring examples. Keep other style parsers and unrelated expectations unchanged.",
  "kind": "edit",
  "inputs": [
    {
      "name": "located-target",
      "semantic_role": "sphinx-repair-target",
      "artifact_kind": "owner-bindings-and-syntax-observations",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "diagnosis",
      "state": "located-and-policy-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "modified-target",
      "semantic_role": "sphinx-repair-state",
      "artifact_kind": "code-and-public-regression-diff",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "repair",
      "state": "modified-awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:sphinx-parameter-parser", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:sphinx-variadic-fixtures", "value": true, "evaluator": "file_exists"},
    {"key": "strict-sphinx-escape-policy-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "escaped-variadics-match-signatures", "value": true, "evaluator": "evidence"},
    {"key": "unescaped-starred-fields-do-not-satisfy-docs", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-parameter-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-google-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observation-current"],
  "oracle": [
    {
      "id": "inspect-diff",
      "instruction": "Review the public diff for escaped one/two-star recognition, capture/extraction alignment, normalization confined to Sphinx names, raw escaped examples where applicable, and positive/negative assertions. Diff review does not establish execution success.",
      "evidence_refs": ["pylint-dev/pylint:5406:fix", "pylint-dev/pylint:5406:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:sphinx-parameter-parser", "role:sphinx-variadic-fixtures", "role:escaped-docstring-example"],
  "write_set": ["role:sphinx-parameter-parser", "role:sphinx-variadic-fixtures", "role:escaped-docstring-example"],
  "source_ids": ["pylint-dev/pylint:5406:repair:608ed329aaee"],
  "evidence_refs": ["pylint-dev/pylint:5406:fix", "pylint-dev/pylint:5406:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:f2490b7f20db2a942170750b"
}
```

Behavioral effects require evidence from the separate validation Action. Any edit makes previous validation observations stale without weakening preserved-behavior obligations.
