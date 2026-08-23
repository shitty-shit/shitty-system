# Memory Loop Setup Guide

Version: 1.0 | Requires: AnythingLLM Desktop, Python 3.10+

## Overview

The Agent Memory Loop is a persistent, LAN-accessible memory spine for the
ShittyShit / LACES_CASES agent ecosystem. It lives inside AnythingLLM, using
LanceDB for vector search and AnythingLLM's API for read/write access.

After setup, any agent on your network can:
- **Read** context from all previous agent sessions
- **Write** observations, decisions, and facts back into the loop
- **Search** semantically across all memory entries

## Prerequisites

1. **AnythingLLM Desktop** installed and running on the Mothership
2. **API key** enabled in AnythingLLM (Settings → Tools → Developer API)
3. **Python 3.10+** with `requests` installed

## Quick Start

### 1. Set environment variables

```bash
# On the Mothership (where AnythingLLM runs)
export ANYTHINGLLM_API_KEY="your-api-key-from-anythingllm-settings"
export ANYTHINGLLM_BASE_URL="http://localhost:3001"
export MEMORY_AGENT_NAME="freebuff-cli"
```

For agents on other machines on the LAN:
```bash
# Replace 192.168.x.x with the Mothership's LAN IP
export ANYTHINGLLM_API_KEY="your-api-key-from-anythingllm-settings"
export ANYTHINGLLM_BASE_URL="http://192.168.1.100:3001"
export MEMORY_AGENT_NAME="claude-code"
```

### 2. Create the workspace

```bash
cd memory-loop
python memory.py setup --seed-dir seed
```

This creates a workspace called "Agent Memory Loop" in AnythingLLM and
seeds it with the initial context documents (Canonical Tetrad summary,
graphify knowledge graph dump, and architecture overview).

### 3. Test the connection

```bash
python memory.py status
```

Expected output:
```json
{
  "anythingllm_reachable": true,
  "workspace_exists": true,
  "document_count": 3,
  "error": null
}
```

### 4. Write your first memory entry

```bash
python memory.py remember \
  --type observation \
  --title "Memory loop is operational" \
  --body "The Agent Memory Loop workspace is created in AnythingLLM. \
All agents on the LAN can now read and write memory entries via the API." \
  --tags memory-loop setup operational \
  --confidence EXTRACTED
```

### 5. Query the memory loop

```bash
python memory.py recall "what is the memory loop and is it working?"
```

## Using from Python

```python
from memory import MemoryLoop

loop = MemoryLoop()

# Write an observation
loop.remember(
    type="observation",
    title="Discovered that AnythingLLM indexes new docs within 5 seconds",
    body="After uploading a memory entry, LanceDB has it searchable within "
         "2-5 seconds. This means agents can write and immediately read back.",
    tags=["anythingllm", "performance", "indexing"],
    confidence="EXTRACTED",
)

# Query for context
context = loop.recall("how fast does AnythingLLM index documents?")
print(context)

# Direct vector search
results = loop.search("local model routing")
for r in results:
    print(r.get("metadata", {}).get("title"))
```

## Agent Integration

### Freebuff / CLI agents

Add this to your session start and end:

```python
# At session START
from memory import recall
context = recall("current priorities, recent decisions, system state")
print(f"MEMORY CONTEXT:\n{context}")

# ... do work ...

# At session END
from memory import remember
remember(
    type="handoff",
    title=f"Session {session_id} complete",
    body=f"Summary of what was done, decisions made, open questions...",
    tags=["session-handoff"],
    priority="P1",
    next_steps="What the next agent should pick up",
)
```

### Claude Code

Add to `CLAUDE.md`:

```markdown
## Memory Loop

Before starting any task, run:
```bash
python memory-loop/memory.py recall "current priorities, recent decisions, open questions"
```

After completing work, run:
```bash
python memory-loop/memory.py remember \
  --type observation \
  --title "Summary of what was done" \
  --body "..." \
  --tags claude-code session-handoff
```
```

### Codex

Add to `AGENTS.md` memory section:

```markdown
## MEMORY LOOP

At session start, call `python memory-loop/memory.py recall "priorities and context"`.
At session end, call `python memory-loop/memory.py remember ...` with results.
```

## Network Access

To make the memory loop available to agents on other machines:

1. **Ensure AnythingLLM binds to the network interface.**
   In AnythingLLM's `.env` (usually in the AnythingLLM install directory):
   ```
   ANYTHINGLLM_SERVER_HOST=0.0.0.0
   ```
   This makes the API listen on all interfaces, not just localhost.

2. **Find the Mothership's LAN IP:**
   ```bash
   ipconfig  # Windows
   # or
   hostname -I  # Linux
   ```

3. **Agents on other machines use that IP:**
   ```bash
   export ANYTHINGLLM_BASE_URL="http://192.168.1.100:3001"
   ```

## Workspace Structure

The "Agent Memory Loop" workspace contains:

| Document | Purpose |
|---|---|
| `SYSTEM_CONTEXT.md` | Immutable reference: what the memory loop is and how to use it |
| `CANONICAL_TETRAD.md` | Summary of me.md, toolstack.md, projectstack.md, biz.md |
| `GRAPH_DUMP.md` | Dump of the graphify knowledge graph for cross-reference |
| `YYYY-MM-DD-HHMMSS-*.md` | Agent memory entries (grows over time) |

## Troubleshooting

### "AnythingLLM not reachable"
- Is AnythingLLM Desktop running?
- Is the API enabled in Settings → Tools → Developer API?
- Is the API key correct?
- If accessing from LAN, is the host set to `0.0.0.0`?

### "Workspace not found"
- Run `python memory.py setup` again
- Check the workspace slug matches: `agent-memory-loop`

### "Memory entries not searchable"
- AnythingLLM indexes new documents within 2-10 seconds
- Check that the file was uploaded: `python memory.py status` shows document count
- Large documents may take longer to embed

### "Module not found: requests"
```bash
pip install requests
```

## Maintenance

- **Purge old entries:** Delete stale memory files from AnythingLLM's document list
  (in the workspace UI) periodically. Dolt keeps the history if you need it.
- **Check health:** `python memory.py status` before important sessions.
- **Update seed:** When the Canonical Tetrad changes, re-seed with updated docs.
