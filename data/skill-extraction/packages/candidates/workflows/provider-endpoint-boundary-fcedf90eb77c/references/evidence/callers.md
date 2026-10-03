# Normalized and direct factory entry paths

## Kind

call_site

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, packages/cli/src/test-utils/AppRig.tsx:307-324; packages/core/src/core/contentGenerator.test.ts:657-661, 690-694 and 719-727.

## Observation

The harness's refresh-auth stub invokes the factory with authType, proxy and an API-key fixture, omitting vertexai and baseUrl. Added tests also invoke the configuration builder before the factory, while the sparse Vertex test calls the factory directly with only authType. These observed entry paths support locating final resolution at the convergent factory rather than only in the builder. The sparse checkout lacks production configuration/client files, so complete production coverage remains unknown.
