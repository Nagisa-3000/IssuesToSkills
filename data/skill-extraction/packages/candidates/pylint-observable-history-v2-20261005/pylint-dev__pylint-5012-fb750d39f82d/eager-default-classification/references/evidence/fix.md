# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5012:fix",
  "source_id": "pylint-dev/pylint:5012:repair:fb750d39f82d",
  "available_at": "2021-09-20T20:11:44Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff changed `is_default_argument` in `pylint/checkers/utils.py`. Its FunctionDef/Lambda branch previously searched only `scope.args.defaults`. It now sets `all_defaults = itertools.chain(scope.args.defaults, (d for d in scope.args.kw_defaults if d is not None))` and returns `any(default_name_node is node for default_node in all_defaults for default_name_node in default_node.nodes_of_class(nodes.Name))`. Exact-node identity and the false fallback remain. The ChangeLog states that the keyword-only parameter default false positive was fixed and closes #5012. Historical CI/test execution is unknown from the supplied implementation evidence."
}
```
