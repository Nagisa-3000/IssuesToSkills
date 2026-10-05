# Historical episode

SourceRecord: `pylint-dev/pylint:4668:repair:f6c813824183`.

The report showed `UnusedPrivateMember.__new__` allocating `obj`, assigning `obj.func` and `obj.__args`, and returning `obj`. Its `exec` method read `self.__args`. The reported command `pylint sample2.py` emitted W0238 on the private assignment. Reported versions were pylint 3.0.0-a4, astroid 2.6.2, and Python 3.7.3; these are reproduction details, not current dependency requirements.

The historical implementation owner was `pylint/checkers/classes.py`. For each private assignment, the repair initialized acceptable receiver names with `self`. If the assignment scope was an `astroid.FunctionDef` named `__new__`, it added names from returns whose values were `astroid.Name`. A matching private attribute read through `self` could then consume an assignment on an acceptable receiver. The preceding matching branch involving `cls` and `self` remained.

The historical fixture owner was `tests/functional/u/unused/unused_private_member.py`. The added `FalsePositive4668` returned `true_obj` in one branch and `false_obj` in another. Both initialized `__args`; the second also initialized `__secret_bool`. An instance method read both attributes through `self`. An unreachable `return 3+4` exercised the non-name guard. The class locally disabled protected-access, no-member, and unreachable diagnostics, not the target diagnostic.

The ChangeLog said the fix closed #4668. The authoritative source pins PR #4708 and revision `f6c813824183d5d3738e0c426001a7b39948bc99`.

These facts support a name-based constructor exception, not general alias or object-identity inference. Historical assertions are available at the repair commit; historical CI/test execution remains unknown. The [Workflow](workflow.md) and Actions are newly authored representations of this repair, not claims that the historical maintainers executed these exact contracts.

## Validation-only qualification audit

The complete supplied causal-verification report was inspected separately from historical evidence and authored functional outcomes.

Identity and closure controls:

- Original base: `7cff708784fffac69efcef4b2351e525742c9e82`.
- Fixed revision: `f6c813824183d5d3738e0c426001a7b39948bc99`.
- Issue/fix: `pylint-dev/pylint:4668` / `pylint-dev/pylint:pr:4708`.
- Resolution relationship: direct closure, verified in the supplied report.
- Repair availability: `2021-07-18T13:11:15Z`, before the exclusive cutoff.
- Qualification time: `2026-10-04T11:03:51.741792+00:00`.
- Report hash: `f473d7fcb03a19fbdc8dca8654c00cf7dc4f7d9fd68eebebdcdb8b5ecba3f722`.
- Observations digest: `18c06636574cff65e859259a3e4ce480910153133e589886412722bc3e70de11`.

The original-base, base-with-regression, and historical-fixed observations identify the same 18 functional items. Original base passed all 18, exit 0. Base with committed regression assertions failed only `unused_private_member`, exit 1, with unexpected warnings at lines 149, 154, and 155; the other 17 passed. Historical fixed passed all 18, exit 0.

All three runs reported the same runtime digest, `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`, no timeout, and an adopted isolated workspace. The single fail-to-pass item was `tests.test_functional::test_functional[unused_private_member]`. The report's 18 pass-to-pass entries compare original-base with historical-fixed; they do not claim all items passed in the base-with-regression control.

Qualification scope is `changed-test-files-with-original-base-control`. The selected functional subset does not prove whole-project correctness or transfer. Whole-project regression was explicitly unchecked, and this was not a formal SWE run.

This later replay qualifies the historical source only. Its date is not backdated, its runtime details are not historical repair mechanisms, and it did not execute any newly authored Skill functional case. Current commands must be rebound to current public resources.
