# Pattern、CrossBind 与 Ranker 的实际完成度（2026-10-05）

**目标尚未全部完成。M0–M3 已有代码和契约测试，真实泛化与组合验收仍不完整；M4 尚无合格的训练 Ranker，M5 尚未正式冻结，M6 的正式 SWE 运行仍为 0。**

当前机器快照为 [v7](results/pattern-crossbind-ranker-current-status-20261005-v7.json)。[v6](results/pattern-crossbind-ranker-current-status-20261005-v6.json) 保留引用协议实跑前的状态。[v5](results/pattern-crossbind-ranker-current-status-20261005-v5.json) 保留当时的状态；其中 v9 数据集仍在编译、原生 Action 的 v3 复核仍排队等描述已由以下实际结果更新。

| 阶段 | 已实现或实际完成 | 尚缺的验收 |
| --- | --- | --- |
| M0 | Action/Pattern/Task 契约；输入输出见证、当前绑定、工作区封印、来源与包 hash；精确 Git root/HEAD 验证 | 原生编辑及验证 Action 的完整功能案例、跨项目可用性 |
| M1 | 单 Workflow 重写；依赖 DAG、必要效果、不变量检查；历史不可变，每项变化保留来源和理由 | 在新 Issue 上确认真实 Pattern，执行重写并证明收益 |
| M2 | Bind/Cut/Match/Bridge/Compose/Validate；PASS/FAIL/UNKNOWN、冲突与循环检查；两个父 Workflow、四个组合候选上限 | 真实互补来源的两父组合执行、独立验证与效果证据 |
| M3 | Workflow 与 Plan 两处 prompted 排序；准入门槛、拒绝、先探查、受限 Action 补召回与统一预算 | 完整开发集校准、真实效果验证 |
| M4 | 逐题时间隔离、修复/别名/复制来源排除、两类候选监督与训练工具；42 条真实执行观察已编译；全部 42 个适用性证据包已封存 | 获接受的独立适用性标签、有效训练偏好、合格训练模型与校准 |
| M5 | 正式冻结和独立评估工具 | 正式 KB、题目、模型、预算和验收协议的联合冻结 |
| M6 | 配对修复、模块消融和冻结候选池排序评估入口 | 正式 SWE 配对实验与消融尚未运行 |

历史开发实验已结束：**27/27 分支**，包括 9 个基础 Agent 和 18 个冻结 Plan。基础 Agent 修复 **7/9**，Plan 分支修复 **14/18**；每道题的三个分支修复结果一致。该固定池没有已确认 Pattern、两个父 Workflow 的组合或原生 Action 执行记录。指导分支提供探查义务后回退。这是历史开发监督，不能证明 Skill、重写或 CrossBind 提高了 SWE 修复率。原始固定代码和结果保留，未重跑或改写原实验。

v9 数据集编译已实际成功（311.58 秒，0 次模型调用）：**42 条执行观察**，包括 24 条 Workflow、18 条 Plan；20 条训练观察、22 条开发观察，形成 30 对偏好。训练侧 **16 对全是平局**；开发侧 13 对平局、1 对非平局。执行标签的 applicability 均为未知，operational_mode 与经验适用性分开。没有把未执行候选标失败，也没有制造非平局来启动权重训练。v8 的 300 秒超时版本及原始输入继续保留。

新增 [适用性监督模块](../src/arex_skill_graph/applicability_supervision.py) 与 [历史复核 CLI](../experiments/review_historical_applicability.py)。每个候选分别检查机制、责任边界、前提、反例、绑定及验证；先提出带双侧证据引用的标签，再以原始证据和独立上下文复核。单次提案、UNKNOWN、拒绝及不完整的复核均不能创建标签。标签只监督 applicability，不产生 repair utility、execution outcome 或操作授权。实际复核仍使用同一模型族，明确记录 model_generated_label=true、human_reviewed=false、independent_model_family=false，不能称为人工或跨模型判定。

准备流程已对**全部 42 个冻结候选/问题组合**完成校验：候选与公开输入 hash 一致；按题重建或冻结目录；排除自身答案、同一修复、重复来源和已暴露题；重新准入原生包；公开代码从准确的 pinned base 读取，同时包含生产修复和回归断言所涉及的文件。历史修复、资格验证和独立因果对照只能进入离线标签评估器。准备包的复用还要检查完整候选集合、独立 oracle 的文件 hash、每个包的身份与封印，不能偷偷删题或换候选。此阶段 **0 次模型调用、0 个标签**。42 项真实复核在 Pylint authoring 的请求完成边界串行调度。v1 实跑发生引用协议失败：7 次实际模型调用、7 个拒绝响应、0 个接受标签；剩余 35 项未启动，不能标为失败候选。模型引用了包内 Episode/anchor ID，而接口只接受证据 artifact ID，详见 [保留的失败审计](results/historical-applicability-citation-failure-audit-20261005-v1.json)。该版本在无活动请求的完成边界安全结束，作者已恢复。现在明确提供可引用 artifact 清单，并把实际 ID 枚举及题目/候选身份写入每次响应 Schema；校验标准保持不变，没有由 host 替换引用或制造标签。v2 使用同一完整的冻结 42 项候选池重跑。截至当前快照，1 项已获接受，等级分布为 {"unrelated": 1}；这些标签尚未并入训练数据，也不建立修复效果。接受数量以快照中的 actual progress 为准，排队、协议修正及 Schema 测试均不算监督完成。

原生 overload-inspect 四场景实验已完成独立上下文复核，见 [v5 复核审计](results/native-overload-independent-functional-review-audit-20261005-v5.json)。原始演练为 **26 次模型调用**；该版复核为 **5 次调用**。q0 的五项 authored checks 全部 PASS，确认一个只读 overload-review；q1 已有 async-aware gate、q2 装饰器身份机制不同，均正确拒绝确认；q3 执行不可用，也正确拒绝，但领域状态仍为 UNKNOWN。四项 policy verdict 均 PASS。**这证明诊断输出与拒绝边界，不证明编辑成功、修复成功或跨项目泛化。**该包仍是 Pyflakes 的两个来源形成的 local_template，没有晋升正式 KB。

原生复核的 v1/v2 协议失败、v3 调用前被取代和 v4 的所有权失败均保留。v4 q0 实际是 Git 的 dubious ownership 导致无法读取身份，并非 fixture 使用了父项目 HEAD；四个 fixture 有各自独立、未变化的 Git HEAD。v5 使用准确的 broker owner 校验这些 fixture。代码现在区分“Git 身份不可读”与“HEAD 真正不同”，并拒绝未版本化目录继承父仓库的身份，未增加全局 safe.directory。

Pylint 资格流程已处理 **1160/1160** 个规范化候选，得到 **78** 个 verified 来源，范围是修改测试，不能描述为整项目完整验证。authoring v1 的必需协议资源缺失属于基础设施失败（0 包、0 次模型调用）。v2 针对全部合格来源串行抽取，不设预定族或任意 top-N。当前快照中的结构合法包仍是 **definition_only_not_executed**；不得把结构验证等同于 Action 功能验收或正式 KB 准入。pyflakes-mechanism-history-v5 的未审阅输出与其他失败版本继续保留。

当前完整测试 **525 passed、19 skipped**。新增适用性协议与 CLI 集成测试 **45 passed**；Task Git 身份及原生 reviewer 的当前变化也包含在完整测试中。修改 Python 文件的 Ruff E4/E7/E9/F 与 git diff --check 通过。跳过项不计为通过。这些结果验证工程行为，不确认泛化、修复收益或 SWE 有效性。

历史范围保持 Pylint 5273、Pyflakes 501、Ruff 3582，共 **9356 个 Issue**；主截止 T=2024-01-01T00:00:00Z，训练截止 τ=2021-01-01T00:00:00Z，均为严格时间边界。已暴露的 Pylint #10034 继续排除正式评价。

后续验收顺序仍是：完成原生编辑、验证 Action 的正反例；核验 Pylint 抽取并验证 Pyflakes/Pylint/Ruff 的实际共同机制及互补动作；获得有依据的适用性和效果监督后训练、校准；最后联合冻结并执行正式 SWE 配对与消融实验。在这些证据出现前，目标保持未完成。
