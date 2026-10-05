# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3737:body",
  "source_id": "pylint-dev/pylint:3737:repair:3ed4b9c0cc18",
  "available_at": "2020-07-12T18:25:07Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied Ipsum.dolor(self, elit=None) and LoremIpsum.dolor(self, *args, **kwargs), forwarding to super().dolor(*args, **kwargs). Running pylint lorem.py reportedly emitted W0222 signature-differs at the override; the expected behavior was no such error. Versions were pylint 2.5.3, astroid 2.4.2, and Python 3.8.2. This is a reported reproduction, not an executed Skill case."
}
```
