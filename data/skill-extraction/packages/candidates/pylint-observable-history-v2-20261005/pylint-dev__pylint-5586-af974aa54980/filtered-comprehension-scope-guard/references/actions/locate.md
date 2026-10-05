# Locate the filter/homonym interaction

Inspect the current Python variable checker and public reproduction without changing implementation or tests. Resolve semantic roles to current symbols and files. Diagnose the scope interaction, not merely the diagnostic's spelling.

```arex-contract-v4
{
  "id": "workflow:verified-history:4d5404af23a33d07f9c8cd24:locate",
  "intent": "Establish applicability and bind current semantic owners.",
  "mechanism": "Compare the filter-local target with the enclosing exception-handler homonym and inspect the exact parent/filter membership relation.",
  "semantic_role": "scope-interaction-probe",
  "owner_role": "python-variable-use-dispatch",
  "operation": "Read current code, inspect the AST of a public reproduction, and run a bound diagnostic probe without modifying implementation or tests. Record responsible branch, filter shape, target binding and public test owner.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "scope-analysis", "semantic_role": "verified-filter-homonym-analysis", "artifact_kind": "analysis-record", "language": "python", "scope": "current-checkout", "phase": "diagnosis", "state": "observed"}
  ],
  "preconditions": [
    {"key": "public-reproduction-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "supported-filter-interaction-observed", "value": true, "evaluator": "evidence"},
    {"key": "semantic-owners-bound", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "nonfilter-homonym-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "late-binding-and-loop-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-filter-interaction",
      "instruction": "Observe the reported diagnostic on the public reproduction and inspect whether its name is comprehension-local, its immediate parent belongs to a comprehension's filters, and the enclosing homonym branch accounts for the diagnostic. Confirm no source/test edits.",
      "evidence_refs": ["pylint-dev/pylint:5586:body", "pylint-dev/pylint:5586:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:python-variable-use-dispatch", "role:python-public-functional-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5586:repair:af974aa54980"],
  "evidence_refs": ["pylint-dev/pylint:5586:body", "pylint-dev/pylint:5586:fix"],
  "resource": "references/actions/locate.md",
  "package_id": "workflow:verified-history:4d5404af23a33d07f9c8cd24"
}
```

If the branch or shape is UNKNOWN, continue inspection only. If inspection establishes a different mechanism, stop this Workflow.
