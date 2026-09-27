# Promotion Decision — Hermes independent 2026-09-26

## 总结决定

**不 promote 为 validated。** 本 run 只证明 Hermes 内部存在四个真实、可区分的修复机制，并足以提出候选 Atomic Skills、一个候选 Workflow 和一个 provisional Pattern。没有跨仓库复现、held-out benchmark、迁移成功率或独立 reviewer validation，因此所有 promotion status 都保守处理。

## Atomic Skill decision

| Candidate | 决定 | 证据 | 主要限制 |
|---|---|---|---|
| `reserve-shared-request-headroom-before-binding-a-threshold` | provisional candidate；可作为内部检索候选 | `f92006ce1...` 在 `_check_compression_model_feasibility` 直接做 tool estimate + 12K reserve + floor，并有重工具/floor tests | 只有一个直接 aux-request realization；12K 常数不是通用常数 |
| `budget-batched-results-against-recipient-residual-capacity` | provisional candidate | `35a0803a3...` 的 batch-split budget、static/dynamic min、lossless spill 和对应测试 | 证据集中在 delegation summary；尚未证明适用于任意 event/log pipeline |
| `bind-capacity-math-to-the-receiver-current-usage-provenance` | candidate, not promoted | `903b9bf18...` + `091388525...` 直接区分 session sum、aggregator current prompt、MoA folded usage、unknown，并有三项回归测试 | 需要在其他 aggregation topology 验证；不能把 current prompt assumption 当成所有 provider 的唯一真相 |
| `make-compaction-produce-reclaimable-progress` | provisional candidate | `76381e2a8...` 同时覆盖 small-window floor、summary wire cap、reasoning feedback、no-op guard 和 E2E-like unit contracts | 这是多个 compaction seam 的组合，尚未证明每个子措施都能独立迁移 |

## Workflow decision

`repair-shared-context-capacity-pressure`：**provisional within Hermes**。

批准的使用条件：

- 必须先证明 policy 和 downstream material 共享一个有限 context/capacity pool；
- 必须分支处理 provider admission、recipient fan-out、usage provenance 和 compaction progress；
- 必须同时做数值 boundary 和行为-level provider/transcript tests；
- unknown usage 不得假设为 zero；
- 单仓库证据只能停在 provisional。

拒绝的泛化：

- 不能把 display-only percentage cap、worker concurrency cap、generation race 或 search-output densification 自动纳入该 Workflow。
- 不能把 75%、12K、10K、24K、4 chars/token 等项目常数当作可迁移默认值。

## Candidate Pattern（不标 validated）

### `receiver-owned residual capacity with progress-preserving admission`

**候选表述**：

> 在任何会把材料送入有限 context 的 pressure/compression path 中，先确定接收方与其 current usage provenance，再从同一 capacity pool 扣除 mandatory request/output material；对 batch 结果按 recipient residual capacity 分摊；未知 usage 走保守静态 ceiling；若用 compaction 解压，必须证明压缩后仍有可回收 middle，并保留显式意图与 required atomic groups。

**为什么有足够证据提出但不足以验证**：

- Case 1：raw threshold 没扣 system/tools/flush overhead 会在 provider boundary 400；
- Case 2：N 个 summary 的总和而不是单项大小决定 parent overflow；
- Case 3：同一个公式若使用 session sum、MoA foreign usage 或 unknown=0，仍然会错；
- Case 4：即使 admission 没超，如果 compaction 没有 progress，系统会 thrash。

这四个案例构成相互补充的机制链，但全都来自 Hermes，不能声称 Pattern 已跨代码库/架构验证。

## 重复与互补决定

- 现有 `data/skill-extraction/agent-runs/hermes/` 已有 `623b21bf...`、`4252aecc...`、`b7803a17...`、`af0be164...` 等 residual-capacity/threshold derivation 案例。本 run 不重复其 SHA、文件和结论。
- 本 run 选择互补案例：aux system/tool request headroom、delegation batch spill、usage provenance、anti-thrashing progress。它们共享语义族，但每个有不同 owner、consumer、call point 和 test oracle。
- `15cfd208...` 被列为排除：它主要修 display/measurement signal contract；`c68091c04`/`40051c2a1`/`3f7e0fd07` 被列为排除：它们修 concurrency/generation ownership；`6e369a376...` 被列为排除：它是 worker scheduler capacity。

## 后续验证建议（不是本 run 已完成的结论）

1. 在第二个 agent/runtime 仓库寻找同样的 receiver-owned residual capacity + unknown fallback + progress oracle。
2. 用 synthetic held-out cases 分离四个子技能，测试是否能预测 bug location/required invariant，而不是只复述 commit message。
3. 对 spill/readback、MoA/aggregator provenance 和 model-switch rederivation 做跨实现测试。
4. 只有跨仓库 + held-out 结果达到预设门槛后，才考虑把 Candidate Pattern 标为 validated。
