# Preserve explicit mode and default omitted mode

## Kind

implementation

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, packages/core/src/core/contentGenerator.ts:153-175 and 314-319; selected parent comparison at the SDK constructor.

## Observation

The builder infers vertexai in credential-dependent branches, while direct factory inputs can omit it. The SDK constructor changes from forwarding config.vertexai to a nullish fallback using whether authType is USE_VERTEX_AI. Explicit false therefore survives even on the Vertex route; omitted mode becomes true for Vertex and false for other routes in the shared branch. This explicit-false preservation is established by the expression, not an executed historical test. Endpoint fallback selection separately follows authType.
