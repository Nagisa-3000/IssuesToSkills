# Selected implementation comparison

## Kind

diff

## Source

Local git comparison cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45^1..cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45; selected parent resolves to c5ad0abb5de461416306a516ddbb26dc78f87d40. Changed files: packages/core/src/core/contentGenerator.ts, packages/core/src/core/contentGenerator.test.ts and docs/reference/configuration.md.

## Observation

The inspected comparison adds the URL guard, route-selected fallback endpoint and nullish provider-mode default. It adds seven constructor tests and adjusts eight existing mode expectations. The three-file comparison contains 242 insertions and 11 deletions. There is one recorded parent, so no merge-parent separation was needed. This supports one coherent factory-boundary Workflow, not an independent cross-repository Pattern.
