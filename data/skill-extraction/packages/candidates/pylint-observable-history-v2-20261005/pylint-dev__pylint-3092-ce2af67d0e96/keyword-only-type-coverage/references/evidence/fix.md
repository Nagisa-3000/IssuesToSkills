# Merged collector change

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3092:fix",
  "source_id": "pylint-dev/pylint:3092:repair:ce2af67d0e96",
  "available_at": "2019-09-23T08:04:38Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/extensions/docparams.py, DocstringParameterChecker retained the loop over arguments_node.args and arguments_node.annotations. It added a separate enumerate(arguments_node.kwonlyargs) loop that tests arguments_node.kwonlyargs_annotations[index] and, when present, adds arg_name.name to params_with_type before the existing _compare_missing_args call. The authoritative source identifies this commit as the verified resolution. Historical test execution is not established by this implementation entry."
}
```
