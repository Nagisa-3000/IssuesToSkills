# Original report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:561:body",
  "source_id": "PyCQA/pyflakes:561:repair:13cad915e6b1",
  "available_at": "2020-06-25T12:54:24Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter describes a false positive in PyFlakes 2.2.0, absent in 2.1.1: Literal renamed at import from typing or typing_extensions causes string arguments to be interpreted as unresolved forward references, producing F821 undefined name 'none'. The supplied reproduction uses import typing as ty, from typing_extensions import Literal as ty_Literal, @ty.overload, and decoder: ty_Literal[\"none\"] = \"none\". This is the original report, not a supplied independent historical execution record."
}
```
