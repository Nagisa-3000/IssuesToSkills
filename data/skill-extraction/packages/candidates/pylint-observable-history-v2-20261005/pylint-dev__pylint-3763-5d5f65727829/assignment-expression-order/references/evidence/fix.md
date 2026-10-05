# Historical merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3763:fix",
  "source_id": "pylint-dev/pylint:3763:repair:5d5f65727829",
  "available_at": "2021-03-26T21:01:46Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff expands a conditional-expression definition-statement check from astroid.Assign to Assign, AnnAssign, AugAssign, and Expr. It retains an IfExp value requirement, `frame is defframe`, and `defframe.parent_of(node)`. Definition-order logic also gains a fallback requiring `not PY39_PLUS`, equal definition/read line numbers, an Assign/AnnAssign/AugAssign statement, and a JoinedStr value. The comment attributes this to pre-3.9 multiline-string AST nodes sharing line numbers. The constants module adds `PY39_PLUS = sys.version_info[:2] >= (3, 9)`. The changelog records improved assignment-expression handling and closure of #3763 and #4238. Original historical CI/test execution is unknown."
}
```
