# Merged classifier implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:771:fix",
  "source_id": "PyCQA/pyflakes:771:repair:f2671ffe1785",
  "available_at": "2023-04-25T23:37:22Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py changed getAlternatives' ast.Try condition from if to elif, retained its return expression [n.body + n.orelse] + [[hdl] for hdl in n.handlers], and added 'elif sys.version_info >= (3, 10) and isinstance(n, ast.Match):' returning '[mc.body for mc in n.cases]'. The ast.If return remained '[n.body]'. This is the implementation at the verified repair revision; the entry contains no test-run transcript."
}
```
