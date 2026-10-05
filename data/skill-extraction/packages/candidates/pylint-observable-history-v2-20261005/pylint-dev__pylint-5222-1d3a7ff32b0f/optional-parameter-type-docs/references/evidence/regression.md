# Committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5222:regression",
  "source_id": "pylint-dev/pylint:5222:repair:1d3a7ff32b0f",
  "available_at": "2021-10-30T22:33:23Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed test_finds_args_without_type_numpy changes the function signature to my_func(named_arg, typed_arg: bool, untyped_arg, *args). Its Args section retains named_arg : object and *args : descriptions and adds typed_arg and untyped_arg as name-only headers with indented descriptions. The expectation changes from assertNoMessages to assertAddsMessages containing only MessageTest(msg_id='missing-type-doc', node=node, args=('untyped_arg',)). This exact assertion requires no missing-param-doc for either description-only parameter while retaining the legitimate missing-type diagnostic for the unannotated parameter. The return section remains. Assertions were available at the historical repair commit; original execution is unknown and authored Skill cases remain unexecuted."
}
```
