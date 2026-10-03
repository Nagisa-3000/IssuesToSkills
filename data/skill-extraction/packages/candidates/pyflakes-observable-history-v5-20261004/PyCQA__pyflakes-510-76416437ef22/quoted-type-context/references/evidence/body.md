# Historical public reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:510:body",
  "source_id": "PyCQA/pyflakes:510:repair:76416437ef22",
  "available_at": "2020-02-03T15:28:16Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report imports Union and cast from typing, assigns x = cast('Union[str, int]', 42), and calls reveal_type(x). Reported pyflakes output says typing.Union is imported but unused and reveal_type is undefined. The reporter explicitly says the reveal_type diagnostic is correct. Reported mypy output reveals Union[builtins.str, builtins.int]. The report motivates whole-expression quoting for cases such as circular imports. These are supplied reporter observations, not independently executed current checks."
}
```
