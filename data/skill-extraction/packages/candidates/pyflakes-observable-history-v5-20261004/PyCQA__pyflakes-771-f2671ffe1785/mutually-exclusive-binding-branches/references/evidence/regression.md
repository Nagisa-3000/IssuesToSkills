# Added regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:771:regression",
  "source_id": "PyCQA/pyflakes:771:repair:f2671ffe1785",
  "available_at": "2023-04-25T23:37:22Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff added TestMatch.test_defined_in_different_branches in pyflakes/test/test_match.py. It calls self.flakes on a function f(x) containing match x, case 1 with `def y(): pass`, case _ with `def y(): print(1)`, and `return y` after the match. No expected diagnostic arguments are supplied. This records a no-diagnostic regression assertion available at the historical commit, not a historical execution result. Later changed-test-only qualification is recorded separately in provenance."
}
```
