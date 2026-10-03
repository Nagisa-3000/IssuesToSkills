# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:771:fix",
  "source_id": "PyCQA/pyflakes:771",
  "available_at": "2023-04-25T23:37:22Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff modified getAlternatives(n) in pyflakes/checker.py. The ast.If result remained return [n.body]. The ast.Try condition changed from if to elif while retaining return [n.body + n.orelse] + [[hdl] for hdl in n.handlers]. The added condition was 'elif sys.version_info >= (3, 10) and isinstance(n, ast.Match):' with 'return [mc.body for mc in n.cases]'. This exposes separate case bodies and guards ast.Match access by Python version."
}
```
