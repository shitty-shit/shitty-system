#!/usr/bin/env python3
"""
Agent Memory Loop — Client

Talks to AnythingLLM's API to read and write memory entries for the
persistent agent memory loop.

Usage:
    from memory import MemoryLoop

    loop = MemoryLoop()

    # Write a memory entry
    loop.remember(
        type="observation",
        title="Toolstack routes coding to Codex + Claude Code",
        body="...",
        tags=["toolstack", "routing"],
        related_nodes=["toolstack_md", "codex_claude_code"],
    )

    # Query the memory loop
    context = loop.recall("what coding agents are available?")
    print(context)

    # Or use the module-level convenience functions:
    import memory
    memory.remember(type="fact", title="...", body="...")
    answer = memory.recall("what tools do we use for local models?")
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_BASE_URL = os.environ.get("ANYTHINGLLM_BASE_URL", "http://localhost:3001")
DEFAULT_API_KEY = os.environ.get("ANYTHINGLLM_API_KEY", "")
DEFAULT_WORKSPACE_SLUG = os.environ.get("MEMORY_WORKSPACE_SLUG", "agent-memory-loop")
DEFAULT_WORKSPACE_NAME = "Agent Memory Loop"

CONFIG_DIR = Path.home() / ".config" / "memory-loop"
CONFIG_FILE = CONFIG_DIR / "config.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_config() -> dict[str, Any]:
    """Load persisted config, falling back to env vars and defaults."""
    defaults: dict[str, Any] = {
        "base_url": DEFAULT_BASE_URL,
        "api_key": DEFAULT_API_KEY,
        "workspace_slug": DEFAULT_WORKSPACE_SLUG,
        "workspace_name": DEFAULT_WORKSPACE_NAME,
        "agent_name": os.environ.get("MEMORY_AGENT_NAME", "freebuff-cli"),
    }
    if CONFIG_FILE.exists():
        try:
            saved = json.loads(CONFIG_FILE.read_text())
            defaults.update(saved)
        except (json.JSONDecodeError, OSError):
            pass
    return defaults


def _save_config(data: dict[str, Any]) -> None:
    """Persist config to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


def _slugify(name: str) -> str:
    """Turn a name into a workspace-friendly slug."""
    return (
        name.lower()
        .replace(" ", "-")
        .replace("_", "-")
        .rstrip("-")
    )


def _timestamp() -> str:
    """ISO 8601 timestamp in local time."""
    return datetime.now(timezone.utc).astimezone().isoformat()


def _entry_filename(entry_type: str, title: str) -> str:
    """Generate a chronologically-sortable filename for a memory entry."""
    ts = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d-%H%M%S")
    short = _slugify(title)[:60]
    return f"{ts}-{entry_type}-{short}.md"


# ---------------------------------------------------------------------------
# Memory Loop Client
# ---------------------------------------------------------------------------


class MemoryLoop:
    """Client for the Agent Memory Loop backed by AnythingLLM."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        workspace_slug: str | None = None,
        workspace_name: str | None = None,
        agent_name: str | None = None,
    ):
        config = _load_config()
        self.base_url = (base_url or config["base_url"]).rstrip("/")
        self.api_key = api_key or config["api_key"]
        self.workspace_slug = workspace_slug or config["workspace_slug"]
        self.workspace_name = workspace_name or config["workspace_name"]
        self.agent_name = agent_name or config["agent_name"]
        self.session = requests.Session()
        if self.api_key:
            self.session.headers["Authorization"] = f"Bearer {self.api_key}"
        self.session.headers["Content-Type"] = "application/json"

    # -- Public API ----------------------------------------------------------

    def remember(
        self,
        type: str,
        title: str,
        body: str,
        *,
        tags: list[str] | None = None,
        confidence: str = "EXTRACTED",
        source_file: str | None = None,
        related_nodes: list[str] | None = None,
        priority: str = "P2",
        model: str | None = None,
        session_slug: str | None = None,
        action_taken: str | None = None,
        next_steps: str | None = None,
    ) -> dict[str, Any]:
        """Write a memory entry to the loop.

        Args:
            type: observation, decision, question, fact, handoff, or correction.
            title: One-line summary.
            body: Full context and reasoning.
            tags: List of category tags for filtering.
            confidence: EXTRACTED, INFERRED, or AMBIGUOUS.
            source_file: Relative path to the file this knowledge came from.
            related_nodes: Graphify knowledge graph node IDs.
            priority: P0, P1, P2, or P3.
            model: Which model the agent was running.
            session_slug: Groups entries from the same session.
            action_taken: What the agent did with this knowledge.
            next_steps: What should happen next.
        """
        filename = _entry_filename(type, title)
        md = self._build_entry_markdown(
            type=type,
            title=title,
            body=body,
            tags=tags or [],
            confidence=confidence,
            source_file=source_file,
            related_nodes=related_nodes or [],
            priority=priority,
            model=model,
            session_slug=session_slug,
            action_taken=action_taken,
            next_steps=next_steps,
        )
        return self._upload_document(filename, md)

    def recall(self, question: str, *, top_n: int = 10) -> str:
        """Query the memory loop for context relevant to *question*.

        Sends the question to AnythingLLM's workspace chat endpoint, which
        performs RAG over all indexed memory entries via LanceDB.
        """
        url = urljoin(self.base_url, f"/api/v1/workspace/{self.workspace_slug}/chat")
        payload = {
            "message": (
                f"You are the Agent Memory Loop retrieval system. "
                f"Answer the following question using ONLY the documents "
                f"in this workspace. Cite specific memory entries by their "
                f"filenames and frontmatter. If the workspace doesn't contain "
                f"relevant information, say so.\n\n"
                f"Question: {question}"
            ),
            "mode": "query",
        }
        try:
            resp = self.session.post(url, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data.get("textResponse", data.get("response", str(data)))
        except requests.RequestException as e:
            return f"[Memory loop unavailable: {e}]"

    def search(self, query: str) -> list[dict[str, Any]]:
        """Return raw document chunks semantically similar to *query*.

        Bypasses the chat layer — direct vector search results.
        """
        url = urljoin(self.base_url, f"/api/v1/workspace/{self.workspace_slug}/chat")
        payload = {"message": query, "mode": "query"}
        try:
            resp = self.session.post(url, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            sources = data.get("sources", [])
            return sources
        except requests.RequestException:
            return []

    def snapshot(self) -> list[dict[str, Any]]:
        """Return all documents currently in the workspace."""
        url = urljoin(self.base_url, f"/api/v1/workspace/{self.workspace_slug}")
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data.get("workspace", {}).get("documents", [])
        except requests.RequestException:
            return []

    # -- Setup ---------------------------------------------------------------

    def setup_workspace(
        self,
        *,
        system_prompt: str | None = None,
        seed_dir: str | None = None,
    ) -> bool:
        """Create (or verify) the memory loop workspace in AnythingLLM.

        Args:
            system_prompt: Custom system prompt for the workspace chat.
            seed_dir: Directory of .md files to seed into the workspace.
        """
        # Check if workspace already exists
        existing = self._list_workspaces()
        if self.workspace_slug in existing:
            print(f"Workspace '{self.workspace_slug}' already exists.")
            return True

        # Create workspace
        url = urljoin(self.base_url, "/api/v1/workspace/new")
        payload: dict[str, Any] = {
            "name": self.workspace_name,
        }
        try:
            resp = self.session.post(url, json=payload, timeout=30)
            resp.raise_for_status()
            created = resp.json()
            actual_slug = _slugify(self.workspace_name)
            if actual_slug != self.workspace_slug:
                self.workspace_slug = actual_slug
                self._save_config()
            print(f"Created workspace: {created.get('workspace', {}).get('name', actual_slug)}")
        except requests.RequestException as e:
            print(f"Failed to create workspace: {e}")
            return False

        # Update system prompt if provided
        if system_prompt:
            self._update_system_prompt(system_prompt)

        # Seed with initial documents
        if seed_dir:
            self._seed_from_directory(Path(seed_dir))

        self._save_config()
        return True

    def status(self) -> dict[str, Any]:
        """Health check: is AnythingLLM reachable and is the workspace ready?"""
        result: dict[str, Any] = {
            "anythingllm_reachable": False,
            "workspace_exists": False,
            "document_count": 0,
            "error": None,
        }
        try:
            # Check AnythingLLM is up
            resp = self.session.get(urljoin(self.base_url, "/api/v1/auth"), timeout=10)
            result["anythingllm_reachable"] = resp.status_code == 200
        except requests.RequestException as e:
            result["error"] = str(e)
            return result

        # Check workspace
        workspaces = self._list_workspaces()
        result["workspace_exists"] = self.workspace_slug in workspaces
        if result["workspace_exists"]:
            docs = self.snapshot()
            result["document_count"] = len(docs)

        return result

    # -- Internal ------------------------------------------------------------

    def _build_entry_markdown(
        self,
        type: str,
        title: str,
        body: str,
        tags: list[str],
        confidence: str,
        source_file: str | None,
        related_nodes: list[str],
        priority: str,
        model: str | None,
        session_slug: str | None,
        action_taken: str | None,
        next_steps: str | None,
    ) -> str:
        timestamp = _timestamp()
        tag_list = "\n".join(f"  - {t}" for t in tags)
        node_list = "\n".join(f"  - {n}" for n in related_nodes)
        model_line = f"model: {model}\n" if model else ""
        session_line = f"session: {session_slug}\n" if session_slug else ""
        source_line = f"source_file: {source_file}\n" if source_file else ""

        action_block = ""
        if action_taken:
            action_block = f"\n## Action Taken\n{action_taken}\n"

        next_block = ""
        if next_steps:
            next_block = f"\n## Next\n{next_steps}\n"

        return f"""---
type: {type}
agent: {self.agent_name}
{model_line}{session_line}timestamp: {timestamp}
confidence: {confidence}
tags:
{tag_list}
{source_line}related_nodes:
{node_list}
priority: {priority}
---

# {title}

{body}
{action_block}{next_block}"""

    def _upload_document(self, filename: str, content: str) -> dict[str, Any]:
        """Upload a markdown memory entry to the workspace."""
        # Write to temp file for upload
        tmp = Path(tempfile.gettempdir()) / filename
        tmp.write_text(content, encoding="utf-8")

        url = urljoin(self.base_url, "/api/v1/document/upload")
        try:
            with open(tmp, "rb") as f:
                files = {"file": (filename, f, "text/markdown")}
                # Remove Content-Type header for multipart upload
                headers = {k: v for k, v in self.session.headers.items() if k.lower() != "content-type"}
                resp = requests.post(
                    url,
                    files=files,
                    headers=headers,
                    timeout=30,
                )
                resp.raise_for_status()
                result = resp.json()
        except requests.RequestException as e:
            result = {"error": str(e), "success": False}
        finally:
            tmp.unlink(missing_ok=True)

        # Tag the document for the workspace if needed
        # (AnythingLLM auto-adds uploaded docs to the current workspace context)

        return result

    def _update_system_prompt(self, prompt: str) -> None:
        """Set the workspace's system prompt."""
        url = urljoin(self.base_url, f"/api/v1/workspace/{self.workspace_slug}/update")
        payload = {"openAiPrompt": prompt}
        try:
            self.session.post(url, json=payload, timeout=30)
        except requests.RequestException:
            pass

    def _list_workspaces(self) -> set[str]:
        """Return slugs of all existing workspaces."""
        url = urljoin(self.base_url, "/api/v1/workspaces")
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return {w.get("slug", _slugify(w.get("name", ""))) for w in data.get("workspaces", [])}
        except requests.RequestException:
            return set()

    def _seed_from_directory(self, directory: Path) -> None:
        """Upload all .md files in *directory* to the workspace."""
        md_files = sorted(directory.glob("*.md"))
        if not md_files:
            return
        print(f"Seeding workspace with {len(md_files)} document(s)...")
        for f in md_files:
            content = f.read_text(encoding="utf-8")
            self._upload_document(f.name, content)
            time.sleep(0.5)  # Be gentle to AnythingLLM

    def _save_config(self) -> None:
        """Persist current config to disk."""
        _save_config({
            "base_url": self.base_url,
            "api_key": self.api_key,
            "workspace_slug": self.workspace_slug,
            "workspace_name": self.workspace_name,
            "agent_name": self.agent_name,
        })


# ---------------------------------------------------------------------------
# Module-level convenience API
# ---------------------------------------------------------------------------

_loop: MemoryLoop | None = None


def _get_loop() -> MemoryLoop:
    global _loop
    if _loop is None:
        _loop = MemoryLoop()
    return _loop


def remember(**kwargs: Any) -> dict[str, Any]:
    """Write a memory entry. See MemoryLoop.remember() for parameters."""
    return _get_loop().remember(**kwargs)


def recall(question: str, **kwargs: Any) -> str:
    """Query the memory loop. See MemoryLoop.recall() for parameters."""
    return _get_loop().recall(question, **kwargs)


def search(query: str) -> list[dict[str, Any]]:
    """Raw vector search. See MemoryLoop.search()."""
    return _get_loop().search(query)


def setup_workspace(**kwargs: Any) -> bool:
    """Create and seed the workspace. See MemoryLoop.setup_workspace()."""
    return _get_loop().setup_workspace(**kwargs)


def status() -> dict[str, Any]:
    """Health check. See MemoryLoop.status()."""
    return _get_loop().status()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Agent Memory Loop CLI")
    sub = parser.add_subparsers(dest="command")

    setup_p = sub.add_parser("setup", help="Create and seed the memory loop workspace")
    setup_p.add_argument("--seed-dir", help="Directory of .md files to seed")
    setup_p.add_argument("--system-prompt", help="Custom system prompt")

    remember_p = sub.add_parser("remember", help="Write a memory entry")
    remember_p.add_argument("--type", required=True, choices=["observation", "decision", "question", "fact", "handoff", "correction"])
    remember_p.add_argument("--title", required=True)
    remember_p.add_argument("--body", required=True)
    remember_p.add_argument("--tags", nargs="*", default=[])
    remember_p.add_argument("--confidence", default="EXTRACTED")
    remember_p.add_argument("--source-file")
    remember_p.add_argument("--related-nodes", nargs="*", default=[])
    remember_p.add_argument("--priority", default="P2")
    remember_p.add_argument("--action-taken")
    remember_p.add_argument("--next-steps")

    recall_p = sub.add_parser("recall", help="Query the memory loop")
    recall_p.add_argument("question")

    sub.add_parser("status", help="Health check")

    args = parser.parse_args()

    if args.command == "setup":
        ok = setup_workspace(
            system_prompt=args.system_prompt,
            seed_dir=args.seed_dir,
        )
        sys.exit(0 if ok else 1)
    elif args.command == "remember":
        result = remember(
            type=args.type,
            title=args.title,
            body=args.body,
            tags=args.tags,
            confidence=args.confidence,
            source_file=args.source_file,
            related_nodes=args.related_nodes,
            priority=args.priority,
            action_taken=args.action_taken,
            next_steps=args.next_steps,
        )
        print(json.dumps(result, indent=2))
    elif args.command == "recall":
        print(recall(args.question))
    elif args.command == "status":
        print(json.dumps(status(), indent=2))
    else:
        parser.print_help()
