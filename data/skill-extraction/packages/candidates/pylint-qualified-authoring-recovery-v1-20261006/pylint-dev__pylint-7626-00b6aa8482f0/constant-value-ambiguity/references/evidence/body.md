# Public reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7626:body",
  "source_id": "pylint-dev/pylint:7626:repair:00b6aa8482f0",
  "available_at": "2022-10-16T11:55:43Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report initializes flag_a and flag_b to False, sets them to True in separate loop branches over ['alfa', 'bravo'], and evaluates (flag_a and flag_b) or returns_false(). It reports R1709 suggesting returns_false(), although some_function() returns True. Removing or returns_false() removes the reported warning. The supplied command is pylint --rcfile=/dev/null thecodeabove.py; reported versions are pylint 2.15.4, astroid 2.12.11, and Python 3.8.12. This is reporter-supplied output, not a newly executed Skill check."
}
```
