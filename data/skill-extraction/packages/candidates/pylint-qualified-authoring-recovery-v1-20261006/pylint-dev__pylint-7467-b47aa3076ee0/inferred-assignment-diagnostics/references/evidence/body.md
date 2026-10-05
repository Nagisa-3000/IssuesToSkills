# Historical report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7467:body",
  "source_id": "pylint-dev/pylint:7467:repair:b47aa3076ee0",
  "available_at": "2022-09-15T14:15:12Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied AnotherClass and Pylint7429, whose foo method assigns self.__class__, myvar = AnotherClass, \"myvalue\". The reported command pylint /tmp/pylint7429.py crashed at _check_invalid_class_object, inferred = safe_infer(node.parent.value), with AttributeError: 'ClassDef' object has no attribute 'value' and F0002 astroid-error. The reported environment was Pylint 2.15.2, astroid 2.12.9, Python 3.8.13, NixOS 22.05. Expected behavior was no crash; versions prior to 2.9 reportedly ran fine. This is a historical report, not an executed Skill functional case."
}
```
