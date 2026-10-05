# Historical episode

Authoritative source: `pylint-dev/pylint:4676:repair:e4cd2ef1b016`.

The reporter received R1732 (`consider-using-with`) on `open(file2)` inside a conditional expression serving as the second context item. Its alternative was `contextlib.nullcontext()`. The expected behavior was no warning because the resource was already used in a `with` statement.

## Historical implementation and assertions

The implementation owner was `pylint/checkers/refactoring/refactoring_checker.py`. The resource-call condition formerly excluded only an immediate `astroid.With` parent:

```python
not isinstance(node.parent, astroid.With)
```

The repair replaced that condition with:

```python
not _is_part_of_with_items(node)
```

The helper obtained `frame = node.frame()`, walked `current.parent` while `current != frame`, and returned an inclusive line-range comparison at the first encountered `astroid.With`. Its interval began at `current.items[0][0].lineno` and ended at `current.items[-1][0].tolineno`; it compared `node.lineno` with those boundaries. If no qualifying ancestor was encountered, it returned `False`.

This is a frame-bounded source-line approximation, not a blanket exemption for body calls and not a general proof of resource lifetime ownership.

The regression owner was `tests/functional/c/consider/consider_using_with_open.py`. Added assertions covered a ternary with two `open` branches, a direct single-line `with`, and a multiline ternary with an inline body. The existing body-call warning control remained. The fixture disabled `multiple-statements` to permit compact syntax. `ChangeLog` and `doc/whatsnew/2.9.rst` recorded the fix; the changelog said `Closes #4676`.

## Evidence index

- [Issue title](evidence/title.md)
- [Original report](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Committed assertions](evidence/regression.md)

The [Workflow](workflow.md) links [probe](actions/probe.md), [repair](actions/repair.md), and [validation](actions/validate.md) contracts. These are authored conditional operations, not a claim that this exact task plan was historically executed.

## Validation-only qualification audit

The supplied complete independent report pins:

- Original base: `0f8212f43c60b41438a5485faec6cbec143f57c1`.
- Fixed revision: `e4cd2ef1b016dece104cccf33bd0d455f335f5af`.
- Issue: 4676; pull request: 4679.
- Verified direct closure, issue relationship, and historical artifact identity.
- Checked at `2026-10-04T11:05:04.836345+00:00`.

Its original-base, base-with-regression, and historical-fixed runs used the same runtime digest, the same selection of functional tests, and the same reported isolation scheme. All completed without timeout and adopted their workspaces.

The original base passed all 17 selected cases with exit 0. The base with committed regression assertions failed the `consider_using_with_open` target with unexpected diagnostics on lines 56, 65, and 66; 16 adjacent cases passed, with exit 1 overall. The historical fixed revision passed all 17 selected cases with exit 0.

The report lists one fail-to-pass target and 17 original-base-to-fixed pass-to-pass cases. The target belongs to the latter list because it passed before adding the regression assertions and at the fixed revision; it did not pass the base-with-regression control.

Scope is `changed-test-files-with-original-base-control`. Whole-project regression was not checked; cross-project transfer is untested. Qualification is validation of already-public artifacts after the cutoff, not historical information to backdate. Historical CI/test execution remains unknown. No newly authored Skill functional case was executed.

The exact qualification report hash is in [provenance](provenance.json). Contemporary runtime and log details support qualification only, not the historical mechanism.
