# Guard the branch and add an assignment-bearing regression

Use current semantic bindings, not historical paths. Require parent existence before enabling the nonlocal branch that later follows `parent.scope()`. A local scope alias may be used only after confirming it denotes the same scope. Do not replace this with exception swallowing or bypass the independent invalid-nonlocal diagnostic.

Add the current fixture equivalent of:

```python
nonlocal APPLE  # expected invalid-nonlocal diagnostic
APPLE = 42
```

The assignment is essential. Retain existing fixture cases and expectations. Match current diagnostic names and fixture conventions rather than hard-coding historical line numbers.

```arex-contract-v4
{
  "id": "workflow:verified-history:4e26a5bccbfef931bbba5ba0:guard",
  "intent": "Prevent enclosing-scope traversal at a root scope and lock the behavior into public regression assertions.",
  "mechanism": "Short-circuit branch selection on parent existence before inspecting nonlocal declarations for enclosing-scope handling.",
  "semantic_role": "root-scope-guard-and-regression",
  "owner_role": "assignment-scope-checker",
  "operation": "Edit the confirmed branch to require an enclosing parent; add a module-level nonlocal declaration followed by assignment and its expected ordinary diagnostic to the bound public fixtures.",
  "kind": "edit",
  "inputs": [
    {"name": "diagnosed-checkout", "semantic_role": "scope-repair-checkout", "artifact_kind": "checkout", "language": "python", "scope": "assignment-checker-and-functional-fixtures", "phase": "pre-edit", "state": "mechanism-confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "modified-checkout", "semantic_role": "scope-repair-checkout", "artifact_kind": "checkout", "language": "python", "scope": "assignment-checker-and-functional-fixtures", "phase": "post-edit", "state": "guard-and-regression-added", "optional": false}
  ],
  "preconditions": [
    {"key": "root-parent-absence-causes-branch-failure", "value": true, "evaluator": "evidence"},
    {"key": "current-owner-bindings-observed", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-baseline-observed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "root-parent-guard-installed", "value": true, "evaluator": "evidence"},
    {"key": "assignment-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "invalid-nonlocal-diagnostic-retained", "value": true, "evaluator": "evidence"},
    {"key": "nested-nonlocal-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-assignment-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-guard-and-regression",
      "instruction": "Review the public diff: the parent guard precedes the unsafe branch, independent diagnostics remain enabled, the regression includes an assignment, and existing expectations are retained. Runtime assurance is supplied by the validate Action.",
      "evidence_refs": ["pylint-dev/pylint:8735:fix", "pylint-dev/pylint:8735:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8735:repair:33d3f22b767e"],
  "evidence_refs": ["pylint-dev/pylint:8735:fix", "pylint-dev/pylint:8735:regression"],
  "read_set": ["role:assignment-scope-checker", "role:scope-diagnostic-fixtures"],
  "write_set": ["role:assignment-scope-checker", "role:scope-diagnostic-fixtures"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:4e26a5bccbfef931bbba5ba0"
}
```
