# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8536:body",
  "source_id": "pylint-dev/pylint:8536:repair:b63c8a1c148e",
  "available_at": "2023-04-03T19:13:54Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reproduction imported typing.TypeAlias. It assigned int to GoodTopLevelName and bad_top_level_name at module scope and to GoodLocalName and bad_local_name inside my_func, all explicitly annotated TypeAlias. The reporter invoked pylint t.py and supplied output containing only C0103 invalid-name for bad_top_level_name, with type-alias wording. Expected behavior also included invalid-name for bad_local_name. Reported versions were Pylint 2.17.2, astroid 2.15.2, and Python 3.11.2. This output is reporter-supplied; historical CI execution is not established."
}
```
