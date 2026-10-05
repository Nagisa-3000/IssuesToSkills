# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8719:body",
  "source_id": "pylint-dev/pylint:8719:repair:6fca82360c67",
  "available_at": "2023-05-26T21:11:45Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used CSV_KWARGS = {\"newline\": \"\", \"encoding\": \"utf-8\"} with open(\"foo.csv\", **CSV_KWARGS) in a with statement. The reported command pylint --score=false a.py emitted W1514 at line 2 column 5: Using open without explicitly specifying an encoding (unspecified-encoding). The reporter expected no warning for that supplied encoding. Reported versions were Pylint 2.17.4, astroid 2.15.4 and Python 3.10.10 on macOS Monterey v12.6. This is reported behavior, not execution by the authored Skill."
}
```
