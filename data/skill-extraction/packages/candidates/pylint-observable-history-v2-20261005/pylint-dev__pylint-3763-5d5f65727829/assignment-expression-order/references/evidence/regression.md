# Historical committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3763:regression",
  "source_id": "pylint-dev/pylint:3763:repair:5d5f65727829",
  "available_at": "2021-03-26T21:01:46Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed assignment_expression fixture adds `x2: bool = b2 if (b2 := True) else False`, initialized augmented assignment `x3 += b3 if (b3 := 4) else 6`, and standalone `foo if (foo := 3 - 2) > 0 else 0` marked only for pointless-statement. It adds multiline f-string examples with a walrus assignment in an earlier interpolation and a read in a later interpolation under ordinary, annotated, and initialized augmented assignment. The expected-output file contains pointless-statement at line 56 and retains used-before-assignment for err_a, err_b, and err_d at shifted lines 74, 75, and 77. Visible genuine early-read examples include `assert err_a, (err_a := 2)` and `print(err_b and (err_b := 2))`. These are committed assertions; historical execution is unknown. Newly authored Skill functional cases remain unexecuted."
}
```
