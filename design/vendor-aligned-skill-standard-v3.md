# Vendor-aligned Skill standard v3

日期：2026-09-26
状态：AREX canonical proposal for implementation and extraction

## 1. 对标结论

Anthropic/OpenAI 风格的 Agent Skill package 解决的是**如何被发现、按需加载和执行**，而不是如何表达从代码中归纳出的知识本体。因此 AREX 使用两条正交轴：

```text
语义轴：Evidence -> Case Action -> Case Workflow -> Atomic -> Workflow -> Pattern
部署轴：metadata -> SKILL.md instructions -> references/scripts/assets
```

AREX 不把每个 Case、Commit、Atomic 或 Pattern 都注册成顶层 Agent Skill。默认部署单元是 Workflow Skill；Atomic 和 Pattern 作为按需引用的图节点/资源，只有满足独立触发和完整契约时才升级为顶层包。

## 2. 统一 package contract

每个可部署 package 使用以下形态：

```text
skill-name/
  SKILL.md                 # 必需：metadata + concise execution contract
  references/              # 可选：atomic details, evidence, examples, schemas
  scripts/                 # 可选：deterministic checks or transformations
  assets/                  # 可选：templates/fixtures/output resources
```

### Metadata / discovery

- `name`: 稳定、小写、短、以行为或目标命名；不放仓库名、Issue 号或函数名。
- `description`: 同时写“解决什么问题”和“何时触发”；不能只写主题词。
- `version`: 语义版本；知识更新和实现绑定分开版本化。
- `compatibility`: 可选的 runtime/provider/project constraints。
- `risk`: `low | medium | high`，影响执行自由度和验证要求。

### SKILL.md body

- Purpose
- Use when
- Do not use when
- Preconditions / inputs
- Main procedure or workflow
- Decision rules
- Preserved invariants
- Validation / stopping conditions
- Failure recovery
- Resource loading rules

### Resources

- `references/`: 深度说明、原子步骤、证据索引、反例、迁移绑定。
- `scripts/`: 只放可重复、确定性的操作；脚本不能取代语义判断。
- `assets/`: 模板、样例、fixture；不把大规模证据全文塞进 `SKILL.md`。

## 3. AREX semantic levels

### 3.1 Atomic Skill — 一个小问题 + 一个可迁移的解决范式

Atomic 不是“改一个函数”、不是 commit 摘要，也不是一串固定文件路径。它应当只解决一个主要机制问题，并包含一个主要语义变换。

**判定阈值：**

- 一个清楚的问题机制；
- 一组最小输入；
- 一个可参数化的解决原则；
- 一个可检查的不变量；
- 一组行为级 oracle；
- 明确 exclusions/counterexamples；
- 通常可在 3–8 个主要步骤内执行。

**Atomic 必备字段：**

```yaml
id: atomic:derive-policy-from-residual-capacity
name: derive-policy-from-residual-capacity
title: Derive policy from residual capacity
version: 1.0.0
lifecycle: candidate | reviewed | validated | deprecated
description: ... # what + when
problem_signature: ...
observable_cues: []
preconditions: []
exclusions: []
non_goals: []
problem_mechanism: ...
semantic_roles: []
required_inputs: []
produced_outputs: []
parameter_slots: []
variation_points: []
solution_principle: ...
procedure: []
decision_rules: []
preserved_invariants: []
side_effects: []
failure_modes: []
validation_oracles: []
boundary_partition: []
counterexamples: []
case_realizations: []
evidence_ids: []
confidence: 0.0
```

**Atomic 正文写法：**先描述小问题机制，再描述解决范式；不要先描述实现文件。实现路径、调用点和测试放在 evidence/reference 中。

### 3.2 Workflow Skill — 对 Atomic 的条件编排

Workflow 是一个面向目标的、可验证的条件 DAG。它不是把 Atomics 机械串联，而是定义：诊断、绑定、决策、执行、验证、恢复和停止条件。

**Workflow 必备字段：**

```yaml
id: workflow:repair-shared-capacity-pressure
name: repair-shared-capacity-pressure
version: 1.0.0
description: ... # goal + trigger
objective: ...
inputs: []
outputs: []
preconditions: []
steps:
  - id: diagnose-capacity
    uses: atomic:...
    input_bindings: {}
    output_bindings: {}
    entry_conditions: []
    success_conditions: []
    failure_transitions: []
    retry_policy: null
branches: []
join_conditions: []
invariants: []
validation_plan: []
recovery_plan: []
stopping_conditions: []
realizations: []
```

**Workflow 需要表达的控制流：**

```text
diagnose -> normalize -> bind -> transform -> validate -> observe
              |             |         |
           reject         retry     recover
```

如果两个步骤没有数据依赖、控制依赖或验证依赖，就不应因为它们出现在同一 PR 中而强行放进同一个 Workflow。

### 3.3 Pattern — 解释为什么这类 Workflow 有效

Pattern 是策略族，不是可直接执行的步骤列表。它应解释因果机制、适用条件、变体、trade-off、替代方案和反例。

**Pattern 必备字段：**

```yaml
id: pattern:residual-budget-invariant
name: residual-budget-invariant
version: 1.0.0
intent: ...
problem_mechanism: ...
causal_rule: ...
forces: []
applicability_conditions: []
variant_selection: []
tradeoffs: []
alternatives: []
exclusions: []
counterexamples: []
supporting_workflows: []
supporting_cases: []
held_out_evals: []
promotion_status: provisional | validated
```

Pattern 必须至少有两个独立 Workflow/仓库 realization 才能进入 generalized/provisional；没有 held-out transfer 结果，不得标记为 validated。

### 3.4 Project Binding — 运行时语义绑定

Project Binding 不是知识层 Skill。它把抽象角色映射到具体仓库的文件、符号、配置字段、测试命令、provider 能力和参数来源。

```yaml
id: binding:repo-x:shared-capacity
skill: workflow:repair-shared-capacity-pressure
project: repo-x
role_bindings: {}
parameter_bindings: {}
validation_commands: []
compatibility_constraints: []
```

## 4. Promotion rules

```text
Case Action        永远保留为 evidence-grounded instance
Case Workflow      只能说明该次变更怎样完成
Atomic Skill       一个机制 + 一个解决范式 + 一个 oracle
Workflow Skill     可组合的条件 DAG + validation/recovery
Pattern            跨实现因果策略族 + 反例 + transfer evidence
```

- 单一仓库只能产生 Atomic candidate，不能产生跨仓库 Pattern。
- 多个 commit 不等于多个 Skills；先按语义 Action 分解，再判断是否可复用。
- 关键词、commit title、文件名、embedding 只能用于候选发现，不能作为泛化证明。
- Pattern 的支持必须能回溯到 Evidence；所有 generalized assertion 都标明 epistemic status 和 confidence。

## 5. 当前 residual-budget family 的投影

```text
Pattern:  residual-budget-invariant
Workflow: repair-shared-capacity-pressure
Atomics:  derive-policy-from-residual-capacity
           normalize-capacity-reservation-boundaries
           replay-capacity-policy-across-reconfiguration

DeepSeek-only optional Atomic:
           derive-auxiliary-output-cap-from-headroom

Separate adjacent Atomics:
           place-pressure-check-at-next-request-boundary
           account-for-all-context-visible-artifacts
           preserve-original-context-on-summary-failure
```

默认包：

```text
repair-shared-capacity-pressure/
  SKILL.md
  references/atomic/*.md
  references/pattern.md
  references/evidence/*.md
  scripts/validate_capacity_policy.py   # only if deterministic implementation is added
```

## 6. Evaluation contract

每个可执行 Workflow 至少有：

- positive case;
- boundary case;
- negative/exclusion case;
- regression case.

评估记录应区分：检索命中、正确绑定、步骤执行、行为验证、回退/恢复、token usage。不能用“生成了一个看起来合理的 Skill 文本”替代 transfer evaluation。
