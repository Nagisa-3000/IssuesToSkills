# Added regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:395:regression",
  "source_id": "PyCQA/pyflakes:395:repair:066ba4a93c10",
  "available_at": "2019-01-01T13:10:34Z",
  "kind": "historical_regression_assertions",
  "observation": "The undefined-name test diff adds test_moduleAnnotations decorated with @skipIf(version_info < (3, 6), 'new feature in 3.6'). Its docstring says module-scope __annotations__ should not emit an undefined-name warning on Python versions greater than or equal to 3.6. The assertion is self.flakes('__annotations__'). Existing surrounding WindowsError and __file__ magic-global tests remain context. This is a regression assertion available at the historical commit; historical execution is not supplied."
}
```
