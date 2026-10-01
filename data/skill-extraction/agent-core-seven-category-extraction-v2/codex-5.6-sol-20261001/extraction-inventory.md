# Agent-core 七类 Issue Skill 抽取结果（v2）

更新时间：2026-10-01（Asia/Shanghai）

## 本轮边界

本轮只做真实实现证据驱动的 `Issue/PR/commit -> ChangeEpisode -> candidate Atomic -> candidate Workflow` 抽取。
没有执行 Pattern 归纳、graph/catalog 构建、检索、graph expansion、LLM judge/use、反馈治理或 holdout agent 对照实验。

## 总体结果

- 训练 case：28（7 类 × 4 个仓库）。
- admitted ChangeEpisode：28/28。
- JSON Schema 独立复验：28/28 通过。
- candidate Atomic：79。
- candidate Workflow：29。
- 原表 exact row：7；显式 verified substitute：21。
- untouched holdout：7；泄漏检查：0。
- 模型与来源：`openai/gpt-5.6-sol`，RVNPU Responses endpoint，离线 pinned-local-git evidence bundle。
- API key 只作为进程环境变量传入，没有写入 manifest、报告或抽取 artifact；临时 CODEX_HOME 已清理。
- 本机 Linux Codex runtime 缺少 bubblewrap，因此正式抽取使用了 bypass sandbox；抽取后复查：原本 clean 的 Hermes/Pi 仍 clean，六个 source checkout 均未新增 untracked 文件，临时 worktree 和测试目录已清理。
- 项目回归：PYTHONPATH=. ./.venv-linux/bin/pytest -q，85 passed。

## 分类汇总

| 类别 | admitted | exact | substitute | Atomic | Workflow | untouched holdout |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `provider-interface-adaptation` | 4 | 0 | 4 | 12 | 4 | earendil-works/pi #5823 |
| `credential-resolution-and-authentication` | 4 | 2 | 2 | 14 | 4 | Aider-AI/aider #750 |
| `context-budget-and-compaction` | 4 | 1 | 3 | 8 | 4 | NousResearch/hermes-agent #43547 |
| `state-continuity-and-resume` | 4 | 1 | 3 | 12 | 4 | openai/codex #47761 |
| `structured-tool-contract-integrity` | 4 | 1 | 3 | 9 | 5 | google-gemini/gemini-cli #29308 |
| `effect-control-and-isolation` | 4 | 1 | 3 | 10 | 4 | QwenLM/qwen-code #10859 |
| `failure-recovery-and-streaming` | 4 | 1 | 3 | 14 | 4 | earendil-works/pi #9735 |

## Case 与抽取出的 Skill 名称

### provider-interface-adaptation

Holdout（未抽取）：[earendil-works/pi #5823](https://github.com/earendil-works/pi/issues/5823)

- **Aider-AI/aider #88** — substitute for seed #2765; ref `549a1a76403e`
  - Episode: Adapt provider configuration and request routing for alternate hosted endpoints
  - Atomic: `configure-provider-client-at-startup`, `decouple-worker-construction-from-provider-initialization`, `adapt-request-routing-fields-at-provider-call`
  - Workflow: `adapt-a-client-to-an-alternate-compatible-provider-interface`
  - Evidence 12；unresolved questions 3；validation PASS
- **NousResearch/hermes-agent #125942** — substitute for seed #121359; ref `33c6ab002d1f`
  - Episode: Restore resumed sessions through the canonical persisted runtime route
  - Atomic: `reconcile-partial-persisted-route-with-provider-fallback`, `adapt-resume-consumer-to-canonical-route-reader`, `validate-conflicting-route-precedence`
  - Workflow: `unify-resume-routing-around-the-latest-persisted-runtime`
  - Evidence 13；unresolved questions 2；validation PASS
- **QwenLM/qwen-code #11657** — substitute for seed #9452; ref `3ba01990e13e`
  - Episode: Adapt outbound reasoning fields to a strict OpenAI-compatible endpoint
  - Atomic: `Route an endpoint-specific adapter by canonical hostname`, `Remove only a synthesized duplicate field at the outbound boundary`, `Validate continuation against a strict endpoint contract`
  - Workflow: `Adapt a generic compatible request shape to a stricter endpoint`
  - Evidence 11；unresolved questions 2；validation PASS
- **google-gemini/gemini-cli #25357** — substitute for seed #15430; ref `cb289e0724b4`
  - Episode: Adapt content-generation client configuration to provider-specific endpoint overrides
  - Atomic: `resolve-provider-specific-endpoint-override`, `guard-custom-endpoint-transport`, `align-downstream-provider-mode-with-authentication`
  - Workflow: `adapt-provider-client-to-secure-endpoint-overrides`
  - Evidence 12；unresolved questions 2；validation PASS

### credential-resolution-and-authentication

Holdout（未抽取）：[Aider-AI/aider #750](https://github.com/Aider-AI/aider/issues/750)

- **NousResearch/hermes-agent #289** — exact; ref `221e4228ecb4`
  - Episode: Prefer the endpoint-specific API credential across runtime resolution paths
  - Atomic: `prioritize-service-specific-credential`, `reconcile-credential-precedence-across-initialization-paths`, `encode-conflict-and-fallback-regression-cases`
  - Workflow: `correct-provider-aware-credential-precedence`
  - Evidence 10；unresolved questions 2；validation PASS
- **QwenLM/qwen-code #9016** — exact; ref `fd9c452dc889`
  - Episode: Allow a keyless cloud-provider configuration to resolve Application Default Credentials without changing principals
  - Atomic: `classify-project-based-credential-eligibility`, `reconcile-credential-validation-gates`, `construct-client-with-authentication-mode-and-absent-key`, `map-missing-credential-errors-to-actionable-alternatives`, `report-routing-configuration-as-indeterminate-authentication`
  - Workflow: `enable-default-credential-authentication-without-silent-principal-fallback`
  - Evidence 16；unresolved questions 3；validation PASS
- **earendil-works/pi #7176** — substitute for seed #9245; ref `b63403a50f57`
  - Episode: Preserve explicitly configured credential-profile precedence over ambient access keys
  - Atomic: `prefer_application_configured_profile`, `preserve_ambient_access_key_fallback`, `validate_credential_source_precedence_matrix`
  - Workflow: `repair_configured_credential_source_precedence`
  - Evidence 9；unresolved questions 3；validation PASS
- **google-gemini/gemini-cli #28472** — substitute for seed #28337; ref `f743ab579098`
  - Episode: Continue credential resolution after a higher-priority cached credential fails verification
  - Atomic: `collect-ordered-credential-candidates`, `verify-credential-candidates-until-success`, `validate-invalid-primary-to-valid-fallback-transition`
  - Workflow: `recover-authentication-through-ordered-credential-fallback`
  - Evidence 10；unresolved questions 3；validation PASS

### context-budget-and-compaction

Holdout（未抽取）：[NousResearch/hermes-agent #43547](https://github.com/NousResearch/hermes-agent/issues/43547)

- **Aider-AI/aider #3764** — substitute for seed #3493; ref `188e9e1114f0`
  - Episode: Make recursive chat-history compaction use non-mutating head selection and accurate tail accounting
  - Atomic: `select-head-within-summarizer-input-budget`, `reconcile-summary-and-tail-against-output-budget`
  - Workflow: `compact-oversized-history-with-complete-budget-accounting`
  - Evidence 10；unresolved questions 3；validation PASS
- **QwenLM/qwen-code #11894** — exact; ref `398739139261`
  - Episode: Recognize an official model alias when resolving context and output budgets
  - Atomic: `map-official-alias-to-capability-tier`, `lock-alias-budget-resolution-with-regression-coverage`
  - Workflow: `repair-resource-budget-resolution-for-an-official-alias`
  - Evidence 9；unresolved questions 3；validation PASS
- **earendil-works/pi #6647** — substitute for seed #10075; ref `65dd2e0ed6c7`
  - Episode: Retry transient compaction and branch-summary failures under the configured retry budget
  - Atomic: `retry-transient-assistant-operation-with-bounded-backoff`, `apply-retry-policy-to-context-summarization-boundaries`, `publish-summarization-retry-lifecycle`
  - Workflow: `make-context-reduction-resilient-to-transient-stream-failures`
  - Evidence 14；unresolved questions 3；validation PASS
- **google-gemini/gemini-cli #8379** — substitute for seed #27738; ref `b416508ef1c6`
  - Episode: Cap shell-tool output truncation to the remaining model context budget
  - Atomic: `bound-output-threshold-by-remaining-context`
  - Workflow: `make-tool-output-truncation-context-aware`
  - Evidence 10；unresolved questions 3；validation PASS

### state-continuity-and-resume

Holdout（未抽取）：[openai/codex #47761](https://github.com/openai/codex/issues/47761)

- **Aider-AI/aider #591** — substitute for seed #2979; ref `45b2ba8a1056`
  - Episode: Restore persisted conversation context when starting a new session
  - Atomic: `reconstruct-persisted-conversation-turns`, `restore-history-only-when-runtime-context-is-empty`, `bound-restored-history-compaction`, `signal-restored-context-to-user`
  - Workflow: `resume-persisted-conversation-with-bounded-context`
  - Evidence 10；unresolved questions 3；validation PASS
- **NousResearch/hermes-agent #228** — exact; ref `56b53bff6e42`
  - Episode: Preserve caller-owned conversation history while resuming an agent conversation
  - Atomic: `isolate-resumed-history-container`, `verify-input-and-result-history-diverge-on-extension`
  - Workflow: `resume-from-caller-state-without-transferring-container-ownership`
  - Evidence 9；unresolved questions 3；validation PASS
- **QwenLM/qwen-code #9050** — substitute for seed #9573; ref `e0b8bea9e0ba`
  - Episode: Keep cold session restoration inside the selected workspace's runtime storage context
  - Atomic: `scope-route-restore-to-selected-runtime-storage`, `scope-protocol-restore-to-selected-runtime-storage`
  - Workflow: `preserve-selected-runtime-context-across-session-restore`
  - Evidence 10；unresolved questions 3；validation PASS
- **earendil-works/pi #7707** — substitute for seed #10121; ref `a838c069e631`
  - Episode: Publish session forks and torn-tail repairs atomically
  - Atomic: `provide-atomic-file-replacement`, `publish-complete-state-atomically`, `derive-canonical-fork-mutations`, `preserve-write-continuity-after-append-failure`
  - Workflow: `make-multi-write-session-publication-crash-safe`
  - Evidence 15；unresolved questions 2；validation PASS

### structured-tool-contract-integrity

Holdout（未抽取）：[google-gemini/gemini-cli #29308](https://github.com/google-gemini/gemini-cli/issues/29308)

- **NousResearch/hermes-agent #101899** — substitute for seed #123832; ref `cf8b08edac3a`
  - Episode: Strip truncated tool-argument markup glued to a bare tool name
  - Atomic: `strip-bare-name-prefixed-tool-fragments`
  - Workflow: `repair-truncated-structured-output-sanitization`
  - Evidence 10；unresolved questions 2；validation PASS
- **QwenLM/qwen-code #4695** — exact; ref `3ce46949c213`
  - Episode: Halt repeated variants of read-only repository inspection commands
  - Atomic: `classify-read-only-inspection-variants`, `guard-consecutive-semantic-stagnation`, `propagate-typed-loop-termination`
  - Workflow: `add-a-semantic-circuit-breaker-for-variant-tool-calls`
  - Evidence 12；unresolved questions 3；validation PASS
- **earendil-works/pi #7494** — substitute for seed #10086; ref `cbaca60389f5`
  - Episode: Preserve required tool-call correlation IDs when converting versioned model histories
  - Atomic: `classify-protocol-variants-requiring-correlation-ids`
  - Workflow: `restore-structured-call-result-correlation-at-a-version-boundary`
  - Evidence 11；unresolved questions 2；validation PASS
- **openai/codex #44472** — substitute for seed #46195; ref `03f014564dee`
  - Episode: Fail closed when tool-call completeness evidence is reused, ambiguous, missing, or truncated
  - Atomic: `track-bounded-identity-evidence`, `validate-wrapper-output-associations`, `localize-budget-damage-by-cell`, `refresh-recorder-without-changing-execution`
  - Workflow: `establish-fail-closed-tool-call-completeness`, `apply-live-recorder-rollout-safely`
  - Evidence 14；unresolved questions 3；validation PASS

### effect-control-and-isolation

Holdout（未抽取）：[QwenLM/qwen-code #10859](https://github.com/QwenLM/qwen-code/issues/10859)

- **NousResearch/hermes-agent #232** — exact; ref `7166647ca132`
  - Episode: Preserve dangerous-command detection across newline-separated command fragments
  - Atomic: `make-dangerous-pattern-matching-span-line-boundaries`, `cover-multiline-bypass-families-with-regression-tests`
  - Workflow: `close-a-multiline-bypass-in-an-effect-gating-classifier`
  - Evidence 10；unresolved questions 2；validation PASS
- **earendil-works/pi #5549** — substitute for seed #9936; ref `d041b5cc354f`
  - Episode: Centralize project trust policy and isolate executable project effects
  - Atomic: `separate-passive-context-from-trust-gated-effects`, `inherit-nearest-ancestor-trust-with-explicit-overrides`, `resolve-trust-through-one-precedence-policy`, `bootstrap-trust-hooks-without-loading-project-effects`
  - Workflow: `centralize-and-enforce-project-effect-approval`
  - Evidence 17；unresolved questions 3；validation PASS
- **google-gemini/gemini-cli #25935** — substitute for seed #26004; ref `ed469e492b41`
  - Episode: Fail closed when restricted shell-command arguments cannot be parsed in automatic-approval mode
  - Atomic: `Deny restricted automatic shell authorization when parsing is invalid`
  - Workflow: `Close an automatic-approval bypass caused by uncertain command parsing`
  - Evidence 8；unresolved questions 2；validation PASS
- **openai/codex #48155** — substitute for seed #42184; ref `645b683a9e71`
  - Episode: Broaden approved-command writes without weakening explicit filesystem denials
  - Atomic: `derive-approved-policy-with-retained-denials`, `project-approved-policy-to-safe-linux-mounts`, `advertise-isolation-guarantees-as-opt-in-capabilities`
  - Workflow: `safely-broaden-filesystem-effects-for-an-approved-command`
  - Evidence 12；unresolved questions 3；validation PASS

### failure-recovery-and-streaming

Holdout（未抽取）：[earendil-works/pi #9735](https://github.com/earendil-works/pi/issues/9735)

- **NousResearch/hermes-agent #115822** — substitute for seed #121320; ref `656eb283096c`
  - Episode: Recover reasoning-only incomplete turns by failing over without leaking protocol-specific replay state
  - Atomic: `track-consecutive-nonproductive-stream-responses`, `escalate-persistent-stream-stall-to-bounded-failover`, `reconcile-turn-identity-after-midturn-failover`, `sanitize-protocol-specific-recovery-state-on-failover`
  - Workflow: `recover-a-reasoning-only-stream-stall-through-safe-failover`
  - Evidence 16；unresolved questions 3；validation PASS
- **QwenLM/qwen-code #7832** — exact; ref `d7c0d4ca7706`
  - Episode: Resume partially delivered streams after retryable socket closure without duplicating output
  - Atomic: `route transport failure by delivered semantic output`, `stage an isolated continuation request`, `fold attempt output without replayed overlap`, `restore complete durable response history`, `clear continuation state when recovery strategy is superseded`
  - Workflow: `recover a retryable mid-stream transport cut while preserving response continuity`
  - Evidence 14；unresolved questions 3；validation PASS
- **google-gemini/gemini-cli #26519** — substitute for seed #29264; ref `f5c0977e96b0`
  - Episode: Recover a streamed response after premature transport closure
  - Atomic: `Classify premature stream closure as a recoverable transport failure`
  - Workflow: `Restore streamed-response progress after a recognized premature closure`
  - Evidence 5；unresolved questions 3；validation PASS
- **openai/codex #47641** — substitute for seed #39988; ref `9d8de196748b`
  - Episode: Honor server retry advice without restarting its countdown
  - Atomic: `capture-server-retry-deadline`, `preserve-retry-deadline-across-error-transforms`, `schedule-http-retry-at-server-deadline`, `schedule-stream-retry-with-elapsed-work-accounted`
  - Workflow: `preserve-and-honor-server-retry-timing`
  - Evidence 15；unresolved questions 3；validation PASS

## 输出

- 总 inventory：`data/skill-extraction/agent-core-seven-category-extraction-v2/codex-5.6-sol-20261001/extraction-inventory.json`
- 合并后的 28 条 canonical episode：`data/skill-extraction/agent-core-seven-category-extraction-v2/codex-5.6-sol-20261001/episodes-all.json`
- 每类原始 response、prompt、bundle、stdout/stderr、validation、summary：`data/skill-extraction/agent-core-seven-category-extraction-v2/codex-5.6-sol-20261001/01-*` 至 `07-*`
- 正式 manifest：`experiments/manifests/agent-core-seven-category-extraction-v2`

## 暂缓事项

- Pattern induction
- graph storage and materialization
- BM25, embedding, and HNSW retrieval
- graph expansion
- LLM judge/use
- feedback and update/merge/retirement
- holdout agent comparison and final evaluation
