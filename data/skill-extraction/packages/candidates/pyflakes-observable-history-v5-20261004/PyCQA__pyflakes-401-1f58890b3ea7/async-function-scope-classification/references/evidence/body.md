# Original reproduction and traceback

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:401:body",
  "source_id": "PyCQA/pyflakes:401:repair:1f58890b3ea7",
  "available_at": "2019-01-01T20:31:28Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report supplied `class foo: pass` followed by `async def func(foo: foo): pass`. The traceback included deferred function handling, ARGUMENTS, ARG, `Argument(node.arg, self.getScopeNode(node))`, addBinding, and getParent, ending at `node = node.parent` with AttributeError on Module. The reported environment was Debian unstable, Python 3.7, and pyflakes revision 066ba4a93c1077f9154d6ff3806fe1e3a66843a1. The reporter suspected revision 9dd73ec54411a563410872b47e76f0f89f34ecfe introduced the bug; that attribution was not independently established in the supplied evidence. The traceback is a reported execution, not a new reproduction performed by this package."
}
```
