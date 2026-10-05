# Historical committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3798:regression",
  "source_id": "pylint-dev/pylint:3798:repair:1a1dea5d6bc2",
  "available_at": "2020-10-10T08:09:42Z",
  "kind": "historical_regression_assertions",
  "observation": "The commit added tests/functional/p/postponed_evaluation_activated_with_alias.py importing annotations from __future__ as __annotations__. Cases were MyClass.from_string returning MyClass, MyClass.validate_b taking OtherClass before its definition, Example.obj annotated with Other before its definition, and ExampleSelf.next annotated with ExampleSelf. The fixture disabled missing-docstring, no-self-use, unused-argument, pointless-statement, too-few-public-methods and no-name-in-module, but not undefined-variable or used-before-assignment. The companion .rc set [testoptions] min_pyver=3.7. These are assertions committed at the historical repair; historical test and CI execution are unknown. Later qualification is separate validation-only provenance."
}
```
