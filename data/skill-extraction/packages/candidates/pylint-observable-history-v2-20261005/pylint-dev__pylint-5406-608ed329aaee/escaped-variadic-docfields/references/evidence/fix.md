# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5406:fix",
  "source_id": "pylint-dev/pylint:5406:repair:608ed329aaee",
  "available_at": "2021-12-03T15:35:29Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff changed SphinxDocstring parameter-name recognition from optional unescaped asterisks to alternatives for one backslash followed by one or two asterisks and a word name, or an ordinary word name. Extraction retained match.group(2) and added name.replace(\"\\\\\", \"\") before adding the name to params_with_doc. The colorize_ansi docstring became raw and changed ':param **kwargs:' to ':param \\**kwargs:'. The ChangeLog records corrected Sphinx asterisk handling and closes #5406. Historical CI/test execution is unknown."
}
```
