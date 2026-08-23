# MCP Configuration Examples

The memory loop MCP server exposes five tools over stdio. Connect any
MCP-compatible agent to get native tool access without HTTP.

## Tools Exposed

| Tool | What it does |
|---|---|
| `remember` | Write a memory entry (observation, decision, question, etc.) |
| `recall` | Query the loop for context (RAG over all entries) |
| `search_memory` | Raw vector search over entries |
| `memory_status` | Health check — is the loop up? |
| `memory_snapshot` | List all documents in the workspace |

---

## Claude Desktop

Add to `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "memory-loop": {
      "command": "python",
      "args": [
        "C:\\Users\\idfk\\path\\to\\memory-loop\\mcp_server.py"
      ],
      "env": {
        "ANYTHINGLLM_API_KEY": "your-api-key-here",
        "ANYTHINGLLM_BASE_URL": "http://localhost:3001",
        "MEMORY_AGENT_NAME": "claude-code"
      }
    }
  }
}
```

After restarting Claude Desktop, you'll see five `memory-loop/*` tools available.
Claude can call them directly:

```
> Write a memory entry about the routing change we just made.

[Claude calls remember() with type=decision, title="...", body="..."]
```

---

## Freebuff Desktop

Freebuff supports MCP servers natively. Add to your Freebuff config:

```json
{
  "mcp": {
    "servers": [
      {
        "name": "memory-loop",
        "command": "python",
        "args": ["C:\\Users\\idfk\\path\\to\\memory-loop\\mcp_server.py"],
        "env": {
          "ANYTHINGLLM_API_KEY": "your-api-key-here",
          "ANYTHINGLLM_BASE_URL": "http://localhost:3001",
          "MEMORY_AGENT_NAME": "freebuff-cli"
        }
      }
    ]
  }
}
```

---

## Codex

Add to `~/.codex/config.toml`:

```toml
[[mcp_servers]]
name = "memory-loop"
command = "python"
args = ["C:\\Users\\idfk\\path\\to\\memory-loop\\mcp_server.py"]

[mcp_servers.env]
ANYTHINGLLM_API_KEY = "your-api-key-here"
ANYTHINGLLM_BASE_URL = "http://localhost:3001"
MEMORY_AGENT_NAME = "codex"
```

---

## Testing the MCP server manually

You can test the server directly from the command line by sending JSON-RPC
requests to stdin:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python memory-loop/mcp_server.py
```

Expected response:
```json
{"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "memory-loop", "version": "1.0.0"}}}
```

List tools:
```bash
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | python memory-loop/mcp_server.py
```

Call memory_status (AnythingLLM doesn't need to be running for this):
```bash
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"memory_status","arguments":{}}}' | python memory-loop/mcp_server.py
```

---

## How agents should use the tools

### Session start pattern

```
1. Call memory_status → verify loop is reachable
2. Call recall("current priorities, recent decisions, open questions, system state")
   → get the full context laid out by previous agents
```

### During work pattern

```
When you discover something important:
  → Call remember(type="observation", ...)

When you make a decision:
  → Call remember(type="decision", ...)

When you hit something you can't answer:
  → Call remember(type="question", ...)
```

### Session end pattern

```
Call remember(
  type="handoff",
  title="Session YYYY-MM-DD complete",
  body="Summary of what was done, decisions made, open questions...",
  tags=["session-handoff"],
  priority="P1",
  next_steps="What the next agent should start with"
)
```
