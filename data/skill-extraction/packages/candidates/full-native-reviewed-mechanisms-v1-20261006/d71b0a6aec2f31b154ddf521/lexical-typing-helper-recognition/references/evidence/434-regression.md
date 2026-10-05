# Issue 434 committed assertions

```arex-evidence-v4
{"id":"PyCQA/pyflakes:434:regression","source_id":"PyCQA/pyflakes:434:repair:232cb1d27ee1","available_at":"2019-03-01T12:37:21Z","kind":"historical_regression_assertions","observation":"The test_type_annotations.py diff adds test_overload_in_class using a module-level overload import and two decorated methods followed by implementation, and test_overload_with_multiple_decorators using identity dec above overload on two declarations and dec on implementation. Both self.flakes calls expect no diagnostics. Existing test_not_a_typing_overload appears in adjacent context. No dedicated new shadowing assertion is shown. Historical execution is unknown."}
```
