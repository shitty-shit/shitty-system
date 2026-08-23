from __future__ import annotations

import importlib.util
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "freebuff_bridge.py"
SPEC = importlib.util.spec_from_file_location("freebuff_bridge", SCRIPT)
bridge = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(bridge)


class BridgeTests(unittest.TestCase):
    def test_thread_fingerprint_and_text_render(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            state = root / "state"
            project = root / "project"
            project.mkdir()
            project_id = "11111111-1111-4111-8111-111111111111"
            storage = state / "projects" / f"project-{project_id}"
            storage.mkdir(parents=True)
            (storage / "project.json").write_text(
                json.dumps({"projectPath": str(project), "database": "desktop-v2.db"}),
                encoding="utf-8",
            )
            database = storage / "desktop-v2.db"
            with closing(sqlite3.connect(database)) as connection:
                connection.executescript(
                    """
                    CREATE TABLE threads (
                      id TEXT PRIMARY KEY, project_id TEXT, project_path TEXT,
                      title TEXT, status TEXT, harness_id TEXT, model TEXT,
                      created_at INTEGER, updated_at INTEGER
                    );
                    CREATE TABLE messages (
                      seq INTEGER PRIMARY KEY, thread_id TEXT, role TEXT,
                      parts_json TEXT, attachments_json TEXT, ts INTEGER
                    );
                    """
                )
                connection.execute(
                    "INSERT INTO threads VALUES (?,?,?,?,?,?,?,?,?)",
                    ("thread-1", project_id, str(project), "Example", "open", "codex", "test", 1000, 2000),
                )
                connection.execute(
                    "INSERT INTO messages VALUES (?,?,?,?,?,?)",
                    (1, "thread-1", "user", json.dumps([{"kind": "text", "text": "hello"}]), "[]", 1000),
                )
                connection.execute(
                    "INSERT INTO messages VALUES (?,?,?,?,?,?)",
                    (2, "thread-1", "assistant", json.dumps([{"kind": "reasoning", "text": "hidden"}, {"kind": "text", "text": "world"}]), "[]", 2000),
                )
                connection.commit()
            located = bridge.project_db(project, state)
            self.assertEqual(located, database)
            with closing(bridge.open_read_only(database)) as connection:
                payload = bridge.thread_payload(connection, "thread-1")
            summary = bridge.thread_summary(payload, database)
            self.assertEqual(summary["message_count"], 2)
            self.assertEqual(len(summary["sha256"]), 64)
            rendered = bridge.render_transcript(payload)
            self.assertIn("hello", rendered)
            self.assertIn("world", rendered)
            self.assertNotIn("hidden", rendered)

    def test_publish_handoff_is_idempotent(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            handoff = root / "handoff.md"
            handoff.write_text("Summary without secrets.\n", encoding="utf-8")
            first = bridge.publish_handoff(handoff, root / "shared", "thread-1")
            second = bridge.publish_handoff(handoff, root / "shared", "thread-1")
            self.assertTrue(first["published"])
            self.assertFalse(second["published"])
            self.assertTrue(Path(first["latest"]).is_file())
            log = root / "shared" / "00_MASTER" / "memory-loop" / "raw" / "freebuff" / "devlog.jsonl"
            self.assertEqual(len(log.read_text(encoding="utf-8").splitlines()), 1)

    def test_normalizes_ijfw_safe_markdown(self):
        encoded = "&gt; Summary | Built the bridge. |  | &gt; Next | Test it."
        normalized = bridge.normalize_ijfw_handoff(encoded)
        self.assertEqual(normalized, "> Summary\nBuilt the bridge.\n\n> Next\nTest it.")


if __name__ == "__main__":
    unittest.main()
