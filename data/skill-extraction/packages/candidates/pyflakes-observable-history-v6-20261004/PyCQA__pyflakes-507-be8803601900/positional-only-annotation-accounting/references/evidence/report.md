# Public reproduction and reported output

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:507:body",
  "source_id": "PyCQA/pyflakes:507:repair:be8803601900",
  "available_at": "2020-01-17T18:53:09Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report imports datetime as Foo and time as Bar from datetime, then defines def x(a: Foo, /, *, b: Bar): pass. Reported versions are flake8 3.7.9 (mccabe 0.6.1, pycodestyle 2.5.0, pyflakes 2.1.1) and pyflakes 2.1.1 on CPython 3.8.1/Linux. The reported flake8 example.py output is example.py:1:1: F401 'datetime.datetime as Foo' imported but unused. The reported pyflakes example.py output is example.py:1: 'datetime.datetime as Foo' imported but unused. These are reporter-supplied observations, not current package execution."
}
```
