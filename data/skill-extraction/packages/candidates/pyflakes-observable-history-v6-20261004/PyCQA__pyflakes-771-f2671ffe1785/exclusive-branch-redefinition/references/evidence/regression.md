# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:771:regression",
  "source_id": "PyCQA/pyflakes:771:repair:f2671ffe1785",
  "available_at": "2023-04-25T23:37:22Z",
  "kind": "historical_regression_assertions",
  "observation": "The merged diff added TestMatch.test_defined_in_different_branches in pyflakes/test/test_match.py. Its self.flakes call supplied a function f(x) with match x, case 1 defining 'def y(): pass', case _ defining 'def y(): print(1)', and 'return y' after the match. No expected diagnostics were supplied. This records a no-diagnostic assertion available at the historical commit, not historical execution; execution status in this entry is unknown."
}
```
