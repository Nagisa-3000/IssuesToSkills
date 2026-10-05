# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4657:regression",
  "source_id": "pylint-dev/pylint:4657:repair:c02682670e0d",
  "available_at": "2021-07-04T15:36:56Z",
  "kind": "historical_regression_assertions",
  "observation": "The unused_private_member fixture added FalsePositive4657 with cls.__attr_a assignment in a classmethod and self.__attr_a access in a property, without an unused-private-member expectation for that assignment. It also added self.__attr_c assignment annotated unused-private-member and a property returning cls.__attr_c annotated undefined-variable. The expected-output file retained seven existing unused-private-member entries, added HIGH confidence annotations, and added unused-private-member at 132:8 and undefined-variable at 137:15 for the negative case. These are assertions committed with the repair; historical test execution is unknown. Authored Skill cases remain unexecuted."
}
```
