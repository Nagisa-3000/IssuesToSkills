# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4668:body",
  "source_id": "pylint-dev/pylint:4668:repair:f6c813824183",
  "available_at": "2021-07-04T08:35:11Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reported sample allocated obj in UnusedPrivateMember.__new__, assigned obj.func and obj.__args, and returned obj. exec read self.__args in self.func(*self.__args). Reported output from pylint sample2.py was W0238 at line 7 for UnusedPrivateMember.__args; the reporter expected no unused-private-member warning. Reported versions were pylint 3.0.0-a4, astroid 2.6.2 and Python 3.7.3. This is reporter-provided reproduction output, not an authored Skill execution."
}
```
