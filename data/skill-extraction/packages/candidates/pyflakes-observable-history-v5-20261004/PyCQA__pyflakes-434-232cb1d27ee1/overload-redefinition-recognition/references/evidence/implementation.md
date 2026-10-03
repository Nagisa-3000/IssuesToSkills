# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:434:fix",
  "source_id": "PyCQA/pyflakes:434:repair:232cb1d27ee1",
  "available_at": "2019-03-01T12:37:21Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged checker diff changed is_typing_overload to take scope_stack. Its new name helper traversed reversed(scope_stack) and returned at the first scope containing the name, accepting only an ImportationFrom with fullName equal to typing.overload; absent names returned False. The ast.FunctionDef guard remained, while the exactly-one-decorator condition became any recognition across decorator_list. The unused-redefinition reporting gate continued checking existing and passed self.scopeStack instead of self.scope. The attribute-form recognition branch was unchanged in the shown diff. This is implementation evidence, not an execution log."
}
```
