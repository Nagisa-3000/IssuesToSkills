# Historical merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3798:fix",
  "source_id": "pylint-dev/pylint:3798:repair:1a1dea5d6bc2",
  "available_at": "2020-10-10T08:09:42Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/utils.py, is_postponed_evaluation_enabled previously set name = 'annotations', obtained module = node.root(), queried module.locals.get(name), and checked that the first binding was an astroid.ImportFrom with modname '__future__'. The repair retained module = node.root() and returned 'annotations' in module.future_imports. The ChangeLog stated 'Fix a bug with postponed evaluation when using aliases for annotations' and 'Close #3798'. This records the merged implementation and closure wording; historical CI execution is unknown."
}
```
