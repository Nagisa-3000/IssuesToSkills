# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4555:fix",
  "source_id": "pylint-dev/pylint:4555:repair:cbd3cc07515e",
  "available_at": "2021-06-17T11:45:43Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff added E0013 / bad-plugin-value with message text Plugin '%s' is impossible to load, is it installed ? ('%s'). load_plugin_modules retained names in _dynamic_plugins and caught ModuleNotFoundError around loading and registration. load_plugin_configuration caught ModuleNotFoundError around loading and optional configuration hooks, then added bad-plugin-value with plugin name and exception at line 0. The message handler initialized minimal statistics when stats was None and used configuration when abspath was None. TextReporter initialized _template to line_format and used its existing template as the fallback on module changes. The ChangeLog explicitly stated the crash fix and closure of #4555. Historical CI execution was not supplied."
}
```
