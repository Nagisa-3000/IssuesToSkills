# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:419:regression",
  "source_id": "PyCQA/pyflakes:419:repair:ba64624f38a5",
  "available_at": "2019-02-01T16:41:28Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied diff in pyflakes/test/test_type_annotations.py adds test_typeCommentsSyntaxErrorCorrectLine. It calls self.flakes with x = 1 on line 1 and '# type: definitely not a PEP 484 comment' on line 2, requesting m.CommentAnnotationSyntaxError, then asserts self.assertEqual(checker.messages[0].lineno, 2). The neighboring test_typeCommentsAssignedToPreviousNode has a visible comment describing association of the type comment with a node above it; its full body is not supplied. These are assertions available at the historical commit. Historical execution status is unknown from the diff, and no column assertion is shown."
}
```
