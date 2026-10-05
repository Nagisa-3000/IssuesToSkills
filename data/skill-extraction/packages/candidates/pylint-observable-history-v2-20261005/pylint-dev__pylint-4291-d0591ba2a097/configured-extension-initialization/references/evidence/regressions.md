# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4291:regression",
  "source_id": "pylint-dev/pylint:4291:repair:d0591ba2a097",
  "available_at": "2021-04-09T19:13:14Z",
  "kind": "historical_regression_assertions",
  "observation": "The commit adds tests/functional/b/bad_builtins.py, .rc and .txt. Configuration loads pylint.extensions.bad_builtin and sets bad-functions=map,input,filter,print. Source uses singular bad-builtin annotations. Expected output is bad-builtin:2:0::Used builtin function 'input'; bad-builtin:3:15::Used builtin function 'filter'. Using a list comprehension can be clearer.; bad-builtin:3:6::Used builtin function 'map'. Using a list comprehension can be clearer.; and bad-builtin:3:0::Used builtin function 'print'. It also updates tests/functional/f/fixture_docparams_missing.py and adds .txt expectations: missing-return-doc:4:0:_private_func:Missing return documentation; missing-return-type-doc:4:0:_private_func:Missing return type documentation; missing-yield-doc:10:0:_private_func2:Missing yield documentation; missing-yield-type-doc:10:0:_private_func2:Missing yield type documentation. These are committed assertions available at the historical revision, not historical execution results."
}
```
