# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5557:fix",
  "source_id": "pylint-dev/pylint:5557:repair:2a69387352bd",
  "available_at": "2021-12-21T13:58:16Z",
  "kind": "historical_merged_implementation",
  "observation": "ComparisonChecker in pylint/checkers/base.py replaced a sum of inferred bare-callable operands with an explicit loop over node.left and node.ops[0][1]. Each operand used utils.safe_infer. The count incremented only when inferred was an instance of bare_callables, 'typing._SpecialForm' was absent from inferred.decoratornames(), and no immediate inferred.body element was a nodes.Raise. The diagnostic still emitted when number_of_bare_callables == 1. ChangeLog and doc/whatsnew/2.13.rst described fixing false positives for callables that raise, such as typing constants, and named closure of #5557. This merged diff does not establish historical test execution."
}
```
