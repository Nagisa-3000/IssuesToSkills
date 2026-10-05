# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4430:regression",
  "source_id": "pylint-dev/pylint:4430:repair:f9df028c23ec",
  "available_at": "2021-05-09T12:19:04Z",
  "kind": "historical_regression_assertions",
  "observation": "Committed tests added lock.acquire() cases marked must not trigger in a @contextlib.contextmanager generator and MyLockContext.__enter__, with release in the generator or __exit__. The separate open fixture added silent open assignments in __enter__ and an imported @contextmanager generator, plus module-level myfile = open(\"test.txt\") marked consider-using-with. Expected output retained ordinary resource warnings and added the module-level open warning. The fixture explains that standard open is uninferable in PyPy and was separated to avoid excluding other resource checks there. These are committed assertions; historical execution status is unknown."
}
```
