# Historical regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3791:regression",
  "source_id": "pylint-dev/pylint:3791:repair:a054796d7008",
  "available_at": "2021-07-22T19:31:25Z",
  "kind": "historical_regression_assertions",
  "observation": "The undefined_variable fixture adds decorated1(x) with @decorator(x for x in range(3)) and decorated2(x) with @decorator(x * x for x in range(3)), without added undefined-variable expectations. It adds decorated3(x) with a separate @decorator(x) above a valid generator decorator and decorated4(x) with @decorator(x * x * y for x in range(3)). The companion expected-output file adds undefined x at 323:11 for decorated3 and undefined y at 328:19 for decorated4. These are committed assertions; historical test execution is unknown."
}
```
