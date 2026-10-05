# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4264:body",
  "source_id": "pylint-dev/pylint:4264:repair:c1c41b849ce0",
  "available_at": "2021-03-29T22:56:43Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The supplied traceback reached visit_assignname and utils.is_class_var, failing at node.parent.annotation.value.name == \"ClassVar\" with AttributeError: 'Attribute' object has no attribute 'name'. The reporter used Pylint 2.7.3 through pre-commit, with Python 3.9 locally and 3.8 in CI, and stated that downgrading to 2.7.2 fixed the failure. Expected behavior was no traceback. The reported reproduction cloned sanitizers/octomachinery, changed the Pylint version and ran tox -e pre-commit -- pylint. The report does not establish an independently executed minimal regression test."
}
```
