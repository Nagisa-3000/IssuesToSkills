# Historical merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:510:fix",
  "source_id": "PyCQA/pyflakes:510:repair:76416437ef22",
  "available_at": "2020-03-17T20:53:38Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff in pyflakes/checker.py imports contextlib and defines TYPING_MODULES as typing and typing_extensions. It generalizes _is_typing through _is_typing_helper and adds _is_any_typing_member. Bare names are checked against the nearest matching scope binding, requiring ImportationFrom, a supported module, and a matching real_name; simple attributes rooted at literal supported module names are also recognized. The in_annotation decorator uses a new _enter_annotation context manager that saves state and restores it in finally. In the subscription handler, the existing Literal special branch is retained; otherwise recognized typing members cause child traversal under annotation context. In the call handler, recognized cast with at least one positional argument and ast.Str as its first argument causes that argument to be visited under annotation context, followed by normal handleChildren traversal. This is implementation evidence for the verified repair; no historical execution log is supplied."
}
```
