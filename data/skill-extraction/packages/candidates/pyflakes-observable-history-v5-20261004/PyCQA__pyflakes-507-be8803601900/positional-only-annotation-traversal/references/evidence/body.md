# Original reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:507:body",
  "source_id": "PyCQA/pyflakes:507:repair:be8803601900",
  "available_at": "2020-01-17T18:53:09Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied `from datetime import datetime as Foo, time as Bar` followed by `def x(a: Foo, /, *, b: Bar): pass`. On CPython 3.8.1 on Linux, Pyflakes 2.1.1 reported `example.py:1: 'datetime.datetime as Foo' imported but unused`; Flake8 3.7.9, with mccabe 0.6.1, pycodestyle 2.5.0 and pyflakes 2.1.1, reported the corresponding F401 at example.py:1:1. The supplied historical commands were `flake8 --version`, `pyflakes --version`, `flake8 example.py`, and `pyflakes example.py`. These are reporter-provided pre-repair observations, not current command bindings."
}
```
