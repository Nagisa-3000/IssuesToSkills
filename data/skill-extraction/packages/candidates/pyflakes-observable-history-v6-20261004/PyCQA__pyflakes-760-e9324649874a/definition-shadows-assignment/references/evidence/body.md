# Historical public report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:760:body",
  "source_id": "PyCQA/pyflakes:760:repair:e9324649874a",
  "available_at": "2023-01-12T14:27:12Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used flake8 6.0.0 with pyflakes 3.0.1 on CPython 3.11.1/Linux. Their transcript reports `ok.py:5:5: F811 redefinition of unused 'bar' from line 2` for two same-name methods in a class, but no output for a class containing `bar = 0` followed by `def bar(self): return 1`. A factory example assigns an email LazyAttribute and later defines a decorated method named email, motivating the report. The reporter explicitly acknowledges useful ordinary variable rebinding and proposes denying attribute redefinition inside class bodies. This is a reported reproduction and proposal, not evidence that every proposed restriction was implemented."
}
```
