# 候选 Atomic Skills（Hermes 独立 run）

这些不是 commit 摘要，而是从四个真实案例抽象出的“小问题 + 可迁移解决范式”。全部仅为 **candidate/provisional**：单仓库证据不足以标记 validated。

## A1 — `reserve-shared-request-headroom-before-binding-a-threshold`

**小问题**：一个输入/历史 threshold 使用 nominal context window，但真正的 provider 请求还会强制携带 system prompt、tool schemas、flush instructions 或其他不可选 payload，导致 threshold 到达后请求才溢出。

**可迁移范式**：
1. 找到同一有限 capacity pool 的所有 mandatory consumers，不只看当前列表中的 message tokens。
2. 在决策边界规范化每个 reservation（实际估计 + 保守静态 reserve）。
3. 以 `residual = nominal_window - mandatory_reservations` 计算 threshold。
4. 对 residual 做明确 floor/degenerate handling，避免负值或把 session 变成不可启动。
5. 在 active model/aux provider/tools 变化时重算，并写测试覆盖空工具、重工具和 floor binding。

**实现 oracle**：threshold 严格小于 aux capacity（当 overhead 非零），同时不低于 minimum；实际 summarizer/flush request 不再因遗漏固定开销而 400。

**直接证据**：`f92006ce1cda1a40249fa4d5dd9c663f70a9de8d` 的 `_check_compression_model_feasibility()`、`estimate_request_tokens_rough([], tools=self.tools)`、`test_auto_lowered_threshold_reserves_headroom_for_tools_and_system`。

**边界**：不要把所有输出都当作 reservation；只有真正共享 provider context/admission pool 的消费者才适用。不要用这个 skill 解决 stale-generation race 或 summary content refusal。

## A2 — `budget-batched-results-against-recipient-residual-capacity`

**小问题**：N 个 worker/child 的结果各自看起来合法，但同时进入一个 recipient context 后总量超限。

**可迁移范式**：
1. 在结果注入 recipient 前统一拦截，而不是依赖每个 child 自己“尽量简短”。
2. 计算 recipient 的已用 prompt、输出 reserve 和剩余 capacity。
3. 按 batch size 分摊动态 budget，再与静态单项 ceiling 取 min。
4. 超预算时保留可读 head+tail/关键边界，完整内容写入可寻址外存并返回精确读取指针。
5. 未知 capacity 时用静态安全 ceiling；空结果、短结果和 over-budget parent 都有明确分支。

**实现 oracle**：batch 增大时单项 cap 减小；short result byte-for-byte pass-through；trim 后 head/tail 可见、full spill 可 `read_file` 恢复；recipient 不因 fan-out 进入 compression/429 death spiral。

**直接证据**：`35a0803a3b64a0b43e49dbbc809c4986be3ae331` 的 `_apply_summary_budget()`、`_parent_summary_char_budget()`、`_trim_summary_with_footer()` 及 `test_batch_overflow_trimmed_and_spilled_losslessly`。

**边界**：这是“接收方上下文容量” skill，不是并发 worker 数量 cap，也不是对所有文本做无损 densification；spill 必须是可寻址且对 remote backend 可用的。

## A3 — `bind-capacity-math-to-the-receiver-current-usage-provenance`

**小问题**：容量公式本身没有错，但 used tokens 来自 session 累加、别的 aggregator/advisor 或“未知被当成 0”，于是动态 budget 不是接收方当前 context 的真实剩余容量。

**可迁移范式**：
1. 明确 budget 的 owner/receiver identity。
2. 在 provider usage 记录点保存该 receiver 的 current prompt（必要时保存 pre-fold/pre-aggregation 值）。
3. 将 cumulative accounting 与 current-prompt accounting 分离命名、分离字段。
4. unknown、zero、negative、foreign aggregate 不要静默等价；unknown 应降级到静态 ceiling 或显式保守分支。
5. 用 fresh parent vs long-lived parent、folded vs unfolded parent、no-usage parent 做等价性/不等价性测试。

**实现 oracle**：相同 current prompt 的 fresh/long-lived parents 得到相同 budget；MoA advisor tokens 不改变 aggregator budget；unknown 不产生虚假的巨大 dynamic budget。

**直接证据**：`903b9bf1873fa52daf9d0000c83ac7ffeb28fc4a` 与 `09138852500bc02062008a565942c0c9176b2fc3` 的 `_last_prompt_size_tokens`、`_parent_prompt_size_tokens()`，以及三项 provenance tests。

**边界**：这不自动解决 provider usage 缺失；它只要求“缺失时不要伪装成 zero”。需要额外决定 static ceiling、拒绝或其他 fallback。

## A4 — `make-compaction-produce-reclaimable-progress`

**小问题**：compaction 虽然被触发，但不可压缩 floor、summary wire cap、reasoning trace feedback 或 no-op cut 使得压缩后仍接近原大小，下一两个 turn 又立即 compaction。

**可迁移范式**：
1. 先测量 compaction 前后真正可回收的 middle，而不是只看触发阈值。
2. 对小 window 提高隐式 trigger floor时只 raise-only，不覆盖更高显式用户意图；在 model/window switch 时重新推导。
3. 对 summary 生成区分 prompt guidance 与 provider wire hard cap，避免 thinking output 被 cap 截断。
4. 去掉会递归进入下一轮 summary 的 reasoning trace；保持 summary 内容契约。
5. 对 no-op compression 计数/冷却，达到 guard 后停止无效重试，并测试仍能找到 non-trivial compressible middle。

**实现 oracle**：小 window 触发较晚但不会被压缩 thrash；summary call 无不当 wire cap；有效压缩重置 no-op counter；连续 no-op 不会每 turn 重入。

**直接证据**：`76381e2a8e3a21fbbd0a192b4b5f7356a7ca47b8` 的 `_effective_threshold_percent()`、summary serializer/output stripping、`tests/run_agent/test_infinite_compaction_loop.py`。

**边界**：它是 progress/liveness skill，不可替换 Case 1 的 provider admission reservation；触发阈值是否“准确”与压缩后是否“有进展”是两个 oracle。

## 不能从本 run 单独提升为 Atomic Skill 的相邻想法

- **display-only pressure normalization**：`15cfd208...` 的 `min(pct, 100)` 解决 UI contract，不足以形成容量治理 skill。
- **generic concurrency capacity**：`6e369a376...` 的 worker cap 与 model context pool 不同。
- **stale-generation / ownership arbitration**：`c68091c04`、`40051c2a1`、`3f7e0fd07` 是并发 publication invariants，不是 residual capacity。
