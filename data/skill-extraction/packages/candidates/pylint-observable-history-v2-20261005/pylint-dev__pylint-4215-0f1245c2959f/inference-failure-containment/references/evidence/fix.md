# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4215:fix",
  "source_id": "pylint-dev/pylint:4215:repair:0f1245c2959f",
  "available_at": "2021-03-08T16:55:45Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff wraps instance = next(len_arg.infer()) in try/except astroid.InferenceError and returns on failure. The generator/comprehension branch remains before the catch and base_classes_of_node(instance) remains after it. The ChangeLog describes a fix for astroid inference error for undefined variables with len() and closes #4215. This evidence does not record historical test or CI execution."
}
```
