# Historical episode

Authoritative source: `pylint-dev/pylint:8613:repair:f223c6de3a39`.

The report supplied:

```python
class X:
    def __index__(self):
        return 1
```

Running `pylint x.py` reportedly emitted:

```text
x.py:2:4: W3201: Bad or misspelled dunder method name __index__. (bad-dunder-name)
```

The expected behavior was no lint. The reported environment was Pylint 2.17.2, astroid 2.15.4, and Python 3.10.11. These details are historical report data, not current environment requirements.

At revision `f223c6de3a39eae6d1c76e30b55da28639dd8777`, the merged fix added `"__index__"` to `EXTRA_DUNDER_METHODS` in historical `pylint/constants.py`. Historical `doc/whatsnew/fragments/8613.false_positive` described the false-positive repair and stated `Closes #8613`.

Historical `tests/functional/ext/bad_dunder/bad_dunder_name.py` added `Apples.__index__`, returning `1`, without an expected bad-dunder warning. These paths are evidence locators, not current bindings.

## Core evidence

- [Title](evidence/title.md)
- [Reported reproduction](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Committed regression assertion](evidence/regression.md)

Historical CI/test execution is unknown. Probe and validation contracts are authored conditional guidance; they do not invent historical commands or execution.

## Independent qualification: validation-only audit

The supplied complete report pins original base `a83137da3d72990d41ae993128fdde297cbc36cf`, issue 8613, PR 8619, and the exact merged revision. Historical artifact verification and the direct closure relationship were reported true.

All controls selected `tests.test_functional::test_functional[bad_dunder_name]`:

| Control | Observation | Exit code |
| --- | --- | --- |
| Original base | Passed | 0 |
| Base with committed regression | Failed: unexpected `bad-dunder-name` at line 52 | 1 |
| Historical fixed | Passed | 0 |

The public qualification command was `python3 -m pytest tests/test_functional.py -k bad_dunder_name -q`; individual runs added `--junitxml=/workspace/verification-results.xml`. Each deselected 826 tests. All controls used runtime digest `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`, adopted isolated workspaces, and did not time out. Isolation was `linux-copied-user-mount-pid-net-chroot-nobody-no-capabilities-v1`; sandbox backend was `namespace-copy`.

Checked at: `2026-10-04T18:03:10.501703+00:00`.

Scope: `changed-test-files-with-original-base-control`.

Limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

The controls support narrow causal qualification, not whole-project correctness. This was not a formal SWE run. Replay information is validation-only and must not be backdated, used as historical mechanism knowledge, or represented as execution of the newly authored Skill cases. Closure-event references in provenance are audit metadata, not additional historical evidence cards.

## Authoring boundary

The supplied historical support contains one authoritative SourceRecord and four core entries. The source projection records retained discussion review, but no additional discussion assertions are packaged. Caller-supplied rejected bundles are correction context, not independent support. No upstream packages or sealed generation-context reference were supplied.
