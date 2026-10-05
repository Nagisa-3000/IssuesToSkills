# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5981:fix",
  "source_id": "pylint-dev/pylint:5981:repair:2c29f4b7dff2",
  "available_at": "2022-03-26T09:00:28Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/base/name_checker/checker.py, the default TypeVar expression changed from ^_{0,2}(?:[^\\W\\da-z_]+|(?:[^\\W\\da-z_][^\\WA-Z_]+)+T?(?<!Type))(?:_co(?:ntra)?)?$ to ^_{0,2}(?:[^\\W\\da-z_]+|(?:[^\\W\\da-z_]+[^\\WA-Z_]+)+T?(?<!Type))(?:_co(?:ntra)?)?$. The added + repeats the uppercase-start class within the mixed-case branch. The changelog describes allowing multiple uppercase characters, including HVACModeT and IPAddressT, and closes #5981. doc/user_guide/options.rst adds IPAddressT as a good TypeVar name and retains bad examples DICT_T, CALLABLE_T, ENUM_T, DeviceType, and _StrType. Historical CI execution is unknown."
}
```
