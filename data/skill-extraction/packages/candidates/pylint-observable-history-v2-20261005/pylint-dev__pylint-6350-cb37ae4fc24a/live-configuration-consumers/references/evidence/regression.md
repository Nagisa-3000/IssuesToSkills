# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6350:regression",
  "source_id": "pylint-dev/pylint:6350:repair:cb37ae4fc24a",
  "available_at": "2022-04-16T19:20:47Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed diff added an empty __init__.py and identical file_one.py and file_two.py under tests/regrtest_data/duplicate_code/ignore_imports. Each contained imports of argparse, math, os, random, and sys. TestSimilarCodeChecker.test_ignore_imports in tests/test_similar.py called _runtest with [path, '-e=duplicate-code', '-d=unused-import', '--ignore-imports=y'] and code=0. These assertions were available at the historical commit; their contemporaneous execution status is unknown."
}
```
