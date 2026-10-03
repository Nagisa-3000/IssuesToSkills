# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:744:regression",
  "source_id": "PyCQA/pyflakes:744:repair:e0d7a6be8959",
  "available_at": "2022-11-24T16:51:46Z",
  "kind": "historical_regression_assertions",
  "observation": "The test_other.py diff adds test_print_augmented_assign in TestIncompatiblePrintOperator. Its comment is 'nonsense, but shouldn’t crash pyflakes' and its assertion is self.flakes('print += 1'). The neighboring test_print_function_assignment is described as a valid assignment tested for false positives. These assertions were available at the repair commit; historical execution results are not supplied."
}
```
