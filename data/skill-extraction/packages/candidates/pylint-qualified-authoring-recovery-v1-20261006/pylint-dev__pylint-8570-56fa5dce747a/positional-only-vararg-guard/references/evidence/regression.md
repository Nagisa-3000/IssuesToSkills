# Historical committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8570:regression",
  "source_id": "pylint-dev/pylint:8570:repair:56fa5dce747a",
  "available_at": "2023-04-13T06:46:51Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed keyword_arg_before_vararg_positional_only fixture asserted warnings for name1(param1, /, param2=True, *args), name2(param1=True, /, param2=True, *args), and name3(param1, param2=True, /, param3=True, *args). It asserted no target warning for name4(param1, /, *args), name5(param1=True, /, *args), name6(param1, /, *args, param2=True), name7(param1=True, /, *args, param2=True), and name8(param1, param2=True, /, *args, param3=True). The .rc set min_pyver=3.8. The .txt contained only the three warnings on lines 6, 7, and 8. These are committed assertions, not historical execution results; historical execution is unknown and Skill functional cases are unexecuted."
}
```
