# Freebuff Shared Memory

Local, repo-backed working memory for Freebuff chats in
`C:\Users\idfk\Desktop\harness`. This is the hot continuity layer, not a
replacement for the LACES_CASES canonical memory loop.

IJFW (`It Just Fucking Works`) is the memory engine. Freebuff connects to its
local MCP server and pins every chat to this repository with
`IJFW_PROJECT_DIR`.

## Canonical paths

- `ijfw/memory/project-journal.md` — append-only timeline of stored memories.
- `ijfw/memory/handoff.md` — latest cross-chat handoff.
- `ijfw/memory/knowledge.md` — durable decisions and patterns.
- `ijfw/wiki/` — promoted concepts, decisions, and milestones.
- `receipts/` — human-readable setup and maintenance receipts.
- `.ijfw/` — generated IJFW indexes and runtime state; not canonical.

## Chat contract

1. At the start of a substantive chat, call `ijfw_memory_prelude` once.
2. Store durable decisions, preferences, discoveries, and corrections when
   they happen.
3. Before ending substantive work, store one compact `handoff` containing:
   what changed, decisions and reasons, open questions, and the next action.
4. Never store credentials, secrets, or raw transcripts.

The goal is continuity, not surveillance. Memory contains compressed working
context so a new chat can resume without replaying old conversations.

## Central memory bridge

The three memory layers have distinct jobs:

1. Freebuff's `desktop-v2.db` is the immutable raw conversation source.
2. IJFW is the compact, fast cross-chat working-memory layer.
3. `D:\SHITTYSHIT` and the guarded `laces_cases memory loop` are the shared
   handoff and canonical-memory surfaces for all local agents.

The bridge reads Freebuff's SQLite database in read-only mode. It does not copy
raw transcripts into memory. It can list or fingerprint a thread, render a
redacted text-only transcript on explicit request, and publish IJFW's sanitized
handoff to `D:\SHITTYSHIT\00_MASTER\handoffs\freebuff\LATEST.md`.

The metadata-only ingest queue is generated with
`scripts/build_ingest_manifest.py`. It records every raw thread's ID, hash,
timestamps, agent/model, and whether a canonical conversation thread exists;
it never copies transcript text.

```powershell
python .\scripts\freebuff_bridge.py threads
python .\scripts\freebuff_bridge.py inspect --thread-id <uuid>
python .\scripts\freebuff_bridge.py publish-handoff --thread-id <uuid>
python .\scripts\build_ingest_manifest.py --output D:\SHITTYSHIT\00_MASTER\conversations\RAW-INGEST-MANIFEST.json
```

Each new central handoff gets an immutable history file and one metadata-only
event in `D:\SHITTYSHIT\00_MASTER\memory-loop\raw\freebuff\devlog.jsonl`.
Publishing the same handoff twice is a no-op.

## Verification

After fully restarting Freebuff:

1. Open a chat in the `harness` workspace and ask it to store a unique canary.
2. Open a separate chat in the same workspace.
3. Ask what the previous chat stored.

The second chat should retrieve the canary through IJFW without receiving the
first chat's raw transcript.

For a local transport and prelude check, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```
