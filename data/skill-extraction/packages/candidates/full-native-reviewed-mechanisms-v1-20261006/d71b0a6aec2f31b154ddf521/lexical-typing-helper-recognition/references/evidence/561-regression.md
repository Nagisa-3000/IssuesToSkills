# Issue 561 committed assertion

```arex-evidence-v4
{"id":"PyCQA/pyflakes:561:regression","source_id":"PyCQA/pyflakes:561:repair:13cad915e6b1","available_at":"2021-10-05T22:44:29Z","kind":"historical_regression_assertions","observation":"The test_type_annotations.py diff adds test_aliased_import. Its self.flakes snippet imports typing as t, defines two t.overload declarations with type comments (None) -> None and (int) -> int, then implementation returning its argument. No diagnostics are expected. This covers aliased overload, not every renamed-Literal claim. No dedicated new shadowing assertion is shown. Historical execution is unknown."}
```
