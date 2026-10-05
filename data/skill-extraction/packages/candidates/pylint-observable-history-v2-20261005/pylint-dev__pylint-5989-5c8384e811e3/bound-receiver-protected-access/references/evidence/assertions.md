# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5989:regression",
  "source_id": "pylint-dev/pylint:5989:repair:5c8384e811e3",
  "available_at": "2022-03-27T12:31:53Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed tests/functional/p/protected_access.py diff added Light with a protected property returning None, a static method func(light), and an ordinary function func(light: Light). Both functions printed light._light_internal and carried [protected-access] annotations. The expected-output file added protected-access diagnostics at line 39 for Light.func and line 43 for func, while retaining its previous line-17 and line-29 entries. These are committed assertions available at the historical repair, not proof that historical CI executed them."
}
```
