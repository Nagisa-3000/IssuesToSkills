# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5981:regression",
  "source_id": "pylint-dev/pylint:5981:repair:2c29f4b7dff2",
  "available_at": "2022-03-26T09:00:28Z",
  "kind": "historical_regression_assertions",
  "observation": "The default TypeVar naming fixture adds HVACModeT = TypeVar(\"HVACModeT\") and _IPAddress = TypeVar(\"_IPAddress\") without invalid-name expectations, and IPAddressU = TypeVar(\"IPAddressU\") with an invalid-name expectation. CALLABLE_T, DeviceType, camelCase forms, and prefixed bad names remain invalid. The companion expected-output file updates positions, adds the IPAddressU diagnostic, and retains variance diagnostics. These are committed assertions available at the repair; original execution is unknown and newly authored Skill evaluations have not been executed."
}
```
