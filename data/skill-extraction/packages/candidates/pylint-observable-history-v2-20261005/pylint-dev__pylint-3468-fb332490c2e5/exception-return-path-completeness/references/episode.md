# Historical episode

SourceRecord: `pylint-dev/pylint:3468:repair:fb332490c2e5`  
Issue: `pylint-dev/pylint:3468`  
Fix: `pylint-dev/pylint:pr:3782`  
Revision: `fb332490c2e59c232c7095dfe3462f8e081e2814`  
Repair available: `2020-09-06T19:08:03Z`  
Cutoff: `2024-01-01T00:00:00Z`

## Report and implementation

The report supplied a value-returning `try` and an `AttributeError` handler containing `pass`; no `inconsistent-return-statements` warning was reported. It reported Pylint 2.4.4, astroid 2.3.3, and Python 3.6.7.

In `pylint/checkers/refactoring/refactoring_checker.py`, the repair added a specific `astroid.TryExcept` rule:

```python
return all(
    self._is_node_return_ended(_child) for _child in node.get_children()
)
```

Generic recursion stopped excluding `astroid.ExceptHandler`. This is the historical implementation over AST children, not evidence of a universally correct control-flow algorithm.

Conditional analysis moved into a helper that excluded nested function definitions. For an `if` without `else`, it required a later direct sibling `Return` and a returning body. Raise analysis moved into a helper retaining bare-raise termination, safe inference for typed raises within `try/except`, matching-handler analysis, and unhandled-raise termination.

The commit also added trailing `return None` in internal functions in `pylint/checkers/classes.py`, `pylint/checkers/imports.py`, `pylint/checkers/misc.py`, `pylint/lint/pylinter.py`, and `pylint/pyreverse/inspector.py`. These are historical consistency adjustments, not authority for unrelated current rewrites.

## Committed assertions

`tests/functional/i/inconsistent_returns.py` added two warning cases:

- A returning `try` with an `AttributeError: pass` handler.
- The same fallthrough handler with additional `KeyError: return True` and `ValueError: raise` handlers.

Two counterexamples expected no warning: explicit `return None` after the statement, and explicit `return None` in the handler.

`tests/functional/i/inconsistent_returns.txt` added the positive diagnostics at historical lines 267 and 277, retaining earlier expectations with shifted lines. The fixture also disabled `blacklisted-name`. These are committed assertions; historical execution is unknown.

## Qualification audit: validation only

The complete caller-supplied report pins original base `e61d55e83fb74e85c7d129834f7c82e6669bae59`, the fixed revision above, matching issue/fix identities, verified historical artifacts, and a direct-closure relationship. Its closure-event locator is an audit reference, not an additional authored historical evidence card.

All three controls used the same runtime digest:
`862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.

The supplied observations and logs agree:

- Original base: exit 0; 40 passed, 2 skipped.
- Base with committed regressions: exit 1; 39 passed, 1 failed, 2 skipped. `inconsistent_returns` failed for missing diagnostics at 267 and 277.
- Historical fixed tree: exit 0; 40 passed, 2 skipped.

`indexing_exception` and `iterable_context_py2` were skipped consistently. No control timed out. The 40 pass-to-pass selections compare original base to fixed; the target also belongs to that comparison while failing with added regressions on base.

Checked at `2026-10-04T09:31:23.398806+00:00`, qualification is not backdated learned content. Scope is `changed-test-files-with-original-base-control`; whole-project regression and cross-project transfer are untested. It was not a formal SWE run and did not execute authored Skill evaluations. The report hash is retained in provenance.

## Reuse boundary

Bind the current Python analyzer semantically, reproduce the missing diagnostic, establish compatible exception-child semantics, and only then modify it. Preserve explicit-`None`, neighboring control flow, and runtime behavior. Current execution records remain separate from this immutable historical episode.
