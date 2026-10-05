# Reported reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4676:body",
  "source_id": "pylint-dev/pylint:4676:repair:e4cd2ef1b016",
  "available_at": "2021-07-06T06:22:07Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter enabled consider-using-with and used `with open(file1) as input_file1, (open(file2) if file2 else contextlib.nullcontext()) as input_file2:` across multiple lines. Reported output was R1732 at line 10, column 8, on the conditional open call. Expected behavior was no warning because the call was already used in a with statement. Reported versions were pylint 2.9.1, astroid 2.6.2, and Python 3.8.10. This is reported reproduction output, not an independently executed Skill evaluation."
}
```
