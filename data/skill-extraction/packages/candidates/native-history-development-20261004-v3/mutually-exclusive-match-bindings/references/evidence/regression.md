# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:771:regression",
  "source_id": "PyCQA/pyflakes:771",
  "available_at": "2023-04-25T23:37:22Z",
  "kind": "historical_regression_assertions",
  "observation": "The merged diff added TestMatch.test_defined_in_different_branches in pyflakes/test/test_match.py. Its self.flakes call contained def f(x), match x, case 1 with def y(): pass, case _ with def y(): print(1), then return y. No expected diagnostic arguments were supplied. This records the no-diagnostic assertion available at the commit. A historical test execution transcript is not supplied; execution status is unknown."
}
```
