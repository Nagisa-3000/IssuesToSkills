# Historical episode

Authoritative source: `pylint-dev/pylint:4415:repair:24b5159e00b8`.

The [title](evidence/title.md) and [body](evidence/body.md) describe a minimal `collections.abc.MutableSequence` implementation reportedly producing `R0901: Too many ancestors (8/7)` with Pylint 2.7.4, astroid 2.5.2, and Python 3.7.7.

The [implementation](evidence/fix.md) replaced an unfiltered count with a count excluding ancestors whose resolved `qname()` appeared in an explicit frozenset. Selected builtins, collections, `_collections_abc`, and typing identities were listed; this was not a blanket exemption for all standard-library classes.

Historical counting owner: `pylint/checkers/design_analysis.py`, `MisdesignChecker.visit_classdef`.

Historical regression owners: `tests/functional/t/too/too_many_ancestors.py` and its `.txt` expected-output file.

These locators are historical, not current bindings.

The [assertions](evidence/regression.md) added `ItemSequence(MutableSequence)` without an expected ancestry warning and retained warnings for `Iiii` and `Jjjj`. Their expected counts changed from 9/7 and 10/7 to 8/7 and 9/7, consistent with excluding `builtins.object`.

The authored probe, repair, and validation contracts are a conditional abstraction, not automation claimed to have existed or executed historically.

## Qualification audit

The supplied complete qualification report pins base `9228c160b703792c0029471f818eb5505188e063`, merged repair `24b5159e00b8a380c1776dab6ce096df7bad79b1`, issue 4415, and PR 4416. It verifies the historical artifact and a direct-closure relationship.

Controls reviewed:

- Original base: exit 0; all 18 selected tests passed.
- Base with committed regression: exit 1; ancestry regression failed with an unexpected ancestry diagnostic; 17 selected tests passed.
- Historical fixed revision: exit 0; all 18 selected tests passed.

The individual observations agree with these aggregate logs. All runs used the same runtime hash, completed without timeout, and reported adopted workspaces under the supplied isolation setting. The original ancestry fixture is included in the original-base-to-fixed pass-to-pass control; this does not mean the augmented regression passed on the defective base.

Qualification time is `2026-10-04T10:45:12.598310+00:00`. Qualification is validation-only and does not backdate new knowledge. Historical CI execution remains unknown.

Scope is `changed-test-files-with-original-base-control`. Whole-project regression, cross-project transfer, formal SWE execution, and newly authored Skill functional cases were not executed. Replay commands and runtime details are not historical mechanisms or automatically authorized current commands.
