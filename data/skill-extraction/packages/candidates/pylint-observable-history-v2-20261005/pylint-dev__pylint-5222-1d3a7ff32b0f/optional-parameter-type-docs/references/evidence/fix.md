# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5222:fix",
  "source_id": "pylint-dev/pylint:5222:repair:1d3a7ff32b0f",
  "available_at": "2021-10-30T22:33:23Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff changes NumpyDocstring.re_param_line from requiring a colon after an optionally starred identifier to accepting colon or newline. The optional type capture includes a terminating newline. It adds Set and Tuple imports and a NumPy-specific match_param_docs that collects ordinary and keyword sections and returns separate documentation and type sets. The description-only branch assigns param_type=None and param_desc=match.group(2), which is the delimiter capture; the other branch uses groups 3 and 4 for type and description. The diff includes print(entries). ChangeLog and the 2.12 notes state that NumPy parameter documentation without explicit typing is handled and close issue 5222, spelling the diagnostic `mising-param-doc`. These are merged implementation facts; original CI execution is unknown."
}
```
