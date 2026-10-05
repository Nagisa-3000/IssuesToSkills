# Original failure report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4555:body",
  "source_id": "pylint-dev/pylint:4555:repair:cbd3cc07515e",
  "available_at": "2021-06-08T13:22:36Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used pylint 2.7.2 with a 2.8.3 configuration containing pylint.extensions.confusing_elif. The traceback terminated with ModuleNotFoundError for that module during load_plugin_modules via astroid.modutils.load_module_from_name and importlib.import_module. The requested outcome was graceful failure while running the other checks. This is a public reported reproduction, not an independently recorded historical test run."
}
```
