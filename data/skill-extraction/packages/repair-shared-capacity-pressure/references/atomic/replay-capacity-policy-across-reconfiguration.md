# Atomic: replay capacity policy across reconfiguration

When model, provider, or context changes, preserve or explicitly replace active reservation state and recompute every derived budget through the same policy seam.

## Invariant

The active runtime envelope is reflected in threshold, retention, and pressure values after reconfiguration.

## Oracle

Test omitted replacement, explicit replacement, context-size change, model switch, and fallback activation.

## Realizations

Hermes `update_model()`, DeepSeek routed policy resolution, and Pi per-model compaction settings provide direct or partial realizations.
