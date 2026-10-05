# Reported reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4732:body",
  "source_id": "pylint-dev/pylint:4732:repair:a2c166cf5fc3",
  "available_at": "2021-07-20T21:38:29Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter ran Pylint 2.9.4 on pobjs[index] = subprocess.Popen(commd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) inside an if index == 0 branch. The traceback reached visit_assign, then _append_context_managers_to_stack, then else assignee.attrname, raising AttributeError: 'Subscript' object has no attribute 'attrname'. The reporter observed failure in Python 3.9 and success in 3.8. These reported observations do not establish historical CI execution or a version-specific repair mechanism."
}
```
