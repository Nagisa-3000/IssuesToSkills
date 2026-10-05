# Historical episode

Authoritative source: `pylint-dev/pylint:8120:repair:660405e62182`.

The original report used Pylint 2.15.10 with the `redefined_variable_type` extension loaded. Two separate async methods assigned `potato` to `Root()` and `{}`. The supplied output warned that its type changed from `a.Root` to `dict`. The synchronous equivalent did not warn. Although the report body called this a “false negative,” the output, title, and implementation describe a false positive.

The historical owner was `MultipleTypesChecker` in `pylint/extensions/redefined_variable_type.py`. The repair added async aliases to the existing scope lifecycle handlers:

```python
visit_functiondef = visit_asyncfunctiondef = visit_classdef
leave_functiondef = leave_asyncfunctiondef = leave_module = leave_classdef
```

The committed fixture at `tests/functional/ext/redefined_variable_type/redefined_variable_type.py` added two top-level async functions assigning `data` to a list of dictionaries and a dictionary, and two async methods assigning `potato` to an integer and a dictionary. No cross-scope warning was expected. Existing fixture context retained an expected warning for a within-scope change from `2.` to `'baz'`.

The release-note fragment at `doc/whatsnew/fragments/8120.false_positive` stated the fix and closed #8120. These implementation and assertion facts were available at the historical repair. Historical CI execution remains unknown.

## Validation-only qualification

The supplied complete independent report was checked on 2026-10-04, not at the historical commit date. It pinned original base `eb950615d77a6b979af6e0d9954fdb4197f4a722` and fixed revision `660405e6218258cee90570e8037c3b5e1440dcb6`, verified the direct closure through PR #8123, and used the same runtime digest across all controls.

The historical replay command selected `redefined_variable_type or regression_newtype_fstring` through `tests/test_functional.py`. Original-base tests passed. Base plus regression failed with unexpected `redefined-variable-type` messages at lines 99 and 109, while the adjacent test passed. The historical fixed checkout passed both selected tests. Exit codes were respectively 0, 1, and 0; no run timed out, and each adopted its workspace.

This supports narrow causal qualification of the supplied repair. It does not establish whole-project correctness, cross-project transfer, historical CI execution, or execution of this Skill. The replay command is audit context, not a current Oracle binding.

See [workflow](workflow.md), [provenance](provenance.json), and the four [evidence](evidence/title.md) [cards](evidence/body.md) [for implementation](evidence/fix.md) [and assertions](evidence/regression.md).
