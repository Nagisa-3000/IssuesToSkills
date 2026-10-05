# Guard and add regression

Reject non-Name inner bases before reading their `.name`. Keep the loop-target guard and dictionary-expression comparison. The historical short-circuit condition included:

```python
not isinstance(node.target, nodes.AssignName)
or not isinstance(value.value, nodes.Name)
or node.target.name != value.value.name
or iterating_object_name != subscript.value.as_string()
```

Adapt identifiers only after binding the corresponding current branch. Do not skip Attribute nodes globally or suppress AttributeError broadly.

Add a public static-analysis fixture with this semantic shape:

```python
class Holder:
    pass

mapping = {}
holder = Holder()
for item in mapping.items():
    holder.item = item
    print(mapping[holder.item[0]])
```

The checker must analyze the loop body even though the mapping is empty. Follow current fixture conventions for unrelated-message suppression; do not weaken prior diagnostic expectations.

```arex-contract-v4
{
  "id": "workflow:verified-history:7c6d31165b0fa4f2628a0ec0:repair",
  "intent": "Guard the unsafe field read and add a focused public regression.",
  "mechanism": "Place short-circuit Name-type discrimination before the inner-base name comparison and retain the attribute-subscript analysis input.",
  "semantic_role": "guarded-lookup-repair",
  "owner_role": "lookup-checker",
  "operation": "Edit the bound checker branch and public fixture: reject non-Name inner bases before field access, preserve existing conditions, and add attribute assignment followed by a nested dictionary lookup regression.",
  "kind": "edit",
  "inputs": [
    {
      "name": "confirmed-bindings",
      "semantic_role": "lookup-repair-bindings",
      "artifact_kind": "binding-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "mechanism-confirmed"
    }
  ],
  "outputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "guarded-lookup-candidate",
      "artifact_kind": "code-and-regression",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "preconditions": [
    {"key": "mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:lookup-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:lookup-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "unsafe-name-read-guarded", "value": true, "evaluator": "evidence"},
    {"key": "attribute-subscript-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "supported-name-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-negative-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-guard-and-fixture",
      "instruction": "Review the current diff. Confirm the Name-type rejection dominates the inner-base name read through short circuiting, existing conditions remain, the public attribute-subscript fixture is present, and prior diagnostic expectations are not weakened.",
      "evidence_refs": ["pylint-dev/pylint:6557:fix", "pylint-dev/pylint:6557:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:6557:repair:5fcccc13f1f7"],
  "evidence_refs": ["pylint-dev/pylint:6557:fix", "pylint-dev/pylint:6557:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:7c6d31165b0fa4f2628a0ec0",
  "read_set": ["role:lookup-checker", "role:lookup-regression-suite"],
  "write_set": ["role:lookup-checker", "role:lookup-regression-suite"],
  "invalidates": ["public-validation-observed"]
}
```

Effects require current diff evidence. Preservation requires review and public validation, not merely matching predicate names. This modifying Action retains [Validate public behavior](validate.md).
