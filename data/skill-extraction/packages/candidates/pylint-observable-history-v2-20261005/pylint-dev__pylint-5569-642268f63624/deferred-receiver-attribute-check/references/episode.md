# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:5569:repair:642268f63624`.

The [title](evidence/title.md) and [report](evidence/body.md), available on 2021-12-20, describe this reproduction:

```python
class A:
    @classmethod
    def b(cls) -> None:
        cls.__a = ''

    def a(self):
        type(self).__a
```

The reporter ran `pylint bugale_test.py` with Pylint 2.12.2, astroid 2.9.0 and Python 3.9.5 on Windows 11. During `leave_classdef`, `_check_unused_private_attributes` accessed `attribute.expr.name` on a `Call`, causing AttributeError and an F0001 fatal diagnostic.

The [merged implementation](evidence/fix.md), revision `642268f636241e733409cb6cdf59f0eb87a03ae1`, became available on 2022-01-11. In historical owner `pylint/checkers/classes/class_checker.py`, it:
- inserted `if self._is_type_self_call(attribute.expr): continue` after attribute-name matching and before the subsequent name-based condition;
- annotated `_is_type_self_call` with `nodes.NodeNG` and `bool`;
- changed `_is_mandatory_method_param` to use `_first_attrs[-1]` when available;
- otherwise obtained the closest `nodes.FunctionDef` ancestor through `utils.get_node_first_ancestor_of_type`;
- returned false if no function or positional arguments existed, otherwise compared a `nodes.Name` with the first positional argument's name.

The implementation comment explains that the function may already have been unregistered. The supplied diff exposes only the beginning of the existing recognizer; inspect its complete conditions in current code rather than inventing them.

The [committed regression](evidence/regression.md) changed historical fixture `tests/functional/u/unused/unused_private_member.py` and its `.txt` expectation:

```python
class TypeSelfCallInMethod:
    """Regression test for issue 5569"""
    @classmethod
    def b(cls) -> None:
        cls.__a = ''  # [unused-private-member]

    def a(self):
        return type(self).__a
```

Expected output retained the warning for `TypeSelfCallInMethod.__a` at the assignment in `b`. Avoiding the crash therefore did not redefine this read as a recognized use.

Historical ChangeLog and `doc/whatsnew/2.13.rst` entries describe the crash fix and state `Closes #5569`. Historical paths and commands above are evidence, not current execution bindings. Historical CI/test execution is unknown.

## Validation-only qualification

The complete supplied qualification controls were inspected for pinned identity, direct closure, original-base behavior, regression-induced failure, fixed behavior and runtime consistency:
- original base: 20 selected cases passed, exit 0;
- base with regression: the private-member case failed with the matching call-receiver exception; 19 others passed, exit 1;
- historical fixed: all 20 selected cases passed, exit 0.

The 20 pass-to-pass entries compare original base with fixed revision, including the private-member case. That same case is fail-to-pass when comparing regression-added base with fixed revision. All three runs shared the runtime digest and did not time out.

The 2026-10-04 qualification supports `changed-test-files-with-original-base-control` only. It is not historical CI, whole-project regression, a formal SWE run, cross-project evidence or execution of this Skill. [Provenance](provenance.json) records the immutable hashes, identities and scope.
