# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5261:body",
  "source_id": "pylint-dev/pylint:5261:repair:0a1ebd488fcd",
  "available_at": "2021-11-05T14:23:47Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report declares class Foo with __ham = 1 and def foo() containing print(self.__class__.__ham). Its traceback reaches _check_unused_private_variables and fails at `and child.expr.name in (\"self\", \"cls\", node.name)` with AttributeError: 'Attribute' object has no attribute 'name'. This is a reported analyzer crash, not an executed authored Skill case."
}
```
