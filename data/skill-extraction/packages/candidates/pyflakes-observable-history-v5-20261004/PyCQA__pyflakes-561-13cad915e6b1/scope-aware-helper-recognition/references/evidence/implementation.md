# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:561:fix",
  "source_id": "PyCQA/pyflakes:561:repair:13cad915e6b1",
  "available_at": "2021-10-05T22:44:29Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff in pyflakes/checker.py adds _module_scope_is_typing(name) inside _is_typing_helper. It iterates reversed(scope_stack). At the first scope containing name, it returns isinstance(scope[name], Importation) and scope[name].fullName in TYPING_MODULES; if no scope contains name, it returns False. For an ast.Attribute with an ast.Name receiver, _module_scope_is_typing(node.value.id) replaces node.value.id in TYPING_MODULES. The helper attribute-name predicate remains and the shown direct ast.Name branch is unchanged. This records the merged repair mechanism, not original test execution."
}
```
