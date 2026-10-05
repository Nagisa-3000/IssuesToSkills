# Committed regression

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6810:regression",
  "source_id": "pylint-dev/pylint:6810:repair:44a3d96e1af9",
  "available_at": "2022-06-03T08:54:58Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff adds test_verbose_abbreviation in tests/config/test_find_default_config_files.py. With pop_pylintrc, a temporary directory, fake_home, and a nested package fixture, it changes directory to a/b/c, expects SystemExit from Run([\"--ve\"]), captures output, and asserts that stderr contains 'No config file found, using default configuration'. The comment says this output exists only in verbose mode. This is a committed historical assertion; historical test execution is unknown."
}
```
