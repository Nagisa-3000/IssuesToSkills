# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:771:fix",
  "source_id": "PyCQA/pyflakes:771:repair:f2671ffe1785",
  "available_at": "2023-04-25T23:37:22Z",
  "kind": "historical_merged_implementation",
  "observation": "In pyflakes/checker.py, getAlternatives retained `if isinstance(n, ast.If): return [n.body]`, changed the ast.Try branch from `if` to `elif` while retaining `return [n.body + n.orelse] + [[hdl] for hdl in n.handlers]`, and added `elif sys.version_info >= (3, 10) and isinstance(n, ast.Match): return [mc.body for mc in n.cases]`. This merged implementation treats each match-case body as an alternative and guards the ast.Match reference by Python version. No historical test execution is contained in this entry."
}
```
