# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:561:regression",
  "source_id": "PyCQA/pyflakes:561:repair:13cad915e6b1",
  "available_at": "2021-10-05T22:44:29Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied diff in pyflakes/test/test_type_annotations.py adds test_aliased_import, documented as detecting typing imported under another name. Its self.flakes input imports typing as t, defines two @t.overload functions named f with type comments (None) -> None and (int) -> int, and then defines a concrete f returning s. No expected diagnostics are passed to self.flakes. The neighboring test_not_a_typing_overload is visible as context, but its full body is not supplied. These assertions are available at the historical repair commit; original execution status is unknown. This regression does not itself test the reported Literal reproduction."
}
```
