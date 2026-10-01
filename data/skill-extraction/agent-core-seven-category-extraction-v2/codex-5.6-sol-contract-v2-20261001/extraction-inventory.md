# Agent-core seven-category extraction: actionable Workflow contract

## Summary

- Training cases: 28
- Admitted ChangeEpisodes: 28
- Candidate Atomics: 75
- Candidate Workflows: 29
- Schema-valid responses: 28
- Holdout leaks: 0

| Category | Episodes | Atomic | Workflow | Exact | Substitute | Holdout |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| provider-interface-adaptation | 4 | 10 | 4 | 0 | 4 | earendil-works/pi #5823 |
| credential-resolution-and-authentication | 4 | 12 | 4 | 2 | 2 | Aider-AI/aider #750 |
| context-budget-and-compaction | 4 | 9 | 4 | 1 | 3 | NousResearch/hermes-agent #43547 |
| state-continuity-and-resume | 4 | 11 | 5 | 1 | 3 | openai/codex #47761 |
| structured-tool-contract-integrity | 4 | 11 | 4 | 1 | 3 | google-gemini/gemini-cli #29308 |
| effect-control-and-isolation | 4 | 11 | 4 | 1 | 3 | QwenLM/qwen-code #10859 |
| failure-recovery-and-streaming | 4 | 11 | 4 | 1 | 3 | earendil-works/pi #9735 |

## Cases

### Aider-AI/aider #88

- Category: `provider-interface-adaptation`
- Episode: Adapt provider configuration across client initialization and request dispatch
- Atomics: Configure the provider client at application startup; Remove provider credentials from domain-component construction; Forward provider-specific routing fields at request dispatch
- Workflows: Adapt a compatible provider across configuration, construction, and request boundaries
- When to use: A provider uses an otherwise compatible client library but requires additional endpoint metadata or routing identifiers.; Provider configuration is currently split into or coupled with a domain-component constructor.; The provider request method accepts routing fields that are not represented in the application's common request construction.
- Anti-goals: Do not redesign model prompting, edit formats, retry policy, or response processing.; Do not force provider-specific optional values into requests when the user did not configure them.; Do not retain credentials in unrelated domain constructor signatures merely to initialize a shared provider client.; Do not claim end-to-end provider connectivity without a request-level or integration oracle.

### NousResearch/hermes-agent #125942

- Category: `provider-interface-adaptation`
- Episode: Restore resumed sessions through the canonical persisted provider route
- Atomics: Complete a partial persisted route without discarding its endpoint metadata; Use the canonical persisted route when rebuilding a resumed client session
- Workflows: Align a resume interface with the authoritative persisted runtime route
- When to use: A producer and one resume consumer use a nested or versioned runtime snapshot while another consumer reconstructs the same route from older top-level or accounting fields.; A resumed model is sent to the wrong provider endpoint or protocol after the session changes providers.; Multiple consumers interpret the same persisted route with different precedence rules.
- Anti-goals: Do not change provider selection for new sessions that have no usable persisted route.; Do not treat accounting buckets as authoritative route identities when they are documented as frozen or non-routable.; Do not remove interface-specific endpoint-ownership checks, stale-provider healing, reasoning settings, service-tier handling, or profile-following behavior.; Do not persist or restore raw API credentials as part of route reconciliation.

### QwenLM/qwen-code #11657

- Category: `provider-interface-adaptation`
- Episode: Adapt replayed reasoning messages to a strict OpenAI-compatible endpoint
- Atomics: Select the compatibility adapter from the canonical endpoint hostname; Remove only the derived field rejected by the endpoint
- Workflows: Adapt a shared request shape for a stricter compatible endpoint
- When to use: A nominally compatible endpoint rejects a field synthesized by shared request construction rather than supplied independently by the caller.; The failure occurs after prior structured assistant output is replayed, including continuations following thinking or tool-use turns.; The endpoint can be identified from configuration using a canonical hostname boundary.
- Anti-goals: Do not remove the accepted source field needed to replay prior reasoning.; Do not disable or change shared mirroring behavior for endpoints that accept or require it.; Do not infer endpoint identity from a hosted model-family name.; Do not mutate persisted or caller-owned conversation history.; Do not discard a distinct explicit field merely because it has the same semantic category as the rejected derived field.

### google-gemini/gemini-cli #25357

- Category: `provider-interface-adaptation`
- Episode: Safely adapt SDK endpoint options to the selected provider interface
- Atomics: Resolve a provider-specific endpoint with explicit configuration precedence; Reject malformed or insecure remote custom endpoints; Reconcile provider identity and forward accepted options to the SDK
- Workflows: Safely route custom endpoints through a multi-provider SDK boundary
- When to use: A client supports multiple provider interfaces selected by an authentication or backend mode.; Callers need endpoint overrides through both an explicit configuration field and provider-specific environment variables.; The external SDK accepts endpoint and provider-mode options that must remain mutually consistent.
- Anti-goals: Do not change authentication credential precedence or introduce new credential requirements.; Do not apply these endpoint environment variables to unrelated authentication paths or alternate client implementations.; Do not permit remote plaintext HTTP merely to maximize compatibility.; Do not let an environment endpoint override a caller-supplied explicit endpoint.

### NousResearch/hermes-agent #289

- Category: `credential-resolution-and-authentication`
- Episode: Prefer endpoint-specific credentials across OpenRouter resolution paths
- Atomics: Align credential precedence with the selected endpoint; Preserve the compatible credential fallback
- Workflows: Repair credential selection when compatible providers share environment variables
- When to use: Authentication fails only when credentials for multiple API-compatible services are simultaneously configured.; A runtime supports an endpoint-specific credential plus a generic compatible fallback.; Credential state can be initialized or refreshed through more than one code path.
- Anti-goals: Do not remove explicit caller-supplied credential precedence.; Do not change provider selection, base-URL selection, client protocol, or token-refresh behavior unless separate evidence requires it.; Do not delete the generic compatible fallback when existing configurations depend on it.; Do not log, compare by value in diagnostics, or expose secret credential contents.

### QwenLM/qwen-code #9016

- Category: `credential-resolution-and-authentication`
- Episode: Allow keyless cloud authentication without changing the configured principal
- Atomics: Classify whether a keyless credential path is eligible; Apply one credential contract across startup validators; Construct the SDK client for the selected authentication mode; Preserve explicitly declared credential authority; Report ambient credentials as unverified until session startup; Emit recovery guidance only for applicable credential paths
- Workflows: Enable ambient credentials without weakening credential precedence
- When to use: A provider SDK supports ambient or application-default credentials, but application validation currently requires an explicit API key.; Passing a placeholder credential changes SDK mode or disables the intended ambient credential resolver.; The same authentication decision is enforced at multiple startup or configuration boundaries.
- Anti-goals: Do not fabricate, inject, or pass a placeholder API key to satisfy validation.; Do not silently fall back to ambient credentials when the selected provider entry declares a specific key source.; Do not infer the selected authentication mode from project configuration alone when explicit mode selection is required.; Do not report a configured project as proof that a usable credential has resolved.; Do not broaden the keyless path to unrelated authentication modes.

### google-gemini/gemini-cli #28472

- Category: `credential-resolution-and-authentication`
- Episode: Try credential sources in priority order until one authenticates
- Atomics: Collect credential candidates without stopping at the first source; Verify candidates sequentially and continue after rejection
- Workflows: Restore authentication fallback across prioritized credential sources
- When to use: Multiple credential sources have defined precedence and an earlier source can be present but expired, revoked, malformed, or otherwise unusable.; Authentication currently chooses the first readable credential rather than the first credential that passes its real verification oracle.
- Anti-goals: Do not reorder explicit credential precedence, including access-token overrides and the relative priority of local cache versus environment-selected credentials.; Do not accept a credential merely because its file parsed successfully.; Do not remove compute, interactive, or manual authentication paths used after cached candidates are exhausted.; Do not persist compute-provided credentials or broadly redesign the login flow.

### earendil-works/pi #7176

- Category: `credential-resolution-and-authentication`
- Episode: Preserve an explicitly selected credential profile over ambient access keys
- Atomics: Distinguish an authoritative profile choice from ambient profile discovery; Suppress lower-priority access keys when an authoritative profile is selected
- Workflows: Restore deliberate credential selection without breaking ambient fallback
- When to use: A client configuration can contain both a profile selector and directly injected credentials, and the SDK gives the direct credentials higher precedence.; Authentication resolution carries a request-explicit or stored/scoped profile into the provider runtime while ambient access keys may also be visible.
- Anti-goals: Do not disable ambient access-key authentication when no authoritative profile was selected.; Do not treat a merely ambient profile as equivalent to a request-explicit or stored/scoped selection.; Do not alter bearer-token selection, skip-auth dummy credentials, region selection, endpoint selection, or proxy behavior.

### Aider-AI/aider #3764

- Category: `context-budget-and-compaction`
- Episode: Bound summarizer input in one forward pass and restore accurate tail-budget accounting
- Atomics: Select summarizer input with one bounded forward pass; Account for preserved context before accepting compaction
- Workflows: Compact oversized history within both model-input and retained-context budgets
- When to use: Conversation history exceeds its configured retained-token budget and can be divided into a head to summarize and a recent tail to preserve.; The summarizer model has a finite input capacity that may differ from the retained-history budget.
- Anti-goals: Do not change the summary prompt, model-fallback behavior, or role filtering performed by the summary operation.; Do not discard or summarize the selected recent tail merely to simplify accounting.; Do not treat fewer list operations as sufficient validation of message-selection semantics or budget correctness.

### earendil-works/pi #6647

- Category: `context-budget-and-compaction`
- Episode: Make context-compaction and branch-summary requests resilient to transient stream failures
- Atomics: Retry a transient summary request within a bounded budget; Apply the retry policy to every generated context summary; Publish summary retry lifecycle state to callers
- Workflows: Harden context-summary generation against transient request failures
- When to use: A context compaction, truncation, checkpoint, or branch-preservation operation depends on a model-generated summary.; A transient stream or transport failure currently aborts the entire structural context operation on its first failed request.; The runtime already has, or can accept, a bounded retry policy and an operation cancellation signal.
- Anti-goals: Do not retry context-overflow, quota, billing, authentication, or other errors rejected by the transient-error classifier.; Do not create an unbounded retry loop or silently ignore the configured retry budget.; Do not retry summaries supplied by hooks, extensions, caches, or callers when no model request is made.; Do not change summary selection, token budgeting, retained-tail boundaries, prompts, or persistence semantics merely to add request resilience.

### google-gemini/gemini-cli #8379

- Category: `context-budget-and-compaction`
- Episode: Cap shell-output truncation by the remaining model context budget
- Atomics: Cap retained tool output by the remaining context window; Verify context and configuration threshold precedence
- Workflows: Bound tool output by both configured limits and remaining context
- When to use: A tool-output truncation path already accepts a character threshold, but that threshold is static while prompt usage varies.; The runtime can identify the active model's token capacity and observe the latest prompt token count.; Oversized tool output can consume context needed for the next model request.
- Anti-goals: Do not replace or raise a stricter default or user-supplied truncation ceiling.; Do not rewrite the downstream truncation, file-spill, line-retention, or telemetry behavior when the threshold provider is the missing policy boundary.; Do not apply this policy to unrelated tool results when the established call site is scoped to successful string output from the shell tool.; Do not present the four-characters-per-token estimate as exact tokenization.

### QwenLM/qwen-code #11894

- Category: `context-budget-and-compaction`
- Episode: Recognize an official model alias when assigning context and output budgets
- Atomics: Map an official model alias to its actual input and output budgets; Add a two-dimensional regression oracle for the alias
- Workflows: Repair context and output budgeting for a supported model alias
- When to use: A supported model alias is accepted by the endpoint but resolves to a generic or default token limit.; Long sessions or compaction fail because the configured context or output budget is lower than the model capability associated with an equivalent versioned name.; Input and output capabilities are maintained in separate ordered classifiers that can drift or fall through independently.
- Anti-goals: Do not globally raise default context or output limits to accommodate one alias.; Do not reorder or broaden generic family rules in a way that upgrades older models without evidence.; Do not change the compaction algorithm when the demonstrated defect is capability classification.; Do not accept endpoint-incompatible spellings as a substitute for recognizing the endpoint's official identifier.

### Aider-AI/aider #591

- Category: `state-continuity-and-resume`
- Episode: Restore persisted conversation state when starting a new session
- Atomics: Reconstruct conversational messages from the persisted transcript; Restore persisted state only when no explicit state was supplied; Compact restored history within session and model context budgets
- Workflows: Resume a persisted conversation without displacing live state or overflowing context
- When to use: A stateful interactive application persists a transcript across process lifetimes and a new session should continue the prior conversation.; The persisted representation contains both conversational content and operational metadata that must not be replayed as model dialogue.; Restored state can be large enough to require compaction before continued use.
- Anti-goals: Do not replace explicitly supplied in-memory conversation state with disk contents.; Do not replay tool output, session metadata, commands, or blank prompts as conversational messages.; Do not summarize history that already fits the configured retained-history budget.; Do not send an unbounded restored transcript to the summarizer model.

### NousResearch/hermes-agent #228

- Category: `state-continuity-and-resume`
- Episode: Preserve caller-owned conversation history while producing an extended result
- Atomics: Copy caller-owned history before extending it; Verify preserved input and extended output
- Workflows: Resume from history without corrupting caller-owned state
- When to use: A continuation or resume API accepts a caller-supplied mutable sequence and appends new state during processing.; Inspection or regression behavior shows that the routine aliases and mutates the caller's non-empty sequence.
- Anti-goals: Do not remove prior history from the working continuation state.; Do not suppress recording of the new user or assistant messages in the returned state.; Do not deep-copy or transform individual history entries unless nested-entry mutation is separately demonstrated and specified.

### earendil-works/pi #7707

- Category: `state-continuity-and-resume`
- Episode: Publish session forks and torn-tail repairs without exposing partial state
- Atomics: Provide atomic destination replacement; Derive the complete fork state before persistence; Publish a fork only after it is complete; Repair a torn log tail without risking the original
- Workflows: Create a derived session without exposing partial state; Recover a torn persistent log without overwriting the original in place
- When to use: Creating a new persistent state artifact requires copying multiple entries, pointers, or metadata from an existing session.; The destination can be observed by repository listing or opened while multi-step construction failures are possible.
- Anti-goals: Do not publish the destination header before all derived mutations are staged.; Do not change which entries, lanes, name, or labels the fork operation selects.; Do not treat deletion of a partially published destination as equivalent to never publishing it.

### QwenLM/qwen-code #9050

- Category: `state-continuity-and-resume`
- Episode: Restore sessions under the selected workspace runtime’s storage context
- Atomics: Run HTTP session restoration inside the selected runtime’s storage scope; Run ACP session restoration inside the selected runtime’s storage scope
- Workflows: Preserve workspace runtime context throughout session restoration
- When to use: A service supports multiple workspace runtimes or runtime replacement, with separate persisted-session roots.; The restore path passes an explicit runtime root to one service but nested asynchronous restore code also consults an ambient or context-local storage root.; Restoration succeeds in the primary/default workspace but fails, misses state, or observes the wrong root for a secondary or replacement runtime.
- Anti-goals: Do not merge or relocate session stores between workspace runtimes.; Do not change session identifiers, restore metadata, archive-lock semantics, bridge ownership, or load/resume response shapes.; Do not replace workspace selection logic; preserve the already selected runtime and propagate its storage context.; Do not globally mutate a process-wide storage root when a callback-scoped binding is available.

### earendil-works/pi #7494

- Category: `structured-tool-contract-integrity`
- Episode: Preserve paired tool-call identifiers for protocol versions that require them
- Atomics: Classify which protocol versions require explicit tool-call IDs; Preserve matching IDs across tool calls and tool results
- Workflows: Restore tool-call correlation at a versioned protocol boundary
- When to use: A conversation adapter receives internally correlated tool calls and results but emits structured history without their identifiers.; The requirement begins at an identifiable model or protocol version boundary.; One shared capability predicate already controls both call-side and response-side ID serialization.
- Anti-goals: Do not add IDs unconditionally to older protocol versions whose established wire representation omits them.; Do not create separate provider-specific conversion paths when both adapters consume the shared converter.; Do not alter thought-signature handling, tool payloads, or result content while repairing identifier correlation.

### openai/codex #44472

- Category: `structured-tool-contract-integrity`
- Episode: Fail closed when tool-call completion evidence is ambiguous, reused, or truncated
- Atomics: Index observed identifiers before certifying freshness; Validate tool input and output associations; Localize metadata-budget damage to affected cells; Refresh recording state without changing execution behavior
- Workflows: Harden structured tool-call completion proofs
- When to use: A host records nested tool activity and exposes a structured completeness marker to a later model request or downstream consumer.; Invocation or runtime identifiers can be reused across retries, compaction, resume, fork, or asynchronous wait operations.; Recorded evidence is subject to per-call or aggregate serialization budgets.; Recording policy can change during a long-lived session.
- Anti-goals: Do not change tool execution availability, dispatch gates, or nested-tool behavior merely to change recording policy.; Do not infer completeness from a successful wrapper callback, terminal wait, or retained marker when association or inventory evidence is missing.; Do not discard trustworthy metadata for unrelated cells solely because one cell exceeded a budget.; Do not use unbounded sets or unbounded hashing to prove identifier freshness.

### QwenLM/qwen-code #4695

- Category: `structured-tool-contract-integrity`
- Episode: Halt repeated variants of read-only repository inspection commands
- Atomics: Classify only non-progressing overview inspections; Stop a consecutive semantic inspection loop; Propagate the structured halt reason to consumers
- Workflows: Add a precise circuit breaker for argument-varying tool stagnation
- When to use: A tool loop evades exact request equality because the model rewrites arguments while repeating the same observable read-only operation.; The repeated operation has a narrow semantic class with evidence-backed exclusions precise enough for an always-on or high-confidence guard.; The runtime already has a termination path capable of discarding queued calls and emitting a structured reason.
- Anti-goals: Do not classify all repeated uses of one tool name as equivalent.; Do not stop write-bearing, mixed-purpose, targeted-review, or otherwise progress-bearing operations merely because they contain an inspection segment.; Do not place the new precise guard behind a broad heuristic-skip setting when the intended contract is always-on, though an explicit session-level disable may remain honored.; Do not alter unrelated content, thought, read-file, alternating-call, or hard-cap detectors.

### NousResearch/hermes-agent #101899

- Category: `structured-tool-contract-integrity`
- Episode: Strip truncated tool-argument fragments prefixed by a bare tool name
- Atomics: Recognize name-prefixed structured-call fragments without consuming prose; Verify malformed-fragment removal across display and storage boundaries
- Workflows: Repair leaked truncated tool-call fragments while preserving ordinary prose
- When to use: A structured-output sanitizer already handles line-leading argument tags, but raw markup leaks when the first tag is directly attached to a bare identifier-like call name.; The malformed fragment is unrecoverable and should be removed rather than parsed or executed.; More than one consumer boundary is expected to enforce the same stripping contract.
- Anti-goals: Do not interpret, reconstruct, or execute the truncated call.; Do not accept arbitrary prose before an argument tag as a fragment prefix.; Do not remove unrelated preceding or subsequent visible prose.; Do not redesign complete structured-call parsing or unrelated reasoning-tag handling.

### earendil-works/pi #5549

- Category: `effect-control-and-isolation`
- Episode: Centralize hierarchical project trust before loading effect-bearing resources
- Atomics: Separate passive project context from effect-bearing project resources; Load policy hooks without activating project effects; Resolve authorization through one ordered fail-closed policy; Apply the closest saved authorization across directory scopes; Install the decision before project effects and writes
- Workflows: Resolve project authorization before activating local effects
- When to use: A tool discovers project-local configuration, packages, plugins, scripts, skills, prompts, themes, or similar resources that can execute code or change runtime behavior.; Multiple entry points such as the main runtime, package commands, and configuration commands must share the same project authorization semantics.; Authorization may be supplied by explicit overrides, extension hooks, persisted directory policy, global defaults, or an interactive user decision.
- Anti-goals: Do not execute project-local hooks or install project packages to determine whether that same project is trusted.; Do not treat passive instruction files as equivalent to executable or configuration-driven effects unless repository evidence establishes that they execute effects.; Do not let a permissive default override an explicit persisted denial.; Do not silently authorize unresolved effect-bearing projects merely because the caller is non-interactive.; Do not require exact-directory duplication when an explicit parent-scope authorization is intended.

### NousResearch/hermes-agent #232

- Category: `effect-control-and-isolation`
- Episode: Preserve dangerous-command detection across embedded newlines
- Atomics: Make policy patterns span embedded newlines; Add adversarial multiline classification cases
- Workflows: Close newline-based bypasses in a pre-execution command policy
- When to use: A pre-execution policy classifier uses regular expressions containing dot expressions over complete command text.; A known dangerous construct is detected in single-line form but is not detected when semantically connected tokens are separated by a newline.
- Anti-goals: Do not broaden or replace the dangerous-command pattern catalog when changing match traversal alone is sufficient.; Do not alter approval scopes, prompting behavior, environment exemptions, force semantics, or command execution behavior.; Do not normalize away arbitrary whitespace or rewrite the command that will actually be executed.

### google-gemini/gemini-cli #25935

- Category: `effect-control-and-isolation`
- Episode: Deny argument-restricted shell commands when parsing is unreliable in automatic-approval mode
- Atomics: Deny a restricted effect when its arguments cannot be reliably parsed
- Workflows: Fail closed when restricted effect arguments cannot be validated
- When to use: An automatic or non-interactive approval path authorizes effects using constraints on parsed arguments.; The parser can return no details or can return partial details together with an error indicator.; Proceeding after parse failure would prevent the policy engine from validating the restriction that justified approval.
- Anti-goals: Do not convert every parser failure into a blanket denial when no argument-level restriction must be validated.; Do not override an explicit DENY decision.; Do not change normal successful-parse evaluation, redirection handling, rule priority, or unrelated heuristic behavior.

### openai/codex #48155

- Category: `effect-control-and-isolation`
- Episode: Broaden approved-command writes without weakening explicit filesystem denials
- Atomics: Derive a broader approved policy while retaining explicit denials; Compile broad root writes without reopening denied effects; Advertise isolation guarantees without breaking legacy peers
- Workflows: Broaden approved filesystem effects while preserving denial boundaries
- When to use: An approval transition must broaden a restricted command from scoped writes to filesystem-root or volume-root writes.; The sandbox represents explicit denied paths or globs that must survive the approval transition.; The platform implements broad access through bind mounts, volume expansion, or comparable remapping that can shadow devices or reopen aliased targets.
- Anti-goals: Do not retain unrelated read or write grants from the pre-approval policy.; Do not silently drop, weaken, or reinterpret an explicit denial to make broad approval succeed.; Do not bind aliases or protected metadata paths redundantly when doing so can undo an already-applied denial mask.; Do not advertise a safety guarantee on platforms or executors that do not implement it.

### NousResearch/hermes-agent #115822

- Category: `failure-recovery-and-streaming`
- Episode: Recover a reasoning-only incomplete-response stall by handing the turn to a fallback
- Atomics: Detect a consecutive no-answer response stall; Hand a persistently stalled turn to a fallback with one bounded call; Remove source-only continuation state before a protocol handoff
- Workflows: Recover a turn stuck producing internal reasoning without an answer
- When to use: A response API repeatedly returns an incomplete status while exposing no visible answer text and no tool call.; The runtime has an existing fallback chain capable of continuing the same turn.; Continuation replay or a synthetic nudge has already failed to produce observable progress.
- Anti-goals: Do not classify visible partial progress as part of an uninterrupted no-answer streak.; Do not grant an open-ended iteration-budget extension or repeatedly allocate grace calls.; Do not mutate canonical conversation history solely to satisfy the fallback protocol.; Do not send source-protocol continuation markers or opaque replay state to an incompatible destination.; Do not replace the existing terminal partial-result behavior when no fallback can be activated.

### QwenLM/qwen-code #7832

- Category: `failure-recovery-and-streaming`
- Episode: Resume interrupted response streams without duplicating delivered output
- Atomics: Select replay, continuation, or propagation after a stream cut; Stage a request-only continuation from delivered text; Accumulate repeated continuation attempts without duplicated overlap; Reconcile successful or superseded continuation state
- Workflows: Recover a response stream cut after output may have reached the caller
- When to use: A response stream can terminate because of a retryable socket or transport failure after streaming has begun.; The stream owner can distinguish visible answer text from internal reasoning or blank output.; The request layer can issue a new attempt and the consumer supports distinct fresh-retry and continuation-retry semantics.; The conversation owner can reconcile the successful resumed response with text delivered before the final attempt.
- Anti-goals: Do not blindly replay a request after nonblank answer text has reached the caller.; Do not persist synthetic model-prefix or resume-instruction turns as real conversation history.; Do not continue across an emitted function call when doing so would insert a user turn before its required response.; Do not retry indefinitely or merge replayed overlap more than once.; Do not retain continuation state after a fresh restart has instructed the caller to discard prior output.

### google-gemini/gemini-cli #26519

- Category: `failure-recovery-and-streaming`
- Episode: Recover from premature stream closure through the existing network-retry path
- Atomics: Classify premature stream closure as a transient network failure
- Workflows: Recover a streamed operation after a recognized premature transport close
- When to use: A streaming API can yield partial data and then fail with a stable transport error code that is known to represent premature connection closure.; An existing retry framework already classifies transient network codes and wraps or governs stream recovery.; A regression can reproduce failure during stream iteration and supply a successful later attempt.
- Anti-goals: Do not make every stream exception retryable.; Do not alter retry counts, backoff timing, jitter, abort handling, or quota/server-status policies when only one transport classification is missing.; Do not treat the partial response from the failed attempt as proof of successful completion.; Do not suppress the concrete failure type from retry telemetry.

### openai/codex #47641

- Category: `failure-recovery-and-streaming`
- Episode: Honor server retry advice without restarting its countdown
- Atomics: Capture server retry advice as an absolute deadline; Preserve retry deadlines through error translation; Schedule retries against the preserved deadline
- Workflows: Honor server retry deadlines across layered recovery
- When to use: A client receives retry timing from HTTP headers or streamed errors but currently retries using only local backoff.; Retry advice passes through multiple error mappings, notifications, provider adapters, or exhausted-retry state before reuse.; Observed retry waits begin too late because each layer stores or reconstructs a relative duration.
- Anti-goals: Do not make terminal failures retryable merely because they carry retry advice.; Do not expand configured retry budgets or remove existing transport-fallback and unbounded connection-retry policies.; Do not replace local backoff for failures with missing or invalid server advice.; Do not treat an expired valid deadline as missing advice and introduce a new backoff delay.
