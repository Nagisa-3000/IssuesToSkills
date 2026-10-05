# Historical regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5569:regression",
  "source_id": "pylint-dev/pylint:5569:repair:642268f63624",
  "available_at": "2022-01-11T15:50:30Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed fixture adds TypeSelfCallInMethod with classmethod b assigning cls.__a = '' and instance method a returning type(self).__a. The assignment is marked [unused-private-member]. The expected-output file adds unused-private-member at line 318, columns 8 through 15, in TypeSelfCallInMethod.b with message Unused private member `TypeSelfCallInMethod.__a`. The warning remains despite the call-based read. These are assertions available at the historical fixed commit, not proof of historical test execution."
}
```
