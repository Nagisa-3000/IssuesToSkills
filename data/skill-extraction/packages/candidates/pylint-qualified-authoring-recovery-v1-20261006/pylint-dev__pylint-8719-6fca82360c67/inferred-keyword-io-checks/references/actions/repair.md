# Integrate dictionary fallback

Keep ordinary positional/named lookup first. On missing arguments, safely infer unpacked keyword values, inspect supported dictionary items, and return the matching value node or no result.

The historical helper compared `item[0].value == keyword` and returned `item[1]`. This does not establish arbitrary-mapping or nonconstant-key safety. Review current AST shapes; stop on unsupported assumptions.

For mode, retain value inference, invalid-mode reporting, and binary-mode gating. Dictionary-derived mode diagnostics use inference confidence.

For encoding, initialize confidence independently. Missing encoding still warns. A retrieved value inferred to constant `None` still warns, with inference confidence when retrieved through kwargs. An encoding absent from the dictionary retains high absence confidence; inferred mode must not leak its confidence into this warning.

Add public regressions with reviewed message and confidence expectations.

```arex-contract-v4
{
  "id": "workflow:verified-history:0a9b8ce52750bdf712058d20:repair",
  "package_id": "workflow:verified-history:0a9b8ce52750bdf712058d20",
  "resource": "references/actions/repair.md",
  "kind": "edit",
  "intent": "Correct unpacked IO argument discovery without weakening legitimate diagnostics.",
  "mechanism": "Fallback to safe dictionary inference after direct lookup failure, with separate mode and encoding confidence.",
  "semantic_role": "dictionary-keyword-fallback",
  "owner_role": "io-diagnostic-checker",
  "operation": "Modify the argument utility and IO checker, then add public fixtures and reviewed diagnostic assertions.",
  "inputs": [
    {"name": "review", "semantic_role": "io-keyword-repair-context", "artifact_kind": "review-record", "language": "python", "scope": "current-public-checkout", "phase": "pre-edit", "state": "reviewed"}
  ],
  "outputs": [
    {"name": "candidate", "semantic_role": "io-keyword-repair-candidate", "artifact_kind": "checkout-change", "language": "python", "scope": "current-public-checkout", "phase": "post-edit", "state": "unvalidated"}
  ],
  "preconditions": [
    {"key": "io-keyword-owners-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "fallback-applicability-established", "value": true, "evaluator": "evidence"},
    {"key": "role:python-call-analysis", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:io-diagnostic-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:io-functional-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "dictionary-keyword-fallback-integrated", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-assertions-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "direct-argument-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "binary-and-none-encoding-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "fallback-requires-unsupported-mapping-semantics", "value": true, "evaluator": "evidence"}
  ],
  "read_set": ["role:python-call-analysis", "role:io-diagnostic-checker", "role:io-functional-tests"],
  "write_set": ["role:python-call-analysis", "role:io-diagnostic-checker", "role:io-functional-tests"],
  "oracle": [
    {
      "id": "fallback-diff-review",
      "instruction": "Review the current diff for direct-first lookup, safe dictionary inference, separate confidence initialization, binary gating, None warnings, and public regression coverage. Retain the validate Action; diff review alone is not repair acceptance.",
      "kind": "public_probe",
      "command": [],
      "evidence_refs": ["pylint-dev/pylint:8719:fix", "pylint-dev/pylint:8719:regression"]
    }
  ],
  "source_ids": ["pylint-dev/pylint:8719:repair:6fca82360c67"],
  "evidence_refs": ["pylint-dev/pylint:8719:fix", "pylint-dev/pylint:8719:regression"]
}
```
