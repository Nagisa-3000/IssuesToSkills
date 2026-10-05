# Historical episode

Authoritative SourceRecord ID: `pylint-dev/pylint:8563:repair:4a485e28f0a5`.

The original report showed a filtered list comprehension passed to `min` with `default=0`. The emitted `consider-using-generator` suggestion omitted that keyword. Although the reporter requested no diagnostic, the merged resolution retained the warning and repaired the suggested text.

## Historical implementation

In `pylint/checkers/refactoring/refactoring_checker.py`, the branch required a named checked function, exactly one positional argument, and a `nodes.ListComp`. It extracted the comprehension body using `node.args[0].as_string()[1:-1]`.

The added code was:

```python
if node.keywords:
    inside_comp = f"({inside_comp})"
    inside_comp += ", "
    inside_comp += ", ".join(kw.as_string() for kw in node.keywords)
```

The comment changed from “exactly one argument” to “exactly one positional argument.” The positional eligibility gate was unchanged. The news fragment `doc/whatsnew/fragments/8563.bugfix` described improved output for `min()` calls with `default` and closed issue 8563.

## Committed regression assertions

Historical resources:

- `tests/functional/c/consider/consider_using_generator.py`
- `tests/functional/c/consider/consider_using_generator.txt`

The fixture added:

```python
min([x*x for x in range(10)], default=42)  # [consider-using-generator]
min((x*x for x in range(10)), default=42)
```

The expected diagnostic suggested exactly:

```python
min((x * x for x in range(10)), default=42)
```

Existing keyword-free expectations were retained. These assertions were available at the repair commit; supplied historical evidence does not establish historical test execution.

## Independent qualification review

The supplied validation-only report was checked at `2026-10-04T17:52:21.772633+00:00`. It pinned original base `f80a683efc2edb10d4c3780b9866f66a70d397d8`, fixed revision `4a485e28f0a5118b37550123c79f1f6d0dec42a4`, issue 8563, PR 8582, and a verified direct-closure relationship.

All three controls used the same runtime digest, reported no timeout, and adopted the workspace:

- Original base: exit 0, all 18 selected functional cases passed.
- Base with committed regression: exit 1, generator case failed, 17 others passed. Actual output omitted `default=42`; the new expected output retained it.
- Historical fixed revision: exit 0, all 18 selected cases passed.

The generator test belongs to the original-base pass-to-pass set and to the regression-added fail-to-pass comparison; these describe different controls, not contradictory outcomes. The report's runtime hash and observation hash are retained in provenance.

Scope: `changed-test-files-with-original-base-control`.

Exact limits: “Changed test files only; whole-project regression and cross-project transfer are untested.”

This qualification is not pre-cutoff learned content, historical CI execution, or execution of the authored Skill's functional cases.

## Evidence

- [Issue title](evidence/title.md)
- [Original report](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Committed regression assertions](evidence/regression.md)

The Workflow reconstructs conditional operations from these artifacts. Current probes and validations remain obligations for a new checkout, not inferred successful executions.
