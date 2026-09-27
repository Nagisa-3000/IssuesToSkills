# Pattern: Residual-Budget Invariant for Shared-Capacity Pipelines

Status: `provisional generalized Pattern`; supported by direct Hermes and DeepSeek realizations. Requires held-out transfer before `validated`.

## Intent

Keep an upstream pressure/admission decision inside the actually admissible capacity of a pipeline whose downstream stage consumes the same finite window.

## Forces

- Nominal capacity is easy to expose but may not equal admissible input capacity.
- Reservations may come from provider defaults, routed request caps, or target overrides.
- Model/runtime switching changes the capacity envelope.
- Safety headroom protects against boundary drift but reduces usable input budget.
- Auxiliary summary output may or may not share the same budget.

## Causal rule

A pressure policy should be computed over the residual budget after mandatory downstream reservations, and all derived limits must be recalculated whenever the envelope changes.

## Variant selection

- **No reservation / compatibility mode:** use nominal capacity only when the provider contract truly has no mandatory reservation.
- **Residual reservation mode:** subtract all mandatory shared reservations before threshold/retention derivation.
- **Residual + headroom mode:** subtract safety headroom from the residual pressure budget.
- **Shared auxiliary-output mode:** derive a default auxiliary cap from headroom only if the policy contract says they share it; explicit caps win.
- **Independent-pool mode:** do not use this Pattern; model separate budgets.

## Alternatives and trade-offs

- Conservative thresholding reduces provider rejection risk but may compact/shed work earlier.
- A fixed headroom is simple but can waste capacity on small windows; a ratio adapts but can be harder to reason about.
- Rejecting impossible configurations is safer; compatibility fallbacks may preserve legacy sessions but can hide misconfiguration if not observable.

## Counterexamples / exclusions

- Compaction triggered too late because it is scheduled after the last tool result: use a request-boundary timing Atomic.
- Custom messages omitted from token accounting: use a complete-context-accounting Atomic.
- Summary failure handling: use a recovery Atomic; do not treat it as proof of the residual invariant.
- Independent input/output pools: no residual subtraction is warranted.

## Evidence

- Hermes direct realization: `data/skill-extraction/cases/hermes-compaction-reservation/`.
- DeepSeek direct realization: `data/skill-extraction/cases/deepseek-compaction-reservation/`.
- Pi partial alignment: `data/skill-extraction/cases/pi-compaction-budget/`.
- Aider adjacent family: `data/skill-extraction/cases/aider-context-budget/`.
