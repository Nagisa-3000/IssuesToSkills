# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8747:regression",
  "source_id": "pylint-dev/pylint:8747:repair:8614ccf21aa7",
  "available_at": "2023-06-11T23:37:19Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed fixture adds ClassUnderTest methods annotated typing.NoReturn with sys.exit(1), annotated int with return 1, and incorrectly annotated typing.NoReturn with return 1. Each caller returns an integer from a try branch and invokes the corresponding method in an except ValueError branch. Only bug_pylint_8747_wrong, which calls the int-returning method, is marked and added to the expected diagnostic file for inconsistent-return-statements. The incorrect-annotation case states that pylint does not attempt to detect the annotation's falsehood. These are historical committed assertions; historical execution is unknown. Newly authored Skill functional cases remain unexecuted."
}
```
