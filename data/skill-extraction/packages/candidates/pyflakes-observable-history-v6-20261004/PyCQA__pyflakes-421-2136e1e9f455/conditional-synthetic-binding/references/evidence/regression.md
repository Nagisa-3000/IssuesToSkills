# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:421:regression",
  "source_id": "PyCQA/pyflakes:421:repair:2136e1e9f455",
  "available_at": "2019-07-09T13:37:43Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied diff adds test_globalUnderscoreInDoctest to pyflakes/test/test_doctests.py. It calls self.flakes on code importing ugettext from gettext as underscore and defining doctest_stuff with a doctest containing >>> pass, with m.UnusedImport as the expected diagnostic. This is an assertion available at the historical commit, not a supplied historical test-run result. It expresses non-crashing doctest analysis and preservation of the unused-import diagnostic."
}
```
