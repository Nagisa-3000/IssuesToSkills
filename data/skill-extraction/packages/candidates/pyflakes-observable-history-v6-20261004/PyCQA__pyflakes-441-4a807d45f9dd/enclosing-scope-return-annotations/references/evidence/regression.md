# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:441:regression",
  "source_id": "PyCQA/pyflakes:441:repair:4a807d45f9dd",
  "available_at": "2019-07-03T01:37:22Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_type_annotations.py added two tests guarded by `@skipIf(version_info < (3,), 'new in Python 3')`. `test_return_annotation_is_class_scope_variable` defines class-level `Y = TypeVar('Y')` and `def t(self, x: Y) -> Y: return x`, then calls `self.flakes` without expected diagnostics. `test_return_annotation_is_function_body_variable` defines `def t(self) -> Y`, assigns `Y = 2` inside the function body, and calls `self.flakes` with `m.UndefinedName`. These are assertions available at the historical commit; historical execution status is unknown from this entry."
}
```
