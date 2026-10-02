You are solving a held-out implementation task in repository earendil-works/pi.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
failure recovery and streaming

# Issue/task
Retry classifier misses premature stream endings worded by a proxy, e.g. CLIProxyAPI

## Summary

`isRetryableAssistantError` does not recognise a stream that ended before its terminal event when the wording comes from a proxy rather than from pi's own code, so the turn is abandoned instead of retried.

Concretely, this message is not matched by `RETRYABLE_PROVIDER_ERROR_PATTERN`:

```
litellm.APIError: stream error: stream disconnected before completion: stream closed before response.completed
```

## Why this is surprising

pi already handles exactly this condition on its own code path. `packages/ai` throws:

```ts
if (!sawTerminalResponseEvent)
    throw new Error("OpenAI Responses stream ended before a terminal response event");
```

and that sentence **is** in the retryable list. So a user on pi's direct ChatGPT subscription login never sees this failure: pi detects the truncation, recognises its own wording, and retries silently.

Put an OpenAI-compatible proxy in the path and the same physical fault becomes fatal, because the proxy words it differently.

## The structural point

`packages/ai/src/utils/retry.ts` currently enumerates vendor spellings of one condition:

- `"ended without"` — Anthropic
- `"stream ended before message_stop"` — Anthropic (#4433)
- `"stream ended before a terminal response event"` — pi's own Responses check

and is missing at least a fourth, CLIProxyAPI's `"stream disconnected before completion: stream closed before response.completed"`.

A premature stream ending is **one condition**, not one condition per vendor. Enumerating sentences means every new SDK, gateway or proxy that phrases it differently needs another patch here, and users hit a hard failure until it lands.

## Reproduction

An assistant call whose provider returns `stopReason: "error"` with the message above. Expected: `isRetryableAssistantError` returns `true` and the turn is retried under the configured policy. Actual: it returns `false` and the turn is abandoned.

### Captured from a live run

From a live run on a pi -> LiteLLM 1.100.1 -> CLIProxyAPI v7.2.159 -> ChatGPT Codex path, captured 2026-09-18T09:48 +08:00. The upstream cut the stream after 1068 events, the last 2130 of them `response.function_call_arguments.delta`, with no `response.completed`. The gateway reported the cut in band:

```
event: response.function_call_arguments.delta
data: {"type":"response.function_call_arguments.delta","delta":"[REDACTED tool-call argument fragment]","item_id":"[REDACTED]","output_index":0,"sequence_number":1067}

event: error
data: {"type":"error","error":{"code":"request_timeout","message":"stream error: stream disconnected before completion: stream closed before response.completed","param":null,"type":"invalid_request_error"},"sequence_number":1068}
```

LiteLLM turned that into the message pi actually sees:

```
01:49:22 - LiteLLM Proxy:ERROR: proxy_server.py:8778 - litellm.proxy.proxy_server.async_data_generator(): Exception occured - litellm.APIError: stream error: stream disconnected before completion: stream closed before response.completed
```

Redacted from the capture: the request body (541 KB of prompt, conversation and source code), all bearer tokens, cookies, account and session identifiers, quota headers and the text of each tool-call argument delta. Event names, sequence numbers and error payloads are untouched.

That is the same condition pi already retries under two other spellings. Only the wording differs, and the wording is what the classifier matched on.

The fault occurs on roughly 0.13% of requests on this path, always cutting in during `response.function_call_arguments.delta`, and the connection gap is typically one to two seconds. It is exactly the kind of failure retry exists for.

## Suggested fix

Match the condition rather than each vendor's sentence, so a new phrasing is covered without another patch.

## Deeper follow-up, not proposed here

Retryability is decided by regular expression over a human-readable message. That couples pi's control flow to other systems' prose. Providers frequently do carry a machine-readable code — CLIProxyAPI sets `code: "request_timeout"` on this very error — but `AssistantMessage` has no field to carry it, so it is lost before the classifier runs. Threading a structured error code through `AssistantMessage` and classifying on it first, with text matching as the fallback, would remove this class of bug. That is a much larger change and is not what the attached PR does.

PR with an end-to-end regression test attached.


# Visible regression tests retained for this evaluation
- packages/ai/test/retry.test.ts
- packages/coding-agent/test/suite/regressions/9735-proxy-truncated-stream-retry.test.ts

# Validation commands
- `env PATH=/home/chenyujia/.local/node22/bin:/home/chenyujia/.local/node22-global/node_modules/.bin:/usr/bin:/bin npm --prefix packages/ai test -- 'test/retry.test.ts'`
- `env PATH=/home/chenyujia/.local/node22/bin:/home/chenyujia/.local/node22-global/node_modules/.bin:/usr/bin:/bin npm --prefix packages/coding-agent test -- 'test/suite/regressions/9735-proxy-truncated-stream-retry.test.ts'`
- `git diff --check HEAD`

# Arm
guided

# Retrieved Skill Graph guidance
The following are hypotheses retrieved only from the training repositories using lexical/vector retrieval, optional HNSW, and typed graph expansion. Verify every step against the current code and tests; do not copy repository-specific names blindly.

## Retrieved node 1: workflow — recover-recognized-premature-stream-termination
id: workflow:bca58288062025eb
repository: google-gemini/gemini-cli
score: 0.034365
sources: {"graph": 0.007218750000000001, "lexical": 0.01639344262295082, "lexical_raw": 21.426050642626663, "vector": 0.010752688172043012, "vector_raw": 0.19802039199948934}

Extend an existing bounded network-retry policy with a narrowly identified premature-close code, then validate recovery at the streaming boundary, including retry signaling, completed output, and failure classification telemetry.

facets:
{"entry_state": "A stream may emit incomplete content and then terminate with ERR_STREAM_PREMATURE_CLOSE; the shared exact-code classifier does not recognize that code, so the established recovery path cannot select it for retry.", "exit_state": "The premature-close code is narrowly classified as retryable, and a streaming regression proves that the failure produces a retry signal, a complete response from the next attempt, and telemetry containing the concrete error type.", "problem_class": "failure-recovery-and-streaming"}

payload:
{"anti_goals": ["Do not make every stream exception retryable.", "Do not alter retry counts, backoff timing, jitter, abort handling, or quota/server-status policies when only one transport classification is missing.", "Do not treat the partial response from the failed attempt as proof of successful completion.", "Do not suppress the concrete failure type from retry telemetry."], "entry_state": "A stream may emit incomplete content and then terminate with ERR_STREAM_PREMATURE_CLOSE; the shared exact-code classifier does not recognize that code, so the established recovery path cannot select it for retry.", "exit_state": "The premature-close code is narrowly classified as retryable, and a streaming regression proves that the failure produces a retry signal, a complete response from the next attempt, and telemetry containing the concrete error type.", "goal": "Convert a reproducible, coded premature stream closure from an immediate terminal failure into a bounded retry that can deliver a complete subsequent response while retaining observable retry diagnostics.", "not_applicable_when": ["The failure has no stable evidence that it is transient or safe to retry.", "The operation is non-replayable or retrying could duplicate externally visible side effects.", "Cancellation or abort requested by the caller caused the stream termination.", "The retry framework does not cover failures raised during stream iteration.", "The task requires changing retry exhaustion, delay, or response-reconciliation semantics rather than admitting a missing error classification."], "steps": [{"action_id": "semantic-action:49a130b1c42db576", "action_name": "classify-premature-stream-closure-as-retryable", "condition": "Apply only after reproducing a stream-iteration failure carrying the stable premature-close transport code and confirming the operation is covered by the existing bounded retry path.", "depends_on": [], "optional": false, "required": true, "role": "repair", "step_id": "step-1", "validation": "The regression stream first yields incomplete content and throws ERR_STREAM_PREMATURE_CLOSE, then the consumed event stream contains RETRY and the completed second-attempt chunk; retry telemetry reports error_type ERR_STREAM_PREMATURE_CLOSE."}], "stop_conditions": ["Stop if the observed error code differs from the proposed exact classification and no equivalence is established.", "Stop if replaying the streaming operation is not safe.", "Stop if the failure is an explicit abort or cancellation.", "Stop if the stream layer cannot route iteration-time failures through the existing retry mechanism.", "Stop after bounded retries are exhausted; this change does not authorize infinite retrying."], "validation_ladder": ["Static diff check: verify the exact transport code is added to the bounded retryable-code set without broadening generic exception matching.", "Classifier-path check: verify code extraction feeds both retry eligibility and retry error-type reporting.", "Streaming regression: fail after a partial chunk, then require an explicit retry event and completed output from the subsequent stream.", "Observability check: require retry telemetry to retain the exact premature-close code.", "Broader automated test or CI execution is desirable but is not established by the available evidence bundle."], "when_to_use": ["A streaming API can yield partial data and then fail with a stable transport error code that is known to represent premature connection closure.", "An existing retry framework already classifies transient network codes and wraps or governs stream recovery.", "A regression can reproduce failure during stream iteration and supply a successful later attempt."]}

retrieval trace:
- pattern:9cb94d22583f2781 --supported_by/out--> workflow:bca58288062025eb
- pattern:9cb94d22583f2781 --instantiates/in--> workflow:bca58288062025eb

## Retrieved node 2: action — Allow a streamed operation interrupted by a recognized premature-close transport error to recover through the existing retry mechanism instead of terminating immediately.
id: semantic-action:49a130b1c42db576
repository: -
score: 0.025774
sources: {"selected_payload_relation": 0.025773660596245376}

Admit a specific premature-stream-termination code to an existing bounded network-error retry policy so interrupted streaming requests can use the established retry and telemetry path.

facets:
{"grounded_semantics": true, "module_role": "Shared transient-network-failure classifier used by retry execution and retry telemetry", "operation": "classify", "problem_class": "failure-recovery-and-streaming"}

retrieval trace:
- workflow:bca58288062025eb --payload-reference--> semantic-action:49a130b1c42db576

# Applicability judgment
{
  "selected_skill_id": "workflow:bca58288062025eb",
  "applicable": true,
  "confidence": 0.93,
  "rationale": "The candidate matches the causal repair: a premature stream termination is currently excluded from an established bounded retry path because its concrete representation is unrecognized; the change should narrowly admit that condition and validate both classifier behavior and end-to-end recovery. The visible tests establish equivalent evidence through several terminal-event-missing messages, including the proxy wording, and verify a retry signal, exactly one subsequent successful attempt, preserved error text in retry telemetry, and completed assistant output. The representation differs from the candidate’s exact transport-code example—pi receives only a human-readable errorMessage—but the issue evidence establishes semantic equivalence to pi’s and Anthropic’s already-retryable premature-terminal-event failures.",
  "missing_preconditions": [
    "Confirm the implemented text matcher remains narrow to streams ending before a required terminal event and does not classify arbitrary stream exceptions as retryable.",
    "Confirm the failed assistant operation is replay-safe; the supplied regression demonstrates routing through the existing bounded retry framework but does not independently analyze external side effects from partially emitted tool-call arguments.",
    "A stable machine-readable error code is unavailable at the classifier boundary, so exact-code classification and code-based telemetry from the candidate cannot be used; message-based semantic evidence must remain the fallback until structured codes are propagated."
  ]
}

Use the guidance to localize the problem and choose a safe implementation, but rely on the visible tests and current code as the oracle.