# Add a name-specific nonlocal guard and paired assertions

Apply only after compatible current scope semantics have been established. Preserve the result of earlier candidate resolution. Before the exception-handler assignment filter, return that result if a declaration in the queried name's frame explicitly lists that name.

The historical implementation used:

```python
if any(
    isinstance(child, nodes.Nonlocal) and node.name in child.names
    for child in node.frame(future=True).get_children()
):
    return found_nodes
```

This is historical API syntax, not permission to assume the same API in a current checkout.

Add a fixture with an initialized enclosing name, a same-name `nonlocal`, a `try` read and handler increment. Add a negative control with `nonlocal unrelated` but a local assignment to the queried name in the handler. Expect the first diagnostic to disappear and the second to remain. Preserve other diagnostic expectations; adjust coordinates only where fixture insertion changes them.

```arex-contract-v4
{
  "id": "workflow:verified-history:88758c6085df4be35e45f76d:repair",
  "intent": "Correct the filtering exemption without suppressing genuine local errors.",
  "mechanism": "Bypass only the later exception-handler assignment filtering for a name explicitly declared nonlocal in its current frame.",
  "semantic_role": "name-specific-nonlocal-repair",
  "owner_role": "assignment-filter",
  "kind": "edit",
  "operation": "Edit the bound filter owner and diagnostic fixtures to add the narrowly scoped guard and positive/negative regression assertions.",
  "inputs": [
    {"name": "diagnosis", "semantic_role": "scope-filter-diagnosis", "artifact_kind": "anchored-review", "language": "python", "scope": "current-public-checkout", "phase": "pre-edit", "state": "mechanism-confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "candidate", "semantic_role": "nonlocal-filter-candidate", "artifact_kind": "checkout-change", "language": "python", "scope": "current-public-checkout", "phase": "post-edit", "state": "awaiting-validation", "optional": false}
  ],
  "preconditions": [
    {"key": "scope-filter-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "regression-owner-located", "value": true, "evaluator": "file_exists", "description": "role:assignment-regression-suite"}
  ],
  "effects": [
    {"key": "name-specific-nonlocal-guard-installed", "value": true, "evaluator": "evidence"},
    {"key": "paired-regression-assertions-installed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unrelated-nonlocal-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-control-flow-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "queried-name-explicitly-nonlocal-in-frame", "value": false, "evaluator": "evidence"},
    {"key": "compatible-frame-semantics", "value": false, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-narrow-guard-and-tests",
      "instruction": "Review the current diff: the guard matches the queried name in its own frame, returns the earlier candidate result before handler filtering, and adds paired assertions without removing existing diagnostic expectations.",
      "evidence_refs": ["pylint-dev/pylint:5965:fix", "pylint-dev/pylint:5965:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5965:repair:025200c1fdb5"],
  "evidence_refs": ["pylint-dev/pylint:5965:fix", "pylint-dev/pylint:5965:regression"],
  "read_set": ["role:assignment-filter", "role:scope-frame", "role:assignment-regression-suite"],
  "write_set": ["role:assignment-filter", "role:assignment-regression-suite"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:88758c6085df4be35e45f76d"
}
```
