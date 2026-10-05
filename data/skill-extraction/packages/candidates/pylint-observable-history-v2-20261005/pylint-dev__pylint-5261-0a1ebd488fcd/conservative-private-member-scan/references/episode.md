# Historical episode

Authoritative source: `pylint-dev/pylint:5261:repair:0a1ebd488fcd`.

The [title](evidence/title.md) and [report](evidence/body.md) identify a crash in `_check_unused_private_variables` while examining `self.__class__.__ham`. The report's method omitted a `self` parameter; that is not the mechanism of the analyzer crash. The traceback identifies `child.expr.name`, where the receiver is an Attribute rather than a Name.

The [merged implementation](evidence/fix.md) changed historical path `pylint/checkers/classes.py`. Inside the Attribute branch, it first checks receiver type. A non-Name receiver causes `break`; a Name receiver retains the original attribute-name comparison and membership check against `self`, `cls`, and the class name. Bare-name matching, argument exclusion, and loop-else warning emission remain.

The break precedes attribute-name comparison. It conservatively suppresses the current candidate's warning when a compound receiver is encountered, even without establishing a match to that candidate. It is not precise `__class__` inference.

The [regression](evidence/regression.md) appends this fixture to historical path `tests/functional/u/unused/unused_private_member.py`:

```python
class Foo:
    __ham = 1

    def method(self):
        print(self.__class__.__ham)
```

Historical documentation paths `ChangeLog` and `doc/whatsnew/2.12.rst` also received crash-fix entries closing issue 5261. These paths describe history, not current bindings.

The repair was available at `2021-11-05T20:26:54Z`, strictly before the exclusive cutoff. Committed assertions are historical evidence; historical CI execution remains unknown.

## Validation-only qualification audit

The complete supplied controls were inspected for pinned issue/fix identity, original-base behavior, regression-only failure, fixed behavior, closure, and runtime consistency. This audit is not a historical event or an execution of the newly authored Skill.

- Report schema: `historical-causal-verification-v1`.
- Checked at: `2026-10-04T12:01:02.375366+00:00`.
- Base: `96e84595194073ea54a8c7730b86125049c0f4f9`.
- Fixed revision: `0a1ebd488fcdf7bf306615aba29e401ce49e3e10`.
- Issue: `pylint-dev/pylint:5261`.
- Fix: `pylint-dev/pylint:pr:5262`.
- Repair availability: `2021-11-05T20:26:54Z`.
- Exclusive cutoff: `2024-01-01T00:00:00Z`.
- Resolution relationship: verified direct closure.
- Validation report closure locator: `pylint-dev/pylint:5261:event:CE_lADOAtdnV84-V0IOzwAAAAFMZLuh`. This is an audit locator, not an additional core evidence card.
- Historical artifact verified: true; formal SWE run: false.

| Control | Exit | Result |
| --- | --- | --- |
| Original base | 0 | 19 selected cases passed |
| Base with committed regression | 1 | `unused_private_member` failed; 18 others passed |
| Historical fixed | 0 | 19 selected cases passed |

The regression-only log identifies the same unchecked `child.expr.name` access and `AttributeError: 'Attribute' object has no attribute 'name'`.

All non-target observations passed in all three controls: `regression_3416_unused_argument_raise`, `unused_argument`, `unused_argument_py3`, `unused_global_variable1`, `unused_global_variable2`, `unused_global_variable3`, `unused_global_variable4`, `unused_import`, `unused_import_assigned_to`, `unused_import_class_def_keyword`, `unused_import_everything_disabled`, `unused_import_positional_only_py38`, `unused_import_py30`, `unused_name_from_wilcard_import`, `unused_typing_imports`, `unused_variable`, `unused_variable_py36`, and `unused_variable_py38`. The target passed with its original fixture, failed when augmented by the regression, and passed with the historical fix. The report records one fail-to-pass and 19 pass-to-pass observations.

All three runs used identical selected functional-test argv, consistent runtime hashes, adopted isolated workspaces, and no timeout. The selection used the public functional harness with `python3 -m pytest`; its contemporary argv and sandbox/dependency details are validation-only, not historical mechanisms or current command authorization.

- Report hash: `abb07e56032d72b997b5cbed6b820007278f9cb04c0ba424b18e14be3e82f7fb`.
- Observations hash: `8efc2ebdadf28730807d3da38371a798a546a3ee0ddb2e3b1ae3ab455011c28a`.
- Runtime hash, identical across controls: `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.

Scope is `changed-test-files-with-original-base-control`. Whole-project regression and cross-project transfer are untested. Qualification does not backdate learned content, establish current checkout success, or execute authored Skill cases.
