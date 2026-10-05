# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4612:body",
  "source_id": "pylint-dev/pylint:4612:repair:93d6c39e8fbb",
  "available_at": "2021-06-23T17:24:08Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used pylint 2.8.3 and reported a pipeline exception at `i is not None and i.qname() in qnames or i.name in qnames`: `TypeError: 'in <string>' requires string as left operand, not Uninferable`. Removing a failing module moved the exception to another module. This is the reported failure, not an independently captured historical test execution."
}
```
