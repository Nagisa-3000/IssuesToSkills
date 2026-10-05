# Public report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4277:body",
  "source_id": "pylint-dev/pylint:4277:repair:44a3aa25fd9b",
  "available_at": "2021-04-01T03:33:29Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reproduction assigns list() to lowercase shared_var_1 class declarations annotated with bare ClassVar and typing.ClassVar. Reported output gives C0103 class-constant UPPER_CASE diagnostics for both. The report also mentions subscripted annotations and explains that mutable ClassVar does not imply constantness. It reports the symptom on Pylint 2.7.4 and 3.0.0a1 but not 2.7.2, using astroid 2.5.2 and Python 3.8.8. These are report observations, not independently executed historical version comparisons."
}
```
