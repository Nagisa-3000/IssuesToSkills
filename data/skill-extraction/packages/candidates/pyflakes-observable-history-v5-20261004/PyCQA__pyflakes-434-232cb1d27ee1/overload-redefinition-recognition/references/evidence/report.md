# Original report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:434:body",
  "source_id": "PyCQA/pyflakes:434:repair:232cb1d27ee1",
  "available_at": "2019-02-22T13:52:28Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report stated that the function case had been fixed in #320 but class-local functions and multiple decorators still triggered F811. One example imported overload from typing at module scope and defined three class-local utf8 overload signatures followed by an implementation; reported F811 diagnostics identified successive redefinitions. Another example used @overload above @do_nothing on three module-level utf8 signatures followed by an implementation, again reporting successive F811 diagnostics. These are supplied report observations, not newly executed reproductions."
}
```
