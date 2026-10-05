# Committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4264:regression",
  "source_id": "pylint-dev/pylint:4264:repair:c1c41b849ce0",
  "available_at": "2021-03-30T07:19:15Z",
  "kind": "historical_regression_assertions",
  "observation": "The repair added import typing to tests/functional/n/name/name_styles.py. In Bar it added CLASS_CONST3: typing.ClassVar and variable2: typing.ClassVar[int] with an invalid-name marker. Existing direct ClassVar[int], ClassVar and lowercase ClassVar[str] examples remained. The expected output added invalid-name at line 159 in Bar: Class constant name \"variable2\" doesn't conform to UPPER_CASE naming style. Existing diagnostic locations shifted by one after the import insertion. These are committed assertions; historical execution status is unknown."
}
```
