# 服务器迁移交接：2026-10-04

目标继续遵循 [模块设计](pattern-crossbind-ranker-design-20261003.md)和全历史时间切分计划，不缩减到已完成的 Pyflakes 小样本。M4 完整历史监督、M5 冻结与 M6 正式 SWE 实验尚未完成。

本次保存全部待提交源码、驱动与测试修改。完整测试 294 passed（19.51 秒），修改的 Python 文件 lint 通过。最新状态见 [审计 v3](results/temporal-history-development-audit-20261004-v3.json)；旧 v1/v2 报告保留为旧开发快照。

官方控制已完成 48/48，其中 27 个通过；公开输入 48/48，其中 29 个通过，两者交集为 16。交集尚未经过语义去重与邻近回归，不能作为正式 qualified N；正式 solver runs 仍为 0。

Pylint 历史验证被环境中断，已观察 496/1160 请求、1 个通过。设置失败与不支持的测试框架需保留原始分母并修正环境，不记作 Skill 无效。

Pyflakes v6 的 40 个预定历史分支已完成，24 条真实候选执行标签。新排序头确实训练了 12 对，但训练 query 的非平局偏好仍为 0；checkpoint 尚需重载审计，不能声称已学到效用优先级。7 个机制组仅有 Pyflakes 支持，只能为 local_template；原生作者被中断，完整发布包数为 0。

迁移时保留项目 tmp 下的来源仓库、全部控制记录、原始轨迹、模型、训练 checkpoint 和未完成作者审计。服务器先从 GitHub 获取已推送提交，再导入经过 hash 校验的实验归档。虚拟环境和外部 Docker 镜像缓存可在服务器重建；检查点中的绝对路径需显式迁移，不能静默改写原始证据。凭据只在运行进程内存中使用。

恢复优先级：修正 legacy Pylint harness 和版本 runtime；完成原生模板作者及真实 eval；核对 v6 evidence 与因果审查、重载 checkpoint；完成 Ruff 历史资格和完整来源学习；准备自身/相似/混合静态 KB；完成正式 cohort 门槛、开发 smoke 和统一冻结；按预注册方案完成配对与模块实验。

服务器已有旧目录 /home/chenyujia/arex-skill-graph，HEAD 为 9021a95 且有大量未提交记录；本次迁移使用新目录 /home/chenyujia/tritonToLlvm/arex-skill-graph。该路径与原 WSL 的 Linux 路径相同，保留 checkpoint 的绝对身份。旧服务器工作区独立保留。
