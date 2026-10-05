# Probe the scope collision

Locate current semantic owners rather than reusing historical paths. Reproduce the public diagnostic, inspect the name node and candidate-filter branch, and capture hashed anchors and current bindings. Reading/probing must not edit tracked source or tests. If the use is nested inside a larger filter expression rather than a direct member of `ifs`, this historical mechanism does not establish applicability.

```arex-contract-v4
{
  "id": "workflow:verified-history:afcebec8041ecae4f0debb6d:probe",
  "intent": "Establish that the direct comprehension filter/handler collision uses the supported filtering mechanism.",
  "mechanism": "Inspect the reproduction, direct AST membership, and exception-handler assignment-candidate filtering.",
  "semantic_role": "scope-collision-localization",
  "owner_role": "assignment-candidate-filter",
  "operation": "Read current source and run a bound public reproduction or AST probe without editing tracked artifacts. Record the responsible branch, AST relation, diagnostic and hashed anchors.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "localized-scope-case", "semantic_role": "scope-collision-evidence", "artifact_kind": "public-code-and-observations", "language": "python", "scope": "current-checkout", "phase": "pre-edit", "state": "localized", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "supported-filtering-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "assignment-filter-owner-located", "value": true, "evaluator": "symbol_exists", "description": "role:assignment-candidate-filter"},
    {"key": "regression-owner-located", "value": true, "evaluator": "file_exists", "description": "role:assignment-diagnostic-regressions"}
  ],
  "preserves": [
    {"key": "genuine-exception-scope-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-candidate-filter-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-direct-filter-collision",
      "instruction": "Confirm a false diagnostic on the public direct filter-name reproduction and show that its parent is a comprehension, the node is in its filter-test list, and the handler candidate-filter branch is responsible. Confirm the probe made no tracked edits.",
      "evidence_refs": ["pylint-dev/pylint:5817:body", "pylint-dev/pylint:5817:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5817:repair:67055f422132"],
  "evidence_refs": ["pylint-dev/pylint:5817:body", "pylint-dev/pylint:5817:fix"],
  "read_set": ["role:assignment-candidate-filter", "role:assignment-diagnostic-regressions"],
  "write_set": [],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:afcebec8041ecae4f0debb6d"
}
```

Predicate descriptions using `role:` require actual current owner bindings and symbol/file observations, not historical path existence. The semantic mechanism predicate requires evidence-backed review; its name alone is not proof.
