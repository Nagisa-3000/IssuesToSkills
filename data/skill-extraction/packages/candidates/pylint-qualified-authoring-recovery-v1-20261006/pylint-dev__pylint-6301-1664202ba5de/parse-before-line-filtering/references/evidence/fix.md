# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6301:fix",
  "source_id": "pylint-dev/pylint:6301:repair:1664202ba5de",
  "available_at": "2022-04-19T15:21:03Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged pylint/checkers/similar.py diff removed early active_lines enablement filtering from Similar.append_stream. It read complete lines, used lines=[] on UnicodeDecodeError, and appended a LineSet with an optional line_enabled_callback bound to _is_one_message_enabled when a linter existed, otherwise None. LineSet forwarded the callback to stripped_lines. After AST-dependent import/signature preparation, stripped_lines enumerated original lines starting at 1 and skipped a line when line_enabled_callback('R0801', lineno) returned false, before stripping and normalization. The callback type was Callable[[str, int], bool] | None. ChangeLog and doc/whatsnew/2.13.rst described the duplicate-code AstroidError with ignore-imports or ignore-signatures enabled and stated Closes #6301. Historical CI/test execution is unknown."
}
```
