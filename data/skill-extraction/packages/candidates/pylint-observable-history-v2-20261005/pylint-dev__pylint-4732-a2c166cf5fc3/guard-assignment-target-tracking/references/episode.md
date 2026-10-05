# Historical episode

Authoritative source: `pylint-dev/pylint:4732:repair:a2c166cf5fc3`.

Pylint 2.9.4 was reported to crash while linting:

```python
import subprocess

if index == 0:
    pobjs[index] = subprocess.Popen(
        commd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
```

The traceback entered `visit_assign`, then `_append_context_managers_to_stack`, and attempted `assignee.attrname` on a `Subscript`. The reporter observed failure in Python 3.9 and success in 3.8. This does not establish a version-specific repair mechanism.

The merged revision `a2c166cf5fc334c9011422340b9d9d1a575a2a25`, available at `2021-07-21T06:24:01Z`, extended the existing skip condition with:

```python
or not isinstance(assignee, (astroid.AssignName, astroid.AssignAttr))
```

Unsupported targets are skipped before deferred stack lookup and target-name extraction. Existing inference and recognized-resource-call conditions remain.

Historical implementation owner:
`pylint/checkers/refactoring/refactoring_checker.py`.

Historical assertion owners:
`tests/functional/c/consider/consider_using_with.py` and
`tests/functional/c/consider/consider_using_with.txt`.

The committed regression assigned `subprocess.Popen("ls")` to a list item and a dictionary item. Both expected `consider-using-with`. Skipping deferred tracking therefore must not suppress the immediate diagnostic.

## Historical status and later qualification

Historical evidence supplies implementation and committed assertions, not historical CI execution. Historical test execution is unknown.

The supplied validation-only qualification was checked at `2026-10-04T11:18:18.308700+00:00`. Its complete controls identify original base `970c5d25cc944cdf67f4b5acf7dd48fb495bcf7f`, base with committed regressions, and the historical fixed revision. Artifact identity and direct closure were verified.

The original base passed all 17 selected cases. Base with regression passed 16 and failed `consider_using_with` with the reported `Subscript.attrname` exception. Historical fixed passed all 17. The other selected cases passed across controls. All runs reported the same runtime digest, adopted workspaces, and no timeout. The existing target case is pass-to-pass on its original assertions and fail-to-pass after regression expansion.

Qualification scope is changed-test-files-with-original-base-control. Whole-project regression and cross-project transfer were not checked. Later replay is not backdated historical content or execution of authored Skill functional cases.

See [provenance](provenance.json), [title](evidence/title.md), [report](evidence/body.md), [implementation](evidence/fix.md), and [assertions](evidence/regression.md).
