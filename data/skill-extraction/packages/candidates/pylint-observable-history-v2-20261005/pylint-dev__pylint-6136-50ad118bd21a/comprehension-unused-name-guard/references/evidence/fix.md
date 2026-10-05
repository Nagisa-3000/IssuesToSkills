# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6136:fix",
  "source_id": "pylint-dev/pylint:6136:repair:50ad118bd21a",
  "available_at": "2022-04-03T13:18:22Z",
  "kind": "historical_merged_implementation",
  "observation": "In VariablesChecker unused-name handling, the merged diff added `if name in comprehension_target_names: return` before `argnames = node.argnames()`. The argument branch then called `_check_unused_arguments(name, node, stmt, argnames, nonlocal_names)` directly instead of nesting that call under `if name not in comprehension_target_names`. Matching names therefore bypassed both argument and local-variable dispatch. The ChangeLog added `Closes #6136`. Historical CI/test execution is unknown from the supplied core evidence."
}
```
