#!/usr/bin/env python3
"""
MCP Server for the Agent Memory Loop.

Exposes memory tools via the Model Context Protocol (JSON-RPC 2.0 over stdio).
Agents connect to this server to read/write memory without hitting the HTTP API
directly — they get native tool calls.

Usage:
    python mcp_server.py

Configure in Claude Desktop (~/.config/claude/claude_desktop_config.json):
    {
      "mcpServers": {
        "memory-loop": {
          "command": "python",
          "args": ["path/to/memory-loop/mcp_server.py"],
          "env": {
            "ANYTHINGLLM_API_KEY": "your-key",
            "ANYTHINGLLM_BASE_URL": "http://localhost:3001"
          }
        }
      }
    }

Or with Freebuff / Codex / any MCP-compatible orchestrator.
"""

from __future__ import annotations

import json
import sys
from typing import Any

# Ensure we can import memory from the same directory
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from memory import MemoryLoop, _load_config

# ---------------------------------------------------------------------------
# Tool definitions (MCP schema)
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "remember",
        "description": (
            "Write a memory entry to the persistent Agent Memory Loop. "
            "Use this after discovering something important, making a decision, "
            "or finishing work that another agent should know about. "
            "Entries are indexed by LanceDB for semantic retrieval."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["observation", "decision", "question", "fact", "handoff", "correction"],
                    "description": "What kind of memory this is.",
                },
                "title": {
                    "type": "string",
                    "description": "One-line summary of what was observed or decided.",
                },
                "body": {
                    "type": "string",
                    "description": "Full context: what happened, what was discovered, what decision was made and why. Enough detail that a future agent reading this cold understands without re-reading source files.",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Category tags for filtering (e.g., ['toolstack', 'routing']).",
                },
                "confidence": {
                    "type": "string",
                    "enum": ["EXTRACTED", "INFERRED", "AMBIGUOUS"],
                    "description": "How certain this knowledge is. EXTRACTED = directly from sources. INFERRED = reasonable conclusion. AMBIGUOUS = uncertain.",
                },
                "source_file": {
                    "type": "string",
                    "description": "Relative path to the file this knowledge came from.",
                },
                "related_nodes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Graphify knowledge graph node IDs this entry relates to.",
                },
                "priority": {
                    "type": "string",
                    "enum": ["P0", "P1", "P2", "P3"],
                    "description": "How important this is for the next agent to see. P0 = critical system spine.",
                },
                "action_taken": {
                    "type": "string",
                    "description": "What the agent did with this knowledge.",
                },
                "next_steps": {
                    "type": "string",
                    "description": "What should happen next, if anything.",
                },
            },
            "required": ["type", "title", "body"],
        },
    },
    {
        "name": "recall",
        "description": (
            "Query the Agent Memory Loop for context relevant to a question. "
            "Performs RAG over all memory entries via LanceDB. "
            "Use this at the start of a session to get current priorities, "
            "recent decisions, and system state."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "What you want to know. Be specific — e.g., 'current priorities and recent decisions about the toolstack' rather than 'what's up?'.",
                },
            },
            "required": ["question"],
        },
    },
    {
        "name": "search_memory",
        "description": (
            "Raw vector search over memory entries. Returns document chunks "
            "semantically similar to the query. Use this when you need to find "
            "specific past entries without the chat layer's summarization."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search terms to find semantically similar memory entries.",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "memory_status",
        "description": (
            "Health check: is the memory loop reachable? How many entries are stored? "
            "Use this to verify the loop is working before relying on it."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "memory_snapshot",
        "description": (
            "List all documents currently in the memory loop workspace. "
            "Returns filenames and metadata for every entry."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]

# ---------------------------------------------------------------------------
# MCP JSON-RPC handler
# ---------------------------------------------------------------------------


class MCPServer:
    """Minimal MCP stdio server. Handles JSON-RPC 2.0 requests line by line."""

    def __init__(self):
        self.loop: MemoryLoop | None = None
        self._initialized = False
        self._server_info = {
            "name": "memory-loop",
            "version": "1.0.0",
        }

    def _get_loop(self) -> MemoryLoop:
        if self.loop is None:
            self.loop = MemoryLoop()
        return self.loop

    def run(self) -> None:
        """Main loop: read JSON-RPC from stdin, write responses to stdout."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                self._send_error(None, -32700, "Parse error")
                continue

            response = self._handle_request(request)
            if response is not None:
                self._send(response)

    def _handle_request(self, request: dict[str, Any]) -> dict[str, Any] | None:
        req_id = request.get("id")
        method = request.get("method", "")
        params = request.get("params", {})

        if method == "initialize":
            return self._handle_initialize(req_id, params)
        elif method == "notifications/initialized":
            # No response for notifications
            return None
        elif method == "tools/list":
            return self._handle_tools_list(req_id)
        elif method == "tools/call":
            return self._handle_tools_call(req_id, params)
        else:
            return self._make_error(req_id, -32601, f"Method not found: {method}")

    def _handle_initialize(self, req_id: Any, params: dict[str, Any]) -> dict[str, Any]:
        self._initialized = True
        return self._make_response(req_id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
            },
            "serverInfo": self._server_info,
        })

    def _handle_tools_list(self, req_id: Any) -> dict[str, Any]:
        return self._make_response(req_id, {"tools": TOOLS})

    def _handle_tools_call(self, req_id: Any, params: dict[str, Any]) -> dict[str, Any]:
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        try:
            result = self._call_tool(tool_name, arguments)
            return self._make_response(req_id, {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2, ensure_ascii=False),
                    }
                ]
            })
        except ValueError as e:
            return self._make_response(req_id, {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: {e}",
                    }
                ],
                "isError": True,
            })
        except Exception as e:
            return self._make_response(req_id, {
                "content": [
                    {
                        "type": "text",
                        "text": f"Unexpected error: {e}",
                    }
                ],
                "isError": True,
            })

    def _call_tool(self, name: str, args: dict[str, Any]) -> Any:
        loop = self._get_loop()

        if name == "remember":
            required = ["type", "title", "body"]
            for field in required:
                if field not in args:
                    raise ValueError(f"Missing required field: {field}")

            return loop.remember(
                type=args["type"],
                title=args["title"],
                body=args["body"],
                tags=args.get("tags", []),
                confidence=args.get("confidence", "EXTRACTED"),
                source_file=args.get("source_file"),
                related_nodes=args.get("related_nodes", []),
                priority=args.get("priority", "P2"),
                action_taken=args.get("action_taken"),
                next_steps=args.get("next_steps"),
            )

        elif name == "recall":
            if "question" not in args:
                raise ValueError("Missing required field: question")
            return loop.recall(args["question"])

        elif name == "search_memory":
            if "query" not in args:
                raise ValueError("Missing required field: query")
            results = loop.search(args["query"])
            return {
                "count": len(results),
                "results": [
                    {
                        "title": r.get("metadata", {}).get("title", r.get("title", "")),
                        "source": r.get("metadata", {}).get("source", ""),
                        "text": r.get("pageContent", r.get("text", ""))[:500],
                    }
                    for r in results
                ],
            }

        elif name == "memory_status":
            return loop.status()

        elif name == "memory_snapshot":
            docs = loop.snapshot()
            return {
                "count": len(docs),
                "documents": [
                    {
                        "name": d.get("name", d.get("title", "")),
                        "id": d.get("id", ""),
                        "created": d.get("createdAt", ""),
                    }
                    for d in docs
                ],
            }

        else:
            raise ValueError(f"Unknown tool: {name}")

    # -- JSON-RPC helpers ---------------------------------------------------

    def _make_response(self, req_id: Any, result: Any) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": req_id, "result": result}

    def _make_error(self, req_id: Any, code: int, message: str) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message},
        }

    def _send_error(self, req_id: Any, code: int, message: str) -> None:
        self._send(self._make_error(req_id, code, message))

    def _send(self, message: dict[str, Any]) -> None:
        sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
        sys.stdout.flush()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    server = MCPServer()
    server.run()
