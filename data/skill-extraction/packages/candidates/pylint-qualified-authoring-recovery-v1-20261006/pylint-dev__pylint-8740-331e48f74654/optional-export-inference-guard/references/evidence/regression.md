# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8740:regression",
  "source_id": "pylint-dev/pylint:8740:repair:331e48f74654",
  "available_at": "2023-06-06T19:19:41Z",
  "kind": "historical_regression_assertions",
  "observation": "The new tests/functional/u/undefined/undefined_all_variable_edge_case.py describes an edge case where __all__ exists in module locals but cannot be inferred, references tests/functional/n/names_in__all__.py, and contains __all__ += []  # [undefined-variable] on line 5. Its .txt expectation is exactly undefined-variable:5:0:5:7::Undefined variable '__all__':UNDEFINED. These are committed assertions available at the historical revision, not an execution record; historical execution is unknown. Later source qualification is separate validation provenance and does not execute authored Skill cases."
}
```
