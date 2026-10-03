# Original public report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:470:body",
  "source_id": "PyCQA/pyflakes:470:repair:ee1eb0670a47",
  "available_at": "2019-09-23T09:05:30Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report states that synchronous @overload functions are supported but async ones are not. Its example imports overload from typing and defines two annotated synchronous overload declarations plus an implementation of f, followed by two annotated async overload declarations plus an async implementation of g. The reported invocation is 'python -m pyflakes .', with diagnostics \"18:1 redefinition of unused 'g' from line 14\" and \"22:1 redefinition of unused 'g' from line 18\". This is the supplied reported reproduction, not a newly executed check."
}
```
