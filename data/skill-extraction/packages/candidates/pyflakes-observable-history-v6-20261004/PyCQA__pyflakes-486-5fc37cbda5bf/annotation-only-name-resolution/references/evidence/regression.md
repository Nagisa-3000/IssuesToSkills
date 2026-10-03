```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:486:regression",
  "source_id": "PyCQA/pyflakes:486:repair:5fc37cbda5bf",
  "available_at": "2020-09-28T18:06:43Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied test diff asserts UndefinedName for T: object followed by def f(t: T), but no diagnostic for def g(t: 'T'). With from __future__ import annotations, it asserts no diagnostic for either form. Added unused-annotation tests assert no warning for module/class annotation-only declarations and for an annotation-only local, the latter accompanied by a TODO that it should eventually report UnusedVariable. A local x: int followed by unused x = 3 asserts one UnusedVariable. Surrounding shown assertions retain ForwardAnnotationSyntaxError for malformed string annotations. These are assertions available at the historical commit; historical execution results are unknown."
}
```
