# Merged parent guard

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8735:fix",
  "source_id": "pylint-dev/pylint:8735:repair:33d3f22b767e",
  "available_at": "2023-06-06T18:57:38Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/checkers/variables.py changed 'nonlocals_with_same_name = any(' to 'nonlocals_with_same_name = node.scope().parent and any(' before iterating over scope.body for nodes.Nonlocal. This prevents the later enclosing-scope branch when the root scope lacks a parent. The new doc/whatsnew/fragments/8735.other says 'Fix a crash when a nonlocal is defined at module-level' and 'Closes #8735'. The artifact establishes the implementation and closure statement; contemporaneous historical CI execution is unknown."
}
```
