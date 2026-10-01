# Holdout feedback and lifecycle decision

- evaluation status: `pass_directional`
- lifecycle decision: `retain_candidate`
- outcome: `full_tie`
- independent cases: `1`
- replicates: `1`
- promotion supported: `False`

## Paired result

### no_skill

- task solved: `True`
- correctness: `99.4`
- code quality: `93.0`
- overall score: `96.842`
- usage tokens: `335118`
- wall seconds: `131.0398769999956`

### guided

- task solved: `True`
- correctness: `98.4`
- code quality: `93.6667`
- overall score: `97.4567`
- usage tokens: `314977`
- wall seconds: `119.96590489400114`

## Guided minus no-skill

- overall score: `0.6147`
- usage tokens: `-20141`
- wall seconds: `-11.074`

## Evaluator observations

### guided

- Provider inference still occurs after raw exact model-ID matching. If `provider/pattern` is not an exact provider/model pair but would resolve within that provider, an exact slash-containing model ID on another provider may win first.
- Direct exact matching does not canonicalize provider aliases before applying precedence, leaving similar ambiguity for alias-prefixed specifications.
- No permanent regression test was added to the repository patch, although the external holdout and existing resolver suite both passed.
- The full `npm run check` did not pass due to the retained holdout test importing a `.ts` extension; evidence indicates this was test-infrastructure-related rather than a source-code error.

### no_skill

- Provider-prefixed input is parsed twice when the initial provider-scoped parse finds no model and exact raw-ID fallback also fails; this is minor duplication and could make future resolver changes harder to keep consistent.
- Unlike the reference implementation, fallback after unsuccessful provider inference only accepts an exact full raw model ID and does not retry fuzzy full-input matching. This is not required by the reported issue and does not regress the covered existing behavior, but it is a narrower compatibility fallback.
- A full repository check did not complete successfully because the injected holdout test uses a '.ts' import unsupported by the current TypeScript configuration; source-level validation therefore relies primarily on the focused 27-test resolver run.

## Candidate update

- Add a focused case where a canonical or aliased provider prefix competes with a provider-agnostic raw id.
- Add slash-containing model ids with fuzzy matches and thinking-level suffixes so fallback compatibility is observed rather than assumed.
- Run the broader resolver regression suite in addition to the evaluator-authored holdout test.

Treat these observations as holdout evidence, not universal rules. The current update retains the candidate and strengthens edge-case validation; it does not merge, retire, or globally promote the Pattern.

## Promotion blockers

- insufficient_independent_holdout_cases
- insufficient_independent_guided_advantage_cases
- guided_solved_rate_delta_below_threshold
