# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7528:regression",
  "source_id": "pylint-dev/pylint:7528:repair:aca8dd546e6e",
  "available_at": "2022-09-30T11:11:37Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed tests/functional/m/modified_iterating.py diff added an Enum import, MyEnum with FOO and BAR, and EnumClass with ENUM_SET. Its method constructed other_set = set(self.ENUM_SET), iterated self.ENUM_SET, and called other_set.remove(obj). The fixture added unrelated missing-class-docstring and missing-function-docstring suppressions. The tests/functional/m/modified_iterating.txt diff retained all 16 listed mutation diagnostics with line numbers increased by one and added no target diagnostic for the new copy case. These are committed assertion facts preserving existing list, set, and dictionary expectations; historical test and CI execution remain unknown."
}
```
