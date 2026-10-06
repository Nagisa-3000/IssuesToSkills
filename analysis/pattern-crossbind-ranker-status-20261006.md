**尚未全部完成。M0–M3 有核心工程实现；来源独立支持计数已修正，完整工程测试为 979 passed、20 skipped。M4 缺有效监督和真正训练的 LLM Ranker，M5/M6 未验收，正式 SWE 仍为 0。**

本轮修正了“出现任何 alias 重叠就拒绝整个 Pattern”的错误。source ID、issue cluster、fix、revision、alias、copied-from 按传递关系合并；冗余证据保留、同组只计一份支持。至少两个独立组和所有既有机制/角色/必要效果/验证门槛继续适用，作者模型调用前也检查身份组件。真实 #5406 的两份修复与 #2729 的一份修复形成两个组。身份计数仍需结合独立因果审查，不能单独证明 Pattern 机制或功能。

| 阶段 | 已有工程与记录 | 尚未验收 |
| --- | --- | --- |
| M0 | 原生包和 Action/Pattern/Task/Plan 契约、来源/hash/时间/输入隔离；冗余来源按组件计数 | 完整知识库准入和全部包功能验证 |
| M1 | 按效果/角色/偏序生成当前 DAG，保留历史 Workflow 与改动理由 | 当前真实任务绑定、Pattern 重写执行和修复收益 |
| M2 | 六阶段 CrossBind、三态检查、两父四候选、前提/清理/验证闭包 | 真正互补两父组合执行与增量收益 |
| M3 | Workflow/Plan 两处 prompted 排序、硬门槛、拒绝/探查与共同预算 | 开发校准、同一冻结池的排序收益 |
| M4 | 原始 query/逐题 runtime/私有 evaluator 接入；21 分母；18 个逐题完整合格前缀、8 份私有审查输入封存 | 实际机制发现、更多合格 query、有效适用性/效果标签、真实 LLM Ranker 训练和校准 |
| M5 | 局部候选冻结与校验工具 | KB、任务并集、索引、模型、阈值、预算和协议联合冻结 |
| M6 | 配对修复与消融入口 | 正式 SWE 修复、回归/成本/模块消融和冻结池排序比较 |

[本轮工程与逐题准备](source-support-and-temporal-prefix-20261006-v1/README.md)保存 58 项针对性验证、979 项完整工程通过、20 项跳过和源码 hash，以及真实来源计数。逐 query 遍历全部 98 个已有 qualified native 包，在原始输入时间与 pre-2021 截点下执行完整时间/因果排除。16 个前缀有至少两组来源，形成 9 个精确不同语料；不足和未恢复输入均保留。准备实际模型、solver、机制生成和效用标签均为 0，完整全历史学习仍未完成。

当前 registry v3 保留 21 题，18 题有原始公开输入，资格仍为 1 题 ready（#470）、8 题独立审查待完成、9 题控制未通过、3 题输入缺口。8 题已完成独立审查器零调用预检，并启动绑定原作者进程终态的串行队列；具体当前观察状态见[进程快照](source-support-and-temporal-prefix-20261006-v1/live-jobs-snapshot.json)。准备或等待不产生 oracle 接受和效用标签。私有审查材料不会进入 actor 挂载。

[已完成候选与原始控制](original-query-supervision-20261006-v2/README.md)结论保持：18 题准备 104 分支（18 baseline、53 Workflow、33 去重 Plan）。33 个计划仍全部单 Workflow，0 个带 Pattern、0 个真正两父；入口 derivation 标签不是内容重写或拼接成功。registry v3 未覆盖旧 v2 候选池，仍拒绝隐式混用。

主截点完整语料的生成依赖最晚仍为 2023-06-18T14:43:15Z，不能回填早期题目。原串行作者任务和新审查队列均保留原句柄；队列在原作者终态及所有请求结束前不发模型请求。候选包生成和包结构校验仍不能替代功能 eval 或正式 KB 准入。

#470 既有配对实验仍只证明有限测试通过：Skill 组在生产修改前放弃历史指导，tokens 增加 20.54%，没有建立历史 Workflow、Pattern、CrossBind 或 Skill 修复收益。合格训练 Ranker 和正式 SWE 数均为 0。

[机器快照 v38](results/pattern-crossbind-ranker-current-status-20261006-v38.json)及[上一版报告](archive/pattern-crossbind-ranker-status-20261006-v37.md)保留未完成项。剩余工作是实际逐题机制学习、原生包功能资格、当前绑定/重写/互补组合、有效历史监督、真实训练与开发校准、联合冻结及正式配对和消融实验。
