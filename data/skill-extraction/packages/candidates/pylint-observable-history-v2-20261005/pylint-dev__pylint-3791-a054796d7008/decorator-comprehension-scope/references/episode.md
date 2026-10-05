# Historical episode

Authoritative source: `pylint-dev/pylint:3791:repair:a054796d7008`.

## Report

The reporter supplied:

```python
def decorate(seq):
    return lambda f: f

@decorate(x*x for x in range(3))
def f(x):
    pass

@decorate(x*x for x in range(3))
def g(y):
    pass
```

The reported diagnostic was `4:12: E0602: Undefined variable 'x'`, only before `f(x)`. No error was expected for either decorator. The report listed pylint 2.6.0, astroid 2.4.2 and Python 3.8.4, and stated that pylint 2.5.3 had not shown this problem. These are reported historical facts, not current dependency requirements.

## Implementation

The merged change in `pylint/checkers/variables.py` retained the consumed-name gate and introduced a function-decorator-context alternative:

```python
if name in current_consumer.consumed and (
    utils.is_func_decorator(current_consumer.node)
    or not (
        current_consumer.scope_type == "comprehension"
        and self._has_homonym_in_upper_function_scope(node, i)
    )
):
    defnode = utils.assign_parent(current_consumer.consumed[name][0])
    self._check_late_binding_closure(node, defnode)
```

Previously the condition was the consumed-name gate followed directly by the negated comprehension/homonym conjunction. The repair therefore bypasses that exception in decorator context, not for arbitrary unbound names. Outside decorator context the old protection remains. Assignment-parent resolution and late-binding checking remain in the branch.

## Committed assertions

The change added fixtures in `tests/functional/u/undefined/undefined_variable.py` and expectations in `tests/functional/u/undefined/undefined_variable.txt`:

- `decorated1(x)`: `@decorator(x for x in range(3))`, without an added undefined-variable expectation.
- `decorated2(x)`: `@decorator(x * x for x in range(3))`, without an added undefined-variable expectation.
- `decorated3(x)`: a separate `@decorator(x)` above a valid generator decorator, with undefined `x` expected at historical coordinate 323:11.
- `decorated4(x)`: `@decorator(x * x * y for x in range(3))`, with undefined `y` expected at historical coordinate 328:19.

Coordinates and paths are historical references, not current bindings. Historical test execution is unknown; supplied assertions do not establish historical CI success.

## Validation-only qualification audit

The caller supplied a complete `historical-causal-verification-v1` report, checked at `2026-10-04T10:09:20.563285+00:00`. This section records inspection of that report, not execution by this Skill author and not pre-cutoff learned content.

Identity is pinned to issue `pylint-dev/pylint:3791`, fix `pylint-dev/pylint:pr:4737`, pull 4737, original base `31aa6fdad53ae3d768950b8cff976b7a7350c2de`, and merge revision `a054796d7008f4531b482490f917bdef1454b8fd`. Repair availability is `2021-07-22T19:31:25Z`, before the exclusive cutoff `2024-01-01T00:00:00Z`.

The report states verified direct closure and verified historical artifact identity. Its closure reference is `pylint-dev/pylint:3791:event:MDExOkNsb3NlZEV2ZW50NTA1NzcxNTI5Mg==`; no legacy-register relationship check is required. That reference is audit identity only, not an additional historical evidence card.

Complete supplied observations:

| Public test case | Original base | Base with regression | Historical fixed |
|---|---|---|---|
| `tests.test_functional::test_functional[undefined_loop_variable]` | passed | passed | passed |
| `tests.test_functional::test_functional[undefined_variable]` | passed | failed | passed |
| `tests.test_functional::test_functional[undefined_variable_crash_on_attribute]` | passed | passed | passed |
| `tests.test_functional::test_functional[undefined_variable_py30]` | passed | passed | passed |

The original-base control passed four cases. The regression-bearing base failed `undefined_variable` with unexpected undefined-variable diagnostics at lines 319, 324 and 328 and passed three other cases. The historical-fixed run passed all four. The fail-to-pass list contains the expanded `undefined_variable` case; the pass-to-pass list contains all four original-base cases. These describe different fixture states and are consistent.

All three runs have the same reported runtime digest, `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`, and the same argv:

```text
python3 -m pytest tests/test_functional.py -k "undefined_loop_variable or undefined_variable or undefined_variable_crash_on_attribute or undefined_variable_py30" -q --junitxml=/workspace/verification-results.xml
```

The corresponding exit codes are 0, 1, and 0. All runs report no timeout, adopted workspaces, four selected cases, 521 deselected cases, and nine warnings. The backend is `namespace-copy`; each run reports isolation `linux-copied-user-mount-pid-net-chroot-nobody-no-capabilities-v1`. These contemporary details establish report consistency only; they are not historical dependency facts or current Oracle bindings.

Scope is `changed-test-files-with-original-base-control`. The report explicitly states that whole-project regression was not checked, the replay was not a formal SWE run, and verification does not backdate new information. Cross-project transfer is untested. The qualification supports this historical source within that scope; it does not execute the newly authored Skill's functional cases.

Authoritative qualification report hash: `dc081a84a73fdf58b4bd8a03efc4b444c2c6db078f03226b2ac70e1d2b3db2bb`.

Supplied observations hash: `d4257c3b4d5a2fbbbbd6bbac1b2e96be8fa809dad5d28a79b3d058b7dcffbc57`.
