#!/usr/bin/env python3
"""Build a project roster and evidence-gated shortlist from frozen research data."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ACCEPTED_LICENSES = {
    "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "BSD-3-Clause-Clear",
    "BSD-4-Clause", "ISC", "Unlicense", "0BSD", "MPL-2.0", "BSL-1.0",
    "GPL-2.0", "GPL-3.0", "GPL-2.0-only", "GPL-3.0-only",
    "GPL-2.0-or-later", "GPL-3.0-or-later", "LGPL-2.0", "LGPL-2.1", "LGPL-3.0",
    "LGPL-2.1-only", "LGPL-3.0-only", "LGPL-2.1-or-later", "LGPL-3.0-or-later",
    "AGPL-3.0", "AGPL-3.0-only", "AGPL-3.0-or-later", "EPL-1.0", "EPL-2.0",
    "CC0-1.0", "Zlib", "Python-2.0", "Artistic-2.0", "AFL-3.0", "WTFPL",
    "BlueOak-1.0.0", "PSF-2.0", "MIT-CMU", "CECILL-2.1",
}

STATUS_LABELS = {
    "recommended": "推荐",
    "similarity_not_confirmed": "维护/PR/许可通过；相似对照未核实",
    "low_recent_merges": "维护中；近90天合并PR未达20",
    "low_historical_pr": "历史PR未达1000",
    "archived_or_disabled": "已归档/禁用",
    "not_public": "非公开",
    "stale_default_branch": "主分支近期维护未达门槛",
    "license_not_confirmed": "许可证待复核",
    "source_available_license": "当前许可不满足本轮开源条件",
    "unresolved": "仓库身份未核实",
}


def load(root: Path, name: str) -> dict:
    return json.loads((root / name).read_text(encoding="utf-8"))


def save(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def link(name: str) -> str:
    return f"[{name}](https://github.com/{name})"


def cell(value: object) -> str:
    return "—" if value is None else str(value).replace("|", "\\|").replace("\n", " ")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--analysis", type=Path, default=Path("analysis"))
    args = parser.parse_args()
    census = load(args.data, "benchmark-project-census.json")
    metadata = load(args.data, "github-repositories.json")["projects"]
    activity_document = load(args.data, "github-pr-activity.json")
    activity = activity_document["projects"]
    manual = {key.lower(): value for key, value in load(args.data, "manual-license-decisions.json")["projects"].items()}
    groups = load(args.data, "similarity-groups.json")["groups"]
    assert activity_document["query_contract"] == "single_inclusive_github_date_range_v1"
    start = activity_document["windows"]["start90_inclusive"]
    end = activity_document["windows"]["end_exclusive"]
    canonical = {}
    resolved_aliases = {}
    aliases = defaultdict(list)
    for raw, value in metadata.items():
        repository = value["repository"]
        if repository:
            name = repository["nameWithOwner"]
            canonical[name.lower()] = repository
            resolved_aliases[raw.lower()] = repository
            aliases[name].append(raw)
    membership = defaultdict(dict)
    for raw, variants in census["projects"].items():
        repository = metadata[raw]["repository"]
        if repository is None:
            raise ValueError(f"Benchmark repository identity not resolved: {raw}")
        name = repository["nameWithOwner"]
        for variant, count in variants.items():
            # A repository can appear twice under differently cased names.
            if variant in membership[name]:
                previous = membership[name][variant]
                membership[name][variant] = None if count is None or previous is None else count + previous
            else:
                membership[name][variant] = count

    def license_record(repository: dict) -> dict:
        decision = manual.get(repository["nameWithOwner"].lower())
        if decision:
            return {"confirmed": True, **decision}
        spdx = (repository.get("licenseInfo") or {}).get("spdxId")
        return {"confirmed": spdx in ACCEPTED_LICENSES, "open_source_accepted": spdx in ACCEPTED_LICENSES,
                "license": spdx, "source_url": repository["url"],
                "source_ref": ((repository.get("defaultBranchRef") or {}).get("target") or {}).get("oid"),
                "basis": "GitHub licenseInfo; unrecognized/custom licenses require separate review"}

    def recent_branch(repository: dict) -> bool:
        stamp = ((repository.get("defaultBranchRef") or {}).get("target") or {}).get("committedDate")
        return bool(stamp and start <= stamp[:10] < end)

    def healthy_peer(repository: dict) -> bool:
        license = license_record(repository)
        return (not repository["isPrivate"] and not repository["isArchived"] and not repository["isDisabled"]
                and recent_branch(repository) and license["confirmed"] and license["open_source_accepted"])

    verified_groups = []
    peer_map = defaultdict(list)
    for group in groups:
        members = []
        for raw in group["members"]:
            repository = resolved_aliases.get(raw.lower()) or canonical.get(raw.lower())
            if repository:
                members.append(repository)
        unique = {repo["nameWithOwner"]: repo for repo in members}
        healthy = [repo for repo in unique.values() if healthy_peer(repo)]
        if len(healthy) < 2:
            continue
        verified = {**group, "verified_maintained_open_source_members": [repo["nameWithOwner"] for repo in healthy]}
        verified_groups.append(verified)
        for repository in healthy:
            name = repository["nameWithOwner"]
            for peer in healthy:
                if peer["nameWithOwner"] != name:
                    peer_map[name].append({"repository": peer["nameWithOwner"], "group": group["id"],
                                           "in_benchmark_census": peer["nameWithOwner"] in membership,
                                           "basis": group["shared_scope"], "limits": group["limits"]})

    selected = {}
    for name, variants in sorted(membership.items(), key=lambda pair: pair[0].lower()):
        repository = canonical[name.lower()]
        license = license_record(repository)
        recent = activity.get(name)
        if repository["isPrivate"]:
            status = "not_public"
        elif repository["isArchived"] or repository["isDisabled"]:
            status = "archived_or_disabled"
        elif repository["allPR"]["totalCount"] < 1000:
            status = "low_historical_pr"
        elif not recent_branch(repository):
            status = "stale_default_branch"
        elif not license["confirmed"]:
            status = "license_not_confirmed"
        elif not license["open_source_accepted"]:
            status = "source_available_license"
        else:
            assert recent is not None, f"Activity evidence missing: {name}"
            if recent["merged90"] < 20:
                status = "low_recent_merges"
            elif not peer_map[name]:
                status = "similarity_not_confirmed"
            else:
                status = "recommended"
        selected[name] = {
            "status": status, "benchmark_membership": variants,
            "PR_total": repository["allPR"]["totalCount"], "PR_merged_total": repository["mergedPR"]["totalCount"],
            "PR_open": repository["openPR"]["totalCount"], "PR_created90": recent["created90"] if recent else None,
            "PR_merged90": recent["merged90"] if recent else None, "PR_merged365": recent["merged365"] if recent else None,
            "default_branch_commit": ((repository.get("defaultBranchRef") or {}).get("target") or {}).get("committedDate"),
            "default_branch_ref": ((repository.get("defaultBranchRef") or {}).get("target") or {}).get("oid"),
            "license_review": license, "is_fork": repository["isFork"], "parent": repository["parent"],
            "primary_language": (repository.get("primaryLanguage") or {}).get("name"),
            "similar_projects": peer_map[name], "aliases": aliases[name],
            "metadata_observed_at": next(item["observed_at"] for item in metadata.values() if item["repository"] and item["repository"]["nameWithOwner"] == name),
            "activity_observed_at": recent["observed_at"] if recent else None,
        }
    status_counts = Counter(row["status"] for row in selected.values())
    recommended = {name: row for name, row in selected.items() if row["status"] == "recommended"}
    summary = {"schema": "swebench-project-selection-v1", "snapshot_date": "2026-10-03",
               "criteria": {"PR_total_minimum": 1000, "PR_merged90_minimum": 20,
                            "default_branch_commit_in_window": [start, end], "public_maintained_open_source_peer_required": True},
               "raw_benchmark_repository_identities": census["unique_raw_repositories"],
               "canonical_benchmark_projects": len(selected), "recommended_projects": len(recommended),
               "status_counts": dict(status_counts), "verified_similarity_groups": verified_groups, "projects": selected}
    save(args.data / "project-selection.json", summary)

    roster = ["**SWE-bench 项目完整清单与筛选证据**", "", "快照：2026-10-03。基准版本、实际文件统计与来源见 [主报告](swebench-project-selection-20261003.md)。", "",
              "`—` 表示未计算/未查询，不表示零。Multi-SWE-bench JSONL 项目身份来自固定版本文件索引与实际文件首部，未重数其任务总量。", ""]
    for variant, record in census["variants"].items():
        canonical_count = len({metadata[raw]["repository"]["nameWithOwner"] for raw in record["project_counts"]})
        roster += [f"**{variant}**", "", f"固定版本 `{record['revision']}`；{record['repositories']} 个原始仓库身份，归一后 {canonical_count} 个项目；原始行数 {cell(record['raw_rows'])}，不同任务 ID {cell(record['unique_tasks'])}。", "",
                   "| 发布数据中的仓库 | 任务数（不同ID） | 当前规范仓库 | 筛选状态 |", "| --- | ---: | --- | --- |"]
        for raw, count in record["project_counts"].items():
            repository = metadata[raw]["repository"]
            name = repository["nameWithOwner"] if repository else raw
            roster.append(f"| {link(raw)} | {cell(count)} | {link(name)} | {STATUS_LABELS[selected[name]['status']]} |")
        roster.append("")
    roster += ["**归一后的全量项目与 PR 证据**", "", "| 当前项目 | 语言 | PR总量 | 90天新PR | 90天合并PR | 365天合并PR | 主分支最后提交 | 许可 | 筛选状态 |", "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |"]
    for name, row in selected.items():
        roster.append("| " + " | ".join([link(name), cell(row["primary_language"]), str(row["PR_total"]), cell(row["PR_created90"]),
                    cell(row["PR_merged90"]), cell(row["PR_merged365"]), cell((row["default_branch_commit"] or "")[:10] or None),
                    cell(row["license_review"]["license"]), STATUS_LABELS[row["status"]]]) + " |")
    (args.analysis / "swebench-project-inventory-20261003.md").write_text("\n".join(roster) + "\n", encoding="utf-8")

    main_lines = ["**SWE-bench 常用变种的项目清单与维护活跃度筛选**", "",
                  f"调研快照：2026-10-03。核对 10 个公开数据源、18 个 split 入口，得到 {census['unique_raw_repositories']} 个原始仓库身份，GitHub 别名/大小写归一后为 **{len(selected)} 个项目**。其中 **{len(recommended)} 个项目**同时通过本轮维护、历史 PR、近期合并、许可与相似对照门槛。", "",
                  "[完整分基准项目名单与全量筛选表](swebench-project-inventory-20261003.md)；[机器可读筛选结果](data/swebench-projects-20261003/project-selection.json)；[前沿修复 Agent 论文与 benchmark 调研](agent-software-repair-benchmark-survey-20261003.md)。下文推荐池是人工功能组门控后的已核实子集，不是宣称其余项目没有相似替代。", "",
                  "**覆盖范围和项目数量**", "",
                  "Full、Lite、Verified 是当前最常见的论文/榜单对照；另覆盖官方 Multilingual、Multimodal，较新的 Live 系列、Pro、独立 Multi-SWE-bench 和 SWE-rebench。HF 下载量快照保留在 dataset-snapshots.json，仅辅助解释使用范围，不等于独立使用人数或论文引用次数。", "",
                  "| 数据源 / split（固定版本） | 原始任务行数 | 不同任务ID | 发布仓库身份数 | 归一项目数 | 口径 |", "| --- | ---: | ---: | ---: | ---: | --- |"]
    notes = {
        "Full/test": "原版公开 test", "Lite/test": "原版精简 test", "Verified/test": "人工核验 test",
        "Multilingual/test": "官方 9 语言，与 ByteDance 的 Multi-SWE-bench 不同",
        "Multimodal/test": "当前 v2；不沿用早期 617/619 的规模", "Multimodal/dev": "开发集，单列",
        "Live/full": "动态 full；1888行有1个重复ID", "Live/test": "公开 test", "Live/lite": "冻结 lite",
        "Live/verified": "500行有1个重复ID；与原版 Verified 不同",
        "Live-MultiLang/all-public": "8个语言split合并后的项目集合",
        "Pro/default": "2026-09-22 V2；公开11项目", "Pro/hard": "V2 HARD子集，不新增项目",
        "Pro/v1": "保留的原始公开版731题；非当前default",
        "Multi-SWE-bench/released-7-languages": "39个JSONL文件身份；论文1632题未在本轮重数",
        "Multi-SWE-bench/kotlin-additional-files": "当前包新增文件，单列；不冒充原论文7语言实验",
        "Multi-SWE-bench/python-additional-files": "当前包另有500行Python文件，单列",
        "SWE-rebench-leaderboard/test": "HF公开test快照；2026-07 Harbor另有111题，不混入本表",
    }
    for variant, record in census["variants"].items():
        source = f"https://huggingface.co/datasets/{record['dataset_id']}/tree/{record['revision']}"
        canonical_count = len({metadata[raw]["repository"]["nameWithOwner"] for raw in record["project_counts"]})
        main_lines.append(f"| [{variant}]({source}) | {cell(record['raw_rows'])} | {cell(record['unique_tasks'])} | {record['repositories']} | {canonical_count} | {notes[variant]} |")
    main_lines += ["", "各行项目集合有重叠，不能直接相加；同一项目在不同 benchmark 中的题目也不一定相同。Pro 论文整体的41项目包含其他划分，当前公开 HF 仅11项目，本轮不编造私有/未公开项目名单。SWE-rebench 的大规模训练/构建语料与公开 leaderboard 分开；只统计后者。Lite-S 等原版子集不作为新增项目来源，本轮没有单独复算其每项目题量。", "",
                   "**筛选口径**", "",
                   f"历史 PR ≥1,000；{start} 至 2026-10-03（查询时已发生的90个日历日）合并 PR ≥20；主分支最新提交也在此窗口；项目公开、未归档/禁用；许可得到 GitHub 标准许可识别或实际文件复核；至少存在另一个公开、许可可接受且主分支近期更新的相似项目。对照项目不必达到主池1,000 PR门槛，也不必属于 benchmark，分别标注。", "",
                   "PR 总量用 GitHub pullRequests.totalCount，包含打开、关闭及合并 PR，避免把 issues_count 当 PR。近期使用单一 `merged:YYYY-MM-DD..YYYY-MM-DD` / `created:...` 区间。每个查询返回的日期样本逐项验证，保存90天最多25个合并PR、90天新增和365天合并各1个验证样本。各批次 observed_at 保留，统计是查询时快照。", "",
                   "GitHub 日期查询按 UTC 日历日期；2026-10-03 只包含采集时已发生的活动，不代表当天结束后的完整计数。", "",
                   "Bot/非Bot作者只作最多25条样本描述，不当作全季比例。近期主分支提交及合并活动不等于所有PR都是缺陷修复；真正的 Skill 源仍需另行筛选实现、测试与验证证据。GitHub 的 NOASSERTION/null 表示识别不足，不自动等同于非开源。", "",
                   "**原版12个项目：基准题量与当前筛选**", "",
                   "| 项目 | Full | Lite | Verified | 历史PR | 90天合并PR | 当前结论 / 相似项目 |", "| --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    for raw, full_count in census["variants"]["Full/test"]["project_counts"].items():
        name = metadata[raw]["repository"]["nameWithOwner"]
        row = selected[name]
        peers = sorted({peer["repository"] for peer in row["similar_projects"]})[:3]
        conclusion = STATUS_LABELS[row["status"]] + ("；" + ", ".join(link(peer) for peer in peers) if peers else "")
        main_lines.append(f"| {link(name)} | {full_count} | {census['variants']['Lite/test']['project_counts'][raw]} | {census['variants']['Verified/test']['project_counts'][raw]} | {row['PR_total']:,} | {cell(row['PR_merged90'])} | {conclusion} |")
    main_lines += ["", "**已核实推荐项目与相似对照**", "",
                   "下表按功能组列出通过全部主池门槛的 benchmark 项目。对照列表仅保留通过公开性、许可与近期主分支检查的项目；其中一些是库的组件对照、跨语言类比、共享依赖或分叉关系，边界在每行说明。相似性由官方项目描述与人工功能比较支持，尚未进行跨项目修复实验。", "",
                   "| 功能组 | 入选benchmark项目（历史PR / 90天合并PR） | 组内可用项目（含源项目） | 比较范围与限制 |", "| --- | --- | --- | --- |"]
    for group in verified_groups:
        source_names = [name for name in group["verified_maintained_open_source_members"] if name in recommended]
        if not source_names:
            continue
        source_cells = "; ".join(f"{link(name)} ({recommended[name]['PR_total']:,} / {recommended[name]['PR_merged90']})" for name in source_names)
        peer_cells = ", ".join(link(name) + ("（池外）" if name not in membership else "") for name in group["verified_maintained_open_source_members"])
        main_lines.append(f"| {group['title']} | {source_cells} | {peer_cells} | {cell(group['shared_scope'])}；{cell(group['limits'])} |")
    main_lines += ["", "**全部项目的筛选分布**", "", "| 状态 | 项目数 |", "| --- | ---: |"]
    for status, count in status_counts.items():
        main_lines.append(f"| {STATUS_LABELS[status]} | {count} |")
    main_lines += ["", "每个项目在上表只计一个首要状态；可能同时存在其他不足。`维护/PR/许可通过；相似对照未核实` 不是判定它不存在同类项目。未达本轮20个合并PR门槛的成熟库也不等于停止维护；完整表保留其真实量及提交日期。", "",
                   "**值得单独标注的情况**", "",
                   "- `scratchfoundation/scratch-gui` 当前已归档，历史出现在 Multimodal 不保证今天仍适合作为维护中的 PR 源。",
                   "- `ProtonMail/WebClients` 主分支仍有更新，但公开 PR 总量为0；当前公开镜像不满足本轮 PR 源门槛。",
                   "- `hashicorp/terraform` 当前许可为 BUSL-1.1，`flipt-io/flipt` 当前为 FCL-1.0-MIT，本轮不把来源可见/未来开源当成当前的开源许可。",
                   "- `redis/redis` 当前 Redis 8+ 有 AGPLv3 选项；`valkey-io/valkey` 为BSD项目。两者存在分叉关系，需审查近重复修复。",
                   "- Sphinx、SymPy、Matplotlib、jq、Zstandard、MapLibre、Pillow、JavaParser 等已核对实际许可文件；结果和固定提交链接见 manual-license-decisions.json。", "",
                   "优先从 HTTP 客户端、表格/数组、Web、JSON、静态检查、文档构建等明确功能组选择项目。核心12项目提供既有论文对照；多语言与真实应用扩展提供不同语言和工程域。大型数据库、深度学习和基础设施网关的环境成本更高，本次项目活跃度不证明其修复评测更容易。", "",
                   "若用于 AREX 下一阶段，按整个项目留出评测目标，冻结历史截止日及源PR列表；共享依赖、分叉与相同修复别名要做近重复检查。当前调研未向提取器或 catalog 导入 benchmark 的目标补丁或测试，也未执行新的修复率实验。", "",
                   "**来源与复核**", "",
                   "数据版本和公开 metadata：[dataset-snapshots.json](data/swebench-projects-20261003/dataset-snapshots.json)。逐文件项目统计、SHA及文件首部身份检查：[benchmark-project-census.json](data/swebench-projects-20261003/benchmark-project-census.json)。维护/PR证据：[github-repositories.json](data/swebench-projects-20261003/github-repositories.json)、[github-pr-activity.json](data/swebench-projects-20261003/github-pr-activity.json)。相似组及限制：[similarity-groups.json](data/swebench-projects-20261003/similarity-groups.json)。", "",
                   "独立 REST 日期区间复核：[rest-date-range-crosscheck.json](data/swebench-projects-20261003/rest-date-range-crosscheck.json)。离线数据审核与文件哈希：[data-audit.json](data/swebench-projects-20261003/data-audit.json)。[审核脚本](scripts/audit_swebench_project_data.py)不访问网络；可用外部缓存复验完整下载文件的官方哈希。", "",
                   "固定版本完整 Parquet/单文件 Python JSONL 用官方 LFS SHA-256 或 Git blob SHA-1 验证；大型多仓 JSONL 只读取固定版本实际首部，并与官方文件索引的 org/repo 身份交叉匹配，不声称完整内容hash已重新验证。原始问题/补丁/执行日志不进入本报告数据目录；外部缓存不纳入提交。", "",
                   "采集脚本：[项目普查](scripts/swebench_project_census.py)、[GitHub活动](scripts/swebench_repository_screening.py)、[报告和门控](scripts/build_swebench_project_report.py)。脚本使用公开 HTTP 与已登录的 GitHub CLI；API凭据由CLI处理，不读取、打印或写入报告。普查需要 duckdb==1.4.0，当前采集使用 WSL + Windows HTTP；跨平台运行需提供适合本机的HTTP/CLI路径。", "",
                   "在仓库根目录用 Python 3.12 离线重建报告并审核：", "",
                   "```bash",
                   "python analysis/scripts/build_swebench_project_report.py --data analysis/data/swebench-projects-20261003 --analysis analysis",
                   "python analysis/scripts/audit_swebench_project_data.py --data analysis/data/swebench-projects-20261003 --analysis analysis",
                   "```", "",
                   "第二条命令可加 `--cache <外部缓存目录>`，独立复验已完整下载文件的实际哈希；不提供缓存时仅核对记录及官方索引，不声称重读了原始完整文件。", "",
                   "当前公开性/维护性评估对应2026-10-03，不替代 benchmark 历史 base_commit 的环境或许可。部分未来/迁移到其他平台的版本、未公开 Pro 划分、未正式说明评测角色的新增语言文件分别标注；本报告不宣称遍历所有曾存在的衍生变种。", ""]
    (args.analysis / "swebench-project-selection-20261003.md").write_text("\n".join(main_lines), encoding="utf-8")
    print(json.dumps({"canonical_benchmark_projects": len(selected), "recommended": len(recommended),
                      "status_counts": dict(status_counts), "verified_groups": len(verified_groups)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
