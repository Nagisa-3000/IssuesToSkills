# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4612:fix",
  "source_id": "pylint-dev/pylint:4612:repair:93d6c39e8fbb",
  "available_at": "2021-06-23T20:31:17Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/utils.py, decorated_with changed from `i is not None and i.qname() in qnames or i.name in qnames` to `i.name in qnames or i.qname() in qnames` and added generator filter `if i is not None and i != astroid.Uninferable` after `for i in decorator_node.infer()`. The shown context retains `except astroid.InferenceError`. The ChangeLog states that this fixes a crash for @pytest.fixture when astroid cannot infer the decorator name while using open without with, and states Closes #4612. This is merged repair and closure evidence, not a historical CI execution result."
}
```
