# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7528:body",
  "source_id": "pylint-dev/pylint:7528:repair:aca8dd546e6e",
  "available_at": "2022-09-26T10:27:10Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied an enum-backed class-attribute set, constructed other_set = set(self.ENUM_SET), iterated self.ENUM_SET, and removed items from the separate copy. The traceback reached _common_cond_list_set and failed at node.value.func.expr.name == iter_obj.name with AttributeError: 'Attribute' object has no attribute 'name'; the exception was wrapped as AstroidError. Expected behavior was no error. Reported versions were Pylint 2.15.3, astroid 2.12.10, and Python 3.8.12. These are reported reproduction facts, not authored Skill execution."
}
```
