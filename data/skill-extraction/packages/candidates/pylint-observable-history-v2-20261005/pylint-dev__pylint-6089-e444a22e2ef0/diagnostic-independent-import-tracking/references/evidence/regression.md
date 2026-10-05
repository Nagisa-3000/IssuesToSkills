# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6089:regression",
  "source_id": "pylint-dev/pylint:6089:repair:e444a22e2ef0",
  "available_at": "2022-04-03T14:26:48Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed diff extends tests/functional/u/unused/unused_import_everything_disabled.py, whose docstring states unused-import should not be emitted when everything else is disabled. It adds the #6089 reference, from math import e, pi, and class MyClass with e = float(e) and pi = pi. The class docstring says using the same names for class attributes as imports is important. Existing from os import environ and iteration over environ.items() remain. These are committed assertions available at the historical revision; the supplied historical evidence does not establish historical test execution."
}
```
