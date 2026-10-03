# Original report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:561:body",
  "source_id": "PyCQA/pyflakes:561:repair:13cad915e6b1",
  "available_at": "2020-06-25T12:54:24Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter described a false-positive regression in PyFlakes 2.2.0, not 2.1.1: renamed Literal imports from typing or typing_extensions led string arguments to be treated as forward references and caused F821 undefined name 'none' through flake8. The supplied example imports typing as ty and Literal from typing_extensions as ty_Literal, decorates request with @ty.overload, and annotates decoder with ty_Literal[\"none\"]. This is the reporter's observation; no independently executed reproduction is supplied in this entry."
}
```
