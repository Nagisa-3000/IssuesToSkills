# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5406:body",
  "source_id": "pylint-dev/pylint:5406:repair:3b744d180e5e",
  "available_at": "2021-11-26T15:38:14Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "With pylint.extensions.docparams enabled and `pylint echo.py`, the reporter describes a function declaring *args. In Pylint 2.12.1, Sphinx-style `:param args:` produces W9015 for *args missing and W9017 for args differing. `:param *args:` produces no Pylint errors but a Sphinx emphasis warning. `:param \\*args:` in a non-raw Python string produces W1401. The report requests compatibility with Sphinx-accepted spellings and notes prior acceptance of the bare name. These are reported observations, not independently recorded historical test execution."
}
```
