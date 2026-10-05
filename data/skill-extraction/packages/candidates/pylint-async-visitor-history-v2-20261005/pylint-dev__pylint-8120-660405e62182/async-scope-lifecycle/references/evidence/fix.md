# Historical implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8120:fix",
  "source_id": "pylint-dev/pylint:8120:repair:660405e62182",
  "available_at": "2023-01-28T09:29:29Z",
  "kind": "historical_merged_implementation",
  "observation": "MultipleTypesChecker changed 'visit_functiondef = visit_classdef' to 'visit_functiondef = visit_asyncfunctiondef = visit_classdef', and 'leave_functiondef = leave_module = leave_classdef' to 'leave_functiondef = leave_asyncfunctiondef = leave_module = leave_classdef'. The release-note fragment says the redefined-variable-type false positive with async methods is fixed and closes #8120. The supplied implementation diff does not establish historical test execution."
}
```
