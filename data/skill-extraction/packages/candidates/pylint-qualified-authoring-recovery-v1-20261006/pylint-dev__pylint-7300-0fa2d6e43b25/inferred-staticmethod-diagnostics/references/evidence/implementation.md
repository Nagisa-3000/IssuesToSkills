# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7300:fix",
  "source_id": "pylint-dev/pylint:7300:repair:0fa2d6e43b25",
  "available_at": "2022-08-13T18:34:47Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff added an elif branch testing \"builtins.staticmethod\" in node.decoratornames(), with an immediate return, in pylint/checkers/classes/class_checker.py. It followed existing staticmethod handling and preceded the ordinary no-arguments branch that emits no-method-argument. The release fragment stated that the fix removes no-self-argument/no-method-argument false positives when staticmethod is applied using a different name and closes #7300. The supplied implementation evidence does not establish historical CI execution."
}
```
