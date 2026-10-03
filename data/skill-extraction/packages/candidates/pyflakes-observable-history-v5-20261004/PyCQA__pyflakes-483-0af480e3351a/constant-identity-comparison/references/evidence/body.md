# Reported reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:483:body",
  "source_id": "PyCQA/pyflakes:483:repair:0af480e3351a",
  "available_at": "2019-10-24T18:26:15Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter requested pyflakes/flake8 coverage for a Python 3.8 warning that was difficult to raise through pytest. The example sets x = 5 and uses if x is (): followed by print(\"hi\"). The reported command /opt/python3.8/bin/python3 -m py_compile test.py emitted test.py:5: SyntaxWarning: \"is\" with a literal. Did you mean \"==\"? This is reported compiler output, not execution by the Skill author."
}
```
