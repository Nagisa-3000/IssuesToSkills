# 历史 Skill 与修复监督：开发进展

2026-10-04。对照 [模块设计](pattern-crossbind-ranker-design-20261003.md)继续实施。
**已完成真实历史开发监督和本地参数训练；M4 的完整历史监督、M5 冻结、M6 正式 SWE 实验仍未完成。**

最新审计快照见 [机器记录 v2](results/temporal-history-development-audit-20261004-v2.json)，
并保留 [v1 快照](results/temporal-history-development-audit-20261004-v1.json)。
统计属于开发阶段，不能作为 SWE 效果或泛化收益。

2026-10-04 服务器迁移及后续时间隔离修正见 [迁移报告](server-migration-and-temporal-generation-context-20261004.md)。完整源码和历史资料已恢复，v6 检查点完成数值与双重重载审计；12 个训练偏好对全部为平局。最新代码验证为 311 passed、5 skipped，skip 为不可用的挂载隔离测试。下表和旧机器快照记录更早的 v5 开发状态，不将其比例算作 v6 修复收益。M4/M5/M6 仍未完成。

| 项目 | 实际进展 | 解释边界 |
| --- | --- | --- |
| 历史证据审查 | Pylint 5,273、Pyflakes 501、Ruff 3,582，共 9,356 条可观察 Issue，全部审查完成 | 截点为 2024-01-01 UTC，exclusive；审查记录不是 Skill；删除和不可读取的历史不能假装恢复 |
| 正文历史恢复 | 83 条目标中恢复 79 条 | 4 条 Ruff 正文未恢复；另有 Pylint Project V2 事件详情不可读取 |
| 历史修复资格 | Pyflakes 26 个 Issue 来源通过真实 F2P/P2P 控制及 Issue 关闭关联检查 | 只运行变更的测试文件，未证明全项目或跨项目行为；PR mention 本身不构成修复关联 |
| 原生包 | v5、v6 各 26 个完整候选包；v6 已通过契约一致性与全部 verifier | 有 SKILL.md、Actions、证据、provenance、eval 定义和 verifier；functional 定义仍未执行，未准入正式 KB |
| 历史 query | 严格修复前输入的 9 条，train 4 / development 5 | 每条 query 用自身时间候选库；开发候选库截止 2021-01-01；不加载其修复 diff 或未来 Git 对象 |
| 执行监督 | 44 个预定分支：33 个执行、11 个硬拒绝；24 条真实候选执行标签 | 硬拒绝和未执行不产生修复失败标签；预算终止为失败；独立 evaluator 在 solver 停止后运行 |
| 因果重复审查 | 26 个来源及全部 9 个 query 完成模型证据审查，未找到重复或不确定分组 | 是当代审阅意见，可能漏检；不是独立性保证，也不产生修复效用标签 |
| 本地 Ranker | 真正 MiniLM 编码器和参数训练；4 个训练 query、6 个执行偏好对、5 个开发 query；checkpoint 已重载 | 训练对全部是 ties，非平局对为 0；因此不能声称学会了候选效用优先级 |
| 正式 SWE | solver runs = 0，qualified N = null | 官方环境控制继续运行；公开输入、语义去重、邻近回归、完整 KB 与冻结尚未全部完成 |

历史 baseline 7/9 通过其独立验收；24 个实际候选分支中 18 个通过。
候选数因 query 不同，且含按概率抽样的分支，这两个比例不能直接作效果比较。
上述执行监督及训练均使用 v5；不能将其结果算到重新作者的 v6 包上。
更重要的是，**同一 query 的候选执行结果全部打平**：当前数据缺少识别优先级的效用区分信号。
应继续完成 Pylint、Ruff 的完整来源资格与学习，增加独立机制、反例与执行监督，不能挑成功分支来训练。

## 本次纠正的机制

`invalidates` 与 `preserves` / Workflow invariant 不能共用同一 assurance 键。
将“某次验证观察已经过期”与“相邻行为必须保留”分别命名；读操作的不修改属性写入操作和 oracle，
修改型 Workflow 不能承诺整个过程 `checkout-unchanged`。
发布前检查内部矛盾，返回作者重新作者完整包；旧包保持不可变，未放松计划硬门槛。

独立历史验收在应用模型补丁后，仅将其拥有的评测测试路径恢复到 base，再应用独立回归断言。
保留生产修复及其余模型新增测试，避免公开测试编辑造成隐藏补丁设置冲突。
设置失败单独记录，不伪造 outcome=False 训练样本。实际命令执行并完整观察必要测试后才产生执行标签。

solver 的 `solver_ended` 表示正常 finish，`solver_terminated` 表示已停止。
预算或协议终止即使留下能过测试的补丁也保持运行失败；独立评测完成且候选确实进入 solver 请求后，
才可形成失败监督。完整轨迹与成本保留，模型上下文使用有 hash 的公开输出片段、分页文件读取，
避免反复注入完整文件写入和大段测试输出。

Ranker 使用 query / candidate 成对编码并按最长一侧截断，避免 512-token 输入只剩一侧内容。
当前观察允许的 `probe_only` 与真实修复效用分别处理：拒绝阈值依据历史开发执行结果及 replicate 聚合校准，
有执行结果时不把所有 probe 候选直接当作无用。模型预测仍不能补偿当前硬拒绝或授权未知条件下修改。

历史 PR / commit aliases 按同一 Issue、仓库和 merge SHA 归并，保留所有 alias 的审计，优先明确关闭关联。
GitHub 读取超时保留失败分母且不导出原始诊断；逐 locator 的公共 metadata 缓存支持继续采集。
原生包另导出可移植库存，路径相对库存目录；不改作者文件及 manifest hash。

## 复现与后续验收

本次完整代码验证为 **274 passed**，本次修改的 Python 文件 Ruff 检查通过。
Windows / WSL HTTP 桥只经内存和管道传递运行时凭据；solver 容器看不到宿主凭据、网络、Docker socket 或未来仓库。

完成的开发数据及独立验收在本地 `tmp/historical-ranker-execution-v3/`。
完整可重载 checkpoint 在 `tmp/historical-ranker-checkpoint-development-v1/`；
GitHub 的小型审计文件只描述训练和 hash，不假装包含完整模型。
当前请求模型 ID 为 `openai/gpt-6.1-sol`；本地训练的是 MiniLM 排序头，**没有对该远端模型做微调**。

下一阶段继续全历史来源资格、原生包 eval、机制 Pattern 证据与自身/相似/混合 KB，
完成 benchmark 原 Issue 输入、语义去重及官方与邻近验收，统一冻结后再执行配对与模块实验。
开发公开题 10034 已暴露，始终排除于正式分母。


2026-10-04 服务器接续：复制式隔离已验证并接入历史资格、监督和独立验收。完整回归 324 passed/5 legacy-bind skips，风格修正后 15 focused passed。原生机制作者 v3 的 7 组全部 defer、发布 0 包；已修正 provenance 输入与时间/realization 说明，尚未完成新实作者或功能准入。M4–M6 均未完成。详见 [本次报告](server-copied-sandbox-and-native-authoring-20261004.md)。

已启动服务器历史复验：Pyflakes 45 canonical 请求、Pylint 1,160 canonical 请求。源码固定 4907b5c，使用显式 namespace-copy 后端；原注册表、旧复验和失败记录均保留。当前快照见 [调度审计](results/server-historical-requalification-dispatch-20261004-v1.json)。这些是历史资格复验，正式 SWE solver runs 仍为 0。

本次调度观察更新：Pyflakes 完成 45/45 项，26 项通过旧修复因果资格；Pylint 完成 89/1160 项，仍在运行。这些资格不等于 Skill 功能准入或正式 SWE 成效。
