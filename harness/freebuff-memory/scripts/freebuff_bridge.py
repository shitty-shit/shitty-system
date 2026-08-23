#!/usr/bin/env python3
"""Bridge Freebuff's local thread database and IJFW handoffs to shared memory.

Freebuff's SQLite database remains the authoritative raw conversation source.
This script reads it without mutation, fingerprints individual threads, renders
text-only transcripts on demand, and publishes IJFW's sanitized handoff to the
shared D: drive as OKF paperwork.
"""

from __future__ import annotations

import argparse
from contextlib import closing
import datetime as dt
import hashlib
import html
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE_ROOT = Path.home() / ".config" / "freebuff-desktop"
DEFAULT_PROJECT = REPO_ROOT.parent
DEFAULT_HANDOFF = REPO_ROOT / "ijfw" / "memory" / "handoff.md"
DEFAULT_SHARED_ROOT = Path(os.environ.get("SHITTYSHIT_ROOT", "D:/SHITTYSHIT"))

SECRET_PATTERNS = (
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "[REDACTED:private-key]"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"), "[REDACTED:api-key]"),
    (re.compile(r"\bgh(?:p|o|u|s|r)_[A-Za-z0-9]{30,}\b"), "[REDACTED:github-token]"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"), "[REDACTED:google-api-key]"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED:aws-key]"),
)


def redact(text: str) -> str:
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso_from_ms(value: int | None) -> str | None:
    if not value:
        return None
    seconds = value / 1000 if value > 10_000_000_000 else value
    return dt.datetime.fromtimestamp(seconds, dt.timezone.utc).isoformat(timespec="seconds")


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def project_db(project_path: Path, state_root: Path) -> Path:
    wanted = os.path.normcase(str(project_path.resolve()))
    projects_root = state_root / "projects"
    for metadata_path in projects_root.glob("*/project.json"):
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            recorded = os.path.normcase(str(Path(metadata["projectPath"]).resolve()))
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
            continue
        if recorded == wanted:
            database = metadata_path.parent / metadata.get("database", "desktop-v2.db")
            if database.is_file():
                return database
    raise FileNotFoundError(f"No Freebuff database found for {project_path} under {projects_root}")


def open_read_only(path: Path) -> sqlite3.Connection:
    uri = f"file:{path.resolve().as_posix()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def parsed_json(value: str, fallback: Any) -> Any:
    try:
        return json.loads(value)
    except (TypeError, ValueError, json.JSONDecodeError):
        return fallback


def thread_payload(connection: sqlite3.Connection, thread_id: str) -> dict[str, Any]:
    thread = connection.execute(
        """SELECT id, project_id, project_path, title, status, harness_id, model,
                  created_at, updated_at
           FROM threads WHERE id = ?""",
        (thread_id,),
    ).fetchone()
    if thread is None:
        raise KeyError(f"Thread not found: {thread_id}")
    messages = []
    for row in connection.execute(
        """SELECT seq, role, parts_json, attachments_json, ts
           FROM messages WHERE thread_id = ? ORDER BY seq""",
        (thread_id,),
    ):
        messages.append(
            {
                "seq": row["seq"],
                "role": row["role"],
                "parts": parsed_json(row["parts_json"], []),
                "attachments": parsed_json(row["attachments_json"], []),
                "ts": row["ts"],
            }
        )
    return {"thread": dict(thread), "messages": messages}


def payload_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def text_parts(parts: Any) -> str:
    if not isinstance(parts, list):
        return ""
    chunks = []
    for part in parts:
        if not isinstance(part, dict) or part.get("kind") != "text":
            continue
        value = part.get("text")
        if isinstance(value, str) and value.strip():
            chunks.append(value.strip())
    return "\n\n".join(chunks)


def render_transcript(payload: dict[str, Any]) -> str:
    thread = payload["thread"]
    digest = payload_hash(payload)
    lines = [
        "---",
        "type: Source Transcript",
        f'title: "{str(thread["title"]).replace(chr(34), chr(39))}"',
        f"source_thread_id: {thread['id']}",
        f"sha256: {digest}",
        "status: raw-reference",
        "---",
        "",
        f"# {thread['title']}",
        "",
        "> Text-only rendering from Freebuff's read-only SQLite source. Tool calls,",
        "> reasoning, advertisements, and file-change payloads are omitted.",
        "",
    ]
    for message in payload["messages"]:
        body = redact(text_parts(message["parts"]))
        if not body:
            continue
        stamp = iso_from_ms(message["ts"])
        lines.extend([f"## {message['role'].title()} — {stamp}", "", body, ""])
    return "\n".join(lines).rstrip() + "\n"


def thread_summary(payload: dict[str, Any], database: Path) -> dict[str, Any]:
    thread = payload["thread"]
    roles: dict[str, int] = {}
    for message in payload["messages"]:
        roles[message["role"]] = roles.get(message["role"], 0) + 1
    return {
        "source_id": f"freebuff-thread-{thread['id']}",
        "thread_id": thread["id"],
        "title": thread["title"],
        "harness": thread["harness_id"],
        "model": thread["model"],
        "status": thread["status"],
        "created": iso_from_ms(thread["created_at"]),
        "updated": iso_from_ms(thread["updated_at"]),
        "message_count": len(payload["messages"]),
        "roles": roles,
        "sha256": payload_hash(payload),
        "database": str(database),
        "raw_policy": "Database is authoritative; do not copy raw transcript into memory.",
    }


def list_threads(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = connection.execute(
        """SELECT t.id, t.title, t.status, t.harness_id, t.model,
                  t.created_at, t.updated_at, COUNT(m.seq) AS message_count
           FROM threads t LEFT JOIN messages m ON m.thread_id = t.id
           GROUP BY t.id ORDER BY t.updated_at DESC"""
    ).fetchall()
    result = []
    for row in rows:
        item = dict(row)
        item["created_at"] = iso_from_ms(item["created_at"])
        item["updated_at"] = iso_from_ms(item["updated_at"])
        result.append(item)
    return result


def yaml_text(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def normalize_ijfw_handoff(content: str) -> str:
    """Restore IJFW's safe one-line markdown encoding for handoff documents."""
    decoded = html.unescape(content)
    if decoded.startswith(">") and " | " in decoded:
        decoded = decoded.replace(" | ", "\n")
    return decoded.strip()


def publish_handoff(handoff_file: Path, shared_root: Path, thread_id: str | None) -> dict[str, Any]:
    if not handoff_file.is_file():
        raise FileNotFoundError(f"IJFW handoff not found: {handoff_file}")
    source_content = redact(handoff_file.read_text(encoding="utf-8").strip())
    if not source_content:
        raise ValueError(f"IJFW handoff is empty: {handoff_file}")
    digest = hashlib.sha256(source_content.encode("utf-8")).hexdigest()
    content = normalize_ijfw_handoff(source_content)
    now = utc_now()
    stamp = now.strftime("%Y-%m-%dT%H%M%SZ")
    handoffs_dir = shared_root / "00_MASTER" / "handoffs" / "freebuff"
    history_path = handoffs_dir / f"{stamp}-{digest[:8]}.md"
    latest_path = handoffs_dir / "LATEST.md"
    source_line = f"source_thread_id: {thread_id}\n" if thread_id else ""
    document = (
        "---\n"
        "type: Handoff\n"
        f"title: {yaml_text('Freebuff / IJFW session handoff')}\n"
        "description: Sanitized cross-chat handoff mirrored from IJFW for all local agents.\n"
        "tags: [handoff, freebuff, ijfw, a2a]\n"
        f"generated: {{ by: freebuff/ijfw-bridge, at: {now.isoformat()} }}\n"
        f"source: {yaml_text(str(handoff_file))}\n"
        f"source_sha256: {digest}\n"
        f"{source_line}"
        "status: live\n"
        "---\n\n"
        "# Freebuff / IJFW session handoff\n\n"
        f"{content}\n"
    )
    existing = latest_path.read_text(encoding="utf-8") if latest_path.is_file() else ""
    duplicate = existing == document
    if not duplicate:
        atomic_write(history_path, document)
        atomic_write(latest_path, document)
        log_path = shared_root / "00_MASTER" / "memory-loop" / "raw" / "freebuff" / "devlog.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        event = {
            "ts": now.isoformat(),
            "kind": "handoff_published",
            "source": str(handoff_file),
            "source_sha256": digest,
            "thread_id": thread_id,
            "handoff": str(history_path),
        }
        with log_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return {
        "published": not duplicate,
        "sha256": digest,
        "history": str(history_path if not duplicate else latest_path),
        "latest": str(latest_path),
    }


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    ap.add_argument("--state-root", type=Path, default=DEFAULT_STATE_ROOT)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("threads", help="List Freebuff threads for this project")
    inspect = sub.add_parser("inspect", help="Fingerprint one thread without exporting it")
    inspect.add_argument("--thread-id", required=True)
    transcript = sub.add_parser("transcript", help="Render a redacted text-only transcript")
    transcript.add_argument("--thread-id", required=True)
    transcript.add_argument("--output", type=Path)
    publish = sub.add_parser("publish-handoff", help="Mirror IJFW's sanitized handoff to D: shared memory")
    publish.add_argument("--handoff-file", type=Path, default=DEFAULT_HANDOFF)
    publish.add_argument("--shared-root", type=Path, default=DEFAULT_SHARED_ROOT)
    publish.add_argument("--thread-id")
    return ap


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "publish-handoff":
            print(json.dumps(publish_handoff(args.handoff_file, args.shared_root, args.thread_id), indent=2))
            return 0
        database = project_db(args.project, args.state_root)
        with closing(open_read_only(database)) as connection:
            if args.command == "threads":
                print(json.dumps(list_threads(connection), ensure_ascii=False, indent=2))
            elif args.command == "inspect":
                print(json.dumps(thread_summary(thread_payload(connection, args.thread_id), database), ensure_ascii=False, indent=2))
            elif args.command == "transcript":
                rendered = render_transcript(thread_payload(connection, args.thread_id))
                if args.output:
                    atomic_write(args.output, rendered)
                    print(json.dumps({"output": str(args.output), "bytes": len(rendered.encode('utf-8'))}, indent=2))
                else:
                    sys.stdout.write(rendered)
        return 0
    except (FileNotFoundError, KeyError, OSError, sqlite3.Error, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
