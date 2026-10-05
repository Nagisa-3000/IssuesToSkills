# Public crash report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6603:body",
  "source_id": "pylint-dev/pylint:6603:repair:5fee33ffcd52",
  "available_at": "2022-05-13T12:40:29Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report supplies `for i, num in enumerate():` followed by `pass`. Analysis crashes with IndexError: list index out of range. The traceback passes through visit_for into _check_unnecessary_list_index_lookup in pylint/checkers/refactoring/refactoring_checker.py, where the eligibility condition evaluates `or not isinstance(node.iter.args[0], nodes.Name)`."
}
```
