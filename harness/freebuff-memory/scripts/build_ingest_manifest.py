#!/usr/bin/env python3
"""Build a metadata-only queue for raw Freebuff conversations.

The Freebuff SQLite database remains read-only and authoritative. This command
creates a portable manifest of thread identity, provenance, timestamps, and
canonical-link status. It deliberately does not copy transcript text.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
from contextlib import closing

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from freebuff_bridge import (  # noqa: E402
    DEFAULT_PROJECT,
    DEFAULT_SHARED_ROOT,
    DEFAULT_STATE_ROOT,
    list_threads,
    open_read_only,
    payload_hash,
    project_db,
    thread_payload,
)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def canonical_thread_links(shared_root: Path) -> dict[str, str]:
    """Map any explicit raw source thread IDs to canonical thread files."""
    links: dict[str, str] = {}
    threads_dir = shared_root / "00_MASTER" / "conversations" / "threads"
    if not threads_dir.is_dir():
        return links
    pattern = re.compile(r"(?:source_thread_id|thread_id):\s*([^\s\]\},]+)")
    for path in sorted(threads_dir.glob("*.md")):
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for match in pattern.finditer(content):
            links[match.group(1).strip('"\'')] = str(path)
    return links


def build_manifest(project: Path, state_root: Path, shared_root: Path) -> dict:
    database = project_db(project, state_root)
    links = canonical_thread_links(shared_root)
    with closing(open_read_only(database)) as connection:
        rows = list_threads(connection)
        threads = []
        for row in rows:
            payload = thread_payload(connection, row["id"])
            canonical_file = links.get(row["id"])
            threads.append(
                {
                    "source_id": f"freebuff-thread-{row['id']}",
                    "thread_id": row["id"],
                    "title": row["title"],
                    "harness": row["harness_id"],
                    "model": row["model"],
                    "status": row["status"],
                    "created": row["created_at"],
                    "updated": row["updated_at"],
                    "message_count": row["message_count"],
                    "sha256": payload_hash(payload),
                    "canonical_thread": canonical_file,
                    "ingest_status": "linked" if canonical_file else "needs-distillation",
                }
            )
    linked = sum(1 for item in threads if item["canonical_thread"])
    return {
        "schema": "freebuff.raw-ingest-manifest/v1",
        "generated_at": utc_now(),
        "source": {
            "kind": "Freebuff SQLite",
            "project": str(project),
            "database": str(database),
            "policy": "read-only authoritative source; transcript text is not copied into this manifest",
        },
        "canonical": {
            "shared_root": str(shared_root),
            "conversation_dir": str(shared_root / "00_MASTER" / "conversations" / "threads"),
            "linked_threads": linked,
            "needs_distillation": len(threads) - linked,
        },
        "threads": threads,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--state-root", type=Path, default=DEFAULT_STATE_ROOT)
    parser.add_argument("--shared-root", type=Path, default=DEFAULT_SHARED_ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    manifest = build_manifest(args.project, args.state_root, args.shared_root)
    rendered = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_name(f".{args.output.name}.tmp-{os.getpid()}")
        temporary.write_text(rendered, encoding="utf-8", newline="\n")
        os.replace(temporary, args.output)
        print(json.dumps({"output": str(args.output), "threads": len(manifest["threads"]), "bytes": len(rendered.encode("utf-8"))}, indent=2))
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
