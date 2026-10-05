# Original reproduction and traceback

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8735:body",
  "source_id": "pylint-dev/pylint:8735:repair:33d3f22b767e",
  "available_at": "2023-06-06T08:59:09Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report supplied module-level code 'nonlocal X' followed by 'X = whatever' and expected no fatal error. Reported output included E0117 nonlocal-without-binding, then an assignment callback failure in VariablesChecker._check_self_cls_assign at 'scope = node.scope().parent.scope()': AttributeError because the parent was None, followed by F0002 astroid-error. The reported environment was Ubuntu 18.04, CPython 3.11.3, Pylint 3.0.0b1, astroid 3.0.0a3. These are user-reported observations, not newly executed Skill checks."
}
```
