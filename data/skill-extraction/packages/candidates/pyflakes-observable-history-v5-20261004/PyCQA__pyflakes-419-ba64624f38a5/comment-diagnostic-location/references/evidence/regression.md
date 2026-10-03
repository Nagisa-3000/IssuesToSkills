# Historical regression

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:419:regression",
  "source_id": "PyCQA/pyflakes:419:repair:ba64624f38a5",
  "available_at": "2019-02-01T16:41:28Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_type_annotations.py added test_typeCommentsSyntaxErrorCorrectLine. It passed a two-line fixture containing 'x = 1' followed by '# type: definitely not a PEP 484 comment' to self.flakes, expected m.CommentAnnotationSyntaxError, and asserted checker.messages[0].lineno equals 2. These assertions were available at the historical repair commit; historical execution status is not supplied. The excerpt shows the neighboring test name test_typeCommentsAssignedToPreviousNode but not its complete assertions."
}
```
