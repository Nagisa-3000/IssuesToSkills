# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:486:regression",
  "source_id": "PyCQA/pyflakes:486:repair:5fc37cbda5bf",
  "available_at": "2020-09-28T18:06:43Z",
  "kind": "historical_regression_assertions",
  "observation": "The test_type_annotations.py diff added assertions that 'T: object' followed by a bare parameter annotation T emits UndefinedName, while quoted 'T' emits no diagnostic. With 'from __future__ import annotations', both forms emit no diagnostic. Unused module/class annotations emit no diagnostic. An unused function-local annotation also emits no diagnostic, with a TODO that it should emit UnusedVariable. A local annotation followed by 'x = 3' expects one UnusedVariable. Surrounding assertions retain ForwardAnnotationSyntaxError for malformed strings. These are assertions available at the repair commit; historical execution is unknown."
}
```
