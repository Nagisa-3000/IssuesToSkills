# Regression assertion at the repair commit

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:421:regression",
  "source_id": "PyCQA/pyflakes:421:repair:2136e1e9f455",
  "available_at": "2019-07-09T13:37:43Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_doctests.py added test_globalUnderscoreInDoctest. It called self.flakes on source containing from gettext import ugettext as _, followed by doctest_stuff with a >>> pass example, and supplied m.UnusedImport as the expected diagnostic. This asserts analysis completes and the imported underscore remains unused. The assertion was available at the historical commit; no historical execution result or test command is supplied."
}
```
