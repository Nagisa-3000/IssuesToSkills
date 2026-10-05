# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4689:regression",
  "source_id": "pylint-dev/pylint:4689:repair:dd54e55265c5",
  "available_at": "2021-07-20T17:02:52Z",
  "kind": "historical_regression_assertions",
  "observation": "The functional fixture removed warning expectations for ThreadPoolExecutor and ProcessPoolExecutor and added their persistent construction, submit calls, and explicit shutdown without expected R1732. Added pools were expected not to warn when later used in with, including a module pool consumed in a nested function and tuple-unpacked pools. Unused tuple elements and mixed used/unused assignments retained individual consider-using-with expectations. Existing positive resource diagnostics, including subprocess.Popen and multiprocessing cases, remained in the expected-message file. These assertions were available at the historical commit; no historical execution is supplied. Later independent qualification is validation-only provenance, not execution of this Skill's functional definitions."
}
```
