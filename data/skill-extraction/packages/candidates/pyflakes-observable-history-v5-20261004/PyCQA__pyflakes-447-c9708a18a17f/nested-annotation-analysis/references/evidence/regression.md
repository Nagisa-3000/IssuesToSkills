# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:447:regression",
  "source_id": "PyCQA/pyflakes:447:repair:c9708a18a17f",
  "available_at": "2020-02-14T21:31:45Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied test_type_annotations.py diff adds self.flakes assertions for Optional['Queue[str]'], Literal['some string'] imported from typing and typing_extensions, Literal['some string', 'foo bar'], the whole-quoted annotation \"Optional['Queue[str]']\", and partial quotation under from __future__ import annotations. It extends the typing_extensions overload test with an import of typing_extensions and qualified @typing_extensions.overload cases. The annotation tests are gated for Python 3 and the future-annotations case for Python 3.7. These are historical test definitions available at the repair commit, not an included historical run log. Execution status at that historical date is unknown from the supplied assertions."
}
```
