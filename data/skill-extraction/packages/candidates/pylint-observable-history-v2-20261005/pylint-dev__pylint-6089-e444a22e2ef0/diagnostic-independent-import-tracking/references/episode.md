# Historical episode

Authoritative source: `pylint-dev/pylint:6089:repair:e444a22e2ef0`.

The [title](evidence/title.md) and [body](evidence/body.md) report a false W0611 warning for `x` in:

```python
from other import x, y

class MyClass:
    x = float(x)
    y = y
```

The reporter observed the false warning for `x`, not `y`, using
`python -m pylint --disable=all --enable=W0611 <path_to_file>`.
The default invocation did not produce the false positive.

The [merged implementation](evidence/fix.md) removed the early return conditioned on neither undefined-variable nor used-before-assignment being enabled. That return followed late-binding-closure checking and preceded definition/statement/frame processing. The implementation also removed the cached used-before-assignment enablement flag.

The [committed regression](evidence/regression.md) added `math.e` and `math.pi`, with `e = float(e)` and `pi = pi` in a class. Existing `os.environ` iteration remained.

Historical owners were `pylint/checkers/variables.py` and
`tests/functional/u/unused/unused_import_everything_disabled.py`.
These paths identify historical resources, not current bindings.

## Qualification audit boundary

The supplied independent qualification pins original base
`c50834ff6a47ed567756814a77aa370cf9b090a9`, fix `pylint-dev/pylint:pr:6096`,
and merged revision `e444a22e2ef0742e19f510b625f7ec3cea0a1180`.
It reports verified historical artifacts and direct issue closure.

Inspection of all three controls shows:

- Original base: exit 0, 20 selected tests passed.
- Base with committed regression: exit 1, the extended restricted-import test failed with unexpected unused-import; 19 selected tests passed.
- Historical fixed revision: exit 0, 20 selected tests passed.

The observation maps and run outputs agree. All runs report the same runtime digest, adopted workspaces, and no timeout. The reported 20 pass-to-pass cases compare original base to fixed revision; the separately reported failure-to-pass compares the regression-added control to fixed revision. These comparisons are not contradictory.

Qualification was checked on `2026-10-04T13:52:21.797647+00:00`. It is validation-only, not historical learned content. Its closure-event reference is qualification metadata, not an additional historical evidence card. Runtime details and replay commands do not authorize current Skill execution.

The qualification covers changed-test scope with original-base control, not whole-project regression or cross-project transfer. It does not execute the newly authored functional cases. Historical CI/test execution remains unknown.
