# Reject malformed or insecure remote custom endpoints

Atomic ID: `semantic-action:6b88c49d9fea9d8b`

Semantic owner: outbound endpoint policy guard

Operation: guard

Object / parameter slots:
- selected_endpoint
- allowed_loopback_hostnames
- required_remote_protocol

## Preconditions

A non-empty explicit or environment-derived custom endpoint has been selected but has not yet been admitted to outbound client options.

## Action

Parse any selected custom endpoint and enforce encrypted transport for remote hosts while retaining an HTTP exception for local loopback development.

## Invariant

The endpoint is admitted only if it is parseable and uses HTTPS, except that named and numeric loopback hosts may use HTTP; rejected values fail before SDK construction.

## Direct validation

Assert acceptance of an HTTP loopback URL and rejection of both an unparsable string and an HTTP remote URL with the expected error classes/messages.

Step oracle: Unit tests prove loopback HTTP acceptance and rejection of malformed or remote HTTP values.

## Regression validation

- Static diff check: confirm endpoint lookup is inside the intended SDK-construction branch and keyed by the declared authentication type.
- Focused unit checks: verify each provider environment endpoint is forwarded with the matching provider mode.
- Precedence check: set explicit and environment endpoints and verify the explicit value wins.
- Safety checks: verify loopback HTTP succeeds while malformed and remote HTTP endpoints fail before SDK construction.
- Regression checks: retain established constructor-option assertions, now with concrete non-cloud provider mode.
- Repository test execution: run the focused content-generator test file in an intact checkout; this remained deferred in the supplied staged-deletion worktree.

## Failure modes

Defer if the owner, precondition, or oracle differs. Classify a failed postcondition as action_failure; an unavailable oracle as missing_oracle.

## Not applicable when

- The integration has only one provider interface and no competing endpoint sources.
- Endpoint selection and validation are already owned and guaranteed by a lower-level SDK contract.
- The target path does not construct the SDK client that consumes the custom endpoint.

## Evidence

- [ev-diff-01](../evidence/861b3a7316fedbdd.md)
- [ev-test-04](../evidence/b90084f57c95bcbe.md)
