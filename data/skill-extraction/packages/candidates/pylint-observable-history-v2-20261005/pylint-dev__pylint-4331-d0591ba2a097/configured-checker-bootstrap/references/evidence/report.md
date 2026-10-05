# Public reproduction and diagnosis

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4331:body",
  "source_id": "pylint-dev/pylint:4331:repair:d0591ba2a097",
  "available_at": "2021-04-09T15:10:59Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The confusing_consecutive_elif fixture requested [MASTER] load-plugins=pylint.extensions.confusing_elif and expected confusing-consecutive-elif at line 10, column 4, in check_config. Its reported functional comparison failed because that diagnostic was absent. The proposed diagnosis was that LintModuleTest read configuration without loading requested modules before load_config_file. The reporter described trying guarded loading locally and discovering that fixture_docparams_missing, another configured-plugin fixture, lacked its expected-message .txt file. No historical successful CI or whole-project run is established."
}
```
