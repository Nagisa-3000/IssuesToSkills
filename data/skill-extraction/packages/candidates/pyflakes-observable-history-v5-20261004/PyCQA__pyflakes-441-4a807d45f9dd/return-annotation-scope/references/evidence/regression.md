# Regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:441:regression",
  "source_id": "PyCQA/pyflakes:441:repair:4a807d45f9dd",
  "available_at": "2019-07-03T01:37:22Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff adds two tests to pyflakes/test/test_type_annotations.py, each gated by skipIf(version_info < (3,), 'new in Python 3'). test_return_annotation_is_class_scope_variable calls self.flakes on a class with Y = TypeVar('Y') and def t(self, x: Y) -> Y, with no expected messages. test_return_annotation_is_function_body_variable calls self.flakes on a class method def t(self) -> Y whose body assigns Y = 2 and returns Y, expecting m.UndefinedName. These are assertions present at the historical commit; contemporaneous execution status is unknown."
}
```
