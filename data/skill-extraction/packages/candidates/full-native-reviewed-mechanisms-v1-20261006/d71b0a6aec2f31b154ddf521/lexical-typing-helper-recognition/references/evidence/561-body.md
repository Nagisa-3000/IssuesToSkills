# Issue 561 report

```arex-evidence-v4
{"id":"PyCQA/pyflakes:561:body","source_id":"PyCQA/pyflakes:561:repair:13cad915e6b1","available_at":"2020-06-25T12:54:24Z","kind":"issue_body_as_of_cutoff","observation":"The reporter compared PyFlakes 2.2.0 with 2.1.1 and described renamed Literal imports causing strings to be treated as forward references, producing F821 undefined name none. The snippet imports typing as ty, imports Literal from typing_extensions as ty_Literal, decorates request with ty.overload and uses ty_Literal[\"none\"]. This is a report observation, not independent reproduction or proof that module-receiver repair establishes every direct-import alias claim."}
```
