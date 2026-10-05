# Narrow the guard and add the regression

At the current assignment-candidate filtering owner, retain the existing filtering for non-comprehension parents and uses not directly in the comprehension's filter list. Skip that filtering only for the confirmed direct-filter case.

The historical condition used `not isinstance(parent_node, nodes.Comprehension) or node not in parent_node.ifs` in conjunction with `found_nodes`. Preserve this truth condition when adapting it to current symbols; do not invent a broader descendant or name-spelling exemption.

At the current regression owner, add the public `try`/filtered-comprehension/handler collision case with no expected used-before-assignment diagnostic. Retain the adjacent assertion for a real use outside the handler. Do not blanket-suppress diagnostics.

```arex-contract-v4
{
  "id": "workflow:verified-history:afcebec8041ecae4f0debb6d:repair",
  "intent": "Correct the narrowly confirmed scope-collision false positive and commit a public regression.",
  "mechanism": "Guard exception-handler assignment filtering with the direct comprehension-filter AST relation.",
  "semantic_role": "scope-filter-repair",
  "owner_role": "assignment-candidate-filter",
  "operation": "Edit the located candidate-filter condition to bypass only direct comprehension filter tests; add the collision regression to the located diagnostic test owner while preserving genuine-error assertions.",
  "kind": "edit",
  "inputs": [
    {"name": "localized-scope-case", "semantic_role": "scope-collision-evidence", "artifact_kind": "public-code-and-observations", "language": "python", "scope": "current-checkout", "phase": "pre-edit", "state": "localized", "optional": false}
  ],
  "outputs": [
    {"name": "patched-scope-case", "semantic_role": "scope-repair-artifacts", "artifact_kind": "public-code-and-tests", "language": "python", "scope": "current-checkout", "phase": "post-edit", "state": "patched-unvalidated", "optional": false}
  ],
  "preconditions": [
    {"key": "supported-filtering-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "assignment-filter-owner-located", "value": true, "evaluator": "symbol_exists", "description": "role:assignment-candidate-filter"},
    {"key": "regression-owner-located", "value": true, "evaluator": "file_exists", "description": "role:assignment-diagnostic-regressions"}
  ],
  "effects": [
    {"key": "direct-filter-guard-installed", "value": true, "evaluator": "evidence"},
    {"key": "collision-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-exception-scope-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-candidate-filter-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed", "pre-edit-diagnostic-observation"],
  "oracle": [
    {
      "id": "review-narrow-guard",
      "instruction": "Review the diff against the direct membership truth condition. Verify that the public collision regression expects no false diagnostic and existing genuine-error assertions remain. This review alone does not establish test success.",
      "evidence_refs": ["pylint-dev/pylint:5817:fix", "pylint-dev/pylint:5817:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5817:repair:67055f422132"],
  "evidence_refs": ["pylint-dev/pylint:5817:fix", "pylint-dev/pylint:5817:regression"],
  "read_set": ["role:assignment-candidate-filter", "role:assignment-diagnostic-regressions"],
  "write_set": ["role:assignment-candidate-filter", "role:assignment-diagnostic-regressions"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:afcebec8041ecae4f0debb6d"
}
```

Effects are intended postconditions until observed. The separate validation Action is mandatory after any edit.
