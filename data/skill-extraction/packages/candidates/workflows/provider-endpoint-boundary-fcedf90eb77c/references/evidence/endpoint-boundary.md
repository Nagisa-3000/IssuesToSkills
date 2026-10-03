# Shared factory endpoint precedence and branch scope

## Kind

implementation

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, packages/core/src/core/contentGenerator.ts:95-101, 119-175 and 258-320. Before-state: selected parent c5ad0abb5de461416306a516ddbb26dc78f87d40, same file:258-301.

## Observation

The configuration type exposes optional baseUrl and vertexai. The builder retains explicit baseUrl. The shared SDK branch includes Gemini, Vertex and Gateway routes; code-assist routes return through another constructor. At lines 291-311, config.baseUrl wins when truthy, otherwise authType selects one fallback setting; only a truthy result becomes httpOptions.baseUrl. Both selected explicit and fallback values invoke the guard. The SDK constructor retains headers and API version. The parent instead forwarded only config.baseUrl and did not explicitly select these fallback settings. Gateway follows the non-Vertex fallback branch; this is observed scope, not a universal provider policy.
