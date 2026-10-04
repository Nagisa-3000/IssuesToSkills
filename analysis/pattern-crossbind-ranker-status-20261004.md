# Pattern、CrossBind、Ranker 当前验收状态

日期：2026-10-04。对照 [原设计](pattern-crossbind-ranker-design-20261003.md)；详细数据见
[当前状态审计](results/pattern-crossbind-ranker-current-status-20261004-v1.json)。
当前目标未完成。M0–M3 的首版代码和契约/合成集成已具备；真实功能、历史监督与正式 SWE 效果须继续验收。

| 阶段 | 当前状态 | 尚未满足的验收 |
| --- | --- | --- |
| M0 契约与输入隔离 | Action/Pattern/Task/Plan、来源/hash/时间与公开输入边界已实现；新增实际输出复核和当前执行门槛 | 原生 Action 的完整功能验收 |
| M1 Pattern 重写 | 当前绑定、必要效果、替代/删减及偏序 DAG 已实现并有测试 | 跨项目原生机制及新 issue 泛化证据 |
| M2 CrossBind | 最多两个父来源、cut/match/bridge/compose 和冲突/验证闭包已有实现及测试 | 真实项目组合执行和修复收益 |
| M3 prompted Ranker | 原 Workflow 与 Task Plan 两个入口、拒绝、预算计量已有实现及测试 | 完整历史开发校准与实际排序收益 |
| M4 历史监督训练 | 时间隔离工具、小规模历史 checkpoint 训练/重载已运行 | 有效效用排序监督与两入口校准；现有非平局训练对为 0 |
| M5 正式冻结 | 冻结和审计工具存在 | 全历史资格、正式题目并集、模型/阈值/预算/运行时/官方 evaluator 尚未一起冻结 |
| M6 正式实验 | 正式 SWE runs = 0 | 配对修复、共享候选池排序、回归与成本、正式模块消融 |

历史 Workflow 和作者包保持不可变；当前重写是临时 Task Plan。包结构、图中计划 PASS、实际 Action 输出、
正式 KB 准入及新问题修复成功分别记录。当前没有可报告的正式 SWE 成功率或模块收益。

## 本轮执行语义修正

Action 输出必须复核实际 broker 记录、当前 artifacts、包/契约 hash 和公开工作区内容。
未复核/未知端口不能成为下一 Action 的输入；仅复核通过的实际输出和效果进入 TaskContext。
诊断 Action 观察到目标失败可以确认原因，但不会建立修复成功。
DAG 中预期的前序效果只用于条件性计划检查；实际修改仍要求当前前提、输入、绑定及 Oracle 可用。
指导编辑后须刷新；严格功能校准入口要求显式固定 Action catalog，回退不能绕过其执行前提。

当前工作区 seal 覆盖内容，不覆盖 Unix 权限；完整补丁的权限变化由独立审查另核对。
write_file 检查绑定的具体路径。命令修改的实际范围仍需执行后审查，尚未实现按 Action 写集自动回滚的命令事务。

## 真实历史来源的小校准

固定 Pyflakes v4 原生包包含 scope/overload 两个历史 realization，属于单项目 local_template。
[inspection 复核](results/native-scope-inspect-functional-review-20261004-v1.json)覆盖因果省略、已存在分类及执行不可用三种场景。
[输出复核 v2](results/native-scope-observed-output-review-calibration-20261004-v2.json)晋升实际 scope-review 和诊断事实，
保留目标 probe 的 exit 1；没有宣称修复通过。

[当前反例计划 v2](results/native-scope-current-negative-plan-review-20261004-v2.json)在 DAG、端口依赖、
写冲突和验证闭包均 PASS 时，因为实际已存在 async 分类、遗漏前提为 false 和缺少 confirmed 输入而拒绝。
原 v1 报告的缺依赖构造错误保留审计，未作为干净的拒绝证据。

[scope-edit 独立复核](results/native-scope-edit-independent-review-20261004-v1.json)复放 Solver 的完整真实补丁：
普通/async 公开 probe、注册表形状和受影响 annotation suite 通过，已有测试和 parent traversal 保留。
但完整补丁还包含 bin/pyflakes 与 setup.py 的无关可执行位丢失，因此该次 edit 验收 FAIL。
复制后端现已保留可执行位，真实隔离回归通过；仍需一次干净的 scope-edit 运行，随后执行 scope-validate。
缺少 confirmed 前提的另一个实际 Solver 场景保持无修改、无输出。

整个包的 6 个功能案例完成数仍为 0；scope-validate 和 overload 三个 Action 尚未完整执行。
这些是同模型族对历史来源定义的校准，不能用于估计新问题或跨项目泛化，也不准入正式 KB。

## 验证与后续

本轮完整测试：407 passed、17 skipped；另以特权 broker 实际运行 copied namespace 沙箱测试，14 passed、0 skipped。
Ruff E4/E7/E9/F 和 git diff --check 通过。跳过项未伪称执行通过。

接下来完成原生 Action 的实际功能闭环与全历史资格复验，建立有区分度、独立验收的逐 query 时间监督；
然后完成 M4 训练/校准，冻结 M5，再执行 M6。正式题和隐藏结果不参与训练或开发校准。
