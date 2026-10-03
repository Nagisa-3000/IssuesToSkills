# Regression assertions at the repair commit

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:575:regression",
  "source_id": "PyCQA/pyflakes:575:repair:e3f26593eac9",
  "available_at": "2021-03-14T16:02:46Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied tests add test_typednames_correct_forward_ref and test_namedtypes_classes. Four nested List expressions using TypedDict or NamedTuple expect no diagnostics. Seven expressions with missing names in actual type positions expect seven UndefinedName messages, including TypedDict values, NamedTuple field types, nested List[\"a\"], and TypeVar bound/constraint references. A clean group imports A, B, C, D, E and uses nested references in NamedTuple, TypeVar, and cast. Class-based nested TypedDict and NamedTuple annotations expect no diagnostics, guarded below Python 3.6. These are assertions available at the historical commit; no historical execution result is supplied."
}
```
