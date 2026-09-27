# 泛化多层 Skill 规范 v2

状态：Draft for implementation（取代 v1 作为后续抽取的规范）  
版本：2.0.0  
日期：2026-09-26  
适用项目：AREX Skill Graph

## 1. 为什么需要 v2

v1 已经区分 Evidence、Atomic、Workflow、Pattern，但仍存在一个根本混淆：

- 把某个仓库中的具体 Change Action 称为 Atomic Skill；
- 把某个 Issue/PR 的实际处理过程称为 Workflow Skill；
- 主要到 Pattern 层才真正做跨案例抽象。

这会造成“实例描述得比较抽象”被误判成“已经形成可迁移知识”。v2 将**实例/证据**与**可复用知识**彻底分离：

```text
实例平面（发生了什么，不是 Skill）
E0 Evidence Unit
E1 Case Action / Change Instance
E2 Case Workflow / Resolution Trace

知识平面（可迁移的解决能力，才是 Skill）
K1 Atomic Skill Template
K2 Workflow Skill
K3 Resolution / Strategy Pattern

运行时平面（本次如何落地，不是永久 Skill）
R1 Project Binding
```

核心原则：

> Atomic Skill 不是“改了哪个函数”，而是一个与仓库、文件名和符号名解耦的最小语义算子；Workflow Skill 不是“某个 PR 依次做了什么”，而是为一类问题组织这些算子的可复用求解 DAG；Pattern 不是更长的 Workflow，而是解释这类 Workflow 为什么成立、何时适用、如何取舍的因果策略族。

## 2. 设计目标

1. **可迁移**：替换仓库名、路径、符号和具体常量后，知识仍然成立。
2. **可执行**：知识节点具有前置条件、输入/输出状态、参数槽、验证原则和失败恢复。
3. **可追溯**：每个抽象都有真实 Case Action / Case Workflow realization，并最终落到代码、diff、调用点与测试证据。
4. **可证伪**：必须记录排除条件、反例、竞争解释、失败实例和未通过的抽象检查。
5. **可分级**：candidate、reviewed、validated 不是主观标签，而由独立 realization、held-out transfer 和 leakage gate 决定。
6. **可计算**：Schema 验证结构，语义验证器检查引用、DAG、支持多样性、抽象门与晋级门。
7. **节省上下文**：routing、execution、audit 三种视图分离；先检索短摘要，再按需 hydrate 执行与证据。

## 3. 明确的非目标

- 不把 commit、diff hunk、文件修改或测试新增直接称作 Skill。
- 不把一个 Issue 的 commit 时间线直接称作 Workflow Skill。
- 不因为文字里删掉文件名，就认为实现了泛化。
- 不要求所有相似关键词的任务属于同一个 Pattern。
- 不把 HNSW 层级当作业务知识层级。
- 不用 embedding 相似度替代因果机制对齐。
- 不用目标补丁自带测试冒充 held-out transfer。
- 不伪造 Issue/PR 关联、模型身份、token、成本或执行结果。

## 4. 三个平面与六类核心对象

| 平面 | 层 | 对象 | Skill? | 回答的问题 |
|---|---|---|---:|---|
| 实例 | E0 | Evidence Unit | 否 | 什么事实可以复核？ |
| 实例 | E1 | Case Action | 否 | 在一个具体版本中发生了什么语义状态变化？ |
| 实例 | E2 | Case Workflow | 否 | 一个真实任务如何被解决，存在哪些依赖、分支和返工？ |
| 知识 | K1 | Atomic Skill Template | 是 | 最小、独立、可复用的解决算子是什么？ |
| 知识 | K2 | Workflow Skill | 是 | 针对一类问题，应如何组合与编排算子？ |
| 知识 | K3 | Strategy Pattern | 是 | 为什么这套策略成立，何时选它，代价和替代方案是什么？ |
| 运行时 | R1 | Project Binding | 否 | 这些抽象角色在当前 checkout 中对应什么？ |

关系不是简单的“上层包含下层”：

```text
Evidence --grounds--> Case Action
Case Action --part_of--> Case Workflow
Case Action --realizes--> Atomic Skill
Case Workflow --realizes--> Workflow Skill
Atomic Skill --used_by--> Workflow Skill Step
Workflow Skill --variant_of / implements--> Pattern
Project Binding --binds--> Atomic / Workflow / Pattern role or slot
```

## 5. E0：Evidence Unit

Evidence 是不可再分或无需再分的可复核事实载体：

- Issue / PR 正文、review、discussion；
- commit、diff hunk、文件快照；
- 符号定义、调用点、配置流；
- 测试代码、测试 oracle、运行输出；
- benchmark、trace、日志和失败复现。

最低字段：

```text
id, kind, repository, revision, locator,
summary, content_sha256, capture_method, trust, captured_at
```

证据必须区分：

- `observed`：可直接在冻结材料中看到；
- `inferred`：由多个观察推导；
- `generalized`：跨 realization 抽象；
- `hypothesized`：待验证解释，不能参与晋级硬门槛。

Commit subject、label、文件名和 embedding 只可用于候选召回，不能单独证明程序语义。

## 6. E1：Case Action（具体实例，不是 Skill）

Case Action 精确描述一个特定仓库、特定 revision 中的语义变化：

```text
case context
problem manifestation
before state
concrete operation
post state
preserved invariants
changed symbols/files
validation observations
evidence references
```

它允许出现具体路径、符号、类名和数值。例如：

> 在 `ContextCompressor` 中将压力阈值的基数从 `context_length` 改为 `context_length - max_tokens`，并把 `max_tokens` 从初始化与模型切换路径传入。

这是高质量 Case Action，但仍**不是** Atomic Skill。它只是一条真实 realization。

Case Action 的边界以“单一可独立验证的语义状态变化”为准，不以 commit 为准：

- 一个 commit 可拆出多个 Case Action；
- 多个 fixup commit 可合并成一个 Case Action；
- 测试修改可与实现合并，也可作为单独的 validation action；
- 格式化、lockfile、生成文件默认不是 Case Action，除非参与目标行为。

## 7. E2：Case Workflow（具体处理轨迹，不是 Skill）

Case Workflow 是一个真实 Issue/PR/episode 的语义 DAG，保存：

- 故障与任务入口；
- 诊断、设计、实现、集成、验证和修复动作；
- 数据依赖、控制依赖、验证依赖；
- 分支、失败尝试、revert、repair loop；
- 最终验收结果与遗留项。

它不是 commit 列表。时间顺序只能作为弱证据，不能自动生成 `requires`。

允许的主 DAG 边：

- `requires`：target 的成立依赖 source 的产物；
- `enables`：source 使 target 可执行或可判断；
- `precedes`：存在语义顺序但依赖较弱；
- `validates`：source 验证 target 的后置条件。

非排序边：

- `repairs`：source 修复 target 的失败；
- `alternative_to`：互斥或可替代路径；
- `supersedes`：新动作替代旧动作。

## 8. K1：Atomic Skill Template

### 8.1 定义

Atomic Skill 是**最小可复用语义算子**：在满足可判定前置条件时，以参数化操作将一类输入状态变为目标状态，同时保持声明的不变量，并给出与实现无关的验证原则。

它不允许把 repository、path、symbol、commit 或 Issue number 写进核心语义。具体名字只能出现在 realization 或 Binding。

### 8.2 必需内容

每个 Atomic Skill 必须包含：

1. `objective`：要消除的机制性问题，而不是具体 bug 标题；
2. `problem_mechanism`：错误为何发生；
3. `semantic_roles`：例如 `shared_capacity`、`downstream_reservation`、`pressure_policy`；
4. `preconditions`：何时可以应用；
5. `parameter_slots`：需要绑定的容量、比例、策略、边界规则；
6. `operator`：输入状态、参数化变换、输出状态；
7. `postconditions`：应用后必须成立的性质；
8. `preserved_invariants`：不能破坏的性质；
9. `variation_points`：允许不同实现的地方；
10. `failure_modes`：常见误用和失效方式；
11. `validation_principles`：不依赖某个测试函数名的验证方法；
12. `counterexamples`：表面相似但不适用的案例；
13. `non_goals`：明确不解决什么；
14. `realizations`：哪些 Case Action 实现了它；
15. `abstraction_assessment`：泛化检查结果。

### 8.3 示例

错误的 Atomic：

> 修改 `context_compressor.py`，把 `context_length` 减去 `max_tokens`。

正确的 Atomic：

> 当上游工作与下游预留共享同一有限容量时，先从名义容量中扣除所有必须保留的下游预算，再从残余容量推导主动压力阈值；对缺失、非法或超过总容量的 reservation 使用显式边界策略。

可进一步形式化：

```text
C = nominal shared capacity
R = sum(mandatory downstream reservations)
E = boundary_policy(C - R)
T = pressure_policy(E, parameters)

postconditions:
0 <= E <= C
0 <= T <= E
upstream admission does not consume reserved downstream capacity
```

这里的公式、角色和边界策略是 Skill；Hermes 或其他仓库里的文件修改只是它的 realization。

### 8.4 原子性判据

一个 K1 节点只有在以下条件同时满足时才是 atomic：

- 只有一个主要状态变换；
- 删除任一核心 operator 子句都会使主要后置条件不成立；
- 不包含可独立触发、独立验证、独立复用的第二个算子；
- validation principle 直接验证该变换，而非整个 Issue；
- variation point 不改变核心因果机制。

例如，“推导 residual capacity”与“把 reservation 参数贯穿模型切换路径”通常应是两个 Atomic Skills；它们可在 Workflow Skill 中组合。

## 9. K2：Workflow Skill

### 9.1 定义

Workflow Skill 是针对一类问题的**可复用求解 DAG**。它组合 Atomic Skills、诊断步骤、决策点和验证阶梯，但不绑定到某个 Issue 的历史顺序。

它回答：

- 先证明什么，再修改什么？
- 哪些步骤是必要的，哪些是条件分支？
- 参数从哪里发现并如何传播？
- 哪些验证可以局部进行，哪些必须集成验证？
- 失败时回到哪个决策点？

### 9.2 Workflow Skill Step

一个 step 必须描述：

```text
semantic goal
input state / required facts
atomic skill references（可为空，诊断步骤不一定是变换）
produced facts / output state
branch condition
validation principle references
mandatory / optional
acceptable variants
```

K2 的排序必须是**语义排序**，不是 commit 排序。

### 9.3 示例

`Diagnose and repair shared-capacity pressure control`：

1. 识别真正共享的有限资源及其所有消费者；
2. 枚举必须在上游决策前保留的下游 reservation；
3. 计算 residual capacity，并定义非法/退化输入策略；
4. 在统一的 policy choke point 基于 residual capacity 推导阈值；
5. 沿所有构造、配置和运行时切换路径传播 reservation；
6. 分别验证正常边界、reservation 超界、切换一致性和旧行为回归；
7. 若系统实际使用独立容量池，则停止并转用分区容量策略。

这个 Workflow 可以由不同语言、文件结构和测试框架实现。

## 10. K3：Resolution / Strategy Pattern

### 10.1 定义

Pattern 是一个**因果策略族**，解释一个或多个 Workflow Skills 为什么有效、在什么力量与约束下选择它、有哪些替代策略与代价。

Pattern 不是“更大的步骤列表”。它必须包含：

- `causal_mechanism`：导致一类问题的因果链；
- `forces`：相互竞争的目标、成本和约束；
- `applicability` / `exclusions`：适用与排除条件；
- `invariant`：策略必须建立或保持的核心性质；
- `workflow_variants`：一个或多个 K2 变体；
- `decision_rules`：如何选择变体；
- `alternatives`：其他可行策略及其 trade-off；
- `failure_modes`：策略级失效；
- `counterexamples`：可区分边界；
- `transfer_evidence`：跨仓库、跨实现或 held-out 的迁移结果。

### 10.2 示例

`Residual-Budget Invariant for Shared-Capacity Pipelines`：

> 当上游输入、缓存或队列与下游输出、flush、commit 或恢复动作共享一个有限容量时，所有主动 admission / compaction / pressure 阈值必须从扣除必要 reservation 后的残余容量推导，而不能从名义总容量推导。

核心不变量：

```text
admitted_upstream_work + mandatory_downstream_reservation
<= shared_capacity
```

适用场景可跨越：context window、buffer、queue、storage quota、memory pool、rate-limit bucket。  
不适用：上下游拥有物理隔离且不可互借的容量池；reservation 只是软提示且允许被抢占；容量无限或压力策略不依赖容量。

## 11. Abstraction Assessment：不能只靠“措辞抽象”

每个知识节点必须记录以下检查。结果为 `pass`、`fail` 或 `not_run`，并附 rationale 与支持 realization。

### 11.1 Symbol substitution test

把所有仓库名、文件名、符号名和具体常量替换为角色与槽位后，Skill 是否仍精确、可执行？

### 11.2 Repository independence test

仅给另一个仓库的代码结构，不提供来源仓库路径时，是否仍能完成 role binding 和执行？

### 11.3 Implementation variability test

同一语义是否允许通过不同函数拆分、配置机制、语言或测试框架实现？若只容许一种语法补丁，则不是通用 Skill。

### 11.4 Counterfactual transfer test

面对未见过但满足前置条件的新案例，Skill 是否能预测必要改动与验证；面对不满足条件的案例，是否会拒绝应用？

### 11.5 Atomic minimality test（K1 必须）

是否包含第二个可独立触发和验证的状态变换？若有，应拆分。

### 11.6 Causal sufficiency test

Skill 是否解释“为何有效”，还是只描述共同表象或文本相似性？

### 11.7 Counterexample discrimination test

是否存在明确反例；Skill 能否依据结构条件拒绝它，而不是被关键词误导？

## 12. 生命周期与晋级门

### 12.1 K1 Atomic Skill

**candidate**：

- 至少一个证据完整的 Case Action realization；
- problem mechanism、operator、postcondition 和 validation principle 完整；
- 不要求已证明跨仓库泛化。

**reviewed**：满足下列其一：

- 至少两个独立 realization，且不是同一补丁的机械复制；或
- 一个 realization + 一次 leakage-isolated held-out transfer 成功。

并且：

- symbol substitution、repository independence、atomic minimality、causal sufficiency 均 pass；
- 不得在核心字段中泄漏 repository/path/symbol literal。

**validated**：

- 至少一次 leakage-isolated held-out transfer 成功；
- counterfactual transfer 与 counterexample discrimination 均 pass；
- 有明确 negative transfer 或 reject 案例；
- 无未解释的高严重度失败。

### 12.2 K2 Workflow Skill

**candidate**：可由一个 Case Workflow 抽象，但必须明确标为尚未证明泛化。  
**reviewed**：至少两个语义对齐的 Case Workflows，或一个 Case Workflow + held-out 成功；步骤顺序是语义依赖。  
**validated**：在未参与归纳的任务上完成端到端迁移，并记录分支选择、失败恢复和验收结果。

### 12.3 K3 Pattern

**candidate**：至少一个 Workflow Skill 加一个有意义的策略变体，或两个相关 Workflow Skills；因果机制与适用边界完整。  
**reviewed**：优先要求至少三个 task cases、两个 repositories，并覆盖至少一个反例或替代策略。  
**validated**：必须有 leakage-isolated held-out transfer；能正确选择 workflow variant 或拒绝不适用案例。

“两个仓库用了相似变量名”不构成独立支持；fork、cherry-pick、同源实现必须标记 lineage，不能重复计数。

## 13. Held-out 与泄漏隔离

每次 transfer 必须记录：

```text
target case / repository
knowledge cutoff and allowed context
whether target solution was hidden
retrieved Skill versions
binding procedure
predicted plan
performed actions
validation oracle and result
leakage audit
```

隔离级别：

- `none`：看过目标补丁，不可用于晋级；
- `partial`：隐藏补丁但看过高泄漏材料，只可作诊断；
- `solution_hidden`：目标实现与测试答案隐藏；
- `task_isolated`：目标任务在归纳、聚类、prompt 和调参阶段均隔离。

只有 `solution_hidden` 或 `task_isolated` 的成功结果可作为 validated 证据。

## 14. Project Binding

Binding 将抽象角色和参数槽映射到当前 checkout：

```text
semantic role -> path / symbol / config / registry / test entry
parameter slot -> concrete value or discovery procedure
binding confidence
probe evidence
revision and tree fingerprint
invalidation conditions
```

Binding 是临时执行缓存：代码树变化、模型切换或配置入口变化后应标记 stale。它不增加知识节点的泛化支持计数。

## 15. 图节点与边

### 15.1 推荐节点

```text
EvidenceUnit
CaseAction
CaseWorkflow
AtomicSkill
WorkflowSkill
WorkflowSkillStep
StrategyPattern
ProjectBinding
ValidationRecord
TransferRecord
```

### 15.2 跨平面边

- `grounds`：Evidence -> CaseAction / validation / claim；
- `part_of`：CaseAction -> CaseWorkflow；
- `realizes`：CaseAction -> AtomicSkill，CaseWorkflow -> WorkflowSkill；
- `uses`：WorkflowSkillStep -> AtomicSkill；
- `implements`：WorkflowSkill -> StrategyPattern；
- `binds`：ProjectBinding -> knowledge node / role / slot；
- `validated_by`：knowledge node -> TransferRecord / ValidationRecord。

### 15.3 知识平面同层边

- `requires`：语义前置；
- `enables`：产生执行条件；
- `precedes`：弱顺序；
- `validates`：验证另一步的后置条件；
- `alternative_to`：替代策略；
- `specializes`：增加前置条件或收窄参数域；
- `composes_with`：常见组合但无强依赖；
- `conflicts_with`：仅离线审计/过滤使用，不参与正向扩散。

图扩散必须按边类型、方向和查询意图限界。HNSW 仅用于 routing view 的 ANN 召回，它的内部层不等于上述知识层。

## 16. 检索与上下文注入

每个知识节点提供三种投影：

### routing view

用于 BM25/HNSW，包含：

```text
problem mechanism
observable symptoms
semantic roles
preconditions / exclusions
operator or workflow skeleton
artifact and validation terms
```

严禁放入大段 diff 和完整历史。

### execution view

仅对入选节点加载，包含：

```text
operator / DAG
parameter slots
binding questions
decision rules
validation ladder
failure recovery
```

### audit view

需要解释或审核时加载，包含：

```text
realizations
claims and evidence
abstraction assessment
promotion history
transfer and leakage records
rejected alignments
```

推荐检索顺序：

```text
query decomposition
-> retrieve Pattern / Workflow / Atomic routing views independently
-> typed graph expansion
-> diversity and applicability filtering
-> hydrate selected execution views
-> bind roles to current project
-> execute and validate
```

不得默认把全部层次、全部 evidence 注入 LLM。

## 17. LLM 与确定性程序的职责

### 17.1 LLM 必须负责

- 阅读真实 before/after code、调用点和测试 oracle；
- 把 commit 拆成 Case Actions，或把 fixups 合并成一个 Case Action；
- 解释 problem mechanism、state transformation 与 invariant；
- 从 Case Action 归纳 K1，而非改写 commit subject；
- 从多个 Case Workflow 对齐 K2 的语义 DAG；
- 从多个 K2/variant 推导 K3 的因果机制、forces 和 decision rules；
- 给出反例、竞争解释、失败模式和不确定性；
- 主动拒绝只因关键词相似但机制不同的 alignment。

### 17.2 确定性程序必须负责

- 候选召回、context manifest、hash 和版本冻结；
- Schema、引用、DAG、ID 与 provenance 校验；
- repository/path literal leakage 检测；
- realization 数量、repository diversity 和 lineage 去重；
- lifecycle promotion gate；
- held-out isolation metadata；
- 图存储、HNSW、PPR/typed expansion 与 token budget；
- 缓存、去重、审计和可复现实验。

LLM 可以提出晋级建议，但不能绕过确定性 hard gate。

## 18. 推荐的抽取协议

### Phase A：实例恢复

1. 召回真实 Issue/PR/commit 候选；
2. 冻结 before/after、调用点、测试与 metadata；
3. LLM 提取 E1 Case Actions；
4. LLM 建立 E2 Case Workflow DAG；
5. 人工或规则审核 evidence coverage。

### Phase B：知识归纳

6. 对 Case Actions 按 problem mechanism + operator + invariant 对齐；
7. 生成 K1 candidate，并记录拒绝对齐；
8. 对 Case Workflows 做结构对齐，生成 K2 candidate；
9. 比较 K2 variants、forces、alternatives，生成 K3 candidate；
10. 运行 abstraction assessment 与 promotion gate。

### Phase C：迁移验证

11. 冻结 held-out case；
12. 只提供任务上下文和检索到的 knowledge nodes；
13. 生成 Binding、计划、修改和测试；
14. 记录成功、失败、拒绝与 leakage audit；
15. 晋级、拆分、合并或降级节点。

## 19. Residual-capacity 任务族的建议拆分

不要把整个 compaction 修复塞进一个 Atomic Skill。更合理的 K1 候选是：

1. `derive-policy-from-residual-capacity`：从扣除 reservation 后的有效容量推导压力策略；
2. `normalize-capacity-reservation-boundaries`：定义缺失、非法、超界和退化输入策略；
3. `propagate-policy-parameter-across-runtime-reconfiguration`：在构造、配置和模型/运行时切换路径保持参数一致；
4. `centralize-capacity-pressure-at-policy-chokepoint`：避免多个调用点各自使用不一致阈值；
5. `validate-capacity-policy-by-boundary-partitioning`：按正常、零/负、超界、切换和回归分区验证。

K2 才把这些算子编排为 `repair-shared-capacity-pressure-control`。  
K3 再把它归纳为 `residual-budget-invariant-for-shared-capacity-pipelines`。

这个拆分允许未来复用：某些任务只需要 K1.2，某些只需要 K1.3；新的 queue 或 buffer 任务可复用 K3，但选择不同 K2 variant。

## 20. v1 迁移规则

- v1 `Evidence Unit` -> v2 `Evidence Unit`；
- v1 具体 `Atomic Skill / Change Action` -> v2 `Case Action`；
- v1 `Issue Workflow` -> v2 `Case Workflow`；
- v1 真正参数化且通过抽象检查的 Atomic 内容 -> v2 `Atomic Skill`；
- v1 `Resolution Pattern` 不自动成为 v2 Pattern：若主要仍是步骤骨架，先降为 `Workflow Skill`；
- v1 `Project Binding` -> v2 `Project Binding`；
- 所有 lifecycle 重置为 candidate，重新通过 v2 promotion gate。

v1 文件保留用于审计和迁移，不再作为新抽取的 canonical contract。
