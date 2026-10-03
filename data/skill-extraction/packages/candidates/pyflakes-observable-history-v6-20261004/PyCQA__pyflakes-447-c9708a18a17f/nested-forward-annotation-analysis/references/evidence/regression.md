# Regression assertions at the repair commit

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:447:regression",
  "source_id": "PyCQA/pyflakes:447:repair:c9708a18a17f",
  "available_at": "2020-02-14T21:31:45Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied test diff added no-diagnostic self.flakes assertions for Optional['Queue[str]'] return annotations; Literal['some string'] imported from typing and typing_extensions; typing Literal with two string values; a wholly quoted outer annotation containing a nested quoted Queue expression; and partially quoted annotations under from __future__ import annotations. It extended overload coverage with import typing_extensions and qualified typing_extensions.overload decorators followed by an implementation. Version guards were present for Python 3 annotation tests and Python 3.7 postponed annotations. These assertions were available at the historical commit; their historical execution status is unknown from the supplied core evidence."
}
```
