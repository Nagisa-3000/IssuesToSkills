# 对齐 Agent Skills 标准的三层 Skill 规格

状态：Canonical design proposal for v2  
版本：2.1.0  
日期：2026-09-26

## 1. 对标结论

OpenAI Skills、Anthropic Agent Skills 与开放 Agent Skills 规范在部署形式上高度一致：

```text
skill-name/
├── SKILL.md              # 必需：YAML frontmatter + instructions
├── references/           # 可选：按需读取的知识
├── scripts/              # 可选：可重复、确定性的操作
└── assets/               # 可选：模板与输出资源
```

共同原则：

1. `name` 和 `description` 用于发现；description 必须同时说明“做什么”和“何时使用”；
2. 完整 instructions 只在 Skill 被选择后加载；
3. references、scripts、assets 按需访问，实现 progressive disclosure；
4. Skill 应简洁、边界清晰，根据任务风险选择指令自由度；
5. 复杂任务应使用带条件和反馈回路的 workflow；
6. 应以真实任务和 eval 迭代，而不是仅验证文档格式。

外部标准没有定义 Atomic / Workflow / Pattern。本项目新增的是**语义知识本体**，同时保持可导出为标准 Agent Skill 包。

## 2. 两条正交轴，不能混淆

### 2.1 语义抽象轴

```text
Atomic Skill   = 小问题范式 + 最小可复用解决协议
Workflow Skill = 为较大目标编排 Atomic、诊断、决策和验证的 DAG
Pattern        = 解释 Workflow 为何有效、何时选择的因果策略族
```

### 2.2 渐进披露轴

```text
D1 Metadata     = name + description；总是可见，用于路由
D2 Instructions = SKILL.md body；触发后加载，用于执行
D3 Resources    = references/scripts/assets；仅在需要时加载或运行
```

一个语义层可以投影到多个披露层。例如 Workflow 的触发条件进入 metadata，主干 DAG 进入 instructions，Atomic 细节与证据进入 references，确定性检查进入 scripts。

## 3. 什么应该成为可安装的 Agent Skill 包

### 3.1 默认：Workflow Skill 是部署与发现单元

Workflow 通常具有清晰的用户意图、触发语境、完整入口/出口和端到端验证，最适合作为 `SKILL.md`：

```text
name: repair-shared-capacity-pressure

description:
Diagnoses and repairs proactive pressure or compaction policies when upstream
work and downstream reservations share one finite capacity. Use when thresholds
are derived from nominal capacity, reservations are not propagated, or model /
runtime switching changes capacity budgets.
```

### 3.2 Atomic 何时单独导出

Atomic 默认存为图节点和 `references/atomic/*.md`，只有同时满足以下条件才单独注册：

1. 有独立且可辨识的触发请求；
2. 不依赖固定 Workflow 上下文也能执行；
3. 有完整输入、输出和验证契约；
4. 有足够使用频率，注册后的 discovery token 成本合理；
5. description 不会与相邻 Atomic 大量重叠。

否则将 Atomic 暴露为几百上千个顶层 Skill，会造成路由歧义和 metadata 上下文膨胀。

### 3.3 Pattern 何时单独导出

Pattern 默认作为规划与解释 reference，不直接执行。只有用户确实会提出架构级请求，例如“设计共享容量系统的预算策略”“比较 reservation 策略”，Pattern 才适合作为顶层 Skill。对于普通修复任务，它应由 Workflow 自动引用。

## 4. Atomic Skill 规格

### 4.1 定义

Atomic Skill 是：

> 针对一个足够小、可重复识别的问题机制，在明确前置条件下执行一个主要语义变换，并用实现无关的 oracle 验证后置条件的解决范式。

它不是一个 diff，也不是一条“修改某函数”的命令。

### 4.2 必需内容

| 区块 | 必需内容 | 作用 |
|---|---|---|
| Identity | `id`, `name`, `version`, `title` | 稳定引用与版本化 |
| Discovery | `description`, `problem_signature`, `observable_cues` | 说明做什么、何时使用 |
| Boundary | `preconditions`, `exclusions`, `non_goals` | 避免误触发 |
| Semantics | `problem_mechanism`, `semantic_roles` | 解释根因与角色，而非路径 |
| Contract | `required_inputs`, `produced_outputs` | 可组合的输入/输出 |
| Solution | `solution_principle`, `procedure`, `decision_rules` | 最小解决协议 |
| Parameters | `parameter_slots`, `variation_points` | 跨实现绑定与允许变化 |
| Safety | `preserved_invariants`, `side_effects`, `failure_modes` | 防止局部修复破坏系统 |
| Verification | `validation_oracles`, `boundary_partition` | 验证行为而非措辞 |
| Evidence | `case_realizations`, `evidence_ids`, `confidence` | 回到真实代码与测试 |
| Generalization | `counterexamples`, `abstraction_assessment` | 证明边界与可迁移性 |
| Delivery | `routing_view`, `execution_view`, `reference_files`, `scripts` | 渐进披露投影 |

### 4.3 Atomic 的标准正文结构

```markdown
# Derive policy from residual capacity

## Use when
- Multiple stages consume the same finite capacity.
- A downstream stage requires a reservation.
- An upstream threshold is currently based on nominal capacity.

## Do not use when
- Capacity pools are physically isolated.
- The reservation is preemptible and not an invariant.

## Problem mechanism
Nominal-capacity thresholds admit work that consumes capacity required by a
later mandatory stage.

## Required facts
- Identify the shared capacity owner.
- Enumerate mandatory reservations.
- Locate the policy choke point.

## Solution protocol
1. Compute residual capacity after all mandatory reservations.
2. Apply an explicit boundary policy.
3. Derive the proactive threshold from residual capacity.
4. Preserve the reservation across all relevant configuration paths.

## Invariants
- admitted work + reservation <= shared capacity
- threshold <= residual capacity

## Verify
Partition tests into normal, zero/negative reservation, reservation >= capacity,
runtime reconfiguration, and regression cases.

## Failure modes
- Subtracting the reservation at only one call site.
- Double-subtracting an already reserved budget.
- Silently clamping without documenting degenerate behavior.
```

### 4.4 Atomic 的自由度

- **高自由度**：原则适用于多种架构，procedure 是决策准则；
- **中自由度**：有推荐伪代码或参数化 helper；
- **低自由度**：脆弱迁移、格式转换或安全操作，提供固定 script。

自由度必须与风险和实现可变性匹配，不能为了“可执行”而把通用 Atomic 写成单一补丁。

### 4.5 Atomic 原子性检查

一个 Atomic 只允许一个主要问题机制和一个主要后置条件族。以下情况应拆分：

- 参数传播和策略计算可独立失败、独立验证；
- 诊断与修复可以被不同 Workflow 复用；
- 实现修改和迁移/发布有不同风险边界；
- 删除其中一组步骤后，另一组仍是完整能力。

## 5. Workflow Skill 规格

### 5.1 定义

Workflow Skill 是：

> 面向一类较大目标，根据已知状态、诊断结果和分支条件，编排 Atomic Skills、信息收集动作与验证动作的可复用求解 DAG。

它不是某个 PR 的历史时间线。具体 PR 只作为 Case Workflow realization。

### 5.2 必需内容

| 区块 | 必需内容 | 作用 |
|---|---|---|
| Identity | `id`, `name`, `version`, `title` | 稳定引用 |
| Discovery | `description`, `goal`, `trigger_scenarios` | 顶层自动路由 |
| Scope | `entry_conditions`, `exit_conditions`, `exclusions` | 定义任务边界 |
| Diagnosis | `facts_to_collect`, `classification_rules` | 在修改前区分机制 |
| Orchestration | `steps`, `edges`, `atomic_skill_ids` | DAG 而非线性清单 |
| Control flow | `guards`, `branches`, `loops`, `stopping_conditions` | 条件编排和反馈回路 |
| State handoff | 每步 `requires` / `produces` | 使步骤可组合 |
| Binding | `semantic_roles`, `binding_questions` | 映射到新仓库 |
| Variants | `workflow_variants`, `selection_rules` | 避免一个流程硬套所有案例 |
| Recovery | `failure_recovery`, `rollback` | 可恢复执行 |
| Verification | `validation_ladder`, `acceptance_contract` | unit -> integration -> task |
| Output | `deliverables`, `report_contract` | 明确完成定义 |
| Evidence | `case_workflow_realizations`, `transfer_records` | 泛化支持 |
| Delivery | `SKILL.md outline`, references, scripts, assets | 标准包投影 |

### 5.3 Workflow Step 规格

每个 step 必须包含：

```text
id
kind: diagnose | decide | transform | bind | validate | recover
semantic_goal
requires: facts/state
uses_atomic_skills
procedure_summary
produces: facts/state/artifacts
guard
on_success
on_failure
validation
mandatory
```

`requires` 与 `produces` 决定 DAG；commit 时间不能决定 DAG。

### 5.4 Workflow 示例

`repair-shared-capacity-pressure`：

```text
S1 Diagnose shared capacity
   produces: capacity owner, consumers, reservation semantics

S2 Decide applicability
   if isolated pools -> reject this workflow / choose partitioned-capacity variant

S3 Bind capacity roles and parameters
   produces: nominal capacity, reservations, policy choke point, reconfiguration paths

S4 Normalize boundary policy
   uses: normalize-capacity-reservation-boundaries

S5 Derive pressure from residual capacity
   uses: derive-policy-from-residual-capacity

S6 Propagate reservation across runtime paths
   uses: propagate-policy-parameter-across-runtime-reconfiguration

S7 Validate boundary partitions
   uses: validate-capacity-policy-by-boundary-partitioning

S8 Run integration/regression checks
   failure -> return to S3 or S6 according to violated invariant
```

这里 Workflow 的抽象价值是：它表达输入事实、分支、状态交接和失败回路，而不仅是“依次调用 5 个 Atomic”。

## 6. Pattern 规格

### 6.1 定义

Pattern 是：

> 对一类重复问题的因果机制、竞争力量、核心不变量、Workflow 变体及选择规则的可迁移策略模型。

Pattern 通常帮助规划和选择 Workflow，不直接规定具体代码步骤。

### 6.2 必需内容

| 区块 | 内容 |
|---|---|
| Intent | 要保护的系统性质 |
| Context | 结构性前提，而非仓库特征 |
| Causal mechanism | 问题如何产生 |
| Forces | 正确性、延迟、吞吐、复杂度、兼容性等冲突 |
| Invariant | 所有变体必须保持的性质 |
| Applicability / exclusions | 使用边界 |
| Workflow variants | 可选择的 Workflow Skills |
| Decision rules | 根据事实如何选变体 |
| Alternatives | 不采用该 Pattern 时的策略与代价 |
| Consequences | 正负影响与运维成本 |
| Anti-patterns | 常见但错误的策略 |
| Counterexamples | 相似但机制不同的案例 |
| Transfer evidence | 跨仓库、跨域或 held-out 支持 |

### 6.3 Pattern 不应包含

- 某仓库路径和符号；
- 逐文件修改步骤；
- 单个 Issue 的偶然顺序；
- 没有 decision rule 的“经验总结”；
- 仅由关键词聚类得到的共同主题。

## 7. Case 与 Knowledge 的严格分离

```text
Evidence Unit
    grounds
Case Action -------------------- realizes -----------------> Atomic Skill
    part_of                                                   |
Case Workflow ------------------ realizes -----------------> Workflow Skill
                                                               |
                                                   implements / variant_of
                                                               v
                                                            Pattern
```

- `Case Action` 可写路径、符号、具体值；Atomic 核心字段不可写。
- `Case Workflow` 可保存 PR 的 repair/revert；Workflow Skill 只保留可复用结构。
- Case 是 provenance；Knowledge 是执行能力。
- 一个 Case Action 可 realization 多个 Atomic，但每个映射必须说明语义片段。
- 一个 Atomic 可被多个 Workflow 复用。

## 8. 标准 Agent Skill 包的投影

推荐 Workflow 包：

```text
repair-shared-capacity-pressure/
├── SKILL.md
├── references/
│   ├── atomic/
│   │   ├── derive-residual-capacity.md
│   │   ├── normalize-reservation-boundaries.md
│   │   └── propagate-runtime-budget.md
│   ├── pattern.md
│   ├── decision-table.md
│   └── evidence-summary.md
├── scripts/
│   ├── inspect-capacity-flow.py
│   └── validate-boundaries.py
└── assets/
    └── evaluation-case-template.json
```

### 8.1 frontmatter

为兼容 OpenAI、Anthropic 和开放 Agent Skills 标准，最小使用：

```yaml
---
name: repair-shared-capacity-pressure
description: >-
  Diagnoses and repairs pressure or compaction policies when multiple stages
  share finite capacity and downstream work needs reserved headroom. Use when
  thresholds are based on nominal capacity, reservations are lost across
  configuration paths, or boundary behavior is inconsistent.
---
```

约束：

- name 使用小写字母、数字和连字符，长度不超过 64；
- description 非空，建议远低于 1024 字符；
- description 同时写 capability 和 trigger；
- 不把完整步骤塞进 description；
- 避免品牌保留词以获得跨平台兼容性。

### 8.2 SKILL.md body

只放执行主干：

```text
Purpose and scope
Use / do-not-use conditions
Preflight facts
Workflow DAG or conditional procedure
Critical invariants
Validation and stopping conditions
Failure recovery
Links to one-hop references and scripts
```

不放大段原始 diff、所有 realization、完整 API 文档和全部反例；这些进入 references/audit store。

### 8.3 references

- `atomic/`：被当前 Workflow 使用的 Atomic 完整卡；
- `decision-table.md`：复杂分支；
- `pattern.md`：因果背景和 variant 选择；
- `evidence-summary.md`：简化 provenance，完整证据仍在图数据库；
- 引用尽量一层可达，避免链式深层跳转。

### 8.4 scripts

仅放真正提高确定性、重复性或 token 效率的操作：

- 静态检查与数据流提取；
- 边界用例生成；
- schema / invariant validation；
- 结果格式化。

不要用 script 逃避语义判断，也不要在没有重复收益时创建脚手架。

## 9. Discovery、Execution、Audit 三种视图

### Discovery / routing

约等于 Agent Skill metadata：

```text
what it solves
when to use
important symptoms
key exclusions
semantic role keywords
```

### Execution

约等于 SKILL.md body：

```text
required facts
problem-solving protocol or DAG
decision rules
invariants
validation
recovery
references/scripts to load
```

### Audit

保存在图数据库或 evidence references：

```text
case realizations
claims and evidence
rejected alignments
promotion history
transfer results
leakage audit
```

Audit 默认不注入执行上下文。

## 10. 每层的质量标准

### Atomic

- 问题足够小且机制单一；
- solution principle 能跨符号和仓库成立；
- 输入/输出允许 Workflow 编排；
- 有明确不适用条件；
- 有行为 oracle；
- candidate 至少一条真实 realization；
- reviewed 需要两条独立 realization 或 held-out transfer。

### Workflow

- 目标和完成条件明确；
- 步骤通过状态依赖构成 DAG；
- 有诊断、guard、branch 和失败回路，而非固定流水线；
- Atomic 引用的输入/输出兼容；
- candidate 可来自一个 Case Workflow；
- reviewed 需要两个对齐 Case Workflows 或 held-out 成功。

### Pattern

- 有因果机制、forces 和 invariant；
- 至少有策略变体或可比较的替代方案；
- 能选择 Workflow，而非只复述 Workflow；
- 能拒绝反例；
- reviewed 优先要求三个 cases、两个 repositories；
- validated 必须有 leakage-isolated held-out transfer。

### Agent Skill package

- metadata 可区分、不过宽；
- SKILL.md 简洁且只含主干；
- references 按需可发现；
- scripts 可运行并有明确错误；
- 至少三个代表性 eval：正例、边界例、负例/不触发例；
- 与无 Skill baseline 比较任务成功、错误率、token 和工具调用。

## 11. 对当前设计的明确修正

1. 不再把 v1 `Change Action` 称为 Atomic Skill；它是 Case Action。
2. Atomic 改为“小问题 + 解决范式”，增加 discovery、solution protocol、I/O contract 和 oracle。
3. Workflow 改为条件化编排抽象，step 必须有 requires/produces/guard/failure transition。
4. Pattern 只负责因果、forces、invariant、variant selection 和 alternatives。
5. 增加 Agent Skill package projection，不要求每个图节点都导出成 `SKILL.md`。
6. 默认只把高价值 Workflow 注册到 discovery 层；Atomic 按需 hydrate。
7. Graph-of-Skills 是知识后端，Agent Skills 文件夹是部署前端；二者不能互相替代。
