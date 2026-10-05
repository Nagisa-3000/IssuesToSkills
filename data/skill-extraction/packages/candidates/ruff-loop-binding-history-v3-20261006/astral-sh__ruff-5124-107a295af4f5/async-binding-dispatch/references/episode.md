# Historical episode

SourceRecord: `astral-sh/ruff:5124:repair:107a295af4f5`.

The public report described PLW2901 panicking on:

```python
async def f():
    async with a:
        return await b
```

The historical command was:

```shell
ruff --no-cache --select PLW2901 tasks.py
```

The bug was an accepted-variant mismatch: the rule handled `With`, `For`, and `AsyncFor`, but not `AsyncWith`. The merged implementation combined `With` and `AsyncWith` into the same binding-extraction and body-traversal arm. It also changed the rule entry point from a general `Node` to `&Stmt` and updated checker call sites. The unexpected-statement panic remained, with its accepted-variant message updated.

Historical owners were:

- dispatcher: `crates/ruff/src/checkers/ast/mod.rs`;
- rule: `crates/ruff/src/rules/pylint/rules/redefined_loop_name.rs`;
- fixture: `crates/ruff/resources/test/fixtures/pylint/redefined_loop_name.py`;
- expected diagnostics: `crates/ruff/src/rules/pylint/snapshots/ruff__rules__pylint__tests__PLW2901_redefined_loop_name.py.snap`.

These paths are historical locators, not automatic bindings for another checkout.

The committed fixture added asynchronous context-manager cases with reused and distinct variables, and asynchronous-loop reuse coverage. The snapshot reports the reused context-manager name at the inner target and retains loop and assignment diagnostics. These are committed assertions; no historical test-run or CI result was supplied.

## Validation-only qualification

The supplied independent report was checked at `2026-10-05T07:39:03.574356+00:00`. Its pinned identity ties issue 5124 directly to PR 5125 and merge revision `107a295af4f51dce1e78dcbfd234b2a3ad99a00f`. Original-base and exact-fixed tree receipts support artifact identity. Earlier preparation receipts marked incomplete are intermediate receipts, not substitutes for the final causal controls.

For the exact named Rust test, the original base passed, the same base binary with the regression fixture failed at the missing-variant panic, and the historical fixed binary passed. All three phase receipts use the same runtime hash, report unchanged protected inputs and workspace execution hashes during execution, disable snapshot updates and forced passing, and report no timeout. Original-base and base-with-regression use the same binary hash. The fixed build receipt agrees with the fixed execution binary hash. Locked-dependency receipts report an unchanged lockfile.

Qualification scope: `exact-rust-libtest-with-original-base-control-v1`.

Scope limits: “Qualification covers one exact named Rust library test with the original expected snapshot; whole-project regression and cross-project transfer are untested.”

This replay is not a historical execution event, a formal SWE run, semantic-policy acceptance, or execution of these Skill functional cases. Its report hash and validation time are preserved in provenance.
