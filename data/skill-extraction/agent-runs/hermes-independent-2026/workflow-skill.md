# Workflow Skill（候选）：`repair-shared-context-capacity-pressure`

> **状态**：provisional / Hermes-only candidate；不是 validated workflow，也不是默认顶层 Skill。

## 适用的小问题

当系统同时出现以下任一现象时使用：

- compaction threshold 到了，但 auxiliary/provider request 仍因 system/tools/required output 溢出；
- 一次 fan-out 的 N 个结果单项都合理，合并后把 parent context 推爆；
- budget 用了 session 累计、foreign aggregate 或把 unknown 当 zero；
- compaction 频繁触发但压缩后没有可回收 middle，summary 反复膨胀或立即再压缩。

## 不适用

- 只是 UI 百分比显示错误（例如 109% 显示为 100%）；
- 只是 stale generation、锁、publication ownership 或并发 winner/loser；
- 只是 worker 并发数/队列容量，而非 model context capacity；
- 没有证据表明 upstream policy 与 downstream material 共享同一有限 capacity pool。

## 条件 DAG

```text
W0. 收集真实 before/after、调用链、provider boundary 和测试
 ├─ 没有共享 context pool / 只是 display -> STOP，转 observability 或 scheduler workflow
 └─ 有共享 pool -> W1

W1. 定义 capacity owner 和单位
 ├─ aux provider request -> W2
 ├─ parent recipient + N child results -> W3
 └─ compressor 自己压缩 -> W4

W2. 枚举 mandatory request material [A1]
 ├─ system/tools/flush/required output 未计入 -> 规范化并计算 residual
 ├─ residual <= minimum -> 安全 floor / 明确拒绝，不能静默装一个负 threshold
 └─ residual 可用 -> threshold 安装 + provider-facing regression test

W3. 先测 recipient current usage，再按 batch 分摊 [A2, A3]
 ├─ usage unknown -> static ceiling only；不要当作 0
 ├─ usage cumulative/foreign -> 换成 owner current prompt provenance
 └─ usage known -> residual - output reserve，再除以 N，超出则 head+tail + lossless spill

W4. 验证压缩是否有实际 reclaimable progress [A4]
 ├─ trigger 太早且小 window -> raise-only implicit floor，显式更高值优先
 ├─ summary wire cap 截断 thinking -> 只保留 prompt guidance，不发错误 hard cap
 ├─ reasoning trace 被再喂回 -> serialize/store 前剥离
 └─ no-op -> 计数/冷却并阻止无效重入，同时证明仍有 non-trivial middle

W5. 做 boundary + behavior 双层验证
 ├─ numeric boundary: empty/large tools, batch N=1/N>1, floor, unknown, folded
 ├─ behavior: provider request fits, parent transcript fits, spill recoverable
 └─ no cross-repo evidence -> STOP at provisional; 不得标 validated
```

## 步骤说明与 Case Action 映射

### W0 — 事实核查

- 用 `git show <sha>^:<file>` 和 `git show <sha>:<file>` 记录 exact before/after，而不是只读 commit subject。
- 找 decision seam、caller、provider/tool entry、state write-back 和测试。
- 把“同一语义族”与“同一机制”分开：本 run 的四个 Case Action 不应合并成一个泛化的“压缩修复”。

### W1/W2 — 共享容量与 mandatory reservation

- 适用于 Case 1。
- 计算 `residual = nominal_context - tool_overhead - system/flush_reserve`。
- 以 `max(residual, MINIMUM_CONTEXT_LENGTH)` 或明确的拒绝策略安装；要同时检查 warning/replay 与实际 provider call。

### W3 — 接收方 batch admission

- 适用于 Case 2。
- 计算 `context_length - current_prompt - output_reserve`，将 batch 可用预算按 N 分摊。
- dynamic cap 和 static ceiling 取 min；超过后保留 head/tail，全文 spill，并把精确读取位置返回 parent。

### W3 的 provenance 分支

- 适用于 Case 3。
- owner 必须是接收结果的 aggregator；保存 pre-fold/current prompt usage。
- `unknown != 0`；如果没有已完成 usage row，则 dynamic budget 返回 `None`，只走 static ceiling。
- 用 long-lived/fresh 和 folded/unfolded 对照测试，确认 session accounting 不污染 current context accounting。

### W4 — 压缩进展

- 适用于 Case 4。
- 小 context 的 implicit floor 只能 raise-only；切换到大 window 时应回到 configured percentage，切回小 window 时重新加 floor。
- summary 输出要有可控 envelope，但不能用 provider hard cap 把 thinking 结果切断；清除会被递归再注入的 reasoning trace。
- no-op compression 要产生 guard，避免在没有可压缩 middle 时无休止重入。

### W5 — 验证和停止条件

必须至少有：

1. **公式 partition tests**：无 reservation、reservation、floor、N batch、unknown usage、MoA folded usage；
2. **调用链 tests**：安装值真的被 downstream caller 读取；warning/状态 replay 不泄漏 stale value；
3. **行为 tests**：request/parent transcript 不溢出；spill 可读；summary 后有实际 reclaim；
4. **意图保留 tests**：显式用户阈值不被隐式 floor 覆盖；required atomic units 不被切碎；
5. **promotion gate**：若只有 Hermes 单仓库案例，输出 `provisional`，不得输出 `validated`。

## 失败模式 / 防误用

- 只减 `context_length` 却没有列出实际 reservation，可能 double-subtract 或漏掉最重的 tool schema。
- 只给每个 child 一个 magic char cap，没有按 recipient remaining headroom 和 N batch 分配。
- 用 `session_prompt_tokens` 代替 current prompt，把长期累加误认为当前 context。
- 处理 unknown usage 为 0，产生虚假的巨大 budget。
- 为了“防压缩”无条件把显式阈值降低，破坏用户意图。
- 修 UI 百分比而没有修 provider-facing admission；这不是同一个 Workflow。
- 将并发 race 的 generation token 当作容量 headroom；两者需要不同的 invariants。

## 可迁移解法摘要

> **先识别 capacity owner，再识别同池 mandatory consumers；对已知 current usage 计算 residual，并在真正的 provider/transcript boundary 前执行 admission。若压缩是解决方案，还要验证压缩后确有 reclaimable progress；未知状态走保守 fallback，显式意图和 required atomic groups 优先。**
