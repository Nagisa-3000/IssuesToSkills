# Pattern、CrossBind 与 Ranker 的实际完成度（2026-10-05）

目标尚未完成。M0–M3 有代码和契约测试；真实跨项目泛化、有效 Ranker 训练、正式冻结和 SWE 效果验收仍未完成。最新核对及续作证据见本文末尾与 [v4 状态快照](results/pattern-crossbind-ranker-current-status-20261005-v4.json)。较早各节的数字保留其当时的快照含义。

| 阶段 | 已有内容 | 尚未满足的验收 |
| --- | --- | --- |
| M0 | Action/Pattern/Task 契约、实际输入与输出见证、绑定命令与工作区封印校验 | 原生 Action 功能案例未全部完成 |
| M1 | 单 Workflow 重写、保留来源与理由、历史不变；固定候选当前重绑定 | 新 Issue 和跨项目实际泛化未证明 |
| M2 | 语义边界切割、补前提、拼接、冲突与循环检查；两个父 Workflow、四个组合上限 | 真实跨项目组合收益未证明 |
| M3 | Workflow/Plan 两处排序、拒绝和先探查、统一预算 | 真实效果与完整开发集校准待完成 |
| M4 | 时间隔离与训练工具；接通 Workflow/Plan 两类效果监督 | 已有部分固定 Plan 执行标签但尚未合并；原监督训练非平局偏好为 0，有效训练与开发集校准未完成 |
| M5 | 冻结与评估工具 | 正式 KB、题目、模型、预算与协议未冻结 |
| M6 | 配对与消融入口 | 正式 SWE 运行仍为 0 |

## 本轮修正

验证 Action 的 Oracle PASS 需要真实当前绑定命令执行成功，且执行见证的工作区内容/权限封印与当前收据一致。超时、未执行、不同命令、过期封印不能通过。审查输入包含当前 Oracle 命令与完整义务。outcomes-recorded 输出允许含 FAIL/UNKNOWN；生成记录不等于修复接受。

历史评测 v3 在 Solver 结束后独立运行原始代码与 production-only 的已知历史修复，使用同一回归断言、运行时和测试身份。原始目标必须失败、原始对照必须通过、已知修复必须通过。不一致、缺失测试或执行不可用时排除效果监督，不把基础设施问题标为 Skill 失败。快照已重评 **9/9** 个历史题。旧轨迹与标签保留，重评结果另存。

此前 use_frozen_selection 只固定起始计划，刷新后仍调用候选生成。现在受控刷新保持原 Action、Pattern、父 Workflow，仅按当前证据更新绑定、依赖与验证；非法时回退。轨迹保留原候选身份，切换其他候选不能生成该候选的效果标签。

historical_plan_pool.py 冻结原计划、单 Workflow 重写与受限 CrossBind 搜索结果。相同执行结构去重，保留多种来源与拒绝报告。run_historical_ranker_supervision.py 支持 --candidate-kind workflow|plan|both，导出 plan-pools.json、数据集编译可用的 plans.json 与受控运行清单。--prepare-only 不发起 LLM 调用或修复执行，但使用真实本地 embedding 模型。九题候选池已完成：18 个 Plan、0 个两父 Workflow 组合、0 个当前已确认 Pattern；尚未产生 Plan 执行监督。未执行候选不标失败。没有合格当前 Pattern 时保留 None，不强制套用预设机制。

## 实际 Action 小实验

同一不可变、单项目两来源的 async-ast-classification-extension local_template 包：

| 场景 | 实际行为与审查 | 接受边界 |
| --- | --- | --- |
| q0：正确已完成修改 | Python 3.6.15 普通/异步碰撞、受影响注解套件通过；与真实公开的修改前源码比较；全部 authored checks PASS | 只覆盖明确执行与检查范围 |
| q1：错误作用域查找 | 异步目标实际抛出 Module.parent 异常、套件失败；两个 Oracle FAIL，运行时 guard 保持检查 FAIL | 有输出记录，修复仍不可接受 |
| q2：缺少必需旧解释器保证 | Python 3 当前目标与套件通过；没有必需 Python 2.7 执行见证；完整目标 Oracle UNKNOWN | 源码 guard 与 Python 3 通过不能代替必需执行 |

三例均保留真实命令、输出、源码与来源。独立上下文审查使用同一模型家族，不能称为独立模型或独立跨项目泛化。未执行的 Python 3.7/PyPy 等环境不记为通过，整项目回归未执行。包未正式入库或晋升。其他 scope-inspect/scope-edit 和 overload 功能验收仍待完成。

详细证据：[Action 三例审查](results/native-scope-validation-independent-functional-audit-20261005-v1.json)。前两个审查驱动的统计接口/预算失败保留，未形成语义标签；v3 使用包含完整重复见证的独立审查预算，不作为正式配对实验预算。

## 验证与当前数据状态

完整测试：**451 passed、19 skipped**。额外权限下的 copied namespace、Broker 与 Solver 子集：**32 passed、5 skipped**；另外的 Action 记录子集：**4 passed、0 skipped**。普通运行的跳过项包括无特权 Broker/namespace 的环境限制；额外权限下仍跳过的 5 项为服务器不支持的 user namespace 路径。跳过不计为通过，真实 copied namespace 路径已执行。本轮 Python 文件 Ruff E4/E7/E9/F 通过；全仓库此前 211 项既有发现未在本轮清理，不宣称全仓库 lint clean。

Pylint 历史资格快照：**1095/1160** 已处理，**73** 个 verified_resolution；全历史资格未完成。Pylint、Pyflakes、Ruff 的 9356 个历史 Issue 范围、T=2024-01-01、τ=2021-01-01 保持；已暴露的 Pylint #10034 排除正式评估。新作者目录保持原样，不批量提交或晋升。

候选池与重核详情：[双入口监督准备](results/historical-dual-ranker-supervision-preparation-20261005-v1.json)。本地 embedding 的九个推理批次与零次 LLM 调用分别记录。

机器可读快照：[当前状态](results/pattern-crossbind-ranker-current-status-20261005-v3.json)。运行路径与快照不代表最终计数；仍需补全原生功能验收、产生有效 Plan 执行监督和训练非平局偏好，再训练/校准，最后冻结并执行正式 SWE 配对与模块消融实验。

更新后的历史 Workflow 监督：24 个样本、21 对偏好，训练非平局偏好为 0，Plan 执行样本为 0。监督更新未触发新权重训练，也未完成 M4 验收。

## 冻结候选池执行入口的后续验收

历史监督 CLI 新增 --prepared-dir；该模式要求 --candidate-kind plan，复用既有候选池和调度，不重新检索、重写、组合或重建检索索引。执行阶段可以记录自己的模型、运行时和代码版本，候选来源仍指向原准备文件的 hash。

加载时核对公开题目、时间边界、来源包、父 Workflow、Pattern 来源、候选投影与完整调度。候选缺失、非候选身份、未知分支类型、无效采样概率、路径越界及文件篡改被拒绝。每个分支仍在执行前按当前契约重新检查；旧的 PASS/UNKNOWN 报告不会直接授权修改。

真实九题复用核验完成：18 个 Plan、27 个计划执行分支（9 个无指导基线与 18 个 Plan）；所有原始准备文件保持不变，候选生成未重执行。该核验为只读准备验证，LLM 调用、embedding 推理批次、Solver 执行和正式 SWE 运行均为 0。

本轮相关测试为 32 passed，无跳过；修改文件 Ruff E4/E7/E9/F 与 git diff --check 通过。这是新增入口的测试结果，不替换前述完整测试记录，也不构成修复效用验收。

[当前入口的真实候选池核验](results/prepared-plan-execution-readiness-20261005-v2.json)记录代码 hash 和准备文件来源；[先前核验](results/prepared-plan-execution-readiness-20261005-v1.json)保留其较早代码状态。M4 的有效训练、M5 的正式冻结及 M6 的正式实验仍未完成。

## 固定候选的历史 Plan 效果监督执行

已启动固定代码快照下的 27 个历史分支：九个无指导基线与十八个 Plan，单工作线程，实际 copied namespace 隔离和 Solver 结束后的独立验收。此研究为历史开发监督，正式 SWE 运行仍为 0。

首次启动在任何 Solver 执行前终止：复制 inventory 改变了相对 package_path 的解析位置，来源身份 hash 核对失败。保留该记录，不生成修复失败标签。修正后的运行使用内容 hash 固定的原始 inventory 来源位置；九题、十八个 Plan 在特权环境下重新预检通过，候选池保持原身份。

[修正后的运行快照](results/historical-frozen-plan-execution-launch-20261005-v2.json)确认驱动及执行进程存活，完整调度为 27 个分支；该快照完成分支和 Plan 标签均为 0，不提前宣称效果监督或 Ranker 训练完成。[首次终止记录](results/historical-frozen-plan-execution-launch-20261005-v1.json)单独保存。实验使用提交 648f005 的固定代码，后续文档提交不改变运行中的实验。

## 本次续作核对：实现可用，M0–M6 完整验收仍未完成

快照时间：2026-10-04T19:29:14.961559+00:00（UTC）；续作前服务器 main、origin/main 与 GitHub HEAD 均为 a621fd1e6aa30a6638e25e9c309b514c8683d8fe。本轮保留未审阅的 pyflakes-mechanism-history-v5 作者目录，运行中的历史 Plan 研究继续使用提交 648f005 的固定代码。

M0–M3 的实现、契约与错误组合测试已经存在；这不意味着原生 Action 的所有功能案例、真实跨项目 Pattern 重写与两个父 Workflow 的组合已经验收。M4 的历史监督和本地语言模型排序头/可选 LoRA 训练工具已经接通，但尚未接受有有效训练信号的最终 Ranker。M5 正式冻结与 M6 正式配对 SWE/模块消融实验仍未完成，正式 SWE 运行数为 0。

固定候选研究在该快照完成 **21/27** 个分支，已有 **14** 个 Plan 执行标签。完整的 7 个历史题三分支中，无指导基线解决 6/7，两个 Plan 分支合计解决 12/14。当前候选池的已确认 Pattern 数和两个父 Workflow 组合数仍为 0。

已完成 Plan 标签仍是初始操作校验的 probe_only；这些标签不是独立专家对机制适用性的监督。实际收据显示 Plan 的探查义务已交付，完成分支内共记录 14 次条件指导回退，原生 Action 记录共 0 条。结果不能用来宣称重写、CrossBind 或 Skill 提升了 SWE 修复率。新 Plan 标签尚未合并进训练数据；相同或不可用结果仍须保留平局或未知，不能人为制造赢家。

Pylint 本轮资格核验已终态完成：去重后的 **1160/1160** 个候选全部处理，原始别名请求为 1319；**78** 个修复满足当前因果验证标准。5273 个 Pylint 历史 Issue 的时间可用正文/讨论记录已只读核对，全部 78 个验证来源通过原生抽取前置校验。未通过/不可执行的其余候选仍保留其理由和报告，当前验证范围为变更测试文件，不代表整个历史库已完成资格认定、跨项目验证或正式入库。[全部合格来源抽取预检](results/pylint-native-extraction-readiness-20261005-v1.json)记录零次 LLM 调用、零个新生成包。

真实 Pylint 原生 Skill 作者队列已启动：等下述 Action 队列结束后，用单工作线程处理完整的 1160 个候选记录，对全部 78 个合格来源调用现有 extract_verified_history_skills.py，其余记录明确 defer。不按预设问题族或任意 top-N 缩减。输出将位于 data/skill-extraction/packages/candidates/pylint-observable-history-v1-20261005；本快照仍在等待，尚未生成包。新包仅为候选，功能 eval 定义仍是 not_executed，不自动晋升。

新增 prepare_native_overload_functional_cases.py 从精确 Git blob 导出固定的只读开发 fixtures，使用实际当前的输入可用时间。三种代码状态在真实 copied namespace 中执行了 **6 个** counterpart/受影响注解套件命令：同步通过而异步失败、同步异步均通过、两者均因受控装饰器身份错误失败。普通非 overload 重定义的诊断类型和位置在三例中一致；只读快照保持不变。观测包装只记录识别器输入/输出并原样返回原识别结果，不把预期标签写给 solver。

这一步校准了行为，尚不是原生 Action 执行或功能验收。四个原生 overload-inspect 例子的代码已独立封印并进入串行执行队列，包括命令不可执行的第四例。eval_native_action_observation.py 的开发控制先做真实隔离预检，再把被禁的命令记录为 execution_available=false、exit_code=null，不伪造探查结果或成功状态。代码哈希、原生包哈希、实际命令和范围见 [v4 状态快照](results/pattern-crossbind-ranker-current-status-20261005-v4.json)。队列本快照等待历史研究结束；独立审查、overload-edit/validate 及全套原生功能验收仍待完成。

本次 Action 执行与证据审查回归为 **45 passed，0 skipped**；修改 Python 的 Ruff E4/E7/E9/F 和 git diff --check 通过。此前完整测试 451 passed、19 skipped 的记录保留，本次未重复运行完整套件，不把跳过计为通过。

后续仍须：完成原生功能案例并独立审查；从真实独立跨项目来源形成机制及互补 Action；生成时间隔离且有效的 Workflow/Plan 监督并训练、校准；随后统一冻结知识库、题目、模型、预算和协议，最后执行正式 SWE 配对、模块消融及相同冻结候选池的 Ranker 比较。详见 [机器可读 v4 快照](results/pattern-crossbind-ranker-current-status-20261005-v4.json)。
