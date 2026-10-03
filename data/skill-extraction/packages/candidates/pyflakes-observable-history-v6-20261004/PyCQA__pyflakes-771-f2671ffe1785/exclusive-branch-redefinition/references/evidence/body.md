# Public reproduction report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:771:body",
  "source_id": "PyCQA/pyflakes:771:repair:f2671ffe1785",
  "available_at": "2023-04-20T08:52:06Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used Pyflakes 3.0.1 with Python 3.10.8 on Linux. The supplied examples defined fun separately in if/else branches or in match cases True and False and returned fun afterward. The match example reportedly emitted 'redef.py:24:13: redefinition of unused \u0027fun\u0027 from line 19'; the if/else example was presented as not producing that redefinition warning. This is a historical user report, not a separately recorded test execution."
}
```
