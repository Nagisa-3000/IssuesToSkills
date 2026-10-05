# Merged implementation

```arex-evidence-v4
{
  "id": "astral-sh/ruff:5124:fix",
  "source_id": "astral-sh/ruff:5124:repair:107a295af4f5",
  "available_at": "2023-06-15T19:00:20Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff changed redefined_loop_name from a general Node parameter to &Stmt and changed checker calls from &Node::Stmt(stmt) to stmt. The rule matched Stmt::With and Stmt::AsyncWith in one arm, extracting optional with-item binding targets and visiting the body through the existing visitor. The For/AsyncFor arm remained. The fallback panic was retained and its message added AsyncWith to the accepted variants; the expression-node panic branch disappeared with the Node parameter. Helper Expr/Withitem types were simplified and binding-kind enums became private. This implementation is available at the historical revision; historical CI/test execution is unknown."
}
```
