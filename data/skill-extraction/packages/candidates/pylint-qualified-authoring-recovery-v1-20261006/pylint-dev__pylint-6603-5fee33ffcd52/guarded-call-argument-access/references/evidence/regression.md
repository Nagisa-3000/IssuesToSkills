# Committed empty-call regression assertion

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6603:regression",
  "source_id": "pylint-dev/pylint:6603:repair:5fee33ffcd52",
  "available_at": "2022-05-13T13:40:25Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed diff appends an issue-6603 regression to tests/functional/u/unnecessary/unnecessary_list_index_lookup.py: `for i, num in enumerate():  # raises TypeError, but shouldn't crash pylint` followed by `pass`. Existing context includes a nested-unpacking loop over enumerate(pairs). This is an available historical assertion; historical test execution and CI results are unknown."
}
```
