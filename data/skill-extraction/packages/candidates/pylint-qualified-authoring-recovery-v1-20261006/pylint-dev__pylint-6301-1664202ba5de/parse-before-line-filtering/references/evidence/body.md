# Original reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6301:body",
  "source_id": "pylint-dev/pylint:6301:repair:1664202ba5de",
  "available_at": "2022-04-14T07:39:37Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied valid Python importing os and defining bug(), with # pylint:disable=R followed by executable body statements. python -m pylint --ignore-imports=y ./bootstrap.py produced F0002 astroid-error on Pylint 2.13.5, Astroid 2.11.2, and Python 3.10.4. The traceback reached Similar.append_stream, LineSet, stripped_lines, and astroid.parse of joined lines, which raised an expected-indented-block error. Removing the suppression comment, omitting --ignore-imports=y, or downgrading to Pylint 2.12.2 and Astroid 2.9.3 reportedly avoided the failure. These are report observations, not newly executed Skill checks."
}
```
