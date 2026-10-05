# Narrow the homonym condition

The historical change excluded a specific filter-node shape from the conjunction for a comprehension with an enclosing-function homonym. It did not suppress every diagnostic in comprehensions.

```arex-contract-v4
{
  "id": "workflow:verified-history:4d5404af23a33d07f9c8cd24:repair",
  "intent": "Correct the filter-specific scope dispatch.",
  "mechanism": "Add a negative filter-membership condition inside the comprehension/homonym conjunction.",
  "semantic_role": "filter-homonym-guard-edit",
  "owner_role": "python-variable-use-dispatch",
  "operation": "At the bound variable-use dispatch, exclude the evidenced case where the name's grandparent is a comprehension and its parent is a member of that comprehension's filters. Retain the decorator condition, ordinary homonym handling and subsequent late-binding/loop-variable calls. Adapt symbol spelling only after current AST inspection.",
  "kind": "edit",
  "inputs": [
    {"name": "scope-analysis", "semantic_role": "verified-filter-homonym-analysis", "artifact_kind": "analysis-record", "language": "python", "scope": "current-checkout", "phase": "diagnosis", "state": "observed"}
  ],
  "outputs": [
    {"name": "guarded-checker", "semantic_role": "filter-guarded-variable-checker", "artifact_kind": "checkout-code", "language": "python", "scope": "current-checkout", "phase": "implementation", "state": "edited"}
  ],
  "preconditions": [
    {"key": "supported-filter-interaction-observed", "value": true, "evaluator": "evidence"},
    {"key": "semantic-owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:python-variable-use-dispatch", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "filter-homonym-guard-corrected", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "nonfilter-homonym-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "late-binding-and-loop-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "arbitrary-filter-ancestor-traversal-required", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-narrow-guard",
      "instruction": "Review the diff and current AST evidence: only the supported filter/homonym conjunction changes, and the surrounding decorator dispatch and late-binding/loop-variable calls remain intact. Behavioral acceptance requires the validate Action.",
      "evidence_refs": ["pylint-dev/pylint:5586:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:python-variable-use-dispatch"],
  "write_set": ["role:python-variable-use-dispatch"],
  "source_ids": ["pylint-dev/pylint:5586:repair:af974aa54980"],
  "evidence_refs": ["pylint-dev/pylint:5586:fix"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:4d5404af23a33d07f9c8cd24"
}
```

Effects are required postconditions, not observed outcomes. Do not claim them until the diff and public validation support them.
