# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7626:fix",
  "source_id": "pylint-dev/pylint:7626:repair:00b6aa8482f0",
  "available_at": "2022-10-16T17:36:39Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff adds keyword-only compare_constants: bool = False to cached safe_infer. After existing inferred-type ambiguity handling, when compare_constants is enabled and both inferred and selected values are nodes.Const, unequal .value values return None. The Boolean rewrite consumer calls safe_infer(truth_value, compare_constants=True), returns on None or astroid.Uninferable, and otherwise uses bool_value(). Its add_message call specifies confidence=INFERENCE. The changelog states that the false positive involving multiple inferred constant values is fixed and says Closes #7626. Historical CI execution is not provided."
}
```
