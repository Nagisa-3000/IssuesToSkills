# Committed paired assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5965:regression",
  "source_id": "pylint-dev/pylint:5965:repair:025200c1fdb5",
  "available_at": "2022-03-25T09:45:57Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff adds uses_nonlocal() and uses_unrelated_nonlocal() to tests/functional/u/used/used_before_assignment_issue4761.py. The first initializes enclosing count, declares nonlocal count, reads count in try and increments it in except ValueError, with no expected used-before-assignment. The second declares nonlocal unrelated but assigns count in the handler; print(count) in try retains an expected used-before-assignment. The .txt file adds that diagnostic at line 35 and retains existing control-flow diagnostics with shifted coordinates. These are assertions committed with the repair; historical execution status is unknown and authored Skill functional cases have not been run."
}
```
