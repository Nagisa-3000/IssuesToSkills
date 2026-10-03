# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:507:fix",
  "source_id": "PyCQA/pyflakes:507:repair:be8803601900",
  "available_at": "2020-01-17T20:24:48Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py inserted `if PY38_PLUS:` and a loop over `node.args.posonlyargs` in the existing non-legacy argument-collection branch. For each positional-only argument, it appended `arg.arg` to `args` and `arg.annotation` to `annotations`. This insertion preceded the unchanged loop over `node.args.args + node.args.kwonlyargs`. The supplied implementation shows the correction and runtime guard; it does not include a historical test execution log."
}
```
