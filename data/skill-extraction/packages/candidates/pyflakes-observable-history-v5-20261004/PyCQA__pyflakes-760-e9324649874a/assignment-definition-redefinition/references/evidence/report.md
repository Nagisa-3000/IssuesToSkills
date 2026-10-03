# Historical public reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:760:body",
  "source_id": "PyCQA/pyflakes:760:repair:e9324649874a",
  "available_at": "2023-01-12T14:27:12Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used flake8 6.0.0 with mccabe 0.7.0, pycodestyle 2.10.0, pyflakes 3.0.1, and CPython 3.11.1 on Linux. flake8 ok.py reported ok.py:5:5: F811 redefinition of unused 'bar' from line 2 for two methods named bar in one class. flake8 fail.py produced no reported output for class Foo containing bar = 0 followed by def bar(self): return 1. The report described a Factory Boy LazyAttribute named email hidden by a later decorated email method, acknowledged useful ordinary variable rebinding, and proposed denying attribute redefinition in class bodies. These are reported observations and a proposal, not independent execution by this package."
}
```
