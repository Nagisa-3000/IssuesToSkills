# Committed diagnostic assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4238:regression",
  "source_id": "pylint-dev/pylint:4238:repair:5d5f65727829",
  "available_at": "2021-03-26T21:01:46Z",
  "kind": "historical_regression_assertions",
  "observation": "The assignment_expression fixture adds annotated and augmented assignments with walrus-bearing IfExp values, an Expr conditional case expected to emit pointless-statement, and multiline JoinedStr cases in ordinary, annotated, and augmented assignments without used-before-assignment expectations. Existing wrong-use controls including assert err_a, (err_a := 2) and print(err_b and (err_b := 2)) retain used-before-assignment expectations. The expected-output file retains err_a, err_b, and err_d diagnostics at shifted lines 74, 75, and 77 and adds pointless-statement at line 56. These are committed assertions; historical CI execution is unknown."
}
```
