# Merged classification and diagnostic changes

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:483:fix",
  "source_id": "PyCQA/pyflakes:483:repair:0af480e3351a",
  "available_at": "2020-02-17T19:43:55Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff added _is_singleton, _is_tuple_constant, _is_constant, and _is_const_non_singleton in pyflakes/checker.py. For PY38_PLUS, singleton recognition required ast.Constant and a value of bool, type(Ellipsis), or type(None); older non-Python-2 code used ast.NameConstant or ast.Ellipsis, and Python 2 used ast.Name with True, False, Ellipsis, or None identifiers. _is_tuple_constant required ast.Tuple and all(_is_constant(elt) for elt in node.elts), admitting empty and recursively constant tuples. PY38_PLUS constants were ast.Constant or constant tuples; older branches recognized ast.Str, ast.Num, non-Python-2 ast.Bytes, singletons, and constant tuples. The non-singleton predicate was _is_constant(node) and not _is_singleton(node). Checker.COMPARE replaced direct literal-type checks with that predicate on either operand for ast.Is or ast.IsNot, retaining left = right across zipped operators/comparators. pyflakes/messages.py changed IsLiteral.message from 'use ==/!= to compare str, bytes, and int literals' to 'use ==/!= to compare constant literals (str, bytes, int, float, tuple)'. This supplied merged implementation supports the verified repair; no historical test-run transcript is included."
}
```
