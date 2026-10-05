# Committed regression assertion

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5586:regression",
  "source_id": "pylint-dev/pylint:5586:repair:af974aa54980",
  "available_at": "2022-01-12T16:18:43Z",
  "kind": "historical_regression_assertions",
  "observation": "The repair added tests/functional/u/use/used_before_assignment_filtered_comprehension.py with a function containing the reported generator/filter in try and an except ZeroDivisionError block assigning value = 1 and printing value. The file described a homonym between a filtered comprehension and an assignment in an except block and linked issue #5586. No expected used-before-assignment annotation appears in the supplied test diff. These are committed regression assertions; historical test execution is unknown."
}
```
