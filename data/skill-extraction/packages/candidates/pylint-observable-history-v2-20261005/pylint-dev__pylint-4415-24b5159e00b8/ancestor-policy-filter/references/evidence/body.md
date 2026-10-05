# Public reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4415:body",
  "source_id": "pylint-dev/pylint:4415:repair:24b5159e00b8",
  "available_at": "2021-04-28T00:20:16Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied ItemSequence(MutableSequence), implementing __getitem__, __setitem__, __delitem__, insert, and __len__. Running pylint ancestor.py reportedly emitted ancestor.py:4:0: R0901: Too many ancestors (8/7) (too-many-ancestors). Reported versions were pylint 2.7.4, astroid 2.5.2, and Python 3.7.7. The reporter considered suppression or increasing the limit undesirable when using the collections hierarchy as intended. This is a reported reproduction, not independently established historical execution."
}
```
