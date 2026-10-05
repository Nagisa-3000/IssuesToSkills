# Committed regression

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5261:regression",
  "source_id": "pylint-dev/pylint:5261:repair:0a1ebd488fcd",
  "available_at": "2021-11-05T20:26:54Z",
  "kind": "historical_regression_assertions",
  "observation": "The change appends a fixture to tests/functional/u/unused/unused_private_member.py: class Foo declares __ham = 1 and method(self) prints self.__class__.__ham. A comment identifies the __class__ regression and issue 5261. The added fixture has no unused-private-member expectation annotation. These are committed historical assertions; historical CI execution is not established. Later qualification is separate validation-only provenance."
}
```
