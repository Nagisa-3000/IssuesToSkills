# Merged lifecycle repair

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4331:fix",
  "source_id": "pylint-dev/pylint:4331:repair:d0591ba2a097",
  "available_at": "2021-04-09T19:13:14Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/testutils/lint_module_test.py imports utils from pylint.utils. Immediately after read_config_file(test_file.option_file), it checks cfgfile_parser.has_option(\"MASTER\", \"load-plugins\"), gets that option, splits it with utils._splitstrip, and calls load_plugin_modules(plugins). load_config_file remains afterward and except NoFileError: pass remains. This establishes the implemented registration ordering, not a historical test-execution outcome."
}
```
