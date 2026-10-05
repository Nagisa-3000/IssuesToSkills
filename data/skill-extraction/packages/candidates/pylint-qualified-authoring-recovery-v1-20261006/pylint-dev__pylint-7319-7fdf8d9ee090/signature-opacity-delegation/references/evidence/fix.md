# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7319:fix",
  "source_id": "pylint-dev/pylint:7319:repair:7fdf8d9ee090",
  "available_at": "2022-08-21T14:02:23Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/checkers/classes/class_checker.py added `or (meth_node.args.args is None and function.argnames() != [\"self\"])` to an existing early-return condition including parameter-default comparison. Its comment says arguments to builtins such as Exception.__init__() cannot be inspected. The new doc/whatsnew/fragments/7319.bugfix describes preventing useless-parent-delegation for delegation to a C-written builtin with non-self arguments and states 'Closes #7319'. Historical CI/test execution is unknown."
}
```
