# 原始历史查询工件（2026-10-06）

这个目录保存现有合格供给语料中全部 21 个 pre-2021 来源的原始输入恢复登记，以及成功恢复的 19 个公开源码查询。它是训练/开发准备，不是正式 SWE 题集或 Skill 收益结果。

- targets.json、population-register.json：完整选择范围和固定仓库 numeric ID；21 条来源对应 20 个保守组件，完整因果复核未完成。
- input-recovery-completion.json：原始 GH Archive opened 事件检索结果；Pyflakes #419/#422 保留缺口。
- cases/<query>/opened-input.json、qualification.json：原始标题/正文、事件与仓库身份、原始 event hash、保存文件 hash；不包含后续讨论。
- source-selection-policy.json、query-register.json：统一公开发行版选择规则及逐题资格。
- cases/<query>/registry-metadata.json、source-preparation-audit.json：选定 sdist 的上传时间、URL、大小、SHA256、源码树及 Git 对象核验。
- queries.json、cases/<query>/task.json：公开 TaskContext。绝对 root 路径指向服务器缓存，重新准备后需要复验和绑定当前目录。

统一规则为：选择当前可观察、严格早于原始 event 输入时间、只有一个 sdist 的最高稳定版本；排除 prerelease/dev/local，不使用当前 yank 状态，不参考 gold outcomes。当前 registry 观察不能证明已经删除的历史发行版。缓存 archives 与完整源码未加入这个目录；精确身份保存在元数据和审计中。合成 Git commit 使用准备时的时间，不能解释成历史原始提交。

恢复命令可使用 experiments/recover_original_history_queries.py，传入本目录 targets.json 和新的 --output-dir。然后使用 experiments/prepare_original_release_queries.py，传入恢复 completion、本目录 project-map.json、analysis/isolation/historical-causal-isolation-20261006-v1.json 和新的 --output-dir。脚本拒绝覆盖既有版本。若 registry 新观察或源码选择不同，应记录为新查询版本并重新核验，不能自动视为原冻结池。

Pyflakes #574 的原始补丁/API 不兼容和版本专用控制见 ../../results/original-history-query-recovery-and-current-source-controls-audit-20261006-v1.json。其已知修复适配只供 evaluator；不能提供给 planner、Ranker、solver 或知识库。机械控制已通过，独立复核仍待完成。

本次恢复和控制均为 0 次模型调用、0 个新 solver 分支、0 条新效用标签、0 次正式 SWE 运行。时间和源码身份合格不代表 Skill 已完成独立泛化验收。
