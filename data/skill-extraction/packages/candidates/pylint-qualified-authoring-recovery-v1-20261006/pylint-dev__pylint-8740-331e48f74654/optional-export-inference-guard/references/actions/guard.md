# Guard inference consumption

At the bound optional export checker, wrap only consumption of the inferred value. Catch the documented inference-failure exception and return from this check. Leave sentinel handling and successful-value checks intact.

```arex-contract-v4
{
  "id": "workflow:verified-history:9a3cbe2612faf6a1d7c341e8:guard",
  "intent": "Prevent an optional export check from crashing when inference is unavailable.",
  "mechanism": "Narrow exception containment at inference consumption with an early return.",
  "semantic_role": "inference-failure-containment",
  "owner_role": "module-export-checker",
  "operation": "Edit the bound inference-consumption expression to catch only the documented inference-failure exception and return from the optional export checker. Preserve the existing sentinel handling and downstream successful-value checks.",
  "kind": "edit",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "matching-inference-failure-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:module-export-checker", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "inference-failure-guard-installed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "undefined-variable-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "successful-export-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "narrow-guard-review",
      "instruction": "Review the current diff. Require that only inference consumption is inside the new handler, the caught type is the documented inference exception rather than Exception, failure returns from the optional check, and the sentinel and successful list/tuple checks remain intact.",
      "evidence_refs": ["pylint-dev/pylint:8740:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8740:repair:331e48f74654"],
  "evidence_refs": ["pylint-dev/pylint:8740:fix"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:9a3cbe2612faf6a1d7c341e8",
  "read_set": ["role:module-export-checker"],
  "write_set": ["role:module-export-checker"],
  "invalidates": ["public-validation-observed"]
}
```

The installed-guard effect is an obligation, not an observed result. Retain [Validate](validate.md) in the verification closure. Stop rather than broadening the handler or suppressing independent diagnostics.
