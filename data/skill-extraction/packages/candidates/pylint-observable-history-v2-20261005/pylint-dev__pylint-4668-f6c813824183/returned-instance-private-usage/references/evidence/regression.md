# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4668:regression",
  "source_id": "pylint-dev/pylint:4668:repair:f6c813824183",
  "available_at": "2021-07-18T13:11:15Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff added FalsePositive4668 to tests/functional/u/unused/unused_private_member.py. Its __new__ returned true_obj from an args branch after assigning func and __args; the other branch assigned false_obj.func, false_obj.__args and false_obj.__secret_bool and returned false_obj. Both __args assignments were annotated Do not emit message here. exec printed self.__secret_bool and called self.func(*self.__args). An unreachable return 3+4 provided a non-Name return value. The class locally disabled protected-access, no-member and unreachable diagnostics. These are committed assertions; historical execution is unknown."
}
```
