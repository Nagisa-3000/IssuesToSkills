# Committed no-message assertion

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3092:regression",
  "source_id": "pylint-dev/pylint:3092:repair:ce2af67d0e96",
  "available_at": "2019-09-23T08:04:38Z",
  "kind": "historical_regression_assertions",
  "observation": "The commit added test_missing_type_doc_google_docstring_exempt_kwonly_args to TestParamDocChecker in tests/extensions/test_check_docs.py. astroid.extract_node constructs identifier_kwarg_method(arg1:int, arg2:int, *, value1:str, value2:str) with a Google-style Args section describing all four parameters without explicit types. It calls self.checker.visit_functiondef(node) under self.assertNoMessages(). This is an assertion committed at the repair date, not evidence of historical execution; historical CI and test-execution status are unknown."
}
```
