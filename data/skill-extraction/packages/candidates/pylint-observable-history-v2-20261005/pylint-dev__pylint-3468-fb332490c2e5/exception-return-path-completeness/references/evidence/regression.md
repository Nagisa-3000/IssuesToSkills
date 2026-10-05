# Historical assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3468:regression",
  "source_id": "pylint-dev/pylint:3468:repair:fb332490c2e5",
  "available_at": "2020-09-06T19:08:03Z",
  "kind": "historical_regression_assertions",
  "observation": "The fixture added bug_3468 and bug_3468_variant with expected inconsistent-return-statements diagnostics. Both returned bar.baz in try and had AttributeError: pass; the variant also had KeyError: return True and ValueError: raise. Counterexamples used trailing return None or return None in the handler with no expected inconsistent-return diagnostic. Expected output added the positive diagnostics at historical lines 267 and 277 and retained previous expectations with shifted lines. The fixture disabled blacklisted-name. These are committed assertions available at the revision; historical execution is unknown and Skill functional evaluations remain unexecuted."
}
```
