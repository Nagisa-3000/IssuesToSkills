# Public reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:395:body",
  "source_id": "PyCQA/pyflakes:395:repair:066ba4a93c10",
  "available_at": "2018-12-29T09:41:19Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used Python 3.7.1 and pyflakes 2.0.0. For module code a: int = 2 followed by print(__annotations__), the reported diagnostic was t.py:3: undefined name '__annotations__'. The report cites PEP 526's module/class annotation mapping and proposes adding the name to _MAGIC_GLOBALS because it is not in builtin_vars. This is reported behavior and a proposed solution, not independently recorded historical test execution."
}
```
