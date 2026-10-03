# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:561:fix",
  "source_id": "PyCQA/pyflakes:561:repair:13cad915e6b1",
  "available_at": "2021-10-05T22:44:29Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied pyflakes/checker.py diff adds _module_scope_is_typing(name) inside _is_typing_helper. It searches reversed(scope_stack), stops at the first scope containing name, and returns isinstance(scope[name], Importation) and scope[name].fullName in TYPING_MODULES. It returns False when no binding exists. The ast.Attribute branch retains an ast.Name receiver and attribute-name matching, but replaces node.value.id in TYPING_MODULES with _module_scope_is_typing(node.value.id). This records the merged implementation, not a test execution log."
}
```
