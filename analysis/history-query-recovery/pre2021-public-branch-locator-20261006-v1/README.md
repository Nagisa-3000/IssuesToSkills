# 原始历史查询的公共 Push 定位

全量读取公开 ClickHouse 索引在 pre-2021 范围内、三个仓库名别名的 1819 条 PushEvent 定位行，没有任意 top-N。19 条已恢复原始查询各保留发行 README 的 master 分支证据，冻结定位到 18 个归档小时。

索引只是定位线索，不是公开 commit head 的证明，也不代表完整 GitHub push 历史。恢复器必须独立扫描相应 GH Archive 原始小时、按稳定仓库数字 ID 和分支验证公开 PushEvent 与严格 pre-input 时间；只保存匹配 head、时间、事件/仓库 ID 和原始事件 hash，不保存无关事件或 commit message。没有可靠归档证明就保留缺口，不回退到后来的 gold-parent。
