# Public report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:771:body",
  "source_id": "PyCQA/pyflakes:771:repair:f2671ffe1785",
  "available_at": "2023-04-20T08:52:06Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied an if/else function and a match function, each defining fun separately in alternative bodies and returning fun afterward. The match cases were True and False. The reported warning was \"redef.py:24:13: redefinition of unused 'fun' from line 19\" for the second match-case definition. The reported environment was Pyflakes 3.0.1 with Python 3.10.8 on Linux. This is a reported reproduction, not an execution performed by this package."
}
```
