# Committed parser assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3604:regression",
  "source_id": "pylint-dev/pylint:3604:repair:ffb354aea057",
  "available_at": "2020-05-14T17:04:40Z",
  "kind": "historical_regression_assertions",
  "observation": "tests/test_pragma_parser.py added test_parse_message_with_dash. It set comment to '#pylint: disable = raw_input-builtin', searched with OPTION_PO, evaluated list(parse_pragma(match.group(2))), asserted res[0].action == 'disable', and asserted res[0].messages == ['raw_input-builtin']. The identifier includes underscore despite the test name. These are committed assertions; historical execution is unknown."
}
```
