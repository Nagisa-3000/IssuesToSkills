# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:434:regression",
  "source_id": "PyCQA/pyflakes:434:repair:232cb1d27ee1",
  "available_at": "2019-03-01T12:37:21Z",
  "kind": "historical_regression_assertions",
  "observation": "The test diff added test_overload_with_multiple_decorators and test_overload_in_class in the type-annotation suite. The first used @dec above @overload on two declarations, followed by an implementation decorated with @dec. The second used a module-level typing.overload import for two class methods followed by an implementation. Both called self.flakes with no expected diagnostics. The adjacent test_not_a_typing_overload remained visible as context. The supplied historical record establishes assertions available at the commit, not historical test execution results."
}
```
