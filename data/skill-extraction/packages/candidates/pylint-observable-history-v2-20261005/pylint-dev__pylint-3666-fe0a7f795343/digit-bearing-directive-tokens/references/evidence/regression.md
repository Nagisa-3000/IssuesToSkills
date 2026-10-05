# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3666:regression",
  "source_id": "pylint-dev/pylint:3666:repair:fe0a7f795343",
  "available_at": "2020-06-08T05:51:24Z",
  "kind": "historical_regression_assertions",
  "observation": "tests/test_pragma_parser.py added test_disable_checker_with_number_in_name. It searched OPTION_PO in '#pylint: disable = j3-custom-checker', passed match.group(2) to parse_pragma, and for each yielded pragma asserted action == 'disable' and messages == ['j3-custom-checker']. These are committed assertions; original historical execution is unknown."
}
```
