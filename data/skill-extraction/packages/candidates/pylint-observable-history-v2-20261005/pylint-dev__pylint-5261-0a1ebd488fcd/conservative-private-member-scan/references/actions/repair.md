# Guard the scan and add the regression

Edit only after inspection establishes the mechanism and current requirements permit conservative suppression.

The historical equivalent is:

```python
if isinstance(child, nodes.Attribute):
    if not isinstance(child.expr, nodes.Name):
        break
    if child.attrname == assign_name.name and child.expr.name in (
        "self",
        "cls",
        node.name,
    ):
        break
```

Adapt identifiers to the current owner, not semantics. Retain bare-name matching, argument exclusions, and loop-else warning emission. Add a public private-class-variable fixture accessed through `self.__class__` in a method accepting `self`.

The non-Name branch breaks before comparing attribute names. Do not replace it with `continue` or broad exception handling. Preservation predicates are obligations to validate, not proof from a small diff.

```arex-contract-v4
{
  "id": "workflow:verified-history:4244f18e715c9b86c7cef8e0:repair",
  "intent": "Guard unsafe receiver-name access and capture the chained-receiver regression.",
  "mechanism": "A receiver-type guard precedes name-only access; a non-Name receiver conservatively terminates the candidate search.",
  "semantic_role": "guard-and-regression-edit",
  "owner_role": "private-usage-scan",
  "operation": "Edit the bound checker to guard receiver type and break for non-Name receivers; add the chained private-member fixture to bound public regression resources.",
  "kind": "edit",
  "inputs": [
    {"name": "inspection", "semantic_role": "private-scan-binding-evidence", "artifact_kind": "review-record", "language": "python", "scope": "private-member-analysis", "phase": "inspection", "state": "receiver-assumption-established", "optional": false}
  ],
  "outputs": [
    {"name": "edited-snapshot", "semantic_role": "guarded-private-scan-and-regression", "artifact_kind": "source-snapshot", "language": "python", "scope": "private-member-analysis", "phase": "repair", "state": "guard-and-regression-present", "optional": false}
  ],
  "preconditions": [
    {"key": "receiver-assumption-established", "value": true, "evaluator": "evidence"},
    {"key": "role:private-usage-scan", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:private-usage-regressions", "value": true, "evaluator": "file_exists"},
    {"key": "conservative-suppression-acceptable", "value": true, "evaluator": "evidence", "description": "Current public requirements permit warning suppression when this scan encounters unresolved compound receivers."}
  ],
  "effects": [
    {"key": "guard-and-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "simple-receiver-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "argument-exclusion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-unused-emission-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-passed"],
  "oracle": [
    {
      "id": "review-guard-and-fixture",
      "instruction": "Review the public diff: type guard precedes receiver.name, the non-Name branch breaks before attribute-name comparison, original simple-name logic and exclusions remain, and the public fixture declares a private class variable accessed through self.__class__ inside a method accepting self.",
      "evidence_refs": ["pylint-dev/pylint:5261:fix", "pylint-dev/pylint:5261:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5261:repair:0a1ebd488fcd"],
  "evidence_refs": ["pylint-dev/pylint:5261:fix", "pylint-dev/pylint:5261:regression"],
  "read_set": ["role:private-usage-scan", "role:private-usage-regressions"],
  "write_set": ["role:private-usage-scan", "role:private-usage-regressions"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:4244f18e715c9b86c7cef8e0"
}
```

`public-validation-passed` is a freshness-sensitive observation. It is distinct from the preserved behavior assurances and Workflow invariants.
