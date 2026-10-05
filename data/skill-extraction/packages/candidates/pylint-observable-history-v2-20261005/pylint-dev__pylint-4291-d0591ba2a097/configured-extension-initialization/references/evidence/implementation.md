# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4291:fix",
  "source_id": "pylint-dev/pylint:4291:repair:d0591ba2a097",
  "available_at": "2021-04-09T19:13:14Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff imports utils from pylint.utils in pylint/testutils/lint_module_test.py. Inside the existing try block, immediately after self._linter.read_config_file(test_file.option_file), it checks self._linter.cfgfile_parser.has_option('MASTER', 'load-plugins'). If present, it retrieves the value, normalizes it with utils._splitstrip, and invokes self._linter.load_plugin_modules(plugins). self._linter.load_config_file() remains afterward; except NoFileError: pass remains intact. This establishes implemented registration before configuration application. Historical CI/test execution is unknown."
}
```
