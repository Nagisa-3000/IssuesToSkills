# Historical episode and learning boundary

Source: `pylint-dev/pylint:7528:repair:aca8dd546e6e`.

The repair became available at `2022-09-30T11:11:37Z`, before the exclusive cutoff `2024-01-01T00:00:00Z`.

## Original failure

The reporter created an enum-backed class-attribute set, constructed `other_set = set(self.ENUM_SET)`, iterated `self.ENUM_SET`, and removed elements from `other_set`.

The traceback reached `_common_cond_list_set` in `pylint/checkers/modified_iterating_checker.py`:

```python
node.value.func.expr.name == iter_obj.name
```

The iterable was an Attribute without `.name`. The resulting AttributeError was wrapped as AstroidError. The reported environment was Pylint 2.15.3, astroid 2.12.10, and Python 3.8.12; these are historical details, not current requirements.

## Implementation and assertions

The merged implementation narrowed the iterable annotation from `nodes.NodeNG` to `nodes.Name | nodes.Attribute` and introduced:

```python
iter_obj_name = (
    iter_obj.attrname
    if isinstance(iter_obj, nodes.Attribute)
    else iter_obj.name
)
```

The existing comparison used `iter_obj_name`; `infer_val == utils.safe_infer(iter_obj)` and receiver-side `.name` access remained.

The committed `tests/functional/m/modified_iterating.py` fixture added the enum/class-attribute-set copy case. Its companion `modified_iterating.txt` retained all 16 listed mutation diagnostics, shifting their line numbers by one. No target diagnostic was added for the new copy case.

The fragment `doc/whatsnew/fragments/7528.bugfix` described the class-attribute-set crash repair and stated `Closes #7528`.

These are historical implementation and committed assertion facts. Historical CI and test execution are unknown. The authored Workflow reconstructs supported operations, not their actual historical execution order.

## Independent qualification — validation only

The supplied complete three-control report was checked at `2026-10-04T15:50:58.225261+00:00`. Its pinned original base is `530d79051fc2d63512808f40032729b5e18f4769`; its fixed revision is `aca8dd546e6ec03d169eb84d7421d4a1427920ce`. It identifies issue 7528 and PR 7541, reports verified historical artifacts, and records a verified direct-closure relationship.

All three controls used the same selected public functional-test command and runtime SHA-256 `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`. They completed without timeout:

- Original base: exit 0, 18 selected tests passed.
- Base with committed regression: exit 1, the modified-iteration fixture failed with the iterable Attribute `.name` exception; the other 17 selected tests passed.
- Historical fixed revision: exit 0, all 18 selected tests passed.

The report lists one fail-to-pass and 18 pass-to-pass entries. These are not 19 distinct tests: the original modified-iteration fixture passed on the original base, whereas its augmented version failed on the base and passed on the fix.

Exact scope: `changed-test-files-with-original-base-control`.

Exact limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

This was not a formal SWE run or whole-project check. Its closure-event reference is validation metadata, not an additional historical evidence card. Later runtime and replay details are not historical repair mechanisms. Qualification did not execute the newly authored Skill eval cases.

## Generalization boundary

One independent bug cluster and fix support this Workflow. Additional node kinds, receiver-side repairs, other languages, broader alias analysis, whole-project correctness, and cross-project transfer are unverified. No external discovery or upstream package abstraction was performed.
