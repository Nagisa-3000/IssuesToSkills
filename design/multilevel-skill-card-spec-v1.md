# 多层 Skill Card 与证据规范 v1

状态：Superseded by v2；仅用于迁移和审计  
版本：1.0.0（不再用于新抽取）  
日期：2026-09-26  
适用项目：AREX Skill Graph

## 1. 目的

本规范定义从真实软件工程代码中提取、审核、存储、检索和验证 Skill 的统一格式。它必须同时满足五个目标：

1. **可执行**：给定新仓库，Skill 能指导定位、修改和验证，而不只是描述历史改动。
2. **可追溯**：每个语义结论都能回到 Issue、PR、commit、hunk、符号、测试或运行结果。
3. **可泛化**：把仓库特有路径、类名和常量放进证据或 Binding，不污染跨任务 Pattern。
4. **可证伪**：保存排除条件、反例、失败尝试和不确定性；Pattern 需要 held-out 任务验证。
5. **可计算**：字段、引用、生命周期和质量门可由 JSON Schema 与语义验证器检查。

本规范不把 commit message、Issue 标题、文件名聚类或向量近邻直接视为 Skill。它们只能定位候选证据。**代码到语义 Skill 的关键判断由 LLM 阅读代码、diff、调用关系和测试后完成**；确定性程序负责候选召回、上下文冻结、引用校验、去重和质量门。

## 2. 非目标

- 不把每个 commit 强制转成一个 Skill。
- 不把提交时间顺序等同于问题解决顺序。
- 不要求所有任务都能归纳为跨仓库 Pattern。
- 不以字段齐全代替语义正确。
- 不将 HNSW、PPR 或 ranker 的分数当作知识真实性。
- 不把目标 PR 自带测试冒充独立 hidden test。
- 不伪造 LLM 模型、token、成本、运行结果或 Issue/PR linkage。

## 3. 层次模型

| 层 | 名称 | 是否为 Skill | 语义单位 | 主要用途 |
|---|---|---:|---|---|
| L0 | Evidence Unit | 否 | 可定位、可复核的事实载体 | 溯源、审计、反证 |
| L1 | Atomic Skill | 是 | 最小可复用状态变换 | 代码修改与局部验证 |
| L2 | Issue Workflow | 是 | 单个真实任务的有向部分序解决链 | 任务执行与决策 |
| L3 | Resolution Pattern | 是 | 多个 Workflow 对齐后的参数化骨架 | 跨任务、跨仓库泛化 |
| L4 | Project Binding | 否 | 抽象角色到当前 checkout 的临时映射 | 在目标仓库落地执行 |

### 3.1 L0 Evidence Unit

Evidence 是观察来源，不是 Skill。最小要求是：来源类型、仓库、revision、精确 locator、内容摘要、内容摘要哈希及采集方式。Issue/PR 标题和 commit subject 可作为导航信息，但不能单独证明代码行为。

### 3.2 L1 Atomic Skill

Atomic Skill 是一个具有明确前置状态、操作、后置状态和验证契约的最小可复用代码状态变换。

拆分原则：

- 一个 commit 同时改变不同不变量、不同触发条件或可独立验证的行为时，应拆成多个 Atomic Skill。
- 仅格式化、生成文件、锁文件变化默认不产生 Skill，除非它本身是任务语义的一部分。
- 一个语义变换跨多个 fixup commit 才完整时，应合并为一个 Atomic Skill，并保留全部证据。
- 实现与其不可分割的回归测试可属于同一个 Skill；独立的复现、迁移或性能验证可成为单独 Skill。

判定“原子”的操作性标准：删除其中任一核心 operation 后，目标后置条件不再成立；同时它不应包含可被不同触发条件独立复用的第二个状态变换。

### 3.3 L2 Issue Workflow

Workflow 表示一个真实 Issue、PR 或高置信 orphan episode 的解决链。它是 DAG/partial order，而不是 commit 列表。排序来自数据依赖、控制依赖、故障—修复关系和验证依赖；时间戳只作为弱证据。

Workflow 可包含：诊断、复现、发现、设计、实现、集成、验证、修复、回滚和发布步骤。主排序关系 `requires`、`enables`、`precedes`、`validates` 必须无环；`repairs` 可指向先前失败步骤，但不进入主 DAG 的拓扑排序。

### 3.4 L3 Resolution Pattern

Pattern 是至少两个独立 Workflow 的稳定公共骨架。它抽象：

- 共同意图和适用边界；
- 必选步骤与条件分支；
- 参数槽和模块角色；
- 顺序、依赖和验证阶梯；
- 已知失败模式、反例及不可适用条件。

只有一个 Workflow 时，只能保留为 Workflow 或 Pattern candidate note，不能发布为正式 Pattern。跨仓库结论必须至少由两个 repository 支持。描述“听起来通用”不构成泛化证据。

### 3.5 L4 Project Binding

Binding 把 Pattern/Atomic Skill 中的 `session_store`、`provider_adapter` 等角色和参数槽映射到当前 checkout 的路径、符号、注册表、配置项或测试入口。Binding 以 repository tree fingerprint 为缓存键；代码变化后必须重新 probe 或标记 stale。Binding 不进入永久 Pattern 本体。

## 4. Family Bundle 顶层格式

一个 bundle 对应一个候选任务族和一次可回放的提取运行：

```json
{
  "schema_version": "1.0.0",
  "bundle_id": "family:context-state-safety:v1",
  "task_family": {},
  "extraction": {},
  "candidate_episodes": [],
  "evidence_units": [],
  "validations": [],
  "atomic_skills": [],
  "workflows": [],
  "patterns": [],
  "bindings": [],
  "relations": [],
  "rejected_candidates": [],
  "quality_report": {}
}
```

Bundle 是审计和交换单位，不等于在线检索时一次性注入的上下文。在线系统只加载预算内的 routing view，再对入选节点 hydrate execution view；audit view 按需读取。

## 5. Claim：所有语义判断的基本单位

任何 intent、状态、操作、适用条件、顺序、不变量、失败模式或泛化结论都使用 Claim：

```yaml
claim:
  id: claim:<stable-id>
  claim_type: intent | trigger | state | transformation | invariant |
              applicability | ordering | validation | failure_mode | generalization
  statement: 可证伪的单一命题
  epistemic_status: observed | inferred | generalized
  evidence_ids: []
  rationale: 为什么这些证据支持该命题
  confidence: 0.0..1.0
  uncertainty: 已知缺口、替代解释或待验证点
```

三种 epistemic status 的边界：

- **observed**：可从代码、diff、测试或运行结果直接确认，必须至少引用一个 Evidence。
- **inferred**：由多个观察事实推导，例如两个步骤的语义依赖；必须给出推理理由和支持证据。
- **generalized**：跨 Workflow 对齐后的抽象结论；必须能追到多个 Workflow 的 realization，不能只引用一个提交。

Claim 应保持原子性。若一句话包含“并且”连接的两个可分别被证伪的命题，应拆分。

## 6. L0 Evidence 字段

必需字段：

- `id`：内容寻址或稳定命名 ID；
- `kind`：issue、pull_request、review、commit、hunk、file、symbol、test、test_result、runtime_trace、documentation；
- `repository` 与 `revision`；
- `locator`：commit SHA、路径、行区间、符号、测试名或外部编号；
- `summary`：对证据事实的短摘要，不提前写成 Pattern；
- `content_sha256`：冻结上下文的完整性校验；
- `capture_method`：git、filesystem、github_api、test_runner、manual 等；
- `trust`：verified、repository_observed、externally_observed、unverified；
- `captured_at`。

可选字段包括 parent SHA、变更文件、语言、generated/lock 标记、原始指针和许可信息。若 GitHub API 未验证 Issue/PR closing link，linkage 只能标 `inferred` 或 `unverified`。

## 7. L1 Atomic Skill 格式

Atomic Skill 必须包含：

1. `intent`：为何变更；
2. `observable_triggers`：何时需要；
3. `applicability`：requires_all、requires_any、excludes 和 unknown policy；
4. `transformation`：before state、operation、target roles、parameter slots、after state；
5. `invariants_preserved`；
6. `outputs` 与 `side_effects`；
7. `validation_contract_ids`；
8. `repository`、`source_episode_ids` 与 `evidence_ids`；
9. routing、execution、audit 三视图；
10. 多维 quality 和 lifecycle。

operation 应使用“角色 + 状态变换 + 约束”表达，例如：

> 在 context budget 角色中，从总窗口扣除输出 reservation 后计算有效预算；对非正 reservation 做规范化，并在极小有效窗口中保留有界阈值。

而不是“修改 context_compressor.py 第 42 行”，也不是“修复压缩 bug”。

## 8. L2 WorkflowStep 与 Workflow 格式

### 8.1 WorkflowStep

字段包括：

- `role`；
- `goal`；
- `input_state` 与 `output_state`；
- 一个或多个 `atomic_skill_ids`；
- `branch_condition`；
- `validation_ids`；
- `evidence_ids`；
- mandatory/optional 标记及 confidence。

### 8.2 Workflow edges

边必须明确方向和语义：

- `requires`：target 在语义上依赖 source 的结果；
- `enables`：source 使 target 可执行，但不必是严格前置；
- `precedes`：逻辑顺序约束；
- `validates`：source 是对 target 的验证步骤；
- `repairs`：source 修复 target 的失败或不足；
- `alternative_to`：两个步骤为互斥/可替代实现。

每条边都必须带 rationale Claim，不能只靠相邻 commit 自动生成。

### 8.3 Workflow

Workflow 还要记录 anchor、entry/exit state、decision points、repair loops、reverted/superseded changes、deferred items、acceptance validations 和 source revisions。Anchor 优先级：verified resolved Issue + closing PR；merged PR；证据完整的 orphan episode。

## 9. L3 PatternStep 与 Pattern 格式

PatternStep 是多个 WorkflowStep 的对齐结果，包含 operation template、输入输出、模块角色约束、参数引用、applicability、mandatory/branch key、可接受变体、验证模板，以及每个 supporting Workflow 的 realization。

Pattern 必须包含：

- 任务族和共同 intent；
- 参数槽定义（类型、约束、绑定方式）；
- 适用与排除谓词；
- PatternStep 和 Pattern edge；
- 必选骨架、可选分支和决策点；
- 不变量、验证阶梯、失败模式及反例；
- 至少两个 supporting Workflow；
- evidence diversity；
- held-out 结果；
- lifecycle 与 promotion history。

Pattern edge 使用 `requires`、`enables`、`precedes`、`validates`、`alternative_to`。主边必须无环。

## 10. Validation Contract

Validation 不是一条模糊的“运行测试”。其字段包括：

- `purpose`：reproduce、regression、compatibility、performance、safety、static；
- `level`：unit、integration、e2e、repository、runtime；
- `procedure`：命令、测试选择器或可重复步骤；
- `oracle`：期望状态、输出、异常、性能阈值或不变量；
- `environment`；
- `scope`；
- `result`：not_run、pass、fail、error、inconclusive；
- `result_evidence_ids`；
- `independence`：source_patch_test、derived_test、held_out_test、external_suite。

目标 PR 自带测试可证明回归契约，但不能自动视为 held-out。held-out 测试必须与目标 patch 隔离，并记录目标解答访问策略。

## 11. L4 Binding 格式

Binding 必须记录：

- 目标 repository、revision 和 tree fingerprint；
- 绑定到哪个 Pattern/PatternStep/Atomic Skill；
- role → path/symbol 映射；
- parameter → concrete value 映射；
- probe procedure、probe result 和证据；
- status：fresh、stale、rejected；
- invalidation conditions。

Binding 是执行缓存，不作为 Pattern 泛化支持。固定路径和符号只能存在于 Evidence、Workflow 实例或 Binding 中。

## 12. 三种内容视图

| 视图 | 必须包含 | 禁止内容 |
|---|---|---|
| routing | intent、trigger、operation、module role、artifact/test terms、简短 predicate | 大段 diff、完整历史、冗长审计记录 |
| execution | 前置、步骤、分支、参数、验证、失败恢复 | 未证实的仓库特有绑定 |
| audit | claim IDs、evidence IDs、run ID、review notes | 无来源的总结性判断 |

三视图可从同一结构化对象派生，但必须分别做 token 预算。routing view 进入 BM25/HNSW；execution view 仅对选中节点加载；audit view 用于解释和复核。

## 13. 提取协议：LLM 与确定性程序的职责

### 13.1 确定性阶段

1. 召回候选 Issue/PR/commit；
2. 冻结代码、diff、测试、调用点和 metadata；
3. 计算 context manifest SHA256；
4. 检测生成文件、锁文件、revert 和明显噪声；
5. 为 LLM 分配隔离任务族上下文；
6. 校验 schema、引用、DAG、质量门和重复项。

### 13.2 LLM 代码阅读阶段

LLM 必须：

1. 读取真实实现代码和上下文，而非只读 commit subject；
2. 读取 diff 前后状态；
3. 阅读测试 oracle，区分复现、回归和独立验证；
4. 识别一个 commit 中的多个状态变换；
5. 合并跨 fixup commit 的同一变换；
6. 解释 trigger、operation、invariant、side effect 和 validation；
7. 构造 Workflow 的语义部分序；
8. 对多个 Workflow 做结构对齐后才产生 Pattern；
9. 明确记录替代解释、缺失证据和拒绝候选。

LLM 不得：根据文件名猜行为、根据时间顺序生成所有边、把相似措辞当作同一 Pattern、补写未执行的测试结果，或把未知模型/成本写成确定值。

### 13.3 隔离与泄漏控制

- 每次只处理一个冻结的 task family context；
- Pattern 归纳前先独立完成各 Workflow，避免由预设 Pattern 反向污染；
- held-out task 的 target patch、目标答案和隐藏测试不得进入抽取上下文；
- post-hoc audit 若查看 target patch，必须单独记录，不能回写为运行时可用证据；
- context manifest 记录所有输入对象及哈希，以支持回放。

## 14. Extraction Metadata

必须记录：

- `method = llm_code_reading`；
- provider/model；未知时显式写 `unknown`，不得猜测；
- prompt version、schema version、extractor version；
- run ID 和生成时间；
- context manifest 及总哈希；
- temperature/seed（不可用则为 null）；
- human review status、reviewer 和时间；
- leakage policy 和 isolation key。

## 15. 多维置信度

每个 L1–L3 Skill 使用五个维度：

1. `evidence_coverage`：关键 claim 被直接证据覆盖的程度；
2. `semantic_coherence`：trigger—operation—state—validation 是否一致；
3. `boundary_clarity`：适用、排除和原子边界是否明确；
4. `validation_strength`：测试/运行 oracle 的独立性和强度；
5. `cross_repository_support`：跨任务、跨仓库支持程度。

默认 `overall = min(dimensions)`，避免平均值掩盖短板。若人工做 conservative override，只允许降低 overall，并必须记录理由。硬质量门优先于数值：即使分数高，引用悬空、Pattern 只有一个 Workflow 或 validated 无 held-out 结果仍不得晋级。

Atomic Skill 和单仓库 Workflow 的 `cross_repository_support` 应为 `null`（不适用）；`overall` 取所有非空适用维度的最小值。该维度主要约束 Pattern promotion。

## 16. 生命周期与晋级门

### candidate

- schema 和语义引用通过；
- 所有 observed Claim 有 Evidence；
- 不要求人工确认。

### reviewed

- 人工确认边界、主要 claim、证据和验证契约；
- 无 unresolved critical warning；
- Pattern 至少两个 Workflow；若声称 cross-repository，至少两个 repository。

### validated

- 满足 reviewed；
- 至少一个严格 held-out 任务；
- target solution 在执行时为 prohibited 或 not_provided；
- 记录成功、失败和 token/cost（如果真实可得）；
- Pattern 的 mandatory skeleton 在 held-out 中得到验证，或失败被记录为反例并重新降级。

### deprecated

必须有 deprecation reason、replacement（若有）和生效版本。Deprecated 节点可供审计，不应进入默认执行检索。

## 17. 图节点和边映射

### 17.1 节点

- Pattern、PatternStep；
- Workflow、WorkflowStep；
- Atomic Skill（现有代码中的 Action）；
- Commit/Hunk/其他 Evidence；
- Predicate/Validation/Binding。

### 17.2 跨层边

- `declares_step`：Pattern → PatternStep；
- `instantiates`：Workflow → Pattern；
- `has_step`：Workflow → WorkflowStep；
- `realizes`：WorkflowStep → PatternStep；
- `executed_by`：WorkflowStep → Atomic Skill；
- `conforms_to`：Atomic Skill → PatternStep；
- `evidenced_by`：Skill/Step → Evidence；
- `supported_by`：Pattern → Workflow；
- `applicable_when`：Skill/Step → Predicate；
- `verifies`：Validation → Skill/Workflow/Pattern；
- `grounds`：Binding → PatternStep/Atomic Skill。

### 17.3 同层正关系

`requires`、`enables`、`precedes`、`validates`、`repairs`、`alternative_to`、`specializes`、`composes_with`、`requires_pattern`。

冲突、排除、失败和 supersession 默认作为 predicate、counterexample 或 lifecycle metadata，不作为普通正向扩散边。这样可避免 graph propagation 把“不适用”节点当相关正证据放大。

## 18. ID、版本与去重

- ID 在同一 bundle 内全局唯一，建议 `<type>:<sha256-prefix>`；
- Evidence ID 优先内容寻址；语义节点 ID 由规范化核心字段哈希生成；
- 文案调整不改变主语义时增加 patch version；trigger、operation、边界或 mandatory skeleton 改变时增加语义版本；
- 去重分三层：证据内容哈希、Atomic Skill transformation signature、Pattern skeleton signature；
- 向量相似只能产生 merge candidate，最终合并需比较 trigger、state、invariant 和 validation；
- merge 必须保留 alias、来源版本和冲突字段。

## 19. 科学评估

### 19.1 数据划分

按 episode/PR 划分，不能按 hunk 随机划分。跨仓库实验应报告：

- in-repository held-out；
- cross-repository held-out；
- time-split held-out；
- task-family transfer。

### 19.2 对照组

至少比较：

1. no Skill；
2. nearest commit/episode；
3. flat lexical/vector Skill；
4. graph Skill；
5. graph Skill + cross-repository Pattern。

检索消融包括 lexical、exact vector、HNSW、hybrid、one-hop、bounded graph、reverse-aware PPR 和 mandatory closure。HNSW 只影响候选召回效率，不改变 Skill 的语义有效性。

### 19.3 指标

- 任务成功率与测试通过率；
- 首次有效定位时间；
- 修改正确性和回归数；
- 输入/输出 token（真实计量，不用字符代理冒充）；
- Skill 检索 precision/recall/nDCG；
- routing、hydration、graph expansion 延迟；
- 跨仓库迁移成功率；
- 反例率、误适用率和人工审计一致性。

每次实验记录 bundle/version、模型、prompt、环境、seed、预算和 target solution access。

## 20. 机器校验分层

### JSON Schema 可校验

- 类型、枚举、必填字段、字符串格式；
- observed Claim 至少一个 evidence ID；
- Pattern 至少两个 supporting Workflow；
- validated Pattern 至少包含 held-out result；
- confidence 范围；
- 数组最小数量与去重。

### 语义验证器必须校验

- 所有 ID 唯一且引用存在；
- Claim evidence、Workflow action/step、Pattern realization、Validation/Binding 无悬空；
- Workflow 和 Pattern 主排序边无环；
- edge endpoints 类型正确；
- Pattern support 与 realization 一致；
- evidence diversity 与真实 supporting Workflow repository 一致；
- observed/generalized claim 的证据覆盖；
- overall 不高于任何质量维度；
- lifecycle promotion gate；
- validated held-out 结果满足泄漏隔离；
- cross-repository 声明至少两个 repository。

## 21. 最低交付要求

一个可进入下一阶段提取的规范实现至少应包含：

1. 本文档；
2. Draft 2020-12 JSON Schema；
3. 一个能通过 schema 与语义检查的模板；
4. 引用/DAG/promotion 语义验证器；
5. 自动测试：合法模板、非法 epistemic status、单 Workflow Pattern、悬空引用、环和伪 validated；
6. 每个真实提取 bundle 的 context manifest 与 review 状态。

满足这些要求之后，再开始按 task family 逐组读取多个 harness 的真实代码，独立形成 L1、L2，最后归纳 L3；不得先写 Pattern 再把案例硬塞进去。
