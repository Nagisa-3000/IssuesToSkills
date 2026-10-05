# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8559:fix",
  "source_id": "pylint-dev/pylint:8559:repair:2db55f6a4896",
  "available_at": "2023-04-15T01:53:00Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/typecheck.py, the merged diff inserts `elif (keyword in [arg.name for arg in called.args.posonlyargs] and called.args.kwarg): pass` before the existing `else: parameters[i] = (parameters[i][0], True)`. The new branch avoids marking a positional-only parameter supplied when its same-name keyword is accepted by a keyword collector. The changelog fragment doc/whatsnew/fragments/8559.false_negative records the false-negative correction and says Closes #8559; its prose uses *kwargs, while the implementation concerns **kwargs. Historical CI/test execution is unknown."
}
```
