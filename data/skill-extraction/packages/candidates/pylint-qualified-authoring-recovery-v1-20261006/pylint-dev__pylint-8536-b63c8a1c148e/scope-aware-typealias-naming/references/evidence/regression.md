# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8536:regression",
  "source_id": "pylint-dev/pylint:8536:repair:b63c8a1c148e",
  "available_at": "2023-04-07T20:17:19Z",
  "kind": "historical_regression_assertions",
  "observation": "The default naming fixture added my_function with LocalGoodName: TypeAlias = int; local_bad_name: TypeAlias = int marked [invalid-name]; local_declaration: Union[str, int]; LocalTypeAliasToUnion: TypeAlias = Union[str, int]; and local_declaration = 1. Deletion statements provided local-use fixture hygiene. The companion expectation file added invalid-name at line 39, columns 4 through 18, in my_function, with message Type alias name \"local_bad_name\" doesn't conform to predefined naming style and HIGH confidence. Existing expectations were retained. These assertions were committed at the historical revision; historical test and CI execution are unknown."
}
```
