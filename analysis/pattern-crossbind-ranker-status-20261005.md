# Pattern、CrossBind 与 Ranker 的实际完成度（2026-10-05）

目标尚未完成。M0–M3 有代码和契约测试；真实跨项目泛化、有效 Ranker 训练、正式冻结和 SWE 效果验收仍未完成。本轮起点 a989be803952f532579b78904bf1589730543ab9 与重新 fetch 后的 origin/main 一致。

| 阶段 | 已有内容 | 尚未满足的验收 |
| --- | --- | --- |
| M0 | Action/Pattern/Task 契约、实际输入与输出见证、绑定命令与工作区封印校验 | 原生 Action 功能案例未全部完成 |
| M1 | 单 Workflow 重写、保留来源与理由、历史不变；固定候选当前重绑定 | 新 Issue 和跨项目实际泛化未证明 |
| M2 | 语义边界切割、补前提、拼接、冲突与循环检查；两个父 Workflow、四个组合上限 | 真实跨项目组合收益未证明 |
| M3 | Workflow/Plan 两处排序、拒绝和先探查、统一预算 | 真实效果与完整开发集校准待完成 |
| M4 | 时间隔离与训练工具；接通 Workflow/Plan 两类效果监督 | 原 4 train/5 dev 的训练非平局偏好为 0、Plan 样本为 0；新 Plan 执行监督未完成 |
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
