# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:633:regression",
  "source_id": "PyCQA/pyflakes:633:repair:e02336c3d47c",
  "available_at": "2022-05-30T16:20:13Z",
  "kind": "historical_regression_assertions",
  "observation": "The pyflakes/test/test_other.py diff adds test_assign_expr_generator_scope and test_assign_expr_nested to TestUnusedAssignment, each skipped when version_info < (3, 8). The first supplies if (any((y := x[0]) for x in [[True]])): followed by print(y). The second supplies if ([(y:=x) for x in range(4) if [(z:=q) for q in range(4)]]): followed by print(y) and print(z). Both call self.flakes without expected diagnostic arguments, asserting diagnostic-free analysis. These assertions were available at the historical commit; their historical execution status is unknown from this entry."
}
```
