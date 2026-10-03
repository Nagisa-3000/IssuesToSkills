# Original report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:633:body",
  "source_id": "PyCQA/pyflakes:633:repair:e02336c3d47c",
  "available_at": "2021-05-15T18:25:36Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied any((match := pattern.match(item)) for item in list), followed by word = match.group(0) in the enclosing if body. They reported runtime output JOHN but F821 undefined name 'match' at that enclosing use. Their environment was flake8 3.9.2 with mccabe 0.6.1, pycodestyle 2.7.0, Pyflakes 2.3.1, and CPython 3.9.5 on Windows. This is a reported reproduction; no independent execution transcript accompanies it."
}
```
