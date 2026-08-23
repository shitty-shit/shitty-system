from __future__ import annotations

import importlib.util
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_ingest_manifest.py"
SPEC = importlib.util.spec_from_file_location("build_ingest_manifest", SCRIPT)
manifest_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(manifest_module)


class IngestManifestTests(unittest.TestCase):
    def test_manifest_is_metadata_only_and_links_explicit_thread(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            state = root / "state"
            project = root / "project"
            project.mkdir()
            project_id = "22222222-2222-4222-8222-222222222222"
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
                    (1, "thread-1", "user", json.dumps([{"kind": "text", "text": "private source text"}]), "[]", 1000),
                )
                connection.commit()

            shared = root / "shared"
            threads_dir = shared / "00_MASTER" / "conversations" / "threads"
            threads_dir.mkdir(parents=True)
            (threads_dir / "canonical.md").write_text(
                "---\nsource_thread_id: thread-1\n---\n# Canonical\n",
                encoding="utf-8",
            )

            manifest = manifest_module.build_manifest(project, state, shared)
            self.assertEqual(manifest["canonical"]["linked_threads"], 1)
            self.assertEqual(manifest["canonical"]["needs_distillation"], 0)
            self.assertEqual(manifest["threads"][0]["ingest_status"], "linked")
            self.assertEqual(len(manifest["threads"][0]["sha256"]), 64)
            self.assertNotIn("private source text", json.dumps(manifest))


if __name__ == "__main__":
    unittest.main()
