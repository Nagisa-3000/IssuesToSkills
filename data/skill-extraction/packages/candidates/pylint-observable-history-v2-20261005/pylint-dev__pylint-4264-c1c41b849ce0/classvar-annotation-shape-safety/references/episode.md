# Historical episode and validation-only audit

Source: `pylint-dev/pylint:4264:repair:c1c41b849ce0`.

## Historical mechanism

The [title](evidence/title.md) and [body](evidence/body.md) report a 2.7.3 regression with `AttributeError: 'Attribute' object has no attribute 'name'`. The traceback reached `visit_assignname`, then `utils.is_class_var`, then the expression `node.parent.annotation.value.name == "ClassVar"`. The reporter said downgrading to 2.7.2 avoided the failure. Multiprocessing transported the failure; it was not the repaired mechanism.

The [merged implementation](evidence/fix.md) changed the historical owner `pylint/checkers/utils.py:is_class_var`. It rejected parents other than `astroid.AnnAssign`, read the annotation, unwrapped one Subscript, and explicitly distinguished:
- `astroid.Name`, using `.name`;
- `astroid.Attribute`, using `.attrname`.

Either identifier had to equal `ClassVar`. Other shapes returned false.

The [regression assertions](evidence/regression.md) changed `tests/functional/n/name/name_styles.py` and its expected diagnostic file. Existing direct forms remained. The additions were `import typing` and, in class `Bar`:
```python
CLASS_CONST3: typing.ClassVar
variable2: typing.ClassVar[int]  # [invalid-name]
```
The expected output added the class-constant `invalid-name` message for `variable2`. Existing locations shifted after the inserted import. These are historical committed assertions, not evidence of historical execution.

The Attribute match is syntactic: it does not resolve aliases or verify qualifier identity.

## Independent qualification: validation only

The complete supplied three-control report was inspected. Identity was pinned to base `245feaba1ac5d57504a06b25c53aa80800ea643e`, merged repair `c1c41b849ce070447f3efe4ed1a91068d4c85362`, issue `pylint-dev/pylint:4264`, and fix `pylint-dev/pylint:pr:4266`. It verified historical artifact identity and direct closure, using relationship reference `pylint-dev/pylint:4264:event:MDExOkNsb3NlZEV2ZW50NDUyNTY1MTk0Nw==`. That reference is validation identity data, not an additional historical evidence card.

Qualification occurred at `2026-10-04T10:34:21.059440+00:00`. Report hash:
`fa4ddbcf38bd6f6b93f50f62d4830dbae2b03ea54523d87599e67331c0294d29`.

Observations hash:
`781bcafb5a8459d32dfec2841980f51b29d51c4ee93cf79d2d56ee3919163989`.

All three runs report runtime hash:
`862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`,
no timeout, and adopted workspaces.

The selected cases were `namePresetCamelCase`, `name_good_bad_names_regex`, `name_preset_snake_case`, `name_styles`, `namedtuple_member_inference`, and `names_in__all__`.

| Control | Observation |
|---|---|
| Original base | Six passed; exit 0 |
| Base with committed regression | `name_styles` failed at the unsafe `.name` access with AttributeError; five passed; exit 1 |
| Historical fixed | Six passed; exit 0 |

The report's fail-to-pass list contains `name_styles`. Its pass-to-pass list contains all six original-base passing cases; these are distinct comparisons, not additional independent repairs.

The replay selected the cases using `python3 -m pytest tests/test_functional.py -k ... -q`, with JUnit output in individual runs. This is validation-only provenance, not a current oracle command or a historical mechanism.

Scope is `changed-test-files-with-original-base-control`. Whole-project regression was not checked; this was not a formal SWE run. Cross-project transfer is untested. The later controls do not backdate execution evidence and do not execute this newly authored Skill's functional cases. Historical CI status remains unknown.
