# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5406:fix",
  "source_id": "pylint-dev/pylint:5406:repair:3b744d180e5e",
  "available_at": "2022-04-07T08:43:11Z",
  "kind": "historical_merged_implementation",
  "observation": "The diff changes Sphinx's escaped-asterisk repetition allowance from {1,2} to {0,2}, permits an optional escape before asterisks in Google's parameter pattern, and removes backslashes from extracted Google parameter names. Missing comparison skips an unmatched expected name if its star-stripped name is documented. Differing comparison conditionally substitutes documented bare names into the expected set before the existing symmetric-difference and exemption calculation. Changelog entries state that asterisks are no longer required in Sphinx and Google parameter documentation and cite closure of #5406 and #5815. The authoritative SourceRecord identifies a verified resolution; historical CI execution is unknown."
}
```
