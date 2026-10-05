# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4291:body",
  "source_id": "pylint-dev/pylint:4291:repair:d0591ba2a097",
  "available_at": "2021-04-03T16:14:15Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter stated that badfunctions could not be tested through functional tests and suspected that extension-loading code never executed. The supplied source called input(\"Yes or no ? (Y=1, n=0)\") and print(map(str, filter(1, [1, 2, 3]))), with plural bad-builtins annotations. Configuration set [MASTER] load-plugins = pylint.extensions.bad_builtin and [pylint.DEPRECATED_BUILTINS] bad-functions=map,input,filter,print. The report mentioned the separate tests/extensions/test_bad_builtin.py unit test. This is a reported reproduction and suspected diagnosis, not a historical execution log."
}
```
