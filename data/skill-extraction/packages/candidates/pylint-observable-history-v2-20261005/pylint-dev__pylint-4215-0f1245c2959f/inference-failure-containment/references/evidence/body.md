# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4215:body",
  "source_id": "pylint-dev/pylint:4215:repair:0f1245c2959f",
  "available_at": "2021-03-08T10:07:35Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report reproduces a crash with if len(dont_care[0]): pass. After missing-module-docstring, LenChecker.visit_call in pylint/checkers/refactoring/len_checker.py consumes instance = next(len_arg.infer()). Subscript inference reaches name inference and raises astroid.exceptions.NameInferenceError because dont_care is not found. Expected behavior is ordinary warnings rather than a crash. Reported versions are pylint 2.7.2, astroid 2.5.1, and Python 3.9.2 on Windows."
}
```
