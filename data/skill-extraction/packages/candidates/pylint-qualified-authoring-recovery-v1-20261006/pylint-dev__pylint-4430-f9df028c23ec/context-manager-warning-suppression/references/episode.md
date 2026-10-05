# Historical episode

SourceRecord: `pylint-dev/pylint:4430:repair:f9df028c23ec`.

The report reproduced R1732 `consider-using-with` on `self.fd = open("foo")` in `C.__enter__`, although `C.__exit__` closed the handle. Its environment was pylint 2.8.2, astroid 2.5.6, Python 3.9.4. The request also suggested warning for missing cleanup; the merged repair does not implement that suggestion.

At revision `f9df028c23ec5458c80d1dd62a31b217a11ce44f`, historical path `pylint/checkers/refactoring/refactoring_checker.py` gained `_is_inside_context_manager(node)`. It obtains `node.frame()`, rejects frames outside `astroid.FunctionDef`, `astroid.BoundMethod`, and `astroid.UnboundMethod`, then recognizes frame name `__enter__` or `utils.decorated_with(frame, "contextlib.contextmanager")`.

Both the assigned-call condition using `CALLS_RETURNING_CONTEXT_MANAGERS` and the replaceable-call condition using `CALLS_THAT_COULD_BE_REPLACED_BY_WITH` retained safe inference and added `and not _is_inside_context_manager(node)`.

Historical assertions were committed in:

- `tests/functional/c/consider/consider_using_with.py` and `.txt`
- `tests/functional/c/consider/consider_using_with_open.py` and `.txt`

They covered silent lock acquisition and open assignments in `__enter__` and decorated generators, qualified and imported decorators, retained ordinary warnings, and a new module-level open warning. The open fixture explains its separation because standard open inference was unavailable on PyPy.

Historical CI/test-execution status is unknown. The Workflow contracts are authored from these artifacts, not a claim that this exact operational sequence was executed historically.

## Validation-only qualification audit

The supplied independent report was checked at `2026-10-04T10:47:46.541329+00:00`. It pinned original base `9528500f8a4f9927350a7b62c87f634f3ec26722`, the merged revision above, issue 4430, and PR 4453. It verified historical artifacts and direct closure. Its closure locator was `pylint-dev/pylint:4430:event:MDExOkNsb3NlZEV2ZW50NDcxMDc0ODYxMA==`; this is a validation-only locator, not an additional historical evidence card.

The supplied complete controls show:

- Original base: 16 selected functional tests passed; exit code 0.
- Base with committed regression assertions: the expanded `consider_using_with` and `consider_using_with_open` fixtures failed with unexpected warnings in managed cases; 14 other selected tests passed; exit code 1.
- Historical fixed revision: all 16 selected tests passed; exit code 0.

All runs completed without timeout, adopted the workspace, and used the same runtime hash. The report's 16-entry pass-to-pass list describes original-base to historical-fixed preservation; it does not assert that the two expanded fixtures passed on base-with-regression.

The observations support the two-fixture causal repair within the supplied scope. They do not execute the newly authored Skill cases or establish whole-project correctness or transfer. The replay was not a formal SWE run. Later runtime/dependency details are not historical mechanisms.

Scope: `changed-test-files-with-original-base-control`.

Limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

Qualification hashes and the control summary appear in [provenance](provenance.json). The replay date is not backdated.
