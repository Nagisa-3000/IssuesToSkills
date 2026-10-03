# Original report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:574:body",
  "source_id": "PyCQA/pyflakes:574:repair:c23a81037d4f",
  "available_at": "2020-08-16T18:20:15Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied `from typing import Annotated` followed by `Annotated[int, '>1']` and reported `./pyflakes.py:3:16 syntax error in forward annotation '>1'`. This is a reported diagnostic associated with an Annotated metadata string, not an independently supplied historical execution log."
}
```
