# Merged collector change

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:507:fix",
  "source_id": "PyCQA/pyflakes:507:repair:be8803601900",
  "available_at": "2020-01-17T20:24:48Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff in pyflakes/checker.py adds, inside the existing nonlegacy argument-processing branch, an if PY38_PLUS guard followed by for arg in node.args.posonlyargs, args.append(arg.arg), and annotations.append(arg.annotation). This precedes the retained for arg in node.args.args + node.args.kwonlyargs loop. The diff records collection of positional-only names and annotations without removing ordinary or keyword-only collection; it is not a historical execution log."
}
```
