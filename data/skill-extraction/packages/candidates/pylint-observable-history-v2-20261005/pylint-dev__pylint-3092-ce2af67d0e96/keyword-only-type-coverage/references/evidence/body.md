# Public reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3092:body",
  "source_id": "pylint-dev/pylint:3092:repair:ce2af67d0e96",
  "available_at": "2019-09-05T16:44:15Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied indentifier_kwarg_method with arg1:int and arg2:int before *, and value1:str and value2:str after it. A Google-style Args section described all four without explicit types. The reported command python3 -m pylint --disable=all --enable=missing-type-doc pylint_failure.py emitted W9016 for 'value1, value2'. The expected behavior was no false missing-type warning. Reported versions were Pylint 2.3.1, astroid 2.2.5, and Python 3.7.3 on Mac OSX 10.14.6. Positional-only / syntax was explicitly not tested."
}
```
