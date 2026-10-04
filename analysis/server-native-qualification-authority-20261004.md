**服务器原生作者：可检查的历史资格资料接入（2026-10-04）**

当前改动将完整历史修复复验交给原生 Skill 作者检查，并绑定不可变报告哈希。Pyflakes 的 45 个去重候选已完成，26 个通过的来源与已有 26 个原生 Workflow 包逐一匹配。本记录不宣称 Skill 功能用例通过、正式知识库准入、全历史学习完成或 SWE 修复收益；M4、M5、M6 继续未完成。

旧作者只有 qualification attestation 摘要，多个机制组因此 defer；还有草稿混淆上游 Workflow 身份与新 realization 身份，或把独立历史的 Actions 混入同一 realization。此前提交修正了原生协议、上游 provenance 输入及时间解释。本次增加可检查的完整 original-base、base-with-regression、historical-fixed 资料。

[qualification_authority.py](../src/arex_skill_graph/qualification_authority.py) 核对 repository/issue/fix/revision、exclusive cutoff、修复公开日期、闭合关系、三组观察、退出码、超时和 runtime hash，并重新计算 fail-to-pass 和 pass-to-pass。来源别名只能在同一 issue/repository/full merge SHA 下匹配。完整 canonical inventory 与精确来源覆盖在 API 调用前检查；篡改、缺失或不一致均拒绝。相同修复 SHA 的不同标签不能扩增独立 Pattern 支持。

[discover_native_history_patterns.py](../experiments/discover_native_history_patterns.py) 现在必须提供 --verifications。每个机制作者收到完整独立报告；新 provenance 必须保存其 authoritative qualification_report_hashes。完整资料另外保存在 authoring audit 的 qualification-input.json。单条来源作者 [extract_verified_history_skills.py](../experiments/extract_verified_history_skills.py) 同样检查并接收报告、保留哈希，输入协议升级为 v7。历史包保持原样，不覆盖旧作者或旧审计。

报告的 checked_at 和 runtime 是后续验证资料，不是 T 前知识，不写入历史 evidence cards。历史 CI 未知仍是未知；新 Skill evals 的定义保持 not_executed。generation_context 继续记录发现时看到的全部来源，包括未选入机制组的来源；早期历史 query 不能复用全 T 前语料生成的抽象。

验证：最终完整回归 **346 passed、5 skipped**；5 项属于旧 bind 隔离路径，新 copy 路径没有被跳过。相关资格/身份/历史 Ranker 测试 **53 passed**，所有改动 Python 的 Ruff 检查通过。26 个真实来源全部匹配。扫描 4,142 个当前 Git 文件，提供的凭据精确匹配为 0；形状检查命中的 19 个旧公开测试 fixture 单独识别，未输出其占位符内容。结果及代码/日志哈希见 [机器审计](results/server-native-qualification-authority-20261004-v1.json)。未被接受的观察失败也单独记录，不计作通过。

下一步在固定提交上重新调用 7 个机制候选的原生作者，保留每次模型调用、拒绝或 defer。单项目支持最多得到 local_template；不足的完整机制继续 defer。随后仍需独立执行 Skill 功能用例，恢复 Pylint 不同历史版本的依赖、完成 Ruff 和逐 query 时间语料重建，形成有效训练信号并满足正式冻结条件。正式 solver runs 仍为 0。
