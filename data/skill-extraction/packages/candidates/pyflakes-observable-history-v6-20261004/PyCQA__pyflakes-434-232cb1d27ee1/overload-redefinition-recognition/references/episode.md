# Historical episode

Authoritative source: `PyCQA/pyflakes:434:repair:232cb1d27ee1`.

The report described F811 diagnostics between successive `utf8` overload declarations and the final implementation. One example placed declarations inside a class using a module-level `from typing import overload`. Another combined `@overload` with an identity decorator on module-level functions.

The supplied repair at revision `232cb1d27ee134bf96adc8f37e53589dc259b159` changed `pyflakes/checker.py`:

- `is_typing_overload(value, scope)` became `is_typing_overload(value, scope_stack)`.
- Bare-name recognition traversed `reversed(scope_stack)`.
- At the first scope containing the name, it returned whether the binding was an `ImportationFrom` with `fullName == 'typing.overload'`. A shadowing nonmatching binding terminated lookup.
- Recognition retained its `ast.FunctionDef` restriction.
- The singleton decorator requirement became `any(...)` over the decorator list.
- The unused-redefinition gate passed `self.scopeStack` instead of `self.scope`.
- The displayed diff retained the existing attribute-decorator branch; it did not establish a new general resolver for qualified imports.

In `pyflakes/test/test_type_annotations.py`, the regression diff added `test_overload_with_multiple_decorators` and `test_overload_in_class`. Both called `self.flakes(...)` without expected diagnostic classes. The first used `@dec` above `@overload` on two declarations and `@dec` on the implementation. The second placed two overload declarations and an implementation inside a class. Existing `test_not_a_typing_overload` appeared in adjacent context.

These are assertions available at the historical commit, not a test execution log.

## Resolution and qualification

The authoritative record identifies the merged repair as a verified resolution. Qualification checked on `2026-10-03T19:13:14.692124+00:00` reports two fail-to-pass and fifteen pass-to-pass cases, limited to changed test files with original-base control. Whole-project regression and cross-project transfer are untested. This later attestation remains in provenance and is not treated as pre-cutoff knowledge.

## Reconstruction boundary

The packaged Actions are evidence-grounded operational decompositions. They do not claim that the historical author executed this exact plan or that a current plan has already succeeded.

Evidence: [title](evidence/title.md), [report](evidence/body.md), [implementation](evidence/fix.md), [regressions](evidence/regression.md).
