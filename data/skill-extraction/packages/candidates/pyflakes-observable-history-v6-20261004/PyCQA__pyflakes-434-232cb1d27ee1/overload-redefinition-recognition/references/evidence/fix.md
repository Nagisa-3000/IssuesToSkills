# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:434:fix",
  "source_id": "PyCQA/pyflakes:434:repair:232cb1d27ee1",
  "available_at": "2019-03-01T12:37:21Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied checker.py diff changed is_typing_overload to receive scope_stack. Its bare-name helper traverses reversed(scope_stack), returns at the first scope containing the name, and requires an ImportationFrom binding whose fullName equals typing.overload; absence returns False. Recognition still requires value.source to be ast.FunctionDef, but now uses any matching decorator instead of an exactly-one-decorator test. The unused-redefinition gate passes self.scopeStack rather than self.scope. The displayed diff retains the existing attribute-decorator branch. The authoritative source identifies the merged revision as a verified resolution; the implementation diff itself contains no test execution log."
}
```
