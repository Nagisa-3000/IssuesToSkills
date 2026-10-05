# Public report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5557:body",
  "source_id": "pylint-dev/pylint:5557:repair:2a69387352bd",
  "available_at": "2021-12-20T08:44:46Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter imported Any from typing and returned type_ == Any from check_any(type_) -> bool. Running pylint a.py reportedly emitted W0143 comparison-with-callable at line 4, column 11, plus unrelated missing-module-docstring and missing-function-docstring messages. Expected behavior was no comparison-with-callable warning. Reported versions were pylint 2.12.2, astroid 2.9.0, and Python 3.10.0. Windows 10 and reproduction on Ubuntu 20.04 were reported. This is reported reproduction output, not historical regression-suite execution."
}
```
