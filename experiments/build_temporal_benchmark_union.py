#!/usr/bin/env python3
"""Project every registered benchmark variant without exporting solution fields."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.benchmark_identity import (
    METADATA_FIELDS,
    METADATA_PROJECTION_VERSION,
    alias_union,
    project_metadata,
    public_file_in_memory,
)
from arex_skill_graph.history_census import fingerprint, now, write_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    import duckdb

    register = json.loads(args.register.read_text())
    all_records, audits = [], []
    for variant in register["variants_with_target"]:
        relative = variant["variant"].replace("/", "__") + ".json"
        path = args.output_dir / relative
        projection = {
            "version": METADATA_PROJECTION_VERSION,
            "fields_sha256": fingerprint(METADATA_FIELDS),
            "source_identity_sha256": fingerprint(variant),
        }
        if path.exists():
            saved = json.loads(path.read_text())
            if (
                saved["revision"] != variant["revision"]
                or saved.get("projection") != projection
                or saved.get("records_sha256") != fingerprint(saved["records"])
            ):
                raise ValueError(
                    "benchmark projection identity/integrity changed; use a new version directory"
                )
            rows, audit = saved["records"], saved["audit"]
        else:
            rows, file_audits = [], []
            for source in variant["files"]:
                with public_file_in_memory(source["source_url"], source["sha256"]) as (
                    memory,
                    size,
                ):
                    connection = duckdb.connect(":memory:")
                    try:
                        part, file_audit = project_metadata(
                            connection, memory, is_parquet=source["file"].endswith(".parquet")
                        )
                    finally:
                        connection.close()
                rows.extend(part)
                file_audits.append(
                    {
                        "file": source["file"],
                        "sha256": source["sha256"],
                        "full_content_hash_verified": True,
                        "bytes": size,
                        **file_audit,
                    }
                )
            if len(rows) != variant["target_task_identity_count_before_temporal_filter"]:
                raise ValueError("registered benchmark target membership count changed")
            for row in rows:
                row.update(
                    {
                        "variant": variant["variant"],
                        "dataset_id": variant["dataset_id"],
                        "revision": variant["revision"],
                        "material_role": variant["material_role"],
                    }
                )
            audit = {
                "files": file_audits,
                "target_memberships": len(rows),
                "raw_solution_files_persisted": False,
                "solution_fields_returned": False,
            }
            write_json(
                path,
                {
                    "revision": variant["revision"],
                    "projection": projection,
                    "records": rows,
                    "records_sha256": fingerprint(rows),
                    "audit": audit,
                },
            )
        all_records.extend(rows)
        audits.append({"variant": variant["variant"], **audit})
        print(
            json.dumps({"variant": variant["variant"], "target_memberships": len(rows)}), flush=True
        )
    groups = alias_union(all_records)
    write_json(
        args.output_dir / "benchmark-pr-alias-union.json",
        {
            "schema": "temporal-benchmark-pr-alias-union-v2",
            "observed_at": now(),
            "projection_version": METADATA_PROJECTION_VERSION,
            "source_register": str(args.register),
            "target_repository": register["target_repository"],
            "variant_count": len(audits),
            "membership_count": len(all_records),
            "distinct_pr_count": len(groups),
            "records": groups,
            "source_audits": audits,
            "original_issue_union_complete": False,
            "qualified_N": None,
            "solution_fields_returned": False,
            "raw_solution_files_persisted": False,
        },
    )
    print(f"Projected {len(all_records)} memberships into {len(groups)} PR identities", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
