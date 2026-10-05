# Original reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5012:body",
  "source_id": "pylint-dev/pylint:5012:repair:fb750d39f82d",
  "available_at": "2021-09-15T10:15:05Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter ran `pylint pylint_repro.py` on a loop defining and calling `f(*, _i=i)` and `g(_i=i)`, both printing `_i`. Reported output contained W0640 at line 3, column 16 for the keyword-only default, but not the positional default. The reporter expected no warning because the default binds the value eagerly. Reported versions were Pylint 2.10.2, astroid 2.7.3, and Python 3.9.2 on Ubuntu 20.04.3 using pyenv. This is reporter-provided output, not a newly executed Skill test."
}
```
