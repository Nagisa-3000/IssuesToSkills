# Original reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:441:body",
  "source_id": "PyCQA/pyflakes:441:repair:4a807d45f9dd",
  "available_at": "2019-03-19T10:38:28Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied `from typing import TypeVar`, a class IdClass defining `Y = TypeVar('Y')`, and `def id(self, x: Y) -> Y: return x`. The reported command was `pyflakes t.py`; its reported output was `t.py:7: undefined name 'Y'`. The reporter stated that MyPy did not complain. These are original-report observations; this package has not independently executed that historical command or comparison."
}
```
