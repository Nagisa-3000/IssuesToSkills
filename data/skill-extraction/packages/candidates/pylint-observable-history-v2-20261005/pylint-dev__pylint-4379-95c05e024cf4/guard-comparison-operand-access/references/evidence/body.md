# Original public reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4379:body",
  "source_id": "pylint-dev/pylint:4379:repair:95c05e024cf4",
  "available_at": "2021-04-19T14:30:17Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report gives var = 1 followed by if var == -1: var = None. Running pylint a.py reportedly crashes in RefactoringChecker._check_consider_using_min_max_builtin at right_statement_value = right_statement.value with AttributeError: 'UnaryOp' object has no attribute 'value'. Expected behavior is no crash. Reported versions are pylint 2.8.0.dev1, astroid 2.5.3, and Python 3.9.4. This is a reported reproduction, not a historical CI result."
}
```
