# Original reported symptom

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:633:body",
  "source_id": "PyCQA/pyflakes:633:repair:e02336c3d47c",
  "available_at": "2021-05-15T18:25:36Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used any((match := pattern.match(item)) for item in list), followed in the successful branch by word = match.group(0). They reported runtime output JOHN but F821 undefined name 'match' at the later use. Reported versions were flake8 3.9.2, mccabe 0.6.1, pycodestyle 2.7.0, pyflakes 2.3.1, and CPython 3.9.5 on Windows. This is a reported reproduction, not an independently recorded execution."
}
```
