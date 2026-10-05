# Committed diagnostic assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4331:regression",
  "source_id": "pylint-dev/pylint:4331:repair:d0591ba2a097",
  "available_at": "2021-04-09T19:13:14Z",
  "kind": "historical_regression_assertions",
  "observation": "The commit adds tests/functional/b/bad_builtins.py/.rc/.txt, loading pylint.extensions.bad_builtin and setting bad-functions=map,input,filter,print. Four bad-builtin rows assert input at 2:0 and filter, map, print at 3:15, 3:6, 3:0 respectively. The input and print messages are Used builtin function 'input' and Used builtin function 'print'; filter and map additionally say Using a list comprehension can be clearer. The commit annotates _private_func at line 4 with missing-return-doc and missing-return-type-doc and _private_func2 at line 10 with missing-yield-doc and missing-yield-type-doc, adding their four expected output rows. These assertions were available with the repair; historical CI execution is unknown."
}
```
