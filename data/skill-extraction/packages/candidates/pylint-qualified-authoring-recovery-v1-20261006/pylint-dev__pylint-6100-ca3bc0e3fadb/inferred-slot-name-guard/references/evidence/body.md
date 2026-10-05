# Public reproduction and traceback

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6100:body",
  "source_id": "pylint-dev/pylint:6100:repair:ca3bc0e3fadb",
  "available_at": "2022-04-01T19:01:17Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied class MyClass with __slots__ = [str] and command pylint test.py. On Pylint 2.13.4 / astroid 2.11.2 the reported traceback reached slots_names.append(inferred_slot.value) in _check_redefined_slots and raised AttributeError because the inferred node was a ClassDef without value, producing F0001 fatal. The requested behavior was no crash. This is a reported reproduction, not independently executed Skill evidence."
}
```
