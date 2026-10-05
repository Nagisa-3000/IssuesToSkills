# Historical merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8774:fix",
  "source_id": "pylint-dev/pylint:8774:repair:92485a35e516",
  "available_at": "2023-06-18T14:43:15Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff initializes confidence to HIGH in _check_shallow_copy_environ; calls utils.get_argument_from_call(node, position=0, keyword=\"x\") in a try block; catches utils.NoSuchArgumentError; calls utils.infer_kwarg_from_call(node, keyword=\"x\"); returns if the fallback argument is falsy; and sets confidence to INFERENCE for a recovered fallback argument. Existing arg.inferred() and astroid.InferenceError handling remain. When an inferred value's qname equals OS_ENVIRON, shallow-copy-environ is emitted with the selected confidence and the loop breaks. A changelog fragment says the no-argument copy.copy() crash was fixed and closes #8774. The supplied diff does not establish historical CI/test execution."
}
```
