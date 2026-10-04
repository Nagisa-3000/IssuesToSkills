# Public scope reproduction and traceback

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:401:body",
  "source_id": "PyCQA/pyflakes:401:repair:1f58890b3ea7",
  "available_at": "2019-01-01T20:31:28Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report reproduced a crash with class foo: pass followed by async def func(foo: foo): pass. It reported Debian unstable, Python 3.7, and pyflakes revision 066ba4a93c1077f9154d6ff3806fe1e3a66843a1. Deferred function analysis reached argument handling: ARG called addBinding(node, Argument(node.arg, self.getScopeNode(node))); addBinding called getParent(value.source), which accessed node.parent on a Module. The report suspected introducing revision 9dd73ec54411a563410872b47e76f0f89f34ecfe; that attribution is reported suspicion, not independently established causality."
}
```
