# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:575:regression",
  "source_id": "PyCQA/pyflakes:575:repair:e3f26593eac9",
  "available_at": "2021-03-14T16:02:46Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied diff in pyflakes/test/test_type_annotations.py added test_typednames_correct_forward_ref and test_namedtypes_classes. Assertions expected clean List-nested TypedDict dictionary/keyword and NamedTuple sequence/keyword forms; exactly seven UndefinedName messages across seven statements containing genuine unresolved type references, including nested List strings and TypeVar bound/constraint cases; and clean imported nested references in NamedTuple, TypeVar and cast. Class TypedDict and NamedTuple annotations containing functional declarations were asserted clean, with a Python-below-3.6 skip guard. These assertions were available at the historical commit. No historical execution result was supplied."
}
```
