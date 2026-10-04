服务器复制式隔离与原生作者进展（2026-10-04）

已实现显式 namespace-copy 后端并接入 AdaptiveSolver、独立隐藏验收、历史验收、历史修复资格、历史监督与模块实验 CLI。复制式后端要求可信 Linux 特权 broker；命令以 UID/GID 65534、空附加组、零 capabilities 和 no_new_privs 在 user/mount/PID/network namespaces 与复制式 chroot 内执行。没有裸宿主执行降级。PID 1 保留为可信 supervisor；正常结束和超时均终止脱离会话的双重 fork 后代。

运行时复制明确的系统命令、解释器标准库及准备好的隔离虚拟环境。每次命令只获得公开工作区副本；只读探查不回写。普通命令完成后先检查整个结果树的文件、链接、大小和敏感内容，再原子替换 broker 副本。超时、非法链接、FIFO 或新增 Git 历史均不改变原副本。运行时不含宿主 sitecustomize/usercustomize 或构建配置目录。限制：单文件 16 MiB、工作区 512 MiB、地址空间 4 GiB、CPU 120 秒、同 UID 256 个进程。

完整回归 324 passed、5 skipped，103.97 秒。五个 skip 都是既有 bind-mount 隔离不可用；复制式路径没有 skip。随后两处等价风格修改通过 Ruff，相关路径 15 passed，10.23 秒。首次完整运行的 SSH 观察返回 -1、没有可用结果；确认原 pytest 进程消失后改用持久日志，该首次观察未计为通过。见 [执行审计](results/server-copied-sandbox-integration-20261004-v1.json)。

已重建两套服务器历史运行时，并在真实复制式隔离中导入 pytest：Pyflakes 为 Python 3.12.11/pytest 9.1.1；Pylint 为 Python 3.10.18/pytest 8.4.2。原迁移 Pyflakes 环境标记 3.12、实际链接服务器 3.10；原 Pylint 移动后前缀无法初始化。已保留原环境并使用新目录，ABI 不一致会明确拒绝。运行时启动通过仅证明执行环境可用，历史修复资格仍须逐例独立复验。

此前 v3 原生机制作者任务已终止：26 个包、7 个发现组、10 次实际调用，全部 defer、发布 0 包。拒绝涉及 Action 跨 realization 来源边界及本地/上游 Workflow ID 混淆；另有作者因缺少可检查的 qualification 信息或机制支持不足而 defer。没有放宽准入或由宿主补写契约。原生作者现接收上游 provenance；协议明确历史输入与后续旧断言复验时间、本地与上游 IDs、各来源 Action 范围。尚未执行修正后的真实重作者。见 [作者终态](results/server-native-mechanism-authoring-outcome-20261004-v3.json)。同一项目支持仍只能是 local_template；互补修复不能强行算作同一完整机制的重复实现。

下一步按原历史总体注册表，用新后端复验 Pyflakes 51 个请求和 Pylint 1,319 个请求，保留 alias 合并及所有不合格/环境失败。随后恢复因果资格 reconciliation、原生 Skill 功能验证及逐 query 时间重建的 Pattern/Ranker 监督。M4 未完成；正式库和 cohort 未冻结，正式 SWE solver runs=0，qualified N 未确定。复制式后端通过不等于官方 SWE Docker 协议资格完成；Ruff Rust、官方协议和 M5/M6 仍待推进。

服务器历史总体复验已实际启动（源码固定于 4907b5cb315ad14d776907645fad25cc86203120）：Pyflakes 51 个原请求去重为 45 项、3 workers；Pylint 1,319 个原请求去重为 1,160 项、4 workers。实际进程与当次进度见 [调度审计](results/server-historical-requalification-dispatch-20261004-v1.json)。复验结果使用新的服务器目录，不覆盖既有资格记录。首次调度只在系统 Python 3.10 导入阶段失败，未产生子任务；随后使用项目 Python 3.12.11 完成调度。

本次调度观察更新：Pyflakes 完成 45/45 项，26 项通过旧修复因果资格；Pylint 完成 89/1160 项，仍在运行。这些资格不等于 Skill 功能准入或正式 SWE 成效。
