# Original report and reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:483:body",
  "source_id": "PyCQA/pyflakes:483:repair:0af480e3351a",
  "available_at": "2019-10-24T18:26:15Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter requested pyflakes/flake8 coverage for Python 3.8's warning, saying it was very hard to get pytest to raise for it. The supplied program assigned x = 5 and used if x is (): print(\"hi\"). Reported output from /opt/python3.8/bin/python3 -m py_compile test.py showed test.py:5: SyntaxWarning: \"is\" with a literal. Did you mean \"==\"? This is reported compiler output; it is not a supplied execution result for the later analyzer repair."
}
```
