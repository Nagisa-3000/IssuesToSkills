# Historical merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8570:fix",
  "source_id": "pylint-dev/pylint:8570:repair:56fa5dce747a",
  "available_at": "2023-04-13T06:46:51Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/typecheck.py, visit_functiondef retained `if node.args.vararg and node.args.defaults:` and inserted `if node.args.posonlyargs and not node.args.args: return` before add_message. The comment identifies positional-or-keyword parameters as the checked partition when positional-only parameters are present. `visit_asyncfunctiondef = visit_functiondef` remained. The new doc/whatsnew/fragments/8570.false_positive states that the positional-only default before *args false positive is fixed and says Closes #8570. Historical CI/test execution is unknown."
}
```
