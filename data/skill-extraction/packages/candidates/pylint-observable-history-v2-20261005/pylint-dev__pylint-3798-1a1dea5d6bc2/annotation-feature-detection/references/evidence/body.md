# Historical report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3798:body",
  "source_id": "pylint-dev/pylint:3798:repair:1a1dea5d6bc2",
  "available_at": "2020-08-26T19:44:49Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter described Pylint 2.6.0 and earlier under Python 3.7 producing an incorrect Undefined variable 'C' warning for the return annotation of C.create with 'from __future__ import annotations as __annotations__'. Removing the as clause removed the reported warning. The report explained aliasing to avoid binding annotations in the namespace and stated that aliasing should not affect future-clause processing. These are reported observations, not a recorded independent historical test run."
}
```
