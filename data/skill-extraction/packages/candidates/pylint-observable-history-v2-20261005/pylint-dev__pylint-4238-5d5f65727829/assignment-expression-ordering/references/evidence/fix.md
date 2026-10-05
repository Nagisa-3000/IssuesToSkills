# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4238:fix",
  "source_id": "pylint-dev/pylint:4238:repair:5d5f65727829",
  "available_at": "2021-03-26T21:01:46Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff broadens the IfExp defining-statement check from astroid.Assign to Assign, AnnAssign, AugAssign, and Expr. Within existing assignment-expression ordering logic it adds an alternative requiring not PY39_PLUS, equal definition/use lineno, an Assign/AnnAssign/AugAssign defining statement, and a JoinedStr value. The comment identifies pre-3.9 AST multiline-string line-number ambiguity. constants.py defines PY39_PLUS as sys.version_info[:2] >= (3, 9). ChangeLog records improved assignment-expression edge-case handling and closes #3763 and #4238. Historical test execution is not supplied."
}
```
