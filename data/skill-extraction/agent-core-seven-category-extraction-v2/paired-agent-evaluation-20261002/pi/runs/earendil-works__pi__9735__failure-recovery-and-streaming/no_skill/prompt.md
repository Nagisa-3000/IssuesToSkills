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
no_skill

Solve the task from the repository and visible tests without any retrieved Skill context.