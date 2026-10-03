# Documented custom endpoint constraints

## Kind

diff

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, docs/reference/configuration.md:2151-2165; selected comparison with parent c5ad0abb5de461416306a516ddbb26dc78f87d40.

## Observation

The added configuration entries describe Gemini API-key and Vertex endpoint overrides, require valid URLs, and state HTTPS with exceptions for localhost, 127.0.0.1 and [::1]. Documentation does not enumerate Gateway behavior or establish full SSRF protection. Its transport wording must be read with the implementation predicate, which has a hostname-based exception broader than HTTP alone.
