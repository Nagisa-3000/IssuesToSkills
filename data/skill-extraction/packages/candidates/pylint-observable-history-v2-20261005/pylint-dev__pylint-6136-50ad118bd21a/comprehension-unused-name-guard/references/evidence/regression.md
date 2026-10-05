# Committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6136:regression",
  "source_id": "pylint-dev/pylint:6136:repair:50ad118bd21a",
  "available_at": "2022-04-03T13:18:22Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed diff added `func5()` containing `x = []` and `assert [True for x in x]`, with a comment requiring a homonym between `for x` and `in x`. It removed the `[unused-variable]` annotation from `my_int: int` in `type_annotation_unused_after_comprehension`, followed by `_ = [print(sep=my_int, end=my_int) for my_int in range(10)]`, and removed its unused-variable expected-output record. Nearby used-before-assignment expectations remained. These assertions were available at the repair revision; historical execution is unknown and they are not newly executed Skill functional results."
}
```
