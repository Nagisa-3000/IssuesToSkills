# Merged character-class repair

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3604:fix",
  "source_id": "pylint-dev/pylint:3604:repair:ffb354aea057",
  "available_at": "2020-05-14T17:04:40Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged implementation changed MESSAGE_STRING in pylint/utils/pragma_parser.py from r\"[A-Za-z\\-]{2,}\" to r\"[A-Za-z\\-\\_]{2,}\". It added underscore while retaining ASCII letters, hyphen and the two-character minimum. Other shown token definitions were unchanged. The ChangeLog said 'Fix a regression where messages with dash are not fully parsed' and 'Close #3604'. Historical CI/test execution is unknown; contemporary qualification is separate validation-only provenance."
}
```
