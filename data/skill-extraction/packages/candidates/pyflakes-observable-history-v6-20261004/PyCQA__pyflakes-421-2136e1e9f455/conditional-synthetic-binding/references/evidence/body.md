# Public reproduction and traceback

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:421:body",
  "source_id": "PyCQA/pyflakes:421:repair:2136e1e9f455",
  "available_at": "2019-01-30T16:22:37Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report identifies Pyflakes 2.1.0 with Python 3.6.7 on Linux. Its reproduction imports foo as underscore and defines x with two doctest calls to x(). Running PYFLAKES_DOCTEST=1 pyflakes t.py reportedly crashes. The traceback reaches handleDoctests calling self.addBinding(None, Builtin('_')), addBinding calling self.getParent(value.source), and getParent accessing node.parent, ending in AttributeError on None. This records the supplied report; no new execution was performed."
}
```
