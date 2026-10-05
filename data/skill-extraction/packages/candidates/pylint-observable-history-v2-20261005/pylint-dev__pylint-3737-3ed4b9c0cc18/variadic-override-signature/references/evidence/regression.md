# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3737:regression",
  "source_id": "pylint-dev/pylint:3737:repair:3ed4b9c0cc18",
  "available_at": "2020-12-31T08:22:37Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed diff in tests/functional/s/signature_differs.py added Ghij(Abcd), including abcd(self, *args, **kwargs) returning super().abcd(*args, **kwargs), with a docstring asserting variadics should not trigger the warning and no warning annotation. Existing Cdef.abcd(self, aaa, bbbb=None) retained its [signature-differs] annotation. These are committed assertions, not historical execution logs; historical test execution is unknown."
}
```
