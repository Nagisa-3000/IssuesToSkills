# Committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5557:regression",
  "source_id": "pylint-dev/pylint:5557:repair:2a69387352bd",
  "available_at": "2021-12-21T13:58:16Z",
  "kind": "historical_regression_assertions",
  "observation": "tests/functional/c/comparison_with_callable.py gained eventually_raise(), which calls print() then raises Exception, and a comparison a == eventually_raise documented as not emitting comparison-with-callable. The new tests/functional/c/comparison_with_callable_typing_constants.py imported Any and Optional and defined type_ == Any and type_ == Optional comparisons without expected callable-comparison warnings. Its comments explain that these typing constants are implemented as functions that raise when called and that Optional raises via typing._SpecialForm.__call__() rather than its own body. These were committed assertions available at the historical revision; historical CI/test execution is unknown."
}
```
