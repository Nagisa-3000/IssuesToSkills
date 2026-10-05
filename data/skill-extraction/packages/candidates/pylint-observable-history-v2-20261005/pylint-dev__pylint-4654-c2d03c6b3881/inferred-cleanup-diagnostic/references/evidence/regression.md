# Committed regression assertion

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4654:regression",
  "source_id": "pylint-dev/pylint:4654:repair:c2d03c6b3881",
  "available_at": "2021-07-04T17:58:21Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed functional fixture adds test_suppress_in_exit_stack with a regression docstring for issue #4654. Under with contextlib.ExitStack() as stack, it assigns stack.enter_context(open('/sys/firmware/devicetree/base/hwid,location', 'r')) and marks the expression 'must not trigger'. Nearby existing subprocess.Popen controls show an unmanaged allocation marked consider-using-with and direct with usage without that warning mark. These assertions were available at the historical commit; historical execution is unknown. Later source qualification is recorded separately and is not backdated."
}
```
