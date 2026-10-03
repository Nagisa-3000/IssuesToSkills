# Historical episode

## Source

Authoritative repair source: `PyCQA/pyflakes:422:repair:2c29431eaeb9`.

The original title was “2.1.0 is broken.” The supplied body consisted of a Travis CI job URL. Those report entries do not themselves establish a stack trace or precise failure mechanism.

The merged implementation supplied at revision `2c29431eaeb9c5b681f1615bf568fc68c6469486` changed `is_typing_overload` in historical `pyflakes/checker.py`. In the `ast.Name` branch, the existing checks included name membership in the scope and comparison of the binding's `fullName` to `typing.overload`. The repair inserted:

```python
isinstance(scope[node.id], ImportationFrom) and
```

between scope membership and metadata comparison. This uses short-circuit evaluation to restrict that metadata access to the appropriate binding type. The visible diff does not change the `ast.Attribute` branch.

The historical regression was added in `pyflakes/test/test_type_annotations.py` as `test_not_a_typing_overload`. It assigns `x` and `y` identity lambdas, defines `t` once with `@x`, and redefines `t` twice with stacked `@x` and `@y`. The assertion expects exactly two `m.RedefinedWhileUnused` diagnostics.

## Historical assertions versus execution

The supplied commit shows implementation and regression assertions. It does not provide a contemporaneous test execution transcript.

The supplied contemporary qualification was checked on `2026-10-03T19:13:13.277008+00:00`. It reports verified resolution with one fail-to-pass and thirteen pass-to-pass cases, scoped to changed test files with original-base control. It is recorded only as a provenance attestation, not as pre-cutoff learned content. Whole-project regression and cross-project transfer are untested.

## Evidence

- [Original title](evidence/title.md)
- [Original report body](evidence/body.md)
- [Merged guard implementation](evidence/fix.md)
- [Regression assertions](evidence/regression.md)

## Transfer boundary

The supported mechanism is a type guard before subtype-specific metadata access in a heterogeneous scope-binding model. Applying it elsewhere requires current evidence that the metadata belongs to the guarded binding category and that ordinary bindings must be rejected by this particular special-case recognizer. This single episode does not establish a generally applicable template across languages or repositories.
