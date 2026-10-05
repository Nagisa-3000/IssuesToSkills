**尚未全部完成。M0–M3 的核心工程实现已有验证，真实泛化和修复收益尚未验收；M4–M6 未完成，正式 SWE 运行数为 0。**

本轮补齐了完整失败草稿的原生文件修订入口。修订前重新加载来源包，重建并逐字核对原始作者请求，保留完整生成上下文、机制复审、来源资格和上游包 hash。模型只返回现有文件的完整替换内容；证据、provenance、Episode 和未改文件保持不变。修订后的完整包仍须通过原来的来源、时间、角色、效果、Workflow 连贯性和资源完整性检查。

完整工程测试为 **938 passed、20 skipped**，修改文件 lint/format 通过。这些测试和零模型调用预检不建立 Skill 功能验收或新 Issue 的修复收益。

| 阶段 | 已有工程实现 | 尚未验收 |
| --- | --- | --- |
| M0 | Action/Pattern/Task/Plan 契约；输入输出、效果、不变量、绑定、读写、验证、来源及包 hash；时间和因果隔离 | 全包功能验证、完整知识库准入 |
| M1 | 按角色、必要效果与偏序形成当前 DAG；历史 Workflow 不变，变更保留来源和理由 | 当前任务上的实际绑定、Pattern 重写执行与修复收益 |
| M2 | 六阶段 CrossBind；PASS/FAIL/UNKNOWN；前提、清理、验证闭包、冲突和循环检查；最多两父、四组合 | 真正互补的两父组合执行及增量收益 |
| M3 | Workflow/Plan 两处 prompted 排序、硬门槛、拒绝/探查、角色补召回及共同预算 | 有用的开发校准与同一冻结候选池上的排序收益 |
| M4 | 时间隔离监督与训练入口；原始公开状态保留、执行归因检查 | 原始 query/逐题 runtime/独立 evaluator 的统一接入；有用标签、非平局偏好、合格训练 Ranker及校准 |
| M5 | 冻结与校验工具 | KB、任务并集、索引、模型、阈值、预算和协议联合冻结 |
| M6 | 配对修复及消融入口 | 正式 SWE 修复成功、回归损害、成本、模块消融和冻结候选池排序比较 |

[本轮修订记录](native-authoring-revision-20261006-v1/README.md)记录两个实际失败草稿的预检。一份同时有 9 处角色不一致和 9 条缺失评价字段；另一份角色检查 PASS，但仍有 9 条缺失评价字段。角色 PASS 并不说明完整包有效。两次预检实际模型调用均为 0，生成新包为 0，功能 eval 为 0。

20 个独立审查接受的机制分组正在原有串行任务中作者化，已出现 1 个真实模型直接生成、通过完整包验证的项目内 candidate：[lexical-typing-helper-recognition](../data/skill-extraction/packages/candidates/full-native-reviewed-mechanisms-v1-20261006/d71b0a6aec2f31b154ddf521/lexical-typing-helper-recognition/SKILL.md)。它保留 Pyflakes #434/#561 的历史实现，功能 eval 仍为 not_executed，正式 KB 准入为 0。[作者任务观察](native-authoring-revision-20261006-v1/live-author-snapshot.json)仅代表记录时状态。恢复入口尚未执行真实模型修订，原任务终止后再串行恢复完整失败草稿。作者延迟或失败不会被改标为适用性负例。

完整主截点语料的生成依赖最晚为 **2023-06-18T14:43:15Z**，不能回填 pre-2021 Ranker 训练或更早的逐题知识库。训练和逐题机制发现仍须独立使用各自完整且当时已公开的输入，并排除自身 Issue、修复、重复簇和复制来源。

#470 小实验的既有边界保持：基础分支和引导分支均通过限定独立测试，但引导分支在生产代码修改之前放弃了历史 guidance，tokens 增加 20.54%。它支持“候选曝光后回退的分配策略结果”，没有证明历史 Workflow 执行或 Skill 修复收益。当前仍无有用的非平局训练效用偏好和合格训练 Ranker。

[机器快照 v35](results/pattern-crossbind-ranker-current-status-20261006-v35.json)与[上一版完整报告](archive/pattern-crossbind-ranker-status-20261006-v34.md)保留此前实验、失败与限制。下一步仍是原生包恢复及功能资格验证、真实任务绑定/重写/互补组合、时间隔离监督和 Ranker训练/校准、联合冻结及正式配对 SWE 实验。
