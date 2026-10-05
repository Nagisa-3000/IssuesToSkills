# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4555:regression",
  "source_id": "pylint-dev/pylint:4555:repair:cbd3cc07515e",
  "available_at": "2021-06-17T11:45:43Z",
  "kind": "historical_regression_assertions",
  "observation": "The new plugin_does_not_exists.rc configured pylint.extensions.check_does_not_exists_in_venv. The Python fixture disabled missing-docstring, imported ShadokInteger from shadok on line 3 with an import-error annotation, and called it. Expected output was import-error:3:0::Unable to import 'shadok':HIGH. The committed assertion covers continued ordinary analysis despite the absent configured plugin; it does not directly assert bad-plugin-value. The diff also deleted the empty decorator_unused.txt. Historical execution status is unknown; later qualification remains separate validation-only provenance."
}
```
