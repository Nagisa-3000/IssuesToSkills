# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5569:body",
  "source_id": "pylint-dev/pylint:5569:repair:642268f63624",
  "available_at": "2021-12-20T22:34:17Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reproduction assigns cls.__a = '' in a classmethod and reads type(self).__a in an instance method. Running pylint bugale_test.py reportedly produced AttributeError: 'Call' object has no attribute 'name' at attribute.expr.name in _check_unused_private_attributes during leave_classdef, followed by F0001 fatal. Reported versions were Pylint 2.12.2, astroid 2.9.0 and Python 3.9.5 on Windows 11. Expected behavior was not to crash. This is reporter-provided execution evidence, not historical CI."
}
```
