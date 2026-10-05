# Merged diagnostic correction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4654:fix",
  "source_id": "pylint-dev/pylint:4654:repair:c2d03c6b3881",
  "available_at": "2021-07-04T17:58:21Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff added _will_be_released_automatically(node: astroid.Call) -> bool. It returns false unless node.parent is astroid.Call, safely infers node.parent.func with utils.safe_infer, returns false when inference fails, and recognizes func.qname() equal to contextlib._BaseExitStack.enter_context or contextlib.ExitStack.enter_context. The latter identity is commented as necessary for Python 3.6 compatibility. The consider-using-with gate retains could_be_used_in_with and exempts candidates when either _is_inside_context_manager(node) or the new helper succeeds. ChangeLog and the 2.9 whatsnew notes describe the false-positive correction; ChangeLog includes Closes #4654. Historical CI/test execution is not supplied and remains unknown."
}
```
