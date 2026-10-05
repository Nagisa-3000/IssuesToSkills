# Historical episode

SourceRecord: `pylint-dev/pylint:5586:repair:af974aa54980`.

The [report](evidence/body.md) gave this public reproduction:

```python
def func():
    try:
        print(value for value in range(1 / 0) if isinstance(value, int))
    except ZeroDivisionError:
        value = 1
```

The reported command was `pylint a.py`. Its output included E0601, `used-before-assignment`, at the filter's reference to `value`; the expected behavior was no such message. The report said `found_nodes` included the assignment from the exception handler. Its suggestion about `to_consume()` was a hypothesis, not the implemented repair.

The [implementation](evidence/fix.md), committed in revision `af974aa5498071baa73344a8ca84075b2e76305a`, changed the condition in `pylint/checkers/variables.py`. Within the existing comprehension/homonym conjunction, it added:

```python
and not (
    isinstance(node.parent.parent, nodes.Comprehension)
    and node.parent in node.parent.parent.ifs
)
```

This made the supported filter shape no longer satisfy that conjunction. The surrounding condition still led to `_check_late_binding_closure(node)` and `_loopvar_name(node)`. The patch was not a global suppression of E0601, and did not alter all name lookup or exception-handler assignments.

The [regression](evidence/regression.md) added
`tests/functional/u/use/used_before_assignment_filtered_comprehension.py`.
It used the same generator/filter example, then assigned and printed `value` in the handler. The supplied diff contains no expected `used-before-assignment` annotation. Historical execution results are unknown.

The repair also added release notes in `ChangeLog` and `doc/whatsnew/2.13.rst`, describing a false positive affecting unreleased development and closing issue #5586. These notes support the repair's stated scope; they are not separate independent fixes.

## Qualification boundary

The supplied validation-only report pins the issue, PR #5666 and merge revision and records a verified direct-closure relationship. Its original base passed 22 selected cases. Adding the historical regression to that base produced one failure, specifically an unexpected `used-before-assignment` on line 6, while those 22 cases still passed. The historical fixed checkout passed all 23 selected cases.

All three runs used the same reported runtime digest, completed without timeout, and reported exit codes consistent with their outcomes. The report was checked at `2026-10-04T12:49:34.799961+00:00`; this is not a historical execution date. It did not check whole-project regression and was not a formal SWE run. Its identity, hashes and limited conclusions are recorded in [provenance](provenance.json). No contemporary runtime detail is used as a historical repair mechanism.
