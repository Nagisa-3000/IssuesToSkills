# Agent-core common-category extraction: actionable Workflow contract

## Summary

- Training cases: 52
- Admitted ChangeEpisodes: 52
- Candidate Atomics: 143
- Candidate Workflows: 54
- Schema-valid responses: 52
- Holdout leaks: 0

| Category | Episodes | Atomic | Workflow | Exact | Substitute | Holdout |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| model-catalog-and-capability-metadata | 4 | 12 | 4 | 0 | 0 | Aider-AI/aider #4114 |
| provider-error-payload-normalization | 4 | 6 | 4 | 0 | 0 | QwenLM/qwen-code #7010 |
| subprocess-and-pty-lifecycle | 4 | 11 | 4 | 0 | 0 | QwenLM/qwen-code #1780 |
| permission-policy-enforcement | 4 | 14 | 4 | 0 | 0 | google-gemini/gemini-cli #17353 |
| path-root-and-worktree-resolution | 4 | 9 | 4 | 0 | 0 | openai/codex #810 |
| diff-rendering-and-review-navigation | 4 | 11 | 4 | 0 | 0 | earendil-works/pi #7903 |
| key-event-normalization-and-shortcuts | 4 | 7 | 4 | 0 | 0 | NousResearch/hermes-agent #91611 |
| unicode-width-and-terminal-rendering | 4 | 13 | 4 | 0 | 0 | openai/codex #46266 |
| extension-lifecycle-and-reload | 4 | 13 | 5 | 0 | 0 | openai/codex #47679 |
| link-integrity-and-browser-handoff | 4 | 8 | 4 | 0 | 0 | QwenLM/qwen-code #9069 |
| cross-platform-release-packaging | 4 | 12 | 4 | 0 | 0 | QwenLM/qwen-code #12649 |
| sensitive-data-redaction-in-diagnostics | 4 | 10 | 4 | 0 | 0 | Aider-AI/aider #94 |
| persistent-state-and-schema-consistency | 4 | 17 | 5 | 0 | 0 | QwenLM/qwen-code #9426 |

## Cases

### earendil-works/pi #9093

- Category: `model-catalog-and-capability-metadata`
- Episode: Remove an ineligible model from the generated built-in catalog
- Atomics: Exclude an ineligible discovered model from the built-in catalog; Reconcile capability tests with catalog membership
- Workflows: Remove an ineligible model from a generated built-in catalog
- When to use: An upstream catalog still reports a model that product policy classifies as retired, redundant, or unsuitable for the built-in catalog.; The repository generates provider catalogs from upstream metadata and already has a provider-scoped exclusion boundary.; Tests or call sites currently treat the model as a built-in catalog member.
- Anti-goals: Do not edit generated catalog shards directly when the generator is the source of truth.; Do not remove the provider, change request routing, or alter capabilities of unrelated admitted models.; Do not suppress all models from the upstream provider when only one identifier is ineligible.; Do not retain capability assertions for a model whose required invariant is absence.

### NousResearch/hermes-agent #16033

- Category: `model-catalog-and-capability-metadata`
- Episode: Move curated model-picker metadata to a remotely refreshable catalog with resilient local fallbacks
- Atomics: Define a versioned catalog for curated capability metadata; Reject incompatible catalog data before use; Resolve remote metadata through a bounded cache and fallback ladder; Adapt provider catalog entries to stable consumer shapes; Use dynamic curation without weakening picker invariants
- Workflows: Externalize curated capability metadata without making selection depend on the network
- When to use: Curated model or capability lists change more frequently than application releases.; Consumers already have bundled curated defaults that can serve as a safe last-resort snapshot.; Remote metadata can be separated from live capability, pricing, availability, or authorization data and reconciled at a defined selection boundary.
- Anti-goals: Do not make the remote catalog the sole source required for the picker to function.; Do not move volatile pricing, context limits, availability, authorization, or other live provider facts into a slowly cached curation manifest.; Do not bypass existing capability, pricing, tier, or availability filters merely because an identifier appears in the remote catalog.; Do not expose the generic manifest representation directly to consumers that already depend on stable provider-specific result shapes.

### openai/codex #46508

- Category: `model-catalog-and-capability-metadata`
- Episode: Refresh credential-scoped model metadata before starting turns
- Atomics: Reconcile cached capability metadata with the active credentials; Reconcile capability metadata before constructing a turn; Revalidate wakeup ownership after asynchronous discovery
- Workflows: Refresh identity-bound capability metadata before starting turns
- When to use: Capability or model metadata is cached in memory and scoped, directly or indirectly, to an authenticated identity.; Credentials can rotate, be lazily resolved, or be shared across multiple turn-start paths while the process remains alive.; Turn construction consumes catalog fields such as context limits or request capability flags.
- Anti-goals: Do not make remote catalog discovery a mandatory condition for starting a turn.; Do not unconditionally fetch the catalog when static metadata is used or the resolved identity already matches the cached entry.; Do not refresh after the turn context has already captured capability metadata.; Do not let an interrupted queued-work wakeup resume merely because asynchronous discovery completed.

### QwenLM/qwen-code #7144

- Category: `model-catalog-and-capability-metadata`
- Episode: Register a model generation's token capabilities in authoritative and browser-safe catalogs
- Atomics: Register specific input and output capabilities before family fallbacks; Synchronize the isolated consumer's capability mirror
- Workflows: Update ordered model capabilities across authoritative and isolated catalogs
- When to use: A recognized model generation is being classified by a broader family rule or a global default instead of its documented capabilities.; The repository has an ordered capability catalog and one or more isolated consumers that intentionally mirror it.
- Anti-goals: Do not change token-limit lookup, normalization, compaction, or request-clamping algorithms when correcting catalog metadata is sufficient.; Do not replace or widen the broad family fallback, because older or unknown family members must retain their established behavior.; Do not treat the provider's maximum configurable output as the default output value when the documented default is lower.

### Aider-AI/aider #4748

- Category: `provider-error-payload-normalization`
- Episode: Keep dynamically discovered provider error registries catchable
- Atomics: Keep only catchable types in a dynamic error registry
- Workflows: Repair a provider exception registry that admits non-catchable classes
- When to use: A runtime error reports that a class in an except clause does not inherit from the language's exception base.; A provider module exposes ordinary classes whose names satisfy the adapter's error-name convention.; An adapter constructs a catch tuple by combining provider-module discovery with an explicit metadata registry.
- Anti-goals: Do not classify an export as an exception solely because its name ends with an error-like suffix.; Do not add retry metadata for an ordinary provider payload or event class merely to satisfy a discovery-list consistency check.; Do not change retry decisions, user-facing descriptions, or handling semantics for valid provider exceptions unless separate evidence requires it.; Do not normalize provider error message or payload contents; this episode concerns exception-type classification and catchability.

### earendil-works/pi #7205

- Category: `provider-error-payload-normalization`
- Episode: Reject runtime wrapper instances as provider error bodies
- Atomics: Accept only plain structured objects as error bodies
- Workflows: Normalize ambiguous object-valued provider error payloads without losing diagnostics
- When to use: A provider or transport SDK stores heterogeneous values in fields treated as error bodies.; Displayed errors contain serialized wrapper internals or stream state instead of the exception message.; Existing filtering recognizes only a specific runtime capability, such as a pipe method, and misses other class-based wrappers.
- Anti-goals: Do not remove support for string error bodies.; Do not suppress non-empty plain parsed JSON payloads merely because they are object-valued.; Do not redesign provider-specific call sites or error-message prefixes when the defect is in the shared payload-admission boundary.; Do not infer body legitimacy from serializability or enumerable keys alone.

### NousResearch/hermes-agent #3096

- Category: `provider-error-payload-normalization`
- Episode: Add bounded provider error details to failed API-call diagnostics
- Atomics: Include available HTTP status in failure diagnostics; Show bounded details for bad-request failures
- Workflows: Enrich provider failure diagnostics with bounded payload context
- When to use: A shared provider-call boundary catches exceptions that carry HTTP status metadata not currently shown to the operator.; HTTP 400 exceptions may carry actionable response-body details that are absent from, or lost by cleaning, the ordinary exception message.; Streaming and non-streaming request paths converge on the same exception-diagnostic boundary.
- Anti-goals: Do not change retry, fallback, authentication refresh, context compression, interruption, or client-error classification policy.; Do not emit response bodies for every HTTP status.; Do not print an unbounded provider payload or replace the existing cleaned summary with the raw body.; Do not treat this diagnostic presentation change as full provider-payload schema normalization.

### google-gemini/gemini-cli #23341

- Category: `provider-error-payload-normalization`
- Episode: Normalize byte-encoded API error response bodies as UTF-8 without altering unrecognized payloads
- Atomics: Recognize byte-shaped error payloads without corrupting other data; Decode recognized error bytes as UTF-8 text
- Workflows: Normalize byte-encoded provider errors before logging and propagation
- When to use: A provider client sometimes exposes an error response body as a byte array or as comma-separated numeric bytes.; Multi-byte UTF-8 text is currently mojibake because byte values are converted directly to characters.; Normalization can run at a shared failure boundary before logging and propagation.
- Anti-goals: Do not rewrite ordinary textual or structured error payloads.; Do not accept fractional, negative, non-numeric, or greater-than-255 values as bytes.; Do not swallow, replace, or convert the original request rejection into success.; Do not redesign telemetry, retry behavior, authentication handling, or provider request routing.

### earendil-works/pi #4426

- Category: `subprocess-and-pty-lifecycle`
- Episode: Restore interactive terminal state before exiting on an uncaught exception
- Atomics: Scope the uncaught-failure handler to the interactive lifecycle; Finalize a live terminal before fatal exit
- Workflows: Restore an interactive terminal on an uncaught process failure
- When to use: A long-running interactive process enables raw input, hides the cursor, or enables terminal protocols that ordinary process termination will not reliably restore.; Asynchronous callbacks or extension code can throw outside local try/catch boundaries while the terminal remains connected.
- Anti-goals: Do not convert uncaught failures into continued execution after potentially inconsistent process state.; Do not run normal terminal writes when the terminal is already known to be dead or disconnected.; Do not replace graceful shutdown or signal-specific cleanup paths with the last-resort crash path.

### NousResearch/hermes-agent #14901

- Category: `subprocess-and-pty-lifecycle`
- Episode: Isolate stdio child-process diagnostics from the interactive terminal
- Atomics: Provision a reusable file-descriptor-backed diagnostic sink; Mark each child launch in the shared diagnostic stream; Bind child stderr to the selected diagnostic sink
- Workflows: Isolate subprocess diagnostics from an interactive terminal UI
- When to use: A library-managed child process defaults stderr to the parent process's terminal.; The parent concurrently renders an interactive terminal interface whose state can be corrupted by unsolicited writes.; Child stderr is diagnostic output rather than the protocol stream used for parent-child communication.
- Anti-goals: Do not redirect or modify the child's protocol-bearing stdin or stdout streams.; Do not redesign PID tracking, session initialization, reconnection, cancellation, or shutdown behavior.; Do not add a per-line pipe and reader thread solely to prefix diagnostics when a launch marker is sufficient.; Do not make failure to open an optional diagnostic log prevent the child from starting.

### openai/codex #26734

- Category: `subprocess-and-pty-lifecycle`
- Episode: Interrupt non-TTY subprocesses without bypassing normal lifecycle completion
- Atomics: Recognize only the interrupt control payload on closed non-TTY stdin; Propagate an interrupt without consuming lifecycle ownership; Drain interrupted-process output and preserve its real exit result
- Workflows: Add lifecycle-safe interruption for a non-TTY subprocess
- When to use: A long-running process is managed as a persistent session but was launched without a TTY or writable stdin.; The existing control surface represents Ctrl-C as an exact control-character payload.; Graceful interruption must run process signal handlers and preserve normal output and exit observation across local or remote execution.
- Anti-goals: Do not enable arbitrary stdin writes for processes whose stdin is closed.; Do not replace interrupt with hard termination or abort lifecycle observers immediately after signaling.; Do not fabricate a Ctrl-C exit code when the process can report its own handler-selected exit code.; Do not silently claim interrupt support on a backend that cannot implement it.; Do not redesign unrelated process start, read, termination, or hard-kill semantics.

### google-gemini/gemini-cli #29379

- Category: `subprocess-and-pty-lifecycle`
- Episode: Synchronize native PTY exit with public lifecycle completion and make finalization resilient
- Atomics: Reconcile native process exit with PTY lifecycle completion; Neutralize deferred resize work after process exit; Keep output failures from blocking process finalization
- Workflows: Make PTY termination deterministic across asynchronous exit and output paths
- When to use: A PTY-backed subprocess can terminate at the operating-system layer without reliably producing the library's public exit event.; Control operations may be queued internally and execute after process termination.; Output or lifecycle event consumers are outside the lifecycle owner's trust boundary and may throw during output processing or shutdown.
- Anti-goals: Do not immediately finalize at the native exit signal when a short bounded window is needed to drain trailing PTY output.; Do not suppress arbitrary resize, rendering, or consumer errors indiscriminately; contain only errors whose failure must not block lifecycle completion, and preserve logging or rethrow unrelated control errors.; Do not create separate cleanup implementations for native and public exit signals.; Do not change command semantics, output formatting, or successful interactive behavior beyond lifecycle hardening.

### Aider-AI/aider #2126

- Category: `permission-policy-enforcement`
- Episode: Resolve read-only path patterns against the repository root
- Atomics: Align relative pattern discovery with the authoritative resource root
- Workflows: Keep policy-scoped file selection stable across working-directory changes
- When to use: A command accepts relative paths or glob patterns for policy-scoped resources and fails or resolves inconsistently after the process changes into a nested directory.; Path discovery and later canonicalization use different implicit bases, allowing ambient working-directory state to affect which resource receives the policy.
- Anti-goals: Do not broaden editable access or convert read-only resources into editable resources.; Do not restrict already-supported absolute or user-home-expanded resource paths.; Do not change repository membership rules, file contents, or the process current working directory as the repair.

### NousResearch/hermes-agent #23835

- Category: `permission-policy-enforcement`
- Episode: Harden dangerous-command approval boundaries and preserve explicit bypass semantics
- Atomics: Capture process-wide bypass configuration at initialization; Require an exact machine decision token; Detect path-qualified and argument-bearing remote shell pipelines; Audit unattended dangerous-command auto-approvals; Exercise bypass behavior through the captured policy state
- Workflows: Harden approval bypasses and unattended permission decisions
- When to use: A permission or approval subsystem rereads mutable process state when deciding whether to bypass checks.; An external or model-generated response is parsed into an allow/deny decision using substring or otherwise permissive matching.; Equivalent dangerous command spellings evade a syntax-based classifier.; An unattended compatibility path intentionally auto-approves detected dangerous operations but does so silently.
- Anti-goals: Do not move bypass checks ahead of unconditional catastrophic-command or credential guards.; Do not remove session-scoped bypass controls or convert them into process-global state.; Do not change legacy unattended auto-approval into blocking behavior as part of an audit-only hardening change.; Do not treat arbitrary explanatory model text as an authoritative permission decision.; Do not broaden command patterns without retaining benign control cases to detect false positives.

### openai/codex #14171

- Category: `permission-policy-enforcement`
- Episode: Align approval and patch-safety decisions with the effective split filesystem policy
- Atomics: Classify execution approval from effective filesystem access; Propagate effective filesystem policy through every execution path; Delegate patch authorization to the shared effective-access query; Verify legacy configuration converts without permission drift
- Workflows: Align permission decisions with effective filesystem access
- When to use: A system has introduced a richer or split filesystem permission model but approval or safety consumers still inspect a legacy projection.; Different execution paths can reach the same approval decision with inconsistent policy inputs.; Local authorization code duplicates effective-access precedence or carveout calculations.
- Anti-goals: Do not introduce or redesign platform sandbox backend enforcement.; Do not change network-policy behavior except to verify legacy conversion equivalence.; Do not remove the legacy compatibility policy while call sites still require it for unrelated behavior.; Do not broaden filesystem access or suppress prompts merely to simplify the migration.

### QwenLM/qwen-code #4093

- Category: `permission-policy-enforcement`
- Episode: Route shell substitution through reviewable permission decisions with visible warnings
- Atomics: Make implicit shell risks reviewable without weakening explicit denials; Detect shell substitution before lossy normalization and across the full syntax tree; Attach a shared risk warning to shell execution confirmations; Render execution warnings without hiding approval controls
- Workflows: Replace inconsistent syntax denial with informed, policy-preserving review
- When to use: A shell-like tool has syntactic-risk checks duplicated across permission layers or sibling tools and equivalent commands receive different decisions depending on unrelated rules.; A permission fix that removes a hard deny could expose read-only-classification blind spots or lossy-normalization bypasses.; The approval surface needs to explain a risk while retaining usable controls in constrained layouts.
- Anti-goals: Do not weaken or override explicit user-configured deny rules.; Do not classify substitution-bearing commands as read-only merely to make them executable.; Do not apply the agent-tool approval policy to separately scoped user-authored shell-injection defenses.; Do not make warnings themselves errors or force ask when an explicit allow rule intentionally grants permission.

### Aider-AI/aider #4711

- Category: `path-root-and-worktree-resolution`
- Episode: Keep absolute-path conversion usable when canonical resolution encounters a symlink loop
- Atomics: Fall back to a lexical absolute path when canonical resolution fails
- Workflows: Make absolute-path normalization resilient to symlink-resolution failures
- When to use: A shared helper currently relies on canonical path resolution and a reproducible circular symbolic-link input causes that boundary to raise.; Downstream consumers require an absolute path, but do not require the fallback result to dereference every symlink.
- Anti-goals: Do not replace canonical resolution on the successful path.; Do not claim that the fallback identifies the physical filesystem target or validates path existence.; Do not broaden the change to unrelated repository-root discovery or path-containment behavior.; Do not suppress exceptions outside the explicitly selected resolution-failure classes.

### earendil-works/pi #7221

- Category: `path-root-and-worktree-resolution`
- Episode: Deduplicate repository context files in nested linked worktrees
- Atomics: Identify the exact main-repository context shadowed by a nested worktree; Skip only the shadowed context while preserving ancestor inheritance
- Workflows: Remove duplicate context loading in a nested linked worktree
- When to use: A resource loader walks filesystem ancestors and loads context files from multiple directory levels.; A linked worktree can be located beneath its main repository, causing both worktree-root and main-root copies of the same tracked context filename to appear in one ancestor chain.
- Anti-goals: Do not stop traversal at the repository or worktree root.; Do not globally deduplicate files by content, inode, or filename alone.; Do not suppress context belonging to directories above the main repository.; Do not reinterpret bare-worktree containers, sibling worktrees, or submodule superprojects as duplicate main-repository roots.

### NousResearch/hermes-agent #35399

- Category: `path-root-and-worktree-resolution`
- Episode: Resolve file edits against one observable absolute workspace target
- Atomics: Establish one absolute base for relative paths; Use and report the same canonical mutation target; Warn when a relative target escapes the active workspace; Verify routing and observability with a decoy checkout
- Workflows: Keep relative file mutations anchored to the active workspace
- When to use: A tool resolves or checks a relative file path before delegating the actual mutation to another component that may have a different working directory.; A process can operate in one checkout while a task terminal or worktree operates in another.; Successful mutation responses do not currently reveal the absolute on-disk target, making wrong-root edits difficult to diagnose.
- Anti-goals: Do not infer that every relative configured cwd identifies the intended workspace; canonicalization makes it deterministic, while live task cwd supplies workspace authority when available.; Do not re-anchor caller-supplied absolute paths under the active workspace.; Do not turn the workspace-divergence diagnostic into a blanket prohibition against intentional outside-workspace absolute paths.; Do not replace or lower the priority of existing concurrency and staleness diagnostics.; Do not broaden this workflow into redesigning file contents, patch matching, or general filesystem authorization.

### google-gemini/gemini-cli #6507

- Category: `path-root-and-worktree-resolution`
- Episode: Preserve literal file paths containing glob metacharacters across workspace-rooted file tools
- Atomics: Protect an existing literal path before pattern-based discovery; Protect existing literal paths before batch-read expansion
- Workflows: Preserve exact special-character paths across workspace-rooted file operations
- When to use: A file interface accepts both exact relative paths and glob-style patterns through the same parameter.; Existing files or directories contain characters such as square brackets or parentheses that the delegated pattern engine may interpret specially.; The operation evaluates inputs relative to one or more configured workspace or worktree roots.
- Anti-goals: Do not globally escape every input, because doing so would disable intentional wildcard expansion.; Do not change workspace containment, ignore filtering, sorting, content formatting, or file-processing behavior unrelated to input interpretation.; Do not probe only the process current directory or one global target root when pattern evaluation occurs under multiple workspace roots.

### NousResearch/hermes-agent #50731

- Category: `diff-rendering-and-review-navigation`
- Episode: Turn heterogeneous file-edit tool output into compact, reviewable chat diffs
- Atomics: Normalize file-edit results into one review model; Transform a unified diff into a readable review panel; Integrate diff review into navigable tool disclosures
- Workflows: Convert heterogeneous file-edit events into navigable code-review panels
- When to use: A conversational or activity-stream interface receives file mutations from multiple tool/event shapes and reviewers need to inspect the resulting code changes in place.; Mutation results already provide, or can be reconciled to, unified-diff text and a stable event identity.; Raw patch output currently includes transport metadata or generic tool payload detail that obscures the changed code.
- Anti-goals: Do not alter the semantics or contents of the underlying file mutation.; Do not count unified-diff file headers as additions or removals.; Do not require syntax highlighting for a diff to remain visible and readable.; Do not hide pending mutations or failed mutations merely because they lack a diff.; Do not remove access to raw diagnostic payloads when a technical drill-down mode is required.

### openai/codex #41143

- Category: `diff-rendering-and-review-navigation`
- Episode: Bound inline diff previews while preserving complete review views
- Atomics: Bound inline diff rendering by visible rows and scanned source; Route compact and complete review surfaces through distinct rendering contracts
- Workflows: Add a bounded inline diff preview without truncating complete review views
- When to use: An inline or feed-style diff surface eagerly wraps, highlights, or allocates rows for complete change content.; Large, minified, narrow-width, wide-character, or zero-width-heavy changes can make preview cost or height effectively unbounded.; A separate transcript, raw, expanded, or detail surface can remain the source of complete content.
- Anti-goals: Do not impose the preview limit on transcript, raw, expanded, export, or other complete-review surfaces.; Do not remove file summaries or rename metadata merely because the content budget is exhausted.; Do not treat logical source lines alone as the visible budget when viewport wrapping can produce multiple rendered rows.; Do not rely only on display width to bound source scanning, because zero-width input can consume bytes without consuming columns.; Do not truncate small or exact-budget diffs.

### QwenLM/qwen-code #7054

- Category: `diff-rendering-and-review-navigation`
- Episode: Add bounded, workspace-scoped working-tree diff review
- Atomics: Compute a safe, bounded diff for one changed file; Expose diff review through a trusted read-only workspace contract; Render an expandable diff review surface with explicit degradation states; Route every review entry point to the intended workspace
- Workflows: Add bounded, workspace-correct change review
- When to use: A client must review local working-tree changes through a remote, daemon, browser, or otherwise separated presentation layer.; Whole-tree diff retrieval is too expensive or unsafe, so detailed content should be loaded only for the file being reviewed.; The application can address more than one workspace and review actions must retain workspace ownership.
- Anti-goals: Do not mutate the working tree, index, branch, stash, or repository configuration.; Do not eagerly fetch or syntax-highlight every file in the working tree.; Do not silently present capped content as a complete diff.; Do not bypass workspace trust checks or permit path traversal.; Do not forward a local review-navigation command to an agent or command executor.

### google-gemini/gemini-cli #29378

- Category: `diff-rendering-and-review-navigation`
- Episode: Preserve the previously focused terminal when closing a programmatically managed diff tab
- Atomics: Close a managed diff without stealing focus; Verify focus continuity in a real editor host
- Workflows: Preserve user focus when programmatically closing a review diff
- When to use: A programmatically closed diff or review tab causes focus to jump to an editor or another unintended surface.; Several diff-completion entry points converge on one shared tab-closing routine.; The host editor exposes a close option that retains the current focus owner and supports extension-host behavioral tests.
- Anti-goals: Do not change how diff content is accepted, rejected, or transmitted.; Do not keep the diff tab open merely to avoid the focus transition.; Do not expose test-only diff-opening controls in production mode.; Do not treat mocked API assertions alone as proof of real focus routing.

### earendil-works/pi #746

- Category: `key-event-normalization-and-shortcuts`
- Episode: Replace a text-producing shortcut with a modifier-only chord
- Atomics: Replace a text-producing shortcut with a non-text chord; Synchronize user-facing shortcut guidance
- Workflows: Resolve a shortcut that intercepts ordinary text input
- When to use: A shortcut based on Shift plus a printable letter is triggered by ordinary uppercase text input.; The shortcut system supports a distinguishable multi-modifier chord and exposes reserved bindings for conflict checks.
- Anti-goals: Do not change the action's behavior, state transition, or command-based activation path.; Do not modify the global key parser when the conflict is caused by an individual binding choice.; Do not select a replacement solely because it is syntactically valid; account for built-in and common platform conflicts.

### openai/codex #2412

- Category: `key-event-normalization-and-shortcuts`
- Episode: Map a control-character shortcut to backward deletion in the text input handler
- Atomics: Route an equivalent key event to the existing edit action
- Workflows: Add an exact keyboard alias for an existing text-editing command
- When to use: A terminal or input environment emits a distinct key-and-modifier event for a familiar editing command.; The input dispatcher already owns a tested primitive with the required editing semantics.; The proposed event is currently unmatched at the relevant dispatch boundary.
- Anti-goals: Do not reimplement backward-deletion or cursor-boundary logic in the shortcut branch.; Do not broaden the match to additional modifier combinations that are not established as equivalent.; Do not remap unrelated navigation, word-deletion, insertion, or submission commands.

### google-gemini/gemini-cli #582

- Category: `key-event-normalization-and-shortcuts`
- Episode: Route Ctrl+W to the text buffer's existing previous-word deletion operation
- Atomics: Route a normalized shortcut to an existing semantic edit action
- Workflows: Add a shortcut by reusing an existing semantic editing operation
- When to use: A shared input dispatcher already receives normalized character and modifier fields.; The requested shortcut should invoke an existing, independently defined semantic edit operation.; The chord is currently unhandled at the dispatcher reached by the interactive input call site.
- Anti-goals: Do not reimplement word-boundary deletion inside the key-event branch.; Do not globally reinterpret the input character when the required modifier is absent.; Do not reorder or broaden unrelated shortcut predicates merely to add the new chord.; Do not claim regression coverage when no direct shortcut test has been added or run.

### QwenLM/qwen-code #2011

- Category: `key-event-normalization-and-shortcuts`
- Episode: Add a guarded keyboard shortcut for replaying the last failed request
- Atomics: Register and dispatch a conflict-free semantic shortcut; Capture the last failed operation and guard its replay; Reconcile transient error UI before replaying the stored request
- Workflows: Add a guarded keyboard command for replaying the last failed operation
- When to use: A terminal or keyboard-driven interface needs an explicit shortcut to repeat the most recent failed asynchronous operation.; The application can identify and retain the exact prepared operation that failed.; The input layer already routes normalized key events through semantic command matchers and UI actions.
- Anti-goals: Do not make the unmodified character trigger replay or replace an existing shortcut.; Do not replay the most recent successful operation or guess a request when no failed target exists.; Do not interrupt an active response or a confirmation workflow.; Do not duplicate prompt preparation or leave transient retry hints in durable history.; Do not redesign automatic retry policy as part of adding the manual shortcut.

### earendil-works/pi #6987

- Category: `unicode-width-and-terminal-rendering`
- Episode: Align grapheme-cluster width estimates with terminal cell allocation
- Atomics: Reconcile grapheme width with terminal cell allocation; Validate corrected and preserved Unicode width boundaries
- Workflows: Correct terminal widths for multi-code-point graphemes
- When to use: A terminal UI measures text by grapheme clusters but observed rendering advances farther than the computed width.; Failures involve marks, conjuncts, or visible continuations grouped into one grapheme by Unicode segmentation.; The same width primitive controls clipping, padding, wrapping, selection, or overflow checks.
- Anti-goals: Do not equate every Unicode mark with a terminal cell.; Do not change established emoji, CJK, Japanese, ANSI-sequence, or ordinary combining-mark behavior without evidence.; Do not cap repeated spacing or continuation contributions when the terminal model may advance for each one.; Do not treat this heuristic as exact for every terminal implementation.

### NousResearch/hermes-agent #26011

- Category: `unicode-width-and-terminal-rendering`
- Episode: Keep terminal fast-echo optimization on an ASCII-safe boundary
- Atomics: Restrict direct terminal append to layout-stable text; Restrict direct terminal backspace to ASCII graphemes; Validate the optimized and renderer fallback boundaries
- Workflows: Make a terminal input fast path safe for Unicode and IME text
- When to use: A terminal input component writes append or erase sequences directly to the terminal and bypasses its normal renderer.; Unicode or IME input produces duplicated, scattered, ghosted, incorrectly erased, or cursor-desynchronized text.; Existing fast-path eligibility relies mainly on code-unit length or display-width equality.
- Anti-goals: Do not disable the optimization for ordinary printable ASCII edits that satisfy the existing TTY and layout constraints.; Do not treat display width alone as proof that an edit is safe to render outside the normal renderer.; Do not redesign Unicode segmentation, the normal rendering engine, or the input method implementation when a conservative bypass boundary resolves the fault.

### QwenLM/qwen-code #5999

- Category: `unicode-width-and-terminal-rendering`
- Episode: Replace unstable emoji-width markers in terminal-visible text
- Atomics: Normalize terminal-visible markers to stable text symbols; Preserve state distinctions without relying on color; Reconcile translations and documentation with changed display strings; Exercise rendered states through supported component inputs; Guard surfaces that must remain glyph-free
- Workflows: Stabilize Unicode markers across terminal output contracts
- When to use: Terminal alignment, wrapping, or spacing is unreliable because user-visible prefixes contain emoji or emoji-presentation sequences.; A status interface uses colored emoji whose width or meaning changes across terminals, CJK environments, NO_COLOR output, or copied text.; Changing a rendered marker also changes localization keys, snapshots, exact-string tests, or documented examples.
- Anti-goals: Do not replace every Unicode character merely because it is non-ASCII.; Do not make state meaning depend only on color or use one identical shape for semantically opposed states.; Do not alter substantive labels, state transitions, or business behavior while repairing marker width.; Do not propagate the terminal glyph vocabulary into tables, model prompts, web-only text, or other surfaces without verifying their separate presentation contract.; Do not treat updated snapshots alone as proof when the fixture does not actually select the intended state branch.

### google-gemini/gemini-cli #18240

- Category: `unicode-width-and-terminal-rendering`
- Episode: Wrap terminal markdown-table content using Unicode display widths
- Atomics: Allocate column widths from terminal display-cell constraints; Wrap cells into aligned multi-line terminal rows; Remove redundant header markup before wrapping
- Workflows: Replace lossy table truncation with Unicode-aware wrapping
- When to use: A terminal table truncates long headers or cells even though vertical wrapping is acceptable.; Column widths or padding are computed from code-unit or plain string length and become unreliable for emoji or wide scripts.; The renderer receives an explicit terminal-width budget and owns table borders, padding, and row layout.
- Anti-goals: Do not change the semantic contents of table cells merely to make them fit.; Do not optimize for a fixed character count when terminal display width is the relevant invariant.; Do not remove inline rendering or renderer-owned header styling.; Do not introduce horizontal scrolling or widen the terminal as a substitute for bounded wrapping.

### earendil-works/pi #681

- Category: `extension-lifecycle-and-reload`
- Episode: Restore extension module loading inside the compiled runtime
- Atomics: Break the loader/public-entrypoint import cycle; Provide extension imports through runtime-specific module maps; Include the compatible source transformer in the executable dependency graph
- Workflows: Restore extension imports in a compiled executable
- When to use: Extensions load in a normal filesystem-backed runtime but fail after the host application is compiled into a single executable.; The extension loader relies on dynamic evaluation and extensions import host packages or local TypeScript modules that are not independently present in the executable filesystem.; Making the host public API statically available to the loader currently creates an entrypoint/loader initialization cycle.
- Anti-goals: Do not redesign extension discovery, registration, or execution lifecycle when the failure is confined to module resolution and transformation.; Do not expose loader-internal operations from the public package entrypoint merely to preserve an accidental export surface.; Do not replace supported host package imports with copied extension-local implementations.; Do not treat documentation changes or a successful development-mode test as proof that the compiled executable path works.

### NousResearch/hermes-agent #64178

- Category: `extension-lifecycle-and-reload`
- Episode: Make callback delivery lazy-safe and force reload lifecycle-symmetric
- Atomics: Discover extensions before checking or delivering callbacks; Remove legacy global registrations during full unload; Restore configuration-owned hooks after force reload
- Workflows: Make extension callback delivery independent of startup path; Make force reload reconcile legacy and configuration-owned state
- When to use: Some process surfaces invoke shared callback APIs without a guaranteed earlier extension-discovery call.; Callers use a callback-presence predicate as a gate before dispatch, so a pre-discovery false result can suppress delivery.
- Anti-goals: Do not require every caller or startup surface to duplicate extension initialization.; Do not force discovery for injected test doubles or adapters that intentionally lack the real manager's lifecycle state.; Do not change callback return aggregation or callback argument semantics.

### google-gemini/gemini-cli #8692

- Category: `extension-lifecycle-and-reload`
- Episode: Resolve extension uninstall requests by installed name or recorded source
- Atomics: Declare the alternate identifier accepted by the lifecycle command; Resolve a removal identifier to the canonical installed identity
- Workflows: Support safe removal by configured identity or recorded installation source
- When to use: A lifecycle command accepts only an internal or configured name, but users retain and naturally reuse the source URL or path supplied during installation.; Installed records persist provenance that can unambiguously identify the lifecycle target.; Existing cleanup subsystems require a canonical installed name rather than the external identifier.
- Anti-goals: Do not infer a source match from URL fragments, directory names, or configured-name similarity when persisted provenance is absent.; Do not pass a source URL or path directly into storage deletion, enablement-state removal, or telemetry as though it were the canonical installed name.; Do not broaden the change into installation, update, reload, or storage-layout redesign.; Do not remove unrelated installed extensions while resolving the requested identifier.

### QwenLM/qwen-code #6347

- Category: `extension-lifecycle-and-reload`
- Episode: Detect extension changes and reconcile the live runtime without restarting the session
- Atomics: Classify extension file changes by safe refresh scope; Coordinate reload state and suppress self-generated watcher events; Refresh content capabilities in place; Rebuild the extension runtime from one coherent snapshot; Reload configured hooks without discarding session hooks
- Workflows: Reconcile live extension changes at the narrowest safe scope
- When to use: A long-lived process loads extensible capabilities from files that users or development tools can edit outside the process.; Some extension changes can be refreshed locally, while manifests, hooks, topology, or referenced configuration require a coherent whole-package rebuild.; Programmatic extension mutations and filesystem notifications may overlap or echo one another.
- Anti-goals: Do not hot-apply arbitrary or unknown extension files.; Do not treat security-sensitive hook edits as content-only refreshes.; Do not change extension discovery, installation-source, marketplace, or conversion semantics as part of reload coordination.; Do not follow extension-provided symlinks into arbitrary external paths.; Do not hide MCP, LSP, hook, or aggregated content-refresh failures behind a success message.

### earendil-works/pi #7657

- Category: `link-integrity-and-browser-handoff`
- Episode: Close active terminal hyperlinks at truncation boundaries
- Atomics: Close an active hyperlink before truncated output ends
- Workflows: Repair hyperlink state when truncating terminal text
- When to use: A text truncation or clipping function preserves embedded hyperlink control sequences in its retained prefix.; The original hyperlink closer can fall in the discarded suffix, leaving the retained output structurally unbalanced.
- Anti-goals: Do not remove hyperlink targets or visible label content that fits within the existing width budget.; Do not alter visible-width calculation, truncation position, padding, or ellipsis policy.; Do not treat a generic style reset as sufficient to close a separate hyperlink protocol.

### NousResearch/hermes-agent #120790

- Category: `link-integrity-and-browser-handoff`
- Episode: Add a persistent policy for handing clicked links to the system browser
- Atomics: Maintain a synchronized device-local link handoff preference; Expose the link handoff policy as a localized settings control; Apply the handoff policy at the central clicked-link boundary
- Workflows: Add a user-selectable browser handoff policy for clicked links
- When to use: A desktop or embedded application centrally intercepts link clicks and users need a persistent choice between an internal browser surface and the operating-system browser.; The application already has distinct internal-preview and external-handoff primitives that can remain authoritative for explicit actions.
- Anti-goals: Do not change the default destination for users who have not enabled the preference.; Do not replace or remove existing modifier, middle-click, authorization, special-surface, or non-web-scheme routing rules.; Do not make explicit Open in in-app browser or Open in external browser commands obey the ordinary-click preference.; Do not synchronize this device-specific UI preference through remote agent configuration.

### openai/codex #25485

- Category: `link-integrity-and-browser-handoff`
- Episode: Route macOS workspace launches through an encoded application deep link
- Atomics: Encode the requested target in an application-owned deep link; Hand the application-owned link to the operating-system launcher
- Workflows: Replace an unreliable document-open handoff with an explicit application route
- When to use: The operating-system launcher successfully selects or focuses the destination application but its generic document-open argument is not reliably honored.; The destination application provides a supported deep-link route capable of representing the requested target.; The target must survive transport through URL syntax without spaces, fragment markers, or other reserved characters changing its meaning.
- Anti-goals: Do not redesign application discovery, installation, architecture detection, or download behavior.; Do not shell-escape or concatenate the workspace into a URL manually when a structured query serializer is available.; Do not change the CLI workspace argument contract or optimize unrelated installer behavior.; Do not treat successful process launch alone as proof that the target was encoded or delivered correctly.

### google-gemini/gemini-cli #5367

- Category: `link-integrity-and-browser-handoff`
- Episode: Replace repeated automatic browser launches with an explicit documentation handoff
- Atomics: Replace automatic navigation with an explicit user-controlled handoff; Encode a deterministic empty-state handoff contract
- Workflows: Make repeated empty-state documentation handoffs user-controlled
- When to use: A command, status view, refresh path, or similarly repeatable interaction automatically opens documentation when no resources are configured.; Multiple callers converge on the same empty-state branch, making an otherwise helpful browser handoff repeatable.; The external documentation target should remain available, but navigation should require deliberate user action.
- Anti-goals: Do not remove or silently change the established documentation target.; Do not alter configured-resource status, discovery, authentication, or refresh behavior beyond the shared empty-state return path.; Do not optimize browser-launch mechanics or add another environment-specific automatic-launch policy.; Do not claim that the external URL destination or the internal documentation command itself was exercised unless separately validated.

### Aider-AI/aider #4899

- Category: `cross-platform-release-packaging`
- Episode: Extend package installation and validation through Python 3.14 across Linux and Windows
- Atomics: Align package metadata with the expanded runtime range; Partition dependency constraints by runtime capability; Preserve runtime markers in generated release requirements; Expand cross-platform validation to every supported runtime
- Workflows: Extend a packaged application across new interpreter releases
- When to use: Package metadata must admit one or more new interpreter releases.; At least one dependency or removed standard-library module requires different treatment across old and new interpreter cohorts.; The repository commits generated dependency artifacts and validates installation on multiple operating systems.
- Anti-goals: Do not drop an older supported interpreter merely to use one unconditional modern dependency pin.; Do not claim runtime support solely by changing package classifiers or the interpreter upper bound.; Do not let a lock generated on one host replace cross-runtime marker branches with host-specific pins.; Do not broaden unrelated application behavior or optimize dependency versions beyond what compatibility requires.

### earendil-works/pi #4458

- Category: `cross-platform-release-packaging`
- Episode: Add an architecture-specific Windows release artifact across build, packaging, and publication
- Atomics: Extend the release target contract and prerequisites; Package the correct native payload for each architecture; Publish the new artifact in every release path
- Workflows: Add a new architecture to a cross-platform binary release
- When to use: A supported operating-system family lacks a release artifact for one hardware architecture.; The binary includes optional or external native components whose packaged payload must match the target architecture.; Release publication enumerates artifact filenames explicitly.
- Anti-goals: Do not embed every platform's native modules into every compiled binary.; Do not change archive conventions for already-supported operating-system families without a separate requirement.; Do not treat artifact generation alone as completion when release upload lists are explicit.; Do not claim runtime compatibility from archive extraction alone.

### NousResearch/hermes-agent #36134

- Category: `cross-platform-release-packaging`
- Episode: Restore the desktop packaging toolchain in isolated installer stages and report missing prerequisites as failure
- Atomics: Restore the packaging toolchain inside an isolated stage; Fail requested packaging when its toolchain remains unavailable
- Workflows: Make an isolated packaging stage restore prerequisites and report truthful completion
- When to use: Installer stages run in separate processes or otherwise do not inherit PATH mutations from prerequisite stages.; A packaging stage depends on a runtime that may have been installed into an application-managed directory.; The current behavior can skip a requested build and still report successful completion.
- Anti-goals: Do not make optional command-line or first-launch flows rebuild the desktop application when they did not request packaging.; Do not treat signing, notarization, or distributable image production as part of this prerequisite-restoration fix.; Do not accept process success alone when the expected packaged artifact is absent.; Do not replace the managed toolchain policy with an unrelated packaging system.

### google-gemini/gemini-cli #19171

- Category: `cross-platform-release-packaging`
- Episode: Publish the prebuilt CLI bundle with platform-specific optional dependencies
- Atomics: Require and stage the generated release bundle; Reconcile the package manifest with a bundled runtime; Gate bundled preparation by publication target
- Workflows: Package a prebuilt CLI without losing platform-specific runtime support
- When to use: A release pipeline already generates a bundled executable, but the package manifest and files allowlist still describe source-oriented or separately compiled output.; The package needs optional native dependencies selected by operating system or architecture even though ordinary runtime dependencies are absorbed into the bundle.; Different publication targets require distinct package preparation behavior.
- Anti-goals: Do not redesign the bundler or change the runtime behavior of the generated executable.; Do not remove platform-specific optional dependencies merely because ordinary dependencies are bundled.; Do not apply the bundled manifest transformation to registry paths with a separate packaging contract.; Do not treat successful bundle generation alone as proof that the final package tarball is complete.

### NousResearch/hermes-agent #77484

- Category: `sensitive-data-redaction-in-diagnostics`
- Episode: Redact secrets at terminal exception-result and ACP stderr boundaries
- Atomics: Redact exception diagnostics before returning them to the caller; Install redaction on an independently configured diagnostic log sink
- Workflows: Close secret leaks at structured-result and log-output boundaries
- When to use: A structured error result exposes raw exception messages, tracebacks, command context, or comparable diagnostic text to an external consumer.; A subsystem replaces inherited logging handlers or formatters and therefore bypasses an established application-wide redaction formatter.; An existing, tested sensitive-text redaction policy can be reused at the emission boundary.
- Anti-goals: Do not remove the error result, traceback field, log destination, log layout, filters, or status information merely to avoid leakage.; Do not redesign or broaden the secret-detection algorithm when the demonstrated defect is an emission boundary that fails to invoke the existing policy.; Do not claim closure of unrelated secret-emission gaps outside the inspected exception-result and ACP stderr surfaces.

### openai/codex #48686

- Category: `sensitive-data-redaction-in-diagnostics`
- Episode: Remove sensitive response metadata and tool arguments from informational diagnostics
- Atomics: Omit response metadata from successful connection diagnostics; Omit tool arguments from invocation diagnostics
- Workflows: Remove sensitive values from routine diagnostics while preserving operational context
- When to use: An info-level success or invocation message serializes a complete metadata collection or request/tool argument payload.; The sensitive value is needed by runtime processing but is not required to identify the diagnostic event.; The diagnostic can remain useful with bounded identifiers such as a connection target, correlation ID, or operation name.
- Anti-goals: Do not disable successful-connection or tool-invocation diagnostics entirely.; Do not remove metadata or payloads from protocol processing, persistence, or tool execution.; Do not broaden the change to error diagnostics, payload storage, or unrelated telemetry without separate evidence and validation.; Do not optimize diagnostic verbosity or performance beyond eliminating the sensitive formatting operations.

### google-gemini/gemini-cli #26153

- Category: `sensitive-data-redaction-in-diagnostics`
- Episode: Honor the telemetry payload-consent flag across diagnostic logging paths
- Atomics: Gate diagnostic payload fields on explicit logging consent; Reduce mixed diagnostic metadata to explicitly safe aggregates; Apply the same payload boundary across telemetry sinks
- Workflows: Enforce consent-aware redaction at diagnostic emission boundaries
- When to use: A runtime privacy or consent flag is intended to control prompt, response, command, policy, rationale, or comparable free-form diagnostic payloads.; The same logical event is serialized through multiple record types or telemetry backends.; Structured metadata may combine safe aggregate measurements with arbitrary content-bearing values.
- Anti-goals: Do not disable all telemetry when only payload content requires suppression.; Do not remove safe event identity, timing, status, verdict, error, or aggregate measurement fields solely because payload logging is disabled.; Do not treat an entire extensible metadata object as safe merely because some of its current keys are numeric counters.; Do not change the meaning of the runtime consent flag or enable payload logging implicitly.

### QwenLM/qwen-code #6200

- Category: `sensitive-data-redaction-in-diagnostics`
- Episode: Bound sensitive and attacker-controlled data at diagnostic boundaries
- Atomics: Sanitize and bound untrusted diagnostic text; Replace sensitive remote error bodies with bounded metadata; Verify diagnostic non-disclosure and structural safety
- Workflows: Harden diagnostics that may contain sensitive or attacker-controlled data
- When to use: An HTTP, messaging, gateway, persistence, or handler failure can place remote payloads or exception text into logs or caller-visible errors.; A credential-bearing request currently includes its remote error body in diagnostics.; User-controlled or server-controlled text can contain line breaks, terminal controls, invisible separators, bidi controls, or unbounded content.
- Anti-goals: Do not remove stable status codes or ordinary readable context needed to diagnose the failure.; Do not treat simple truncation as sufficient protection against control-character or line-forging attacks.; Do not log credential-adjacent response bodies merely because they may contain a useful server error message.; Do not change transport behavior, retry policy, or unrelated state-persistence semantics as part of the redaction contract.

### earendil-works/pi #6594

- Category: `persistent-state-and-schema-consistency`
- Episode: Add a transactional SQLite session backend with schema-backed summaries and bounded context reconstruction
- Atomics: Move persistent session queries behind the storage contract; Persist canonical events and derived state in one transaction; Initialize persistent storage through recorded migrations; Make compaction entries self-contained for recent context
- Workflows: Introduce a relational session backend without breaking session semantics
- When to use: A new durable backend must implement an existing in-memory or file-backed event-session abstraction.; Resume, listing, statistics, or branch reconstruction requires indexed or materialized state instead of repeatedly scanning the full history.; One logical append updates canonical history and multiple derived representations that must not diverge.
- Anti-goals: Do not replace the append-only session event model with only a mutable snapshot.; Do not make backend-specific database concepts part of the reusable Session caller API.; Do not silently discard legacy compaction records that lack embedded retained messages.; Do not treat materialized summaries as independently writable sources of truth.

### NousResearch/hermes-agent #3249

- Category: `persistent-state-and-schema-consistency`
- Episode: Keep session state available under SQLite contention and reconcile incomplete transcript migration
- Atomics: Make session-row creation safe to repeat; Repair a missing session parent before appending messages; Keep persistence available after transient initialization failure; Give concurrent writers a bounded recovery window; Release the database lock between search context queries; Restore history from the most complete transcript source
- Workflows: Recover session persistence after transient database contention; Prevent transcript truncation while two persistent stores coexist
- When to use: Multiple processes or threads share an embedded session database and startup or flush operations can overlap.; A failed initial parent-row insert currently disables later persistence or leaves child-message writes unable to satisfy their parent relationship.; Search enrichment performs multiple database round trips while sharing the same connection lock.
- Anti-goals: Do not remove foreign-key enforcement or append orphaned messages.; Do not overwrite established session metadata during recovery.; Do not retry forever or conceal persistent storage failures.; Do not change message ordering or the existing flush cursor semantics.

### openai/codex #24819

- Category: `persistent-state-and-schema-consistency`
- Episode: Consolidate dynamic-tool persistence onto rollout session metadata while retaining schema compatibility
- Atomics: Restore immutable session configuration from its authoritative history record; Remove writes, reads, and synchronization for the redundant state replica; Retain the unused persisted schema for mixed-version compatibility; Verify restoration through the real resume request boundary
- Workflows: Consolidate duplicated persistent state without breaking restoration or older schemas
- When to use: The same immutable or thread-start state is persisted in both an authoritative event/history record and a secondary database representation.; Resume or fork behavior can reconstruct the state from the authoritative record.; The duplicated path spans reads, writes, ingestion/backfill, reconciliation, or metadata synchronization and creates competing ownership.; A legacy schema may still be referenced by older supported binaries.
- Anti-goals: Do not change the dynamic-tool contract, ordering, description, input schema, namespace semantics, or caller override precedence.; Do not remove unrelated thread metadata persistence or backfill responsibilities.; Do not drop a legacy table merely because the current runtime stops using it.; Do not treat the secondary database as the new source of truth when the durable session record already owns the state.

### google-gemini/gemini-cli #18506

- Category: `persistent-state-and-schema-consistency`
- Episode: Serialize policy persistence and validate stored regular-expression rules
- Atomics: Serialize persistent read-modify-write updates; Give each atomic write an exclusive staging file; Reject unsafe regular expressions at every state-ingress boundary
- Workflows: Make file-backed policy updates race-safe and safe to restore
- When to use: An event-driven component performs read-modify-write updates against one persistent structured-state file.; Concurrent or closely spaced updates can read the same prior snapshot or share a temporary pathname.; Persisted fields are later compiled or interpreted as executable matching expressions.
- Anti-goals: Do not change policy precedence, decisions, or the representation of accepted rule fields.; Do not serialize unrelated in-memory operations that do not request persistence.; Do not treat the heuristic regex check as a complete regular-expression complexity proof or silently rewrite rejected patterns.
