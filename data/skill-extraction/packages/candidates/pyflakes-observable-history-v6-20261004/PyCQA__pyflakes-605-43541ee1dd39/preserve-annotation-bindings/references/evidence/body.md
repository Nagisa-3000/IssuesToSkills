# Reported mechanism and reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:605:body",
  "source_id": "PyCQA/pyflakes:605:repair:43541ee1dd39",
  "available_at": "2021-01-04T22:37:15Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter attributed the regression to #535 and described an annotation clobbering the __all__ ExportBinding, causing imports no longer to be marked used. The reproduction imports TYPE_CHECKING and List from typing and z from y; if not TYPE_CHECKING it assigns __all__ = (\"z\",), otherwise it declares __all__: List[str]. The report tentatively suggested making Annotated a setdefault on the latest namespace; that suggestion is not the merged implementation."
}
```
