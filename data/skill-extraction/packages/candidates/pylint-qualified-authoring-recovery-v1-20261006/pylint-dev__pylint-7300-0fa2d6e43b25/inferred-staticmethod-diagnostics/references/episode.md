# Historical episode

SourceRecord: `pylint-dev/pylint:7300:repair:0fa2d6e43b25`.

The original report described `no-self-argument` on methods decorated with an alias of `staticmethod`. It also described a `TYPE_CHECKING` arrangement and stated that configuration was irrelevant. The reported environment was pylint 2.12.2, astroid 2.9.0, Python 3.8.13 on Ubuntu 20.04; these are report context, not requirements for current execution. The historical reproduction command was `pylint main.py`.

At revision `0fa2d6e43b25bb4863b0301435b5c5dbef7a1b64`, the implementation added:

```python
elif "builtins.staticmethod" in node.decoratornames():
    # Check if there is a decorator which is not named `staticmethod` but is assigned to one.
    return
```

Historical owner path: `pylint/checkers/classes/class_checker.py`. The branch followed existing direct-staticmethod handling and preceded the check for absence of both regular and positional-only arguments. The existing direct branch's assignment to `_first_attrs[-1]` remained in that branch; the new inferred branch returned directly. This is not evidence to make additional bookkeeping changes.

Historical fixture paths:

- `tests/functional/n/no/no_self_argument.py`
- `tests/functional/n/no/no_self_argument.txt`

The fixture added `MYSTATICMETHOD = staticmethod`, a `returns_staticmethod` function returning `staticmethod(my_function)`, and three methods: a zero-argument direct staticmethod, a zero-argument aliased staticmethod, and a two-argument wrapper-decorated method. The expected output retained two ordinary `no-self-argument` diagnostics, with adjusted line numbers. Committed assertions do not establish historical test execution; that status is unknown.

## Validation-only qualification audit

The supplied independent report pins original base `6f9c371c4f82281570869be2e4c609844bfd8c34`, fix `pylint-dev/pylint:pr:7301`, and merged revision `0fa2d6e43b25bb4863b0301435b5c5dbef7a1b64`. It verifies the direct-closure relationship and the historical artifact. Its closure event reference is audit metadata, not an additional packaged historical evidence card.

The complete supplied controls show:

- Original base: 26 selected tests passed, exit 0.
- Base with committed regression: `no_self_argument` failed on an unexpected `no-method-argument` at line 33; 25 selected tests passed, exit 1.
- Historical fixed revision: 26 selected tests passed, exit 0.
- All three runs used the same runtime digest, did not time out, and adopted the workspace.

The report lists one fail-to-pass case and 26 pass-to-pass entries; the latter includes `no_self_argument` as an original-base-to-fixed control, not as an additional neighboring test. The inspected observations contain 26 selected cases in total.

Checked at: `2026-10-04T15:19:46.537487+00:00`.

Qualification scope: `changed-test-files-with-original-base-control`.

Scope limits: **Changed test files only; whole-project regression and cross-project transfer are untested.**

Runtime digest: `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.

Observations digest: `014d479edbda55f863a9dc4517df26075d8627e8c09b9f106b809f8341245f04`.

Qualification report digest: `7fa110e7d5a5124fba62423edd4fa0767a0da15a9cede864d51f0715536cb5f1`.

This was not a formal SWE run, did not check whole-project regression, and does not backdate new information. These observations qualify the historical source; they are not execution results for the newly authored Workflow or functional cases.
