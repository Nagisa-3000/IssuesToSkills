# Committed regression assertion

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6557:regression",
  "source_id": "pylint-dev/pylint:6557:repair:5fcccc13f1f7",
  "available_at": "2022-05-11T14:20:18Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed fixture tests/functional/u/unnecessary/unnecessary_dict_index_lookup.py added a Test subscripting an attribute section referencing issue 6557. It created `f = Foo()` and, inside `for input_output in d.items():`, assigned `f.input_output = input_output` with a local attribute-defined-outside-init suppression, then evaluated `print(d[f.input_output[0]])`. No unnecessary-dict-index-lookup expectation annotation was added to this case. The artifact establishes a committed static-analysis regression input; historical execution and CI success remain unknown."
}
```
