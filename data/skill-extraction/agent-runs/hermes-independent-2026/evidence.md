# Hermes Agent 独立证据集：compaction / context pressure / shared capacity

- **独立性**：本 run 只在 `hermes-agent` 工作树内用 Git 直接读取 `commit^`、`commit`、diff、调用点和测试；没有调用或询问其他 agent，也没有把别的 run 的结论当作本 run 的证据。
- **仓库**：`https://github.com/NousResearch/hermes-agent.git`
- **分析基线**：工作树 `main`，HEAD `9a6108fdf`（截至 2026-09-26）；历史 commit 可能已经把旧的根级 `run_agent.py`/`tests/` 路径迁移或从物理 checkout 中移走，所以测试证据以相应真实 commit 中的测试 diff 和测试名称为准。
- **选择标准**：保留同一个语义族“有限 context 容量下，在真正的 provider/tool/summary 边界之前保留可用 headroom，并让 compaction 有进展”，但区分四个机制：aux 请求固定开销、batch fan-out 输出、headroom 测量来源、compaction 进展/重复触发。
- **没有把单仓库结果标成 validated**：下述 Atomic Skill/Pattern/Workflow 都是 candidate/provisional；没有跨仓库、held-out 或线上成功率验证。

## Case 1 — auxiliary compression request 的 system/tool 开销必须从 aux capacity 中预留

### 识别信息

- 完整 SHA：`f92006ce1cda1a40249fa4d5dd9c663f70a9de8d`
- parent：`b35d692f45d5f8c4d2ba567a64daa38ebba96a1a`
- 日期：2026-04-25
- subject：`fix(compression): reserve system+tools headroom when aux binds threshold (#15631)`
- 修改文件：
  - `run_agent.py`
  - `tests/run_agent/test_compression_feasibility.py`

### Before / after 代码证据

在 `AIAgent._check_compression_model_feasibility()` 中，旧逻辑在 auxiliary context 小于当前主模型 threshold 时直接把 threshold 降到 aux window：

```python
# before
old_threshold = threshold
new_threshold = aux_context
self.context_compressor.threshold_tokens = new_threshold
```

该值只约束 raw message tokens，但 compression summarizer 和 `flush_memories` 的实际请求还会带 system prompt、tool schemas、flush instruction。after diff 新增：

```python
# after
from agent.model_metadata import estimate_request_tokens_rough
tool_overhead = estimate_request_tokens_rough([], tools=self.tools)
headroom = tool_overhead + 12_000
old_threshold = threshold
new_threshold = max(aux_context - headroom, MINIMUM_CONTEXT_LENGTH)
self.context_compressor.threshold_tokens = new_threshold
```

这不是一般性的“把阈值调小”：它把同一 aux window 中的 mandatory request overhead 作为共享容量保留项，并保留 `MINIMUM_CONTEXT_LENGTH` floor。commit message 说明真实故障是 50+ tools 带来约 25–30K token overhead，raw messages 充满 aux window 后，compression/flush 请求以 HTTP 400 溢出。

### 调用点与状态传播

- 入口/决策点：`AIAgent._check_compression_model_feasibility()`。
- 它在 agent 初始化时做 feasibility check；测试还覆盖第一次 `run_conversation` 时把缓存的 `_compression_warning` 通过 `status_callback` replay 给 gateway。
- 决策读取 `self.tools`，调用 `agent.model_metadata.estimate_request_tokens_rough`，写入 `self.context_compressor.threshold_tokens`，并同步 threshold percent，使后续 main-model context 变化可重新推导。
- 被保护的实际 downstream consumers：auxiliary compression summarizer 以及 `flush_memories`（commit message 与文件注释均明确提到）。

### 测试证据

`tests/run_agent/test_compression_feasibility.py` 在同一 commit 中新增/更新：

- `test_auto_lowered_threshold_reserves_headroom_for_tools_and_system`：50 个 fat tool schemas，断言新 threshold **严格小于** 128,000 aux context，并且不低于 `MINIMUM_CONTEXT_LENGTH`。
- `test_headroom_floors_at_minimum_context`：headroom subtraction 会把值推到 floor 以下时，断言结果仍等于 `MINIMUM_CONTEXT_LENGTH`，session 不因负/过小 threshold 启动失败。
- 原有断言由 `80_000 -> 68_000`、`99_999 -> 87_999`，证明 empty-tools 也包含 12K 静态 headroom，而不是只在工具很多时生效。
- 同文件还保留 aux provider 不存在、aux 小于 hard floor、精确边界无 warning、禁用 compression 不检查、异常不阻塞 startup、init 与 `run_conversation` replay 的回归覆盖。

### 语义边界

- 与 Case 2 的区别：这里预算的是**aux provider 单次请求的输入组成**；没有 batch fan-out，也没有丢弃/外溢 summary。
- 与 Case 4 的区别：这里不改变 compaction 频率或 summary 生成质量，只在 aux threshold binding 时先留出 provider admission headroom。

## Case 2 — delegation batch 的多个子 agent 结果按父 context 的剩余容量分摊，并 lossless spill

### 识别信息

- 完整 SHA：`35a0803a3b64a0b43e49dbbc809c4986be3ae331`
- parent：`3b2bb30c5d46017f2654d5836fadd99776e1aadc`
- 日期：2026-06-30
- subject：`fix(delegation): budget subagent summaries against parent context headroom`
- 相关问题/PR 证据：新增测试模块 docstring 直接标记 `PR #9126`；commit message 描述 fan-out 后的 compression/429 death spiral。
- 修改文件：
  - `hermes_cli/config.py`
  - `scripts/release.py`
  - `tests/tools/test_delegate_summary_budget.py`
  - `tools/credential_files.py`
  - `tools/delegate_tool.py`

### Before / after 代码证据

before 的行为是把每个 child 的完整 `final_response` 原样放回 parent；没有按 batch 总量测算 parent 的剩余 window，也没有 spill。after 在 `tools/delegate_tool.py` 的 `delegate_task()` 中，在结果排序后、把结果通知 memory/parent 之前插入：

```python
# after call site
results.sort(key=lambda r: r["task_index"])
_apply_summary_budget(results, parent_agent)
```

`_parent_summary_char_budget()` 的核心 before/after 机制是：

```python
# after: shared parent capacity, split across N summaries
headroom_tokens = context_length - int(used_tokens) - int(reserved)
batch_token_budget = int(headroom_tokens * _SUMMARY_HEADROOM_FRACTION)
per_summary_tokens = batch_token_budget // max(1, n_summaries)
per_summary_chars = per_summary_tokens * 4
return max(_MIN_SUMMARY_CHARS, per_summary_chars)
```

有效 cap 是 dynamic headroom budget 和配置 `delegation.max_summary_chars` 的 min。超 cap 时 `_trim_summary_with_footer()` 把全文写入 `~/.hermes/cache/delegation/`（经 `tools/credential_files.py` 的 `_CACHE_DIRS` 机制可挂载到 remote backend），in-context 只留 head+tail、line-snapped footer 和精确 `read_file` offset。`hermes_cli/config.py` 新增默认 `max_summary_chars: 24000`，0 可关闭静态 ceiling，但 dynamic parent headroom 仍然生效。

### 调用点与调用链

`delegate_task()` 的 single-task 和 batch 两条路径最终都先构造 `results`，再调用 `_apply_summary_budget(results, parent_agent)`；因此不是只修 batch caller。`_apply_summary_budget()` 读取 parent 的 `context_compressor.context_length/max_tokens`，遍历 summary 字段，必要时调用 `_trim_summary_with_footer()`，再让修改后的 result 进入 parent context。

### 测试证据

新增 `tests/tools/test_delegate_summary_budget.py`，关键测试：

- `test_small_summaries_pass_through_untouched`：短结果不被无谓重写。
- `test_batch_overflow_trimmed_and_spilled_losslessly`：parent 近满时，验证 head marker、tail marker 和 spill 文件，证明可迁移但不丢信息。
- `test_dynamic_budget_shrinks_as_batch_grows`：N 增大时 per-summary budget 变小，验证共享容量而非 per-child magic char limit。
- `test_floor_enforced_when_parent_over_budget`：已超预算时仍有 `_MIN_SUMMARY_CHARS` floor。
- `test_unknown_context_falls_back_to_static_ceiling` 与 `test_disabled_static_ceiling_and_unknown_context_leaves_summary_intact`：未知 parent 状态不凭空制造动态容量。
- `test_empty_results_is_noop`：无 summary 的结果不改变。

### 语义边界

- 这里的 mandatory consumer 是**即将注入 parent context 的 N 个 child outputs**，不是 provider system/tool schemas。
- 处理策略是“动态压缩 in-context 表示 + lossless 外存”，不是删掉 child 结果，也不是让 provider 失败后 retry。

## Case 3 — parent summary budget 必须使用 aggregator 当前 prompt 的真实 provenance，而非 session 累加或 MoA folded usage

### 识别信息

这是一个有明确因果链的 follow-up case，包含两个真实 sequential commits：

- 基线修复：`903b9bf1873fa52daf9d0000c83ac7ffeb28fc4a`，parent `b51c055a12220f8c7c18660e8599365012e19532`，2026-09-05，subject：`fix(delegate): nested orchestrators get their workers' results back — no 420 s deadline on delegate_task, summary budget uses the current prompt not the session sum`
- 独立 review follow-up：`09138852500bc02062008a565942c0c9176b2fc3`，parent `903b9bf1873fa52daf9d0000c83ac7ffeb28fc4a`，2026-09-05，subject：`fix(delegation): summary headroom uses the aggregator's own prompt size; unknown usage means the static ceiling, never zero context`
- 修改文件（合并列出）：
  - `agent/tool_executor.py`（仅本 case 的相邻 deadline 子修复）
  - `agent/turn_usage.py`
  - `tools/delegate_tool_results.py`
  - `tests/agent/test_sequential_deadline_delegate_exempt.py`（相邻 deadline 子修复）
  - `tests/tools/test_delegate_summary_budget.py`

### Before / after 代码证据

903 的问题描述给出真实运行观测：父 session 用 `session_prompt_tokens`（所有 API call 的 prompt token **累计和**）计算 headroom；长 session 后它超过 window，1,393 个 child summary 全部被压到 2,000-char floor，orchestrator 只能基于 stubs 规划。after 将预算来源改为最后一次 prompt 的 usage。

091 又发现两个 provenance holes。旧逻辑对没有 usage row 的 parent 把 unknown 当作 `0`，会让 190K/200K parent 获得约 384K-char 动态预算；同时 MoA folded usage 包含 advisor prompts，而这些并不在 aggregator parent context。after 在 `agent/turn_usage.py` 的 `record_response_usage()` 记录：

```python
agent._last_prompt_size_tokens = int(aggregator_usage.prompt_tokens or 0)
```

`tools/delegate_tool_results.py` 新增 `_parent_prompt_size_tokens()`：

```python
size = getattr(parent_agent, "_last_prompt_size_tokens", None)
if isinstance(size, (int, float)) and size > 0:
    return int(size)
last_usage = getattr(parent_agent, "_last_turn_usage", None) or {}
used = last_usage.get("prompt_tokens") if isinstance(last_usage, dict) else None
if isinstance(used, (int, float)) and used > 0:
    return int(used)
return None
```

`_parent_summary_char_budget()` 在 `None` 时返回 `None`，caller 只使用 static ceiling；只有 known current prompt 才执行 `context_length - current_prompt - max_tokens` 的 dynamic calculation。这样把“没有观测到容量”与“观测到 0 tokens”区分开，也不把 MoA advisor 的 tokens 算进 aggregator 的 context。

### 调用点与调用链

- provider response usage → `record_response_usage()` → `_last_prompt_size_tokens`。
- `delegate_task()` → `_apply_summary_budget()` → `_parent_summary_char_budget()` → `_parent_prompt_size_tokens()`。
- `agent/tool_executor.py` 同 commit 另把 nested `delegate_task` 从 generic sequential deadline 排除；这是相邻的 liveness fix，不把它当成 context-capacity机制本身。

### 测试证据

- `tests/tools/test_delegate_summary_budget.py::test_budget_uses_current_prompt_size_not_the_session_sum`：长-lived parent 的 session sum = 25,000,000、current prompt = 30,000 时，budget 与 fresh parent 相同且高于 floor。
- `::test_unknown_parent_usage_means_static_ceiling_not_zero_context`：`_parent_summary_char_budget(...) is None`。
- `::test_moa_fold_does_not_inflate_the_parents_prompt_size`：folded parent 的 advisor 190K + aggregator 50K 与 unfolded 50K 得到相同 budget。
- 相邻 liveness tests：`test_delegate_task_is_exempt_from_the_sequential_deadline`、`test_exemption_is_narrow`，证明 deadline exemption 是窄集，而非全局关闭 timeout。

### 语义边界

- 与 Case 2 的区别：Case 2 首次引入“按 batch 共享 parent headroom + spill”；Case 3 修的是**budget measurement provenance**，即“到底哪一个 token 计数代表接收方 context”。
- 与 Case 1 的区别：这里没有 system/tool 固定 overhead 估算，容量测量来自真实 provider usage 和 aggregator identity。

## Case 4 — 小 context 的 compaction thrash：提高触发 floor、去掉 summary wire cap、排除 reasoning trace

### 识别信息

- 完整 SHA：`76381e2a8e3a21fbbd0a192b4b5f7356a7ca47b8`
- parent：`8e734810dfcb4f19eac2f442cb75b3962dfec728`
- 日期：2026-07-08
- subject：`fix(compression): stop compaction thrash — 75% trigger floor under 512K, no summary output cap, reasoning-trace exclusion (#60989)`
- 修改文件：
  - `agent/context_compressor.py`
  - `cli-config.yaml.example`
  - `hermes_cli/config.py`
  - `tests/agent/test_compression_small_ctx_threshold_floor.py`
  - `tests/agent/test_context_compressor.py`
  - `tests/run_agent/test_infinite_compaction_loop.py`

### Before / after 代码证据

commit message 给出 before 的可复现机制：sub-512K model 默认 50% trigger；system prompt、tool schemas、protected tail、rolling summary 等 incompressible floor 吃掉回收空间，compaction 每 1–2 turns 重复。

after 在 `ContextCompressor._effective_threshold_percent()` 中新增 raise-only floor：

```python
if context_length and context_length < _SMALL_CTX_WINDOW_LIMIT:
    return max(threshold_percent, _SMALL_CTX_THRESHOLD_PERCENT)
return threshold_percent
```

常量为 `_SMALL_CTX_WINDOW_LIMIT = 512_000`、`_SMALL_CTX_THRESHOLD_PERCENT = 0.75`；`__init__` 和 `update_model()` 都从 `_configured_threshold_percent` 重新推导，small→large 能退回配置值，large→small 会重新获得 floor。高于 75% 的显式用户/model threshold 不被覆盖。

同一 commit 还改了两个会破坏“压缩后有进展”的 seam：

- `_SUMMARY_TOKENS_CEILING` 从 12,000 降到 10,000；summary call 不再把 `max_tokens` 作为 wire hard cap 发送，避免 Anthropic/NIM thinking model 把 cap 消耗在 reasoning 后截断摘要。
- inline `<think>/<reasoning>` 在送给 summarizer 前剥离，summarizer 输出在存入 `_previous_summary` 前也剥离；否则 trace 会随 iterative summary 每轮再喂回，造成摘要膨胀。

### 调用点与调用链

- `ContextCompressor.__init__()`：解析 context length/config threshold，保存 configured percent，调用 `_effective_threshold_percent()`，再计算 `threshold_tokens`。
- `ContextCompressor.update_model()`：模型/provider/context window 改变时重新推导 threshold 与 budgets。
- `ContextCompressor.should_compress()`：用 threshold 和 `last_prompt_tokens` 决定是否进入压缩。
- `ContextCompressor.compress()` → summary serializer/LLM call → `_previous_summary`；上述 cap/trace 修复位于这条实际压缩路径，而不是只改 display。
- `tests/run_agent/test_infinite_compaction_loop.py` 还验证 `_ineffective_compression_count`：连续两次 no-op 后 `should_compress()` 返回 false，防止同一无效动作每 turn 重入。

### 测试证据

`tests/agent/test_compression_small_ctx_threshold_floor.py` 新增/覆盖：

- `test_sub_512k_floors_to_75_percent`
- `test_512k_and_above_keep_configured_percent`
- `test_raise_only_higher_config_wins`
- `test_update_model_rederives_floor_both_directions`
- inline/native reasoning exclusion 和 summarizer output stripping 的四项测试
- `test_no_max_tokens_wire_cap_on_summary_call`
- `test_budget_capped_at_10k_even_on_1m_window`
- tail budget proportion、1K–10K envelope

`tests/run_agent/test_infinite_compaction_loop.py` 覆盖 no-op counter、有效压缩重置 counter、cooldown guard、small conversation 仍有 non-trivial compressible middle；`tests/agent/test_context_compressor.py` 继续覆盖 threshold、max_tokens reservation、small/large model 和 update_model。

### 语义边界

- 与 Case 1 的区别：Case 1 是“aux request 能否装下”的 admission arithmetic；这里是“压缩完成后是否真的释放出足够空间、下一轮不会马上重压”的 progress/liveness。
- 与 Case 2/3 的区别：这里不处理 delegation outputs 的接收容量或 token provenance；核心是 compressor 内部的 trigger、summary wire behavior 和 recursive trace。

## 已排除的相似但机制不同案例

1. **`15cfd2082083099bff7e6d7f61544f802ad06170` / `#3480` — display pressure cap + real usage estimator**
   - 修改 `agent/display.py`、`run_agent.py`、`tests/test_context_pressure.py`。
   - `format_context_pressure*()` 只把显示百分比 `min(int(progress*100),100)` 封顶；`run_agent.py` 还把 rough chars/3 改为 provider `prompt_tokens + completion_tokens`。
   - 它的主要 contract 是 UI 不显示 109% 和 telemetry/decision signal 更真实，不是为 provider request 预留 mandatory capacity，也不是让 summary batch 能装下；故作为排除项而非 Case。
2. **已有 `arex-skill-graph/.../agent-runs/hermes` 中的 residual-capacity 案例**
   - 本 run 检查到已有 run 选择了 `623b21bf...`（output token reservation）、`4252aecc...`（implicit threshold floor）、`b7803a17...`（retained-tail share）、`af0be164...`（single trigger derivation）。
   - 这些不是本 run 的证据来源；为避免完全重复，本 run 不复述同一 SHA/同一 before/after。互补选择了本仓库另一组机制：aux system/tool headroom（Case 1）、delegation fan-out/spill（Case 2）、usage provenance（Case 3）、anti-thrashing progress（Case 4）。概念上都与容量压力相邻，但代码位置、consumer 和 oracle 不同。
3. **`c68091c04`、`40051c2a1`、`3f7e0fd07` — stale generation / held-watermark / concurrent compression race**
   - 这些 commit 修的是并发所有权、代次和 publication no-op；即使都叫 compression，也不是 shared capacity arithmetic，故排除。
4. **`6e369a37622be1785c94640663752cdb655a1f2a` / `#56955` — delegation concurrency cap**
   - `max_concurrent_children` 统一 batch/background worker 并发容量；它是 worker scheduler capacity，不是 model context capacity，排除。
5. **`22b6942fc2fb00d44f4f7c77d85c2a7ce144845c` / `#47866` — search_files lossless densification**
   - 通过改变工具输出表示降低 token 数；没有 context-pressure threshold/headroom contract，不能冒充本族案例。
6. **`b29ee6a6501eb3568d943ce760f271fd93bd5ba9` — desktop E2E test payload margin**
   - 它提高 fixture payload，避免 ambient prompt 漂移导致测试没有跨过 threshold；是测试稳定性/触发 margin 修复，不是 runtime capacity policy。

## 证据强度与限制

- **强证据**：每个入选案例都能从真实 `commit^ -> commit` diff 看到 changed code，且同一 commit 有新增/更新测试；Case 3 还由连续 follow-up 的真实 regression tests 证明初版 measurement holes 被修正。
- **调用链证据**：通过函数名和 diff call site 追踪了 decision seam 到 caller/provider-facing path，而不是只根据 commit subject 做主题聚类。
- **限制**：本 run 没有把四个历史 commit cherry-pick 到当前 HEAD 重跑完整 upstream suite；当前 HEAD 的目录布局与选定历史测试路径不完全一致，故不声称运行时验证或跨仓库验证。测试证据仍然是真实提交中的测试代码和断言。
