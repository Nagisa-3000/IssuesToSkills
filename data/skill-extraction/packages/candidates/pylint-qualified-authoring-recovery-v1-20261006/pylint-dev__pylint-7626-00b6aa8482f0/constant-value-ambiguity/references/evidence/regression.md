# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7626:regression",
  "source_id": "pylint-dev/pylint:7626:repair:00b6aa8482f0",
  "available_at": "2022-10-16T17:36:39Z",
  "kind": "historical_regression_assertions",
  "observation": "The ternary fixture replaces unknown true_value/false_value controls with TRUE_VALUE=True and FALSE_VALUE=False, adds unknown maybe_true/maybe_false expressions without expected rewrite diagnostics, and adds func_control_flow with False-initialized flags reassigned in separate branches of range(2). Its expression (flag_a and flag_b) or func5() has no expected simplify-boolean-expression diagnostic. Expected outputs retain definite truthy consider-using-ternary and definite falsy simplify-boolean-expression messages and change confidence from UNDEFINED to INFERENCE. These assertions were committed at the repair; their original historical execution status is unknown."
}
```
