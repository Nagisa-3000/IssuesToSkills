# Historical episode

Source: `pylint-dev/pylint:5817:repair:67055f422132`.

The [title](evidence/title.md) and [report](evidence/body.md) describe a false `E0601` on the filter `if e` in:

```python
def some_method():
    try:
        some_list = [e for e in (1, 2, 3) if e]
    except Exception as e:
        pass
```

The reporter ran `pylint used_before_assignment.py -E` using Pylint 2.12.2, astroid 2.9.3, and Python 3.9.0. They expected no error because the comprehension variable and handler variable have different scopes.

The [implementation](evidence/fix.md) changed `pylint/checkers/variables.py`. Previously, `if found_nodes:` entered filtering of assignments in exception handlers not containing the use. The new condition was:

```python
if found_nodes and (
    not isinstance(parent_node, nodes.Comprehension)
    or node not in parent_node.ifs
):
```

Thus the filtering step was bypassed specifically for a direct comprehension filter-test node. It was not removed for ordinary uses.

The [regression](evidence/regression.md) added `main5` to `tests/functional/u/used/used_before_assignment_issue626.py`, with `print([e for e in range(3) if e])` inside `try` and `except ValueError as e: print(e)`. The preceding test still annotated `print(e)` outside a handler with `[used-before-assignment]`.

The changelog and `doc/whatsnew/2.13.rst` described the same false-positive fix and said “Closes #5817.” The committed regression is an assertion, not evidence of historical execution; historical CI/test execution is unknown.

## Qualification audit, separate from historical observations

The supplied validation-only report pins base `8c0062f5ac0cfd80a74568e36d1e68e5a128c7f5`, fix `pylint-dev/pylint:pr:5818`, and merge revision `67055f4221324a5aba057c0e7e3a5ffdc41a7e35`, with a verified direct-closure relationship. Its controls were inspected:

- Original base: selected run exited 0; 16 passed.
- Base with committed regression: exited 1; 1 failed and 15 passed. The failure was the issue626 case, with unexpected `used-before-assignment` at line 49.
- Historical fixed revision: exited 0; 16 passed.
- All three runs had the same supplied runtime digest, no timeout, and adopted workspaces.

The original issue626 case is counted among original-to-fixed pass-to-pass controls while its expanded version is the regression fail-to-pass case. These are different comparisons, not contradictory outcomes.

Qualification occurred at `2026-10-04T13:23:18.609443+00:00`, after the historical cutoff. Its scope is `changed-test-files-with-original-base-control`; whole-project regression and transfer are untested. The closure-event locator is qualification metadata, not an additional authored historical evidence card. Later replay commands, dependency warnings, and logs do not supply historical mechanisms or execute Skill functional definitions.
