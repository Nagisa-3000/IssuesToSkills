# Repair the guard and add diagnostic assertions

Within the consumed-name condition, introduce a verified function-decorator-context alternative to the existing negated comprehension/homonym conjunction. Do not remove the consumed-name requirement or broadly suppress decorator diagnostics. Retain assignment-parent resolution and downstream late-binding checks.

Add both bound-`x` generator positives and both genuine-undefined controls to the current public fixture suite. This is a modifying Action and must retain its explicit validate Action.

```arex-contract-v4
{
  "id": "workflow:verified-history:2d9cfc7283460de886b0b9d6:repair",
  "intent": "Correct the decorator-local scope guard and encode its diagnostic boundary.",
  "mechanism": "Use consumed-name AND (function-decorator-context OR NOT(comprehension AND upper-function homonym)).",
  "semantic_role": "scope-guard-repair",
  "owner_role": "name-resolution-checker",
  "operation": "Edit the bound guard with the decorator-context alternative, leaving the non-decorator branch and late-binding path intact. Add generator positives for x and x*x, a separate unbound-x decorator control, and an unbound-y generator-body control in the current public suite.",
  "kind": "edit",
  "inputs": [
    {"name": "scope-binding", "semantic_role": "decorator-scope-binding", "artifact_kind": "binding-record", "language": "python", "scope": "current-checkout", "phase": "pre-edit", "state": "observed", "optional": false}
  ],
  "outputs": [
    {"name": "scope-patch", "semantic_role": "decorator-scope-repair", "artifact_kind": "patch", "language": "python", "scope": "current-checkout", "phase": "post-edit", "state": "unvalidated", "optional": false}
  ],
  "preconditions": [
    {"key": "scope-mechanism-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:name-resolution-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:decorator-context-classifier", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:scope-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "decorator-bound-name-accepted", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-boundary-assertions-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-undefined-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nondecorator-homonym-protection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "late-binding-check-path-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-narrowed-guard",
      "instruction": "Review the current diff for retained consumed-name gating, the decorator-context alternative, unchanged non-decorator homonym protection, and retained assignment-parent and late-binding checks. Inspect all four public regression assertions. Treat behavior effects as expected until post-edit validation observes them.",
      "evidence_refs": ["pylint-dev/pylint:3791:fix", "pylint-dev/pylint:3791:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3791:repair:a054796d7008"],
  "evidence_refs": ["pylint-dev/pylint:3791:fix", "pylint-dev/pylint:3791:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:2d9cfc7283460de886b0b9d6",
  "read_set": ["role:name-resolution-checker", "role:decorator-context-classifier", "role:scope-regression-suite"],
  "write_set": ["role:name-resolution-checker", "role:scope-regression-suite"],
  "invalidates": ["public-validation-observed"]
}
```
