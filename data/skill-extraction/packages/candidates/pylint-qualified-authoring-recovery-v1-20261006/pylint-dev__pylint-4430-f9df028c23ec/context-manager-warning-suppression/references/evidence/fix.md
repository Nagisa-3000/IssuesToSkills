# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4430:fix",
  "source_id": "pylint-dev/pylint:4430:repair:f9df028c23ec",
  "available_at": "2021-05-09T12:19:04Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff added _is_inside_context_manager(node): obtain node.frame(); reject frames not instances of astroid.FunctionDef, astroid.BoundMethod or astroid.UnboundMethod; otherwise recognize frame.name == \"__enter__\" or utils.decorated_with(frame, \"contextlib.contextmanager\"). Both the assigned-call condition using CALLS_RETURNING_CONTEXT_MANAGERS and the replaceable-call condition using CALLS_THAT_COULD_BE_REPLACED_BY_WITH retained safe inference and added not _is_inside_context_manager(node). The ChangeLog states suppression inside context managers and closes #4430. Historical CI/test execution is unknown."
}
```
