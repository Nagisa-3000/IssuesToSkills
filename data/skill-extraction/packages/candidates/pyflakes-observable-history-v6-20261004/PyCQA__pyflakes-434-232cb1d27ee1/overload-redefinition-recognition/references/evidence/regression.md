# Regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:434:regression",
  "source_id": "PyCQA/pyflakes:434:repair:232cb1d27ee1",
  "available_at": "2019-03-01T12:37:21Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied test_type_annotations.py diff added test_overload_with_multiple_decorators and test_overload_in_class. The former uses an identity lambda dec, @dec above @overload on two f declarations, and @dec on the implementation. The latter imports overload outside class C, places two @overload methods inside the class, and follows them with an implementation. Both call self.flakes without expected diagnostic classes. Existing test_not_a_typing_overload appears in adjacent context. These assertions were available at the repair commit; their historical execution status is unknown."
}
```
