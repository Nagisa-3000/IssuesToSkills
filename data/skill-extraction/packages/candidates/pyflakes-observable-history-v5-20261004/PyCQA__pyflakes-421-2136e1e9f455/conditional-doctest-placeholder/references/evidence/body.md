# Reported reproduction and traceback

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:421:body",
  "source_id": "PyCQA/pyflakes:421:repair:2136e1e9f455",
  "available_at": "2019-01-30T16:22:37Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report identified Pyflakes 2.1.0, Python 3.6.7 on Linux. The source imported foo as _ and defined x with two >>> x() doctest examples. The reported command was PYFLAKES_DOCTEST=1 pyflakes t.py. Its traceback showed handleDoctests calling self.addBinding(None, Builtin('_')), addBinding calling self.getParent(value.source), and getParent evaluating node.parent before raising AttributeError: 'NoneType' object has no attribute 'parent'. This is a reported historical run; no current reproduction execution is supplied."
}
```
