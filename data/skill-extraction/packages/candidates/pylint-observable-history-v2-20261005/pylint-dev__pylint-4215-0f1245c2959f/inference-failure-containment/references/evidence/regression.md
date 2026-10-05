# Committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4215:regression",
  "source_id": "pylint-dev/pylint:4215:repair:0f1245c2959f",
  "available_at": "2021-03-08T16:55:45Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff adds github_issue_4215 to tests/functional/l/len_checks.py with if len(undefined_var): pass and if len(undefined_var2[0]): pass, each annotated undefined-variable. tests/functional/l/len_checks.txt adds only undefined-variable expectations for those inputs at lines 183 and 185. Existing len-as-condition expectations remain. These are committed assertions; historical execution status is unknown."
}
```
