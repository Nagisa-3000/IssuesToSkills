# Tree-oriented Skill hierarchy v1

状态：采用中的语义组织规范（2026-09-27）

## 1. 核心组织

Skill 知识层以树形视图组织：

```text
Pattern
└── Workflow Skill
    ├── Atomic Skill
    ├── Atomic Skill
    └── Atomic Skill
```

当前 residual-budget family 的 canonical tree：

```text
pattern:residual-budget-invariant
└── workflow:repair-shared-capacity-pressure
    ├── atomic:derive-policy-from-residual-capacity
    ├── atomic:normalize-capacity-reservation-boundaries
    └── atomic:replay-capacity-policy-across-reconfiguration
```

较窄、尚未进入 canonical workflow 的候选 Atomic 保留在候选池：

```text
atomic:derive-auxiliary-output-cap-from-headroom
atomic:place-pressure-check-at-next-request-boundary
atomic:account-for-all-context-visible-artifacts
```

它们不能因为词汇相似就自动挂入主树；只有经过机制对齐和 Workflow 需要判断后才进入某个分支。

## 2. 树边的语义

主树只使用三种层级关系：

```text
Pattern --abstracts--> Workflow Skill
Workflow Skill --contains/uses--> Atomic Skill
Atomic Skill --leaf-of--> Workflow Skill
```

为了便于树遍历，存储时推荐规范化为父子方向：

```text
parent_id -> child_id
```

因此：

- Pattern 是高层策略抽象；
- Workflow 是一个任务目标的可执行编排；
- Atomic 是最小可迁移解决算子，也是知识树叶子节点。

## 3. 严格树与复用

语义上同一个 Atomic 可能被多个 Workflow 复用，这会使真实关系成为 DAG，而不是严格树。为了同时满足“树形组织”和“共享复用”：

1. **展示/检索主视图**使用 canonical tree。每个树节点有一个 `parent_id`。
2. **语义存储**保留共享关系。复用使用 `reuses`/`uses` 边，而不是复制 Atomic 的内容。
3. 如果一个 Atomic 必须出现在多个树分支，其他位置使用 alias：

```json
{
  "id": "alias:workflow-b:atomic-x",
  "node_type": "atomic_alias",
  "canonical_id": "atomic:atomic-x",
  "parent_id": "workflow:workflow-b"
}
```

这样 UI 和目录仍然是一棵树，真正的知识节点仍然只有一个，避免内容分叉和版本不一致。

## 4. 不进入主树的对象

Evidence、Case Action、Case Workflow、Project Binding 不作为 Pattern/Workflow/Atomic 的树层：

```text
Pattern
└── Workflow
    └── Atomic

Evidence ─grounds→ Case Action ─part_of→ Case Workflow
Case Action ─realizes→ Atomic
Case Workflow ─realizes→ Workflow
Project Binding ─binds→ Workflow/Atomic roles
```

这些是 provenance 和运行时绑定关系，属于侧边关系，不应破坏用户看到的三层 Skill 树。

## 5. 节点内容边界

### Pattern 节点

Pattern 放：

- 因果机制；
- 适用条件；
- 变体选择；
- trade-off；
- 替代策略；
- 反例；
- 支持它的 Workflow；
- held-out transfer 和晋级状态。

Pattern 不放具体执行步骤和仓库路径。

### Workflow 节点

Workflow 放：

- 目标和触发条件；
- 输入/输出；
- Atomic 子节点；
- 输入输出绑定；
- 条件分支；
- 重试和恢复；
- 验证计划；
- 停止条件；
- 工具/MCP 调用顺序；
- Project Binding 要求。

Workflow 是默认的可部署 Agent Skill。

### Atomic 叶子节点

Atomic 放：

- 一个小问题机制；
- 一个可迁移的解决范式；
- 参数槽；
- 前置条件和排除条件；
- 决策规则；
- 不变量；
- 验证 oracle；
- 边界分区；
- 反例；
- 真实 realization 和 evidence 引用。

Atomic 不放完整 Issue 时间线，也不绑定固定文件名和函数名。

## 6. 生命周期

```text
candidate → reviewed → validated → deprecated
```

- 一个 Case 可以产生 Atomic candidate，但不能仅凭一个 Case 宣称泛化。
- Workflow 至少要经过多个 Case 的结构对齐。
- Pattern 至少要有多个独立 Workflow/仓库 realization，并通过 held-out transfer 才能 `validated`。

当前 Pattern `pattern:residual-budget-invariant` 仍是 `provisional`，不能标记为 `validated`。

## 7. 检索顺序

树形检索按照由粗到细进行：

```text
query
  → Pattern candidates
  → Workflow candidates
  → Workflow child Atomic closure
  → applicability / exclusion filtering
  → Project Binding
  → load SKILL.md and selected references
```

不要一开始把整个树和全部 Evidence 注入上下文。在线检索可以使用 lexical/vector/HNSW/graph；LLM 只在需要语义判断或执行 Workflow 时使用。

## 8. Agent Skill package 投影

默认只将 Workflow 导出为顶层 package：

```text
repair-shared-capacity-pressure/
├── SKILL.md
├── references/atomic/*.md
├── references/pattern.md
├── references/evidence-index.md
├── scripts/
└── evals/
```

Atomic 和 Pattern 在知识树中独立存在，但默认作为 Workflow 的引用资源和 Graph 节点，不全部注册为顶层可发现 Skill。
