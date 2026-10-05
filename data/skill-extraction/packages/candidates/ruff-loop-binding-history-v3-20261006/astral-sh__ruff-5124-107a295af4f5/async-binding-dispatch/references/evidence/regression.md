# Committed regression assertions

```arex-evidence-v4
{
  "id": "astral-sh/ruff:5124:regression",
  "source_id": "astral-sh/ruff:5124:repair:107a295af4f5",
  "available_at": "2023-06-15T19:00:20Z",
  "kind": "historical_regression_assertions",
  "observation": "The fixture added async with None as i containing with None as i marked error, async with None as i containing with None as j marked ok, and async for i containing for i marked error. The committed snapshot reports PLW2901 at the inner with target for reused i and at the inner for target for loop reuse. Existing nested-loop, assignment, augmented/annotated assignment, tuple/starred unpacking, nested-scope, subscript and attribute diagnostic assertions remain with shifted locations. Cast calls remain non-diagnostic in the shown assignment context. These are committed assertions available at the repair revision; no historical execution or CI result is supplied, and the newly authored Skill functional cases remain unexecuted."
}
```
