# Committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4277:regression",
  "source_id": "pylint-dev/pylint:4277:repair:44a3aa25fd9b",
  "available_at": "2021-04-01T12:02:36Z",
  "kind": "historical_regression_assertions",
  "observation": "The default-style Final fixture expects invalid-name for variable: Final[str] and annotation-only variable2: typing.Final[int], accepting uppercase Final names. The snake_case fixture expects four uppercase Final names to fail while lowercase names pass. Both new configurations require Python 3.8. Final[typing.ClassVar[str]] demonstrates outer Final recognition, not general typing validity. The ClassVar name_styles fixture removes two lowercase class-constant diagnostics; the surrounding bad_enum_name expectation remains. These are committed assertions available at the repair revision; historical test execution is unknown in the supplied core."
}
```
