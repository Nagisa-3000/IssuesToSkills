# URL parsing and transport guard

## Kind

implementation

## Source

Revision cb289e0724b46ce867b6d3fe4bd0ac6ed890dc45, packages/core/src/core/contentGenerator.ts:104-117 and 291-319.

## Observation

LOCAL_HOSTNAMES contains localhost, 127.0.0.1 and [::1]. validateBaseUrl constructs a URL and throws an invalid-custom-URL error on parse failure. It rejects when protocol is not https: and the parsed hostname is not in the exact allowlist. The selected override is guarded before GoogleGenAI construction. The predicate exempts any parseable protocol for the listed local hostnames; it does not guarantee HTTP-only loopback, DNS safety, redirect restrictions or service compatibility.
