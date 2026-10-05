# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5000:body",
  "source_id": "pylint-dev/pylint:5000:repair:bbaa7bc9200a",
  "available_at": "2021-09-14T07:16:55Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "With use-symbolic-message-instead enabled and command 'pylint test.py', the reporter observed I0023 for '# pylint: disable=W0223', recommending '# pylint: disable=abstract-method', but no output for '# pylint: disable=w0223'. The report says lowercase numeric IDs are accepted and should receive the same recommendation. Reported versions were Pylint 2.10.2, astroid 2.7.3, and Python 3.8.10. These are reporter observations, not executed Skill cases."
}
```
