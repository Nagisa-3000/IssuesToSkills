# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:574:regression",
  "source_id": "PyCQA/pyflakes:574:repair:c23a81037d4f",
  "available_at": "2020-09-28T20:44:22Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_type_annotations.py added four tests guarded with skipIf(version_info < (3,), 'new in Python 3'). Function parameter annotations `Annotated['integer']` and `Annotated['integer', 1]` each expected m.UndefinedName. `Annotated[int, '> 0']` expected no diagnostic. `Union[Annotated['int', '>0'], 'integer']` expected m.UndefinedName. These are assertions available at the repair commit; historical execution status is unknown from the supplied evidence."
}
```
