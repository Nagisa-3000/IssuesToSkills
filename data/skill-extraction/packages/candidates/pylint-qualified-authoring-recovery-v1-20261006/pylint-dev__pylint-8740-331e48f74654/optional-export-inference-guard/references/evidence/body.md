# Original public report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8740:body",
  "source_id": "pylint-dev/pylint:8740:repair:331e48f74654",
  "available_at": "2023-06-06T16:36:42Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report supplies import sys, a sys.version_info >= (3, 7) condition, and __all__ += runners.__all__, with neither __all__ nor runners defined. Expected behavior is that Pylint does not crash. Reported output includes E0602 undefined-variable diagnostics for both names, followed by a traceback from leave_module through _check_all at assigned = next(node.igetattr(\"__all__\")), raising astroid.exceptions.InferenceError, and F0002 astroid-error. The reported environment is Ubuntu 18.04, CPython 3.11.3, Pylint 3.0.0b1 and astroid 3.0.0a3. This is reported reproduction output, not a historical regression-suite execution log."
}
```
