# Reported reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:771:body",
  "source_id": "PyCQA/pyflakes:771",
  "available_at": "2023-04-20T08:52:06Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter contrasted no_redef(value), defining fun(x, y) in if/else branches and returning fun, with redef(value), defining fun(x, y) in case True and case False of match value and returning fun. The reported warning was \"redef.py:24:13: redefinition of unused 'fun' from line 19\" for the match example. The environment was pyflakes 3.0.1, Python 3.10.8 on Linux. This is a reported reproduction, not an independently recorded execution by this package."
}
```
