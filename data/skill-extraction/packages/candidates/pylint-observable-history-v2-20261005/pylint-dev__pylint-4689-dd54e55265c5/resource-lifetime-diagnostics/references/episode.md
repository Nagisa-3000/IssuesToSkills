# Historical episode

The original report asked why a persistent `concurrent.futures.ThreadPoolExecutor`, often kept as a global or singleton, had started receiving R1732 (`consider-using-with`). The reported lifecycle was a legitimate long-lived background task queue, not necessarily a lexical context.

The merged repair removed both executor constructor qualified names from the callable classification that drives the recommendation:

- `concurrent.futures.thread.ThreadPoolExecutor`
- `concurrent.futures.process.ProcessPoolExecutor`

It also deferred reporting for recognized constructor calls assigned to variables. Pending calls were stored in function, class, or module dictionaries. A later `with` whose context expression was an `astroid.Name` removed the first matching pending name, searching function, class, then module state. Remaining calls were reported at scope exit; reassignment of a pending name reported the earlier call. Assignment processing handled inferable tuple/list/set targets by pairing elements with inferred values and skipped cases it could not deduce. Tracked calls were not reported again by the immediate call checker.

This describes the supplied implementation, not a proof of arbitrary name resolution or control-flow completeness. In particular, three scope-category dictionaries are not a demonstrated general nested-frame stack.

## Historical bindings

These paths are historical references, not current bindings:

- Diagnostic owner: `pylint/checkers/refactoring/refactoring_checker.py`
- Public fixture: `tests/functional/c/consider/consider_using_with.py`
- Expected diagnostics: `tests/functional/c/consider/consider_using_with.txt`
- Historical runner used in later qualification: `tests/test_functional.py`
- Release documentation: `ChangeLog` and `doc/whatsnew/2.9.rst`

The fixture replaced executor warning expectations with persistent executor creation, submission, and explicit shutdown. It added module-level pools consumed later, a global pool consumed inside a function, tuple unpacking with both resources consumed, and mixed used/unused assignments. Existing positive resource warnings remained.

## Resolution and execution status

Source: `pylint-dev/pylint:4689:repair:dd54e55265c5`.

Repair revision: `dd54e55265c5b3dc8d99278e77a9c73359fb4ccf`, available 2021-07-20T17:02:52Z. The implementation's release note explicitly says it closes issue #4689.

The supplied historical artifacts contain committed assertions. Historical CI/test execution is unknown.

A separate qualification report checked the historical artifacts on 2026-10-04T11:10:00.066466+00:00. Its complete original-base, base-with-regression, and historical-fixed controls share runtime hash `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`. Original base passed 17 selected tests; base with the new regression failed the target and passed 16; the historical fixed revision passed all 17. All three runs completed without timeout, with exit codes 0, 1, and 0 respectively.

The report's `pass_to_pass` list contains all 17 names, including the target. The causal observation is nevertheless one target fail-to-pass under transplanted regression assertions and 16 other passing selected cases; do not reinterpret this metadata as 17 independent adjacent protections.

Qualification confirms the supplied direct-closure identity and limited causal replay. It is not a newly authored Skill execution, a historical CI event, a formal SWE run, or whole-project validation. Contemporary dependency details and output warnings are not historical repair mechanisms.
