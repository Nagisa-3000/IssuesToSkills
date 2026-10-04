# Pattern、CrossBind、Ranker 当前验收状态

日期：2026-10-04。**尚未全部完成。M0–M3 已有实现和契约测试，M4–M6 尚未通过完整验收。正式 SWE 运行数为 0。** 本文依据[机器审计 v2](results/pattern-crossbind-ranker-current-status-20261004-v2.json)，更新[原设计](pattern-crossbind-ranker-design-20261003.md)的实施状态。包结构、历史修复资格、Action 功能验证、正式知识库准入和 SWE 修复收益分别统计。

| 阶段 | 已有实现与证据 | 尚未完成的验收 |
| --- | --- | --- |
| M0 契约与来源 | Action/Pattern/Task/Plan、输入输出、来源和包 hash、时间与公开输入边界；实际输出复核、执行前提门槛；内容与权限封存；命令越界整体回滚 | 原生 Action 功能案例完整验收及正式知识库准入 |
| M1 Pattern 重写 | 当前绑定、必要效果补齐、删除/替换/重排记录、偏序 DAG；历史包保持不可变 | 真实跨项目机制与独立新 issue 的泛化证据 |
| M2 CrossBind | 两个父 Workflow、四个组合候选的限制；切割、状态匹配、桥接、冲突/环/验证闭包检查 | 真实跨项目组合执行和修复收益 |
| M3 prompted Ranker | 原始 Workflow 与 Task Plan 两处排序；硬门槛、拒绝/仅探查/弃权和预算检查 | 充分的历史开发集校准与真实修复收益 |
| M4 历史训练 | 时间隔离监督工具、pairwise 训练与 checkpoint 重载工具；4 个训练 query、5 个开发 query 的小规模 checkpoint | 非平局训练偏好对仍为 0；效果监督核对未完成；原数据仅有 Workflow 候选，Plan 监督不足 |
| M5 正式冻结 | 冻结与来源校验工具 | 三仓全历史资格、正式题目并集、知识库/模型/阈值/预算/真实 embedding/环境/官方 evaluator 尚未一起冻结 |
| M6 正式实验 | 对照、消融和同一冻结候选池排序比较的运行工具 | 正式 SWE runs = 0；没有可报告的修复成功率或模块收益 |

本次补齐了修改命令的实际写入范围审查：只有当前事实、输入、绑定和 Oracle 支持的修改 Action 可以写入；越界时，命令造成的全部工作区修改回滚，包括原本允许的修改。严格 Action catalog 与已选择计划同时存在时，写入范围取交集。允许创建声明文件所需的新父目录，但不能顺便修改已有父目录的权限。范围检查计入工具预算。

新 Action 记录使用 observation v3，封存文件内容、链接、目录和 Unix 权限，包括根目录。旧 v2 记录保留其原 hash 定义，不静默转成当前可执行事实。带已复核执行状态的 TaskContext 进入隔离副本时，先核实归档内容完全一致，再保留已验证权限；内容不同必须拒绝。未执行的命令保留 UNKNOWN，并移除上一条“最后探查通过”的事实。已获准 Action 的无效输出记录可以被拒绝并纠正，拒绝记录本身不能充当工具证据。

真实历史来源校准仍使用固定的 Pyflakes v4 local_template：一个项目、两个历史来源。它不是跨项目 Pattern，也没有进入正式知识库。[干净 scope-edit 独立复放](results/native-scope-edit-independent-review-20261004-v2.json)确认实际修改只涉及两个声明文件，目标和受影响测试通过，已有 parent traversal、诊断断言及可执行位保留。原始输出仍是 unvalidated；这一复放不能代替 scope-validate 或全包验收。

[scope-validate 实际执行审计](results/native-scope-validation-mechanical-audit-20261004-v1.json)记录了目标/普通对照、annotation suite 和不可用兼容性检查。q0 的目标与受影响 suite 通过，但 Solver 对历史不变量保留及完整运行时兼容性证据仍保留 UNKNOWN，不能把它标成全通过。q2 的目标与 suite 通过，要求的 Python 2.7 命令没有执行，exit_code=null、execution_available=false，因此必须是 UNKNOWN。两者均输出 outcomes-recorded，未修改源文件或预期。

q1 在受控失败输入上实际复现了 Module.parent 异常和 suite 失败。v2 尝试将 guidance refresh 引用为工具证据，记录被拒绝；修正 broker 后的 v3 复验在第 8 次模型请求遇到 HTTP 429，在输出记录前停止。这属于模型调用失败，不能当作 Skill 功能失败或功能通过。原生包定义的六个完整功能案例尚未全部逐项覆盖，本审计保守计完整通过 0/6；overload 三个 Action 的完整实际校准仍未完成。最初三个在快照检查前退出的启动也已[单独记录](results/native-scope-validation-launch-failure-20261004-v1.json)，模型调用为 0，不能混入成功数。

本次最终完整测试 **431 passed、19 skipped**。以特权 broker 执行 copied namespace 与协议专项测试 **27 passed、0 skipped**：其中 16 项是实际 copied namespace 测试，其余 11 项是协议 fixture。修改文件的 Ruff E4/E7/E9/F 检查和 git diff --check 通过。全仓 Ruff 仍有 211 条已有问题，与已提交基线逐项一致，本次未增加；不能描述成全仓 lint 通过。

历史调查范围仍为 Pylint 5273、Pyflakes 501、Ruff 3582，共 9356 个历史 issue。资格复验尚未完成，本次 Pylint 快照为 881/1160、verified_resolution 39，full_history_qualified=false。新的作者任务完成 7 个机制组，其中 6 组输出候选包、1 组延期，均为 definition-only，不能因生成文件就准入正式服务。生成物保留在服务器，不在本次审计中盲目提交或晋升。

继续按以下依赖推进：补齐原生 Action 的公开基线与兼容性证据及完整功能案例；完成三仓历史资格和有依据的机制归纳；逐 query 重建时间隔离的适用性与独立执行效果监督，并覆盖两个排序入口；训练及开发集校准；冻结 M5；最后执行正式 B0–B4/E0–E3 与同候选池排序对照，报告修复、回归和成本。正式题及隐藏结果不参与训练或校准。
