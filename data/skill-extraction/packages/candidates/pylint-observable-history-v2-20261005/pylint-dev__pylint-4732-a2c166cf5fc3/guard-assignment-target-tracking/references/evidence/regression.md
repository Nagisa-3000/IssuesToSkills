# Committed diagnostic assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4732:regression",
  "source_id": "pylint-dev/pylint:4732:repair:a2c166cf5fc3",
  "available_at": "2021-07-21T06:24:01Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed functional fixture added test_subscript_assignment with job_list = [None, None], job_list[0] = subprocess.Popen(\"ls\"), job_dict = {}, and job_dict[\"myjob\"] = subprocess.Popen(\"ls\"). Both calls were marked [consider-using-with]. The expected-output file added consider-using-with messages at 229:18 and 231:24 in test_subscript_assignment. The docstring explains that list or dict item assignments cannot be followed for later use by this variable-or-attribute tracking mechanism, so the message is emitted directly. These are committed assertions, not historical execution results."
}
```
