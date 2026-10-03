"""Issue/cluster denominators and paired descriptive metrics, including failures."""

from collections import defaultdict
import math
import random


def ndcg(ranked_ids, grades, k=8):
    def dcg(ids):
        return sum(
            (2 ** grades.get(cid, 0) - 1) / math.log2(i + 2) for i, cid in enumerate(ids[:k])
        )

    ideal = dcg(sorted(grades, key=lambda cid: (-grades[cid], cid)))
    return dcg(ranked_ids) / ideal if ideal else None


def summarize_runs(rows, *, bootstrap=1000, seed=20261003):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["arm"]].append(row)
    summary = {}
    for arm, items in grouped.items():
        issues = defaultdict(list)
        clusters = defaultdict(list)
        for row in items:
            issues[row["task_id"]].append(row)
        complete = all(row.get("validated_resolved") is not None for row in items)
        for qid, attempts in issues.items():
            cluster_ids = {row["bug_cluster_id"] for row in attempts}
            if len(cluster_ids) != 1:
                raise ValueError("one issue has conflicting cluster identities")
            clusters[next(iter(cluster_ids))].append(
                sum(row.get("validated_resolved") is True for row in attempts) / len(attempts)
            )
        summary[arm] = {
            "attempts": len(items),
            "independent_issues": len(issues),
            "bug_clusters": len(clusters),
            "evaluated_attempts": sum(row.get("validated_resolved") is not None for row in items),
            "ValidatedResolved@1": sum(r.get("validated_resolved") is True for r in items)
            / len(items)
            if complete
            else None,
            "BenchmarkResolved@1": sum(r.get("benchmark_resolved") is True for r in items)
            / len(items)
            if all(r.get("benchmark_resolved") is not None for r in items)
            else None,
            "cluster_mean_resolved": sum(sum(v) / len(v) for v in clusters.values()) / len(clusters)
            if complete
            else None,
            "failures_in_denominator": True,
            "model_calls": sum(r.get("budget", {}).get("model_calls", 0) for r in items),
            "tool_calls": sum(r.get("budget", {}).get("tool_calls", 0) for r in items),
            "model_tokens": sum(r.get("budget", {}).get("model_tokens", 0) for r in items),
            "history_tokens": sum(r.get("budget", {}).get("history_tokens", 0) for r in items),
        }
    paired = []
    for before, after in [("E0", "E1"), ("E1", "E2"), ("E2", "E3"), ("prompted", "trained")]:
        if before not in grouped or after not in grouped:
            continue

        def per_task(arm):
            d = defaultdict(list)
            for row in grouped[arm]:
                if row.get("validated_resolved") is not None:
                    d[row["task_id"]].append(row)
            return d

        a, b = per_task(before), per_task(after)
        delta = defaultdict(list)
        for qid in set(a) & set(b):
            av = sum(r["validated_resolved"] for r in a[qid]) / len(a[qid])
            bv = sum(r["validated_resolved"] for r in b[qid]) / len(b[qid])
            delta[a[qid][0]["bug_cluster_id"]].append(bv - av)
        if delta:
            values = [sum(v) / len(v) for v in delta.values()]
            rng = random.Random(seed)
            samples = sorted(
                sum(rng.choice(values) for _ in values) / len(values) for _ in range(bootstrap)
            )
            paired.append(
                {
                    "before": before,
                    "after": after,
                    "paired_issues": len(set(a) & set(b)),
                    "paired_clusters": len(values),
                    "cluster_mean_delta": sum(values) / len(values),
                    "cluster_bootstrap_95_interval": [
                        samples[int(0.025 * bootstrap)],
                        samples[min(bootstrap - 1, int(0.975 * bootstrap))],
                    ],
                }
            )
    return {"arms": summary, "paired": paired}
