# Public reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:510:body",
  "source_id": "PyCQA/pyflakes:510:repair:76416437ef22",
  "available_at": "2020-02-03T15:28:16Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied 'from typing import Union, cast', then \"x = cast('Union[str, int]', 42)\" and 'reveal_type(x)'. Reported pyflakes output marked typing.Union imported but unused and reveal_type undefined. The reporter explicitly considered reveal_type being undefined correct. Reported mypy output revealed Union[builtins.str, builtins.int]. The report explained that quoting whole types can accommodate circular-import-related forward references. These are reported outputs, not independently executed checks in this package."
}
```
