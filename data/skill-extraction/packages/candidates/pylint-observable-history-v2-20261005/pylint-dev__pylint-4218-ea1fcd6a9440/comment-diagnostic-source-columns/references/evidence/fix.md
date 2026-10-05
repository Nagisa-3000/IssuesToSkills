# Merged coordinate repair

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4218:fix",
  "source_id": "pylint-dev/pylint:4218:repair:ea1fcd6a9440",
  "available_at": "2021-03-25T20:01:54Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/misc.py, EncodingChecker retains self._fixme_pattern.search('#' + comment_text.lower()) and the conditional emission of fixme. It removes 'note = match.group(1)' and replaces col_offset=comment.string.lower().index(note.lower()) with col_offset=comment.start[1] + 1. Message arguments remain comment_text and line remains comment.start[0]. The ChangeLog records 'Fix column index on FIXME warning messages' and 'Closes #4218'. This is implementation and closure evidence; no historical CI execution result is supplied."
}
```
