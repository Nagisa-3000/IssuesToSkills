# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6594:fix",
  "source_id": "pylint-dev/pylint:6594:repair:f6479fd320e7",
  "available_at": "2022-05-13T18:48:10Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff imported `is_node_in_type_annotation_context` into pylint/checkers/typecheck.py and added an early return when `is_postponed_evaluation_enabled(node)` and `is_node_in_type_annotation_context(node)` both held, before `node.expr.infer()`. ChangeLog and doc/whatsnew/2.14.rst stated not to emit no-member inside type annotations with `from __future__ import annotations` and marked issue 6594 closed. The authoritative SourceRecord identifies PR 6608 and revision f6479fd320e78c0f8c7e4ab0751c302e656c64bf as the verified repair. Original historical CI/test execution is unknown."
}
```
