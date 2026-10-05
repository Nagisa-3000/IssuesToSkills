# Merged guard implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6603:fix",
  "source_id": "pylint-dev/pylint:6603:repair:5fee33ffcd52",
  "available_at": "2022-05-13T13:40:25Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/checkers/refactoring/refactoring_checker.py adds `or not node.iter.args` after the enumerate-name check and before `or not isinstance(node.iter.args[0], nodes.Name)` in the early-return condition. ChangeLog and doc/whatsnew/2.13.rst state that the unnecessary-list-index-lookup crash when incorrectly passing no arguments to enumerate() is fixed and include Closes #6603. The supplied historical diff does not establish historical CI execution."
}
```
