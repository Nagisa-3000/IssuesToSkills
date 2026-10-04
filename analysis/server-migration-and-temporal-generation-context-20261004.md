# 服务器迁移与生成上下文的时序准入

2026-10-04。工作区迁移至 vm-node3.s.rvnpu.cn 的
/home/chenyujia/tritonToLlvm/arex-skill-graph。
本报告记录迁移和开发验证，不代表完成 M4、M5 或正式 SWE 修复评测。
机器审计见 [迁移记录](results/server-workspace-migration-audit-20261004-v1.json) 和
[检查点恢复](results/server-ranker-checkpoint-reload-audit-20261004-v1.json)。

本地原有源码修改已提交为 a9637d3c13133f3b78c56c07cf2df01938f809f6，
并推送到 GitHub。迁移后修复原生 realization 身份、作者协议和非有限 Ranker
状态的提交为 ef3bec4525b49627f9f7a2e21aa9707b2c030325。
删除本地项目前，通过 GitHub API 确认 a9637d3 是 main 的祖先。
服务器旧目录 /home/chenyujia/arex-skill-graph 保留。

| 恢复检查 | 实际结果 |
| --- | --- |
| 资源清单 | 325,957 项：324,844 个普通文件、1,113 个符号链接 |
| 普通文件字节 | 3,134,686,709 |
| 实际传输归档 | gzip，1,318,040,308 字节，40 个分块 |
| 完整性 | 整包与清单 SHA256、全部落盘资源 hash/链接目标、资源集合精确匹配 |
| 恢复 | 321,829 项恢复；4,119 项已有相同内容；9 项服务器 tracked 修改保留 |
| 工作目录 | tmp 整目录从已验证快照原子移动；其余 11 项分别复制 |
| 冲突 | 没有覆盖不同的 untracked 文件；3 个新生成的 pip 元数据文件另行保留 |
| 备份 | 完整已验证归档保留在服务器 staging，迁移后快照不再是完整树 |
| 本地 Linux 项目 | 已删除；删除前 HEAD、工作树、挂载与进程 cwd 再次核实 |
| Windows 迁移目录 | 删除被自动审批阻断，仍保留，不能宣称本地清理全部完成 |

原 tar 退出码为 2：三个可重建的 Docker/开发控制缓存无法读取，socket 被忽略。
.git、Python 环境、pytest/ruff 缓存没有作为不可替代项目材料迁移。
这些排除和原始失败保留在审计中；不能将整包传输校验通过改写为原 tar 命令成功。
安全解包及全部归档资源内容核对先完成，随后采用 16 个有界读取线程核对不可变快照。
原 v1 的只读落盘核对由 v2 接续，原日志保留。

恢复后的 v6 开发 Ranker 检查点 hash 为
899f2696083de1bff52f36847cd08d5fd97af08086c428384b9552fa8b7b3279。
原始 dataset 的时间和内容 hash 校验通过；24 个原始候选的特征、评分、概率均有限，
两次独立重载结果精确相同。训练 query 为 4、开发 query 为 5，训练偏好对为 12，
非平局对为 0。此审计验证恢复和数值可靠性，不能证明学习了效用优先级，
也没有完成因果监督 reconciliation 或证明修复收益。

本次补上 Pattern 发现阶段的间接时间泄漏检查。最终支持集之前的案例，并不代表
模型在发现机制时只看到这些案例。新 generation_context 保存完整发现语料及上游
抽象的 SourceRecord、包 hash 和语料 fingerprint。非支持来源仍是学习依赖；
它们不增加独立支持或跨项目证据。每条历史 query 的时间、issue/alias、bug cluster
和 fix 门槛现在同时约束支持来源与整个生成上下文。模型作者必须原样保留该上下文，
不能删掉较晚或属于当前 query 的记录来通过准入。

原生 v4 Pattern/local_template 缺少完整上下文时拒绝准入；已有单来源 Workflow
继续兼容。正式 T 后任务可以使用完整 T 前合格语料的抽象；更早的 Ranker query
需要按其时间重新建立发现语料，不能复用全 T 前发现结果。
M0–M3 的接口、fixture 验证与历史开发进展不等于全历史学习完成。

完整测试：311 passed、5 skipped；时间/作者重点测试：20 passed；修改 Python 文件
Ruff 检查通过。五项 skip 是当前节点挂载隔离不可用的真实隔离测试，不能作通过计。
服务器复制 chroot 原型另有已提交审计，但尚未成为生产修复后端。
当前节点 Docker daemon 不可用，正式 solver runs 仍为 0，qualified N 仍未冻结。
全历史监督、原生 functional eval、Pylint/Ruff 资格、正式库冻结和配对 SWE 实验仍需继续。

Windows 迁移目录 D:/arex-migration-01a0fd61-20261004 的递归删除及七个已核实
payload 文件的逐项删除均被自动审批拒绝，返回理由只有 blocked by policy。
本地 Linux 项目删除已实际完成；Windows 归档没有删除。凭据只经进程内存、stdin
和运行时环境传递，审计文件不包含凭据值。
