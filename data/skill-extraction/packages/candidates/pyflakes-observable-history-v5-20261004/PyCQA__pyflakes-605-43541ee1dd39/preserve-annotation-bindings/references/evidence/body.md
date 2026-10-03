# Original report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:605:body",
  "source_id": "PyCQA/pyflakes:605:repair:43541ee1dd39",
  "available_at": "2021-01-04T22:37:15Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report attributed the regression to #535. Its simplified example from numpy/typing/__init__.py imports TYPE_CHECKING and List from typing and z from y, assigns __all__ = (\"z\",) under if not TYPE_CHECKING, and declares __all__: List[str] in the else branch. The report states that the annotation clobbers the __all__ ExportBinding so imports are no longer marked used. Its proposed setdefault-like approach was a suggestion, not the merged implementation."
}
```
