# Historical report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6593:body",
  "source_id": "pylint-dev/pylint:6593:repair:912a1711a73e",
  "available_at": "2022-05-12T19:29:05Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter ran `pylint a.py` on `for i, num in enumerate(range(3)): pass` followed by `print(i, num)`. The reported output contained W0631 undefined-loop-variable for both i and num on line 3. Expected behavior was no message; the reporter noted no messages without enumerate. Reported versions were Pylint 2.14.0-b1, astroid 2.12.0-dev0, and Python 3.10.2. This is reported reproduction output, not an independently executed Skill evaluation."
}
```
