# Reported public reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4657:body",
  "source_id": "pylint-dev/pylint:4657:repair:c02682670e0d",
  "available_at": "2021-07-02T10:56:48Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report defined __attr_a = None, assigned cls.__attr_a = 'a' in a classmethod, and returned self.__attr_a in a property. Running pylint w0238.py reportedly emitted W0238 at 12:8 for UnusedPrivateMember.__attr_a. The expected behavior was no unused-private-member warning. Reported versions were pylint 2.9.3, astroid 2.6.2, and Python 3.8.3. This is a reported reproduction, not independent historical test-execution evidence."
}
```
