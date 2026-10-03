# Historical original report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:395:body",
  "source_id": "PyCQA/pyflakes:395:repair:066ba4a93c10",
  "available_at": "2018-12-29T09:41:19Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter specified Python 3.7.1 and pyflakes 2.0.0. Module code `a: int = 2` followed by `print(__annotations__)` reportedly produced `t.py:3: undefined name '__annotations__'`. The report cited PEP 526's module/class annotation storage, noted that __annotations__ was absent from builtin_vars, and suggested adding it to _MAGIC_GLOBALS, then containing __file__, __builtins__, and WindowsError. This is a reported reproduction and proposed repair location, not historical execution of the later fix."
}
```
