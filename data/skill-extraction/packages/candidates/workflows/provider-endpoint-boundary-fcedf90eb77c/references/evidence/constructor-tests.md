# Historical constructor argument oracles

## Kind

test

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, packages/core/src/core/contentGenerator.test.ts:23-46 and 642-827; selected parent diff for existing vertexai expectations.

## Observation

The SDK is mocked and settings stubs are restored after tests. Added assertions check Gemini and Vertex fallback endpoints, sparse Vertex route selection with both fallbacks, explicit-over-fallback precedence, local HTTP acceptance, malformed explicit URL rejection and remote HTTP rejection. Eight existing expectations now require vertexai false rather than undefined. These are inspected test definitions, not passing execution results. Rejection tests assert thrown errors but do not explicitly assert zero constructor calls; that stronger check is proposed in the packaged evals.
