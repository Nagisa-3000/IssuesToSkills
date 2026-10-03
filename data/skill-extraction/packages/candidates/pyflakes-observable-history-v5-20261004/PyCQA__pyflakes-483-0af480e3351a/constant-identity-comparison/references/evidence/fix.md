# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:483:fix",
  "source_id": "PyCQA/pyflakes:483:repair:0af480e3351a",
  "available_at": "2020-02-17T19:43:55Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged change introduces _is_singleton with version-specific branches: ast.Constant values that are instances of bool, type(Ellipsis), or type(None) for PY38_PLUS; ast.NameConstant or ast.Ellipsis for earlier Python 3; ast.Name IDs True, False, Ellipsis, None for Python 2. _is_tuple_constant requires ast.Tuple and all(_is_constant(elt) for elt in node.elts). _is_constant accepts ast.Constant or constant tuples for PY38_PLUS; earlier branches accept ast.Str, ast.Num, Python 3 ast.Bytes, singleton nodes, or constant tuples. _is_const_non_singleton combines constant recognition with singleton exclusion. COMPARE applies this predicate to either operand for ast.Is and ast.IsNot and retains left = right for chain advancement. IsLiteral.message becomes 'use ==/!= to compare constant literals (str, bytes, int, float, tuple)'. The authoritative SourceRecord marks the resolution verified. The diff contains no test execution log."
}
```
