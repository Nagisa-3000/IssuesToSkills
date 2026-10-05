# Historical report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3791:body",
  "source_id": "pylint-dev/pylint:3791:repair:a054796d7008",
  "available_at": "2020-08-24T18:24:24Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report applies @decorate(x*x for x in range(3)) to f(x) and g(y). It reports 4:12 E0602 undefined x only before f(x), and expects no error for either decorator. The reporter lists pylint 2.6.0, astroid 2.4.2 and Python 3.8.4 and states the problem did not occur with pylint 2.5.3. These are reported observations, not executed Skill checks."
}
```
