# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:744:regression",
  "source_id": "PyCQA/pyflakes:744:repair:e0d7a6be8959",
  "available_at": "2022-11-24T16:51:46Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied diff in pyflakes/test/test_other.py added TestIncompatiblePrintOperator.test_print_augmented_assign with the comment 'nonsense, but shouldn't crash pyflakes' and invocation self.flakes('print += 1'). The nearby existing test_print_function_assignment was documented as a valid assignment tested for false positives. These assertions were available at the historical commit; no historical execution result is supplied."
}
```
