# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5222:body",
  "source_id": "pylint-dev/pylint:5222:repair:1d3a7ff32b0f",
  "available_at": "2021-10-27T11:40:24Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report supplies func(arg1: bool, arg2: bool) with a NumPy Parameters section. arg1 has `arg1 : bool` and a description; arg2 has a name-only header and an indented description. Configuration loads pylint.extensions.docparams and selects default-docstring-type=numpy. The reported command `pylint pylint_bug.py` produces W9015 missing-param-doc for arg2 and W9012 missing-return-type-doc. The reporter expected neither and reports Pylint 2.11.1, astroid 2.8.4 and Python 3.8.2. This is a reported reproduction, not an executed Skill case; the supplied repair supports parameter recognition rather than a separate return-type resolution."
}
```
