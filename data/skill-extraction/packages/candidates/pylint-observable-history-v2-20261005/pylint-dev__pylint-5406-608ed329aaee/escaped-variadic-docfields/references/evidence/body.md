# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5406:body",
  "source_id": "pylint-dev/pylint:5406:repair:608ed329aaee",
  "available_at": "2021-11-26T15:38:14Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "With pylint.extensions.docparams enabled, the reporter's echo(*args) example using ':param args:' produced W9015 for missing '*args' and W9017 for differing 'args' in Pylint 2.12.1. ':param *args:' produced no reported Pylint errors but a Sphinx inline-emphasis warning. ':param \\*args:' worked with Sphinx but caused W1401 in a non-raw Python string. The report named Sphinx 4.3.0 and requested Sphinx-compatible syntax, acknowledging Google/NumPy differences. These are reported observations and preferences, not independently executed tests or proof that bare variadic names were repaired."
}
```
