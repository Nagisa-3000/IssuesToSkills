# Historical episode

Authoritative repair source: `pylint-dev/pylint:6603:repair:5fee33ffcd52`.

The [title](evidence/title.md) and [report](evidence/body.md), available on 2022-05-13 at 12:40:29Z, describe a crash while analyzing:

```python
for i, num in enumerate():
    pass
```

The traceback reaches `RefactoringChecker._check_unnecessary_list_index_lookup` through `visit_for`. Its eligibility condition evaluates:

```python
or not isinstance(node.iter.args[0], nodes.Name)
```

without first checking whether the positional-argument list is empty.

The [merged implementation](evidence/fix.md), available at 2022-05-13T13:40:25Z, inserts:

```python
or not node.iter.args
```

after the `enumerate` name check and before the first-argument access. Python's short-circuit evaluation then causes an early return for an empty argument list.

Historical implementation owner:
`pylint/checkers/refactoring/refactoring_checker.py`.

The [committed regression](evidence/regression.md) adds the empty-call loop to:
`tests/functional/u/unnecessary/unnecessary_list_index_lookup.py`.
Its comment explicitly distinguishes runtime `TypeError` from analyzer robustness. These are committed assertions, not evidence of historical test execution.

The repair also documents the crash fix in `ChangeLog` and `doc/whatsnew/2.13.rst`, with `Closes #6603`.

## Qualification audit boundary

A supplied independent replay checked the original base
`55cacdbe554449f8f022916ab6c16506b2077cda`, that base with the committed regression, and the historical fixed revision
`5fee33ffcd52a9a078922a3ab881b0d165c32bfa`.

It reported:

- Original base: all 12 selected functional cases passed.
- Base with regression: the targeted list-index-lookup case failed; 11 others passed.
- Historical fixed revision: all 12 passed.
- All three runs used the same runtime digest and did not time out.
- Identity and direct closure to fix `pylint-dev/pylint:pr:6604` were verified.

The replay was checked in 2026, not in 2022. Its qualification scope and limits are retained in [provenance](provenance.json). It is validation-only source qualification, not a new historical mechanism, not whole-project verification, and not execution of the authored Skill evaluations.
