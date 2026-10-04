# Pattern、CrossBind 与 Ranker 的实际完成度（2026-10-05）

**目标尚未全部完成。M0–M3 已有实现和契约测试，真实功能、跨项目重写与组合验收仍不完整；M4 尚无合格的训练 Ranker；M5 尚未正式冻结；M6 的正式 SWE 运行仍为 0。**

最新机器快照为 [v9](results/pattern-crossbind-ranker-current-status-20261005-v9.json)。[v8](results/pattern-crossbind-ranker-current-status-20261005-v8.json) 保留验证第二版运行前的状态。[v7](results/pattern-crossbind-ranker-current-status-20261005-v7.json) 及更早版本保留当时的状态，不随新结果改写。代码、真实 Action 验收、泛化效果分别统计。

| 阶段 | 已实现或实际完成 | 尚缺的验收 |
| --- | --- | --- |
| M0 | Action/Pattern/Task 契约；输入输出见证；主责任与辅助读写角色绑定；来源/包 hash；工作区内容与权限封存；独立输出复核与状态保存；显式封存状态接续 | 原生编辑、验证 Action 的完整正反例功能验收，跨项目可用性 |
| M1 | 单 Workflow 重写；当前依赖 DAG、必要效果、不变量；历史 Workflow 不变，每项重写保留来源及理由 | 新 Issue 上确认真实 Pattern，执行重写并证明收益 |
| M2 | Bind/Cut/Match/Bridge/Compose/Validate；PASS/FAIL/UNKNOWN；冲突、循环与验证完整性检查；最多两个父 Workflow、四个组合候选 | 真实互补来源的两父组合执行及独立效果验证 |
| M3 | Workflow 与 Plan 两处 prompted 排序；准入失败、拒绝全部、先探查；按缺失角色补召回 Action；共享预算 | 开发集校准及真实效果验证 |
| M4 | 按题时间隔离；修复、别名和复制来源排除；两类候选监督与训练工具；42 条执行观察和 42 条获接受的适用性标签已合并为 84 条观察 | 有效正负适用性监督、有依据的非平局排序偏好、合格训练权重及校准 |
| M5 | 正式冻结和独立评估工具 | KB、题目、模型、预算与验收协议的联合冻结 |
| M6 | 配对修复、模块消融及冻结候选池排序比较入口 | 正式 SWE 配对实验和消融尚未运行 |

## 当前最重要的实验结果

历史开发实验完成 **27/27 分支**，包括 9 个基础 Agent 分支和 18 个冻结 Plan 分支。基础 Agent 修复 **7/9**，Plan 分支修复 **14/18**；逐题看，三个分支的修复结果相同。固定池没有已确认 Pattern、两父 Workflow 的组合或原生 Action 执行记录，指导分支探查后回退。**这没有建立 Skill、重写或 CrossBind 的修复收益。** 原固定代码和结果保留，未用新实现改写原实验。

全部 **42/42 候选/问题组合**已完成适用性提案及独立上下文复核，共 **84 次实际模型调用**；42 个标签全部获接受，全部为 **unrelated**，其中 24 个 Workflow、18 个 Plan。每项检查机制、责任边界、前提、反例、绑定及验证，并引用封存的双侧证据。详见 [完整复核审计](results/historical-applicability-completed-review-audit-20261005-v2.json)。这些是同一模型族的独立上下文判断，明确记录 human_reviewed=false、independent_model_family=false，不是人工或跨模型判定，不建立修复 utility。

[最终监督合并审计](results/historical-dual-supervision-merge-audit-20261005-v11.json)核验每个接受标签的原始证明、完整人口、历史因果对照及所有时间/候选身份。合并仍使用原冻结编译器，验证公开输入、候选、catalog hash 和时间切分保持一致。新数据为 **84 条观察：42 条执行监督 + 42 条适用性监督；40 条训练观察、44 条开发观察**。执行观察的 applicability 继续为未知，不能由操作模式推断；适用性标签也没有被填上执行结果。历史修复和隐藏断言仅供离线标签评估，不进入 Ranker 的公开输入。

偏好仍为 **30 对：训练 16 对全部平局；开发 13 对平局、1 对非平局**。没有把未执行候选标失败，没有制造优先级来训练，没有新合格 Ranker 权重。该候选池支持拒绝错误经验的监督，尚不提供选择有效修复经验的充分信号。需要先获得真实可适用、可适配的经验和效果差异，再训练排序。v10 合并器误读终止字段而退出的版本保留，0 次模型调用；v11 已实际编译成功，耗时 326.34 秒，0 次合并模型调用。

## 原生 Action 闭环的实际边界

原生包仍为 Pyflakes 的两来源 **local_template**，不是跨项目 Pattern，未晋升正式 KB。overload-inspect 四场景已完成独立复核：[v5 审计](results/native-overload-independent-functional-review-audit-20261005-v5.json)。q0 的五项 authored checks 全部 PASS，确认一个只读、修改前的 overload-review；已有 async-aware gate、其他装饰器机制及执行不可用三个边界均拒绝确认。不可用场景的领域状态仍为 UNKNOWN。这证明诊断输出及拒绝边界，不能证明修复或泛化。

编辑场景的前三次真实准入各用 1 次模型调用，并因多余未来检查、嵌套 argv、拼接符号名被拒绝；全部版本保留，没有由 host 过滤字段或填 PASS。第四版实际用 **8 次模型调用**修改两个文件，产生 **1695 字节 patch 和 1 个 overload-change 记录**。公开探针的语义输出和 3 个定向测试提供了当前范围内的支持，但 solver 随后耗尽共享 token 预算，未正常结束，不能计为已完成修复。

独立复核在单独 checkout 精确重放实际 patch，并核对内容和权限封印。旧的修改前事实、绑定、端口与语义检查按锚点变化失效。两版输出复核共 **4 次实际调用**，均确认异步分类扩展、新增回归覆盖和 post-edit/unvalidated 输出端口；普通函数行为与相邻诊断有支持，编辑 Oracle、运行时兼容性和下游语义仍为 UNKNOWN。完整 policy 未获接受：第一版缺少执行时的认证输入并发生引用协议失败；第二版保留了 correct_confirmation 与 UNKNOWN domain_state 的矛盾响应。没有改判或删除失败结果。见 [v1 审计](results/native-overload-edit-output-review-audit-20261005-v1.json) 和 [v2 输入上下文审计](results/native-overload-edit-output-review-audit-20261005-v2-input-context.json)。

评估 CLI 现在保存独立复核后的 Task，并把执行时的认证输入与修改后状态分开、使用不同的证据命名空间。只有接受的记录复核才能产生当前输出事实；存在输出端口不能代替未完成的功能 Oracle。

验证 Action 的第一版真实 grounding 完成后，在工具启动前失败：solver 重新导出 pinned Git base，不能接续实际封存的修改后内容。其原始调用 metadata 在未处理异常前未写出，该限制已单独记录：[bootstrap 失败审计](results/native-overload-validation-bootstrap-failure-audit-20261005-v1.json)。未执行验证命令，0 个验证 Action 记录，不能统计为验证通过。

新增**显式接续**入口只允许一致、未陈旧的执行封印，并复制精确公开内容与权限，排除 Git metadata、拒绝外部链接并复验复制期间变化。正式入口的默认 pinned-base 行为保持原样。真实封存输入的[确定性交接对照](results/native-overload-validation-state-transfer-control-20261005-v1.json)通过：默认入口仍拒绝修改后的 checkout，显式入口的封印与实际执行记录一致。该对照为 0 次模型调用，不能当作 Action 功能验收。native 验证第二版已实际完成：**5 次模型调用、1 个真实验证记录、solver 正常结束、0 字节新增 patch**。两个绑定命令分别真实执行、退出码均为 0、未超时；公开目标和非 overload 控制通过，受影响的 type-annotation 模块 **24 项测试通过**，工作区封印保持不变。见 [真实执行审计](results/native-overload-validation-exercise-audit-20261005-v2.json)。

其[独立复核](results/native-overload-validation-independent-review-audit-20261005-v2.json)实际用 **2 次调用**，确认 public-validation-observed、async-target-behavior-correct、overload-suite 和 outcomes-recorded 输出；运行时兼容性、下游语义及完整 target-and-controls Oracle 仍为 UNKNOWN。policy verdict 为 **PASS / correct_refusal**：Agent 正确保留未知、拒绝重复修改和过度确认。领域状态仍为 UNKNOWN，**完整功能验收仍未通过，包未晋升**。这建立了同项目定义演练中的诊断→编辑→只读验证状态传递及拒绝边界，未建立新 Issue 泛化、跨项目迁移或 SWE 效果。

## 工程检查、数据范围与剩余验收

当前最终实现完整测试 **566 passed、19 skipped**；接续及相关定向测试 **52 passed、5 skipped**。修改文件的 Ruff E4/E7/E9/F 与 git diff --check 通过。跳过项不计为通过，工程检查不能替代泛化、修复效果或 SWE 验收。

历史范围保持 Pylint 5273、Pyflakes 501、Ruff 3582，共 **9356 个 Issue**。主截止 T=2024-01-01T00:00:00Z，训练截止 τ=2021-01-01T00:00:00Z，均为严格时间边界。已暴露的 Pylint #10034 继续排除正式评价。

Pylint 资格流程已处理 1160 个规范化候选，得到 78 个 verified 来源，资格范围是修改测试，不能描述为整项目完整验证。针对全体合格来源的抽取不设预定族或任意 top-N。结构合法的包继续属于 definition_only_not_executed。未审阅的 pyflakes-mechanism-history-v5、Pylint authoring 输出与全部失败版本保留，未批量提交或自动纳入正式 KB。

剩余工作是：完成原生编辑/验证的真实正反例；核验 Pyflakes/Pylint/Ruff 的共同机制与互补 Action，并执行真实两父组合；获得有效适用性和效果监督后训练、校准；最后联合冻结 KB、模型、题目、预算和验收协议，执行正式 SWE 配对及模块/Ranker 消融。目标仍未完成。
