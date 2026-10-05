# Historical committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5950:regression",
  "source_id": "pylint-dev/pylint:5950:repair:9c90db16a860",
  "available_at": "2022-03-22T19:00:27Z",
  "kind": "historical_regression_assertions",
  "observation": "The test_main.py diff mocked utility subprocess and executable discovery, plus diagram construction and writing. For png advertised by Graphviz it asserted the fallback notice, one writer call and exit 0. For stderr '...' it asserted the inability-to-determine warning, one writer call and exit 0. For somethingElse it asserted fallback and Graphviz-specific unsupported messages and exit 32; it did not explicitly assert writer non-invocation. Existing import-path cases remained. These are assertions committed at the fix revision; historical execution is unknown. Later replay is validation-only provenance and does not execute this Skill."
}
```
