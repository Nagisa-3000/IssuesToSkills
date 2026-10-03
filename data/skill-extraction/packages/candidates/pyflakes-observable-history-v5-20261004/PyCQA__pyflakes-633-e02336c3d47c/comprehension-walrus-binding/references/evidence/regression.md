# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:633:regression",
  "source_id": "PyCQA/pyflakes:633:repair:e02336c3d47c",
  "available_at": "2022-05-30T16:20:13Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_other.py added test_assign_expr_generator_scope and test_assign_expr_nested to TestUnusedAssignment, both skipped below Python 3.8. The first called self.flakes on if (any((y := x[0]) for x in [[True]])): print(y). The second called self.flakes on if ([(y:=x) for x in range(4) if [(z:=q) for q in range(4)]]): followed by print(y) and print(z). Neither supplied expected diagnostics. These are historical assertions available at the repair commit; their execution at that time is not supplied."
}
```
