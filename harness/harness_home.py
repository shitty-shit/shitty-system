#!/usr/bin/env python3
"""Local-first live Harness Home.

This server is deliberately small and read-only. It inspects the local Docker
stack, the Freebuff SQLite source, the IJFW handoff, .state/state.json, and
recent workspace artifacts, then serves one same-origin dashboard.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import mimetypes
import os
from pathlib import Path
import subprocess
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


ROOT = Path(__file__).resolve().parent
PAGE = ROOT / ".state" / "harness-home" / "index.html"
HANDOFF = ROOT / "freebuff-memory" / "ijfw" / "memory" / "handoff.md"
STATE = ROOT / ".state" / "state.json"
GAPS = ROOT / "ai-system-explainer" / "03-current-state-and-gaps.md"
BRIDGE = ROOT / "freebuff-memory" / "scripts" / "freebuff_bridge.py"

SERVICE_PROBES = [
    ("Open WebUI", "http://127.0.0.1:8080", "web", "shitty-openwebui"),
    ("AnythingLLM", "http://127.0.0.1:3001", "web", "shitty-anythingllm"),
    ("n8n", "http://127.0.0.1:5678", "web", "shitty-n8n"),
    ("LiteLLM", "http://127.0.0.1:4000/health/liveliness", "gateway", "shitty-litellm"),
    ("Chroma", "http://127.0.0.1:8000/api/v2/heartbeat", "database", "shitty-chroma"),
    ("Ollama", "http://127.0.0.1:11434/api/tags", "model runtime", "shitty-ollama"),
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def rel_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def file_href(path: Path) -> str:
    return "/" + rel_path(path)


def safe_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def probe_service(name: str, url: str, kind: str, container: str, containers: dict[str, str]) -> dict[str, object]:
    started = time.perf_counter()
    result: dict[str, object] = {
        "name": name,
        "url": url,
        "kind": kind,
        "container": container,
        "status": "DOWN",
        "detail": "No response",
        "latency_ms": None,
    }
    try:
        request = Request(url, headers={"User-Agent": "HarnessHome/1.0"})
        with urlopen(request, timeout=2.5) as response:
            code = int(response.status)
            result["status_code"] = code
            result["status"] = "HEALTHY" if 200 <= code < 400 else "DEGRADED"
            result["detail"] = f"HTTP {code}"
    except HTTPError as exc:
        result["status_code"] = int(exc.code)
        result["status"] = "DEGRADED"
        result["detail"] = f"HTTP {exc.code}"
    except (URLError, TimeoutError, OSError) as exc:
        result["detail"] = type(exc).__name__
    result["latency_ms"] = round((time.perf_counter() - started) * 1000)
    container_status = containers.get(container)
    if container_status:
        result["container_status"] = container_status
    return result


def docker_containers() -> dict[str, str]:
    try:
        completed = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}|{{.Status}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=4,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return {}
    if completed.returncode != 0:
        return {}
    result: dict[str, str] = {}
    for line in completed.stdout.splitlines():
        if "|" in line:
            name, status = line.split("|", 1)
            result[name.strip()] = status.strip()
    return result


def health_payload() -> dict[str, object]:
    containers = docker_containers()
    services = [probe_service(*probe, containers) for probe in SERVICE_PROBES]
    for name, container in [("Dolt", "shitty-dolt")]:
        status = containers.get(container)
        services.append(
            {
                "name": name,
                "url": "docker://shitty-dolt",
                "kind": "database",
                "container": container,
                "status": "HEALTHY" if status else "DOWN",
                "detail": status or "Container not running",
                "latency_ms": None,
                "container_status": status,
            }
        )
    return {
        "checked_at": now_iso(),
        "services": services,
        "healthy": sum(1 for item in services if item["status"] == "HEALTHY"),
        "total": len(services),
        "containers": containers,
    }


def load_threads() -> dict[str, object]:
    try:
        spec = importlib.util.spec_from_file_location("freebuff_bridge", BRIDGE)
        if spec is None or spec.loader is None:
            raise ImportError("bridge module unavailable")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        database = module.project_db(ROOT, module.DEFAULT_STATE_ROOT)
        with module.open_read_only(database) as connection:
            threads = module.list_threads(connection)
        return {"status": "OK", "database": str(database), "threads": threads[:24]}
    except Exception as exc:  # dashboard must remain useful if Freebuff is closed
        return {"status": "ERROR", "error": f"{type(exc).__name__}: {exc}", "threads": []}


def read_excerpt(path: Path, limit: int = 3200) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError as exc:
        return f"Unable to read {path}: {exc}"


def handoff_payload() -> dict[str, object]:
    if not HANDOFF.is_file():
        return {"status": "MISSING", "source": file_href(HANDOFF), "content": "No IJFW handoff found."}
    stat = HANDOFF.stat()
    return {
        "status": "CURRENT",
        "source": file_href(HANDOFF),
        "path": str(HANDOFF),
        "updated_at": dt.datetime.fromtimestamp(stat.st_mtime, dt.timezone.utc).isoformat(timespec="seconds"),
        "content": read_excerpt(HANDOFF),
    }


EXCLUDED_DIRS = {
    ".git", "__pycache__", ".pytest_cache", "node_modules", "dist", "build",
    ".state/projects/pages", ".ijfw/index", ".state/kiss/inbox", ".state/kiss/drafts",
}


def is_excluded(path: Path) -> bool:
    posix = rel_path(path).replace("\\", "/")
    return any(posix == item or posix.startswith(item + "/") for item in EXCLUDED_DIRS)


def artifacts_payload() -> dict[str, object]:
    items: list[dict[str, object]] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or is_excluded(path):
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        if stat.st_size > 25 * 1024 * 1024:
            continue
        items.append(
            {
                "name": path.name,
                "path": rel_path(path),
                "href": file_href(path),
                "extension": path.suffix.lower().lstrip(".") or "file",
                "size": stat.st_size,
                "updated_at": dt.datetime.fromtimestamp(stat.st_mtime, dt.timezone.utc).isoformat(timespec="seconds"),
            }
        )
    items.sort(key=lambda item: str(item["updated_at"]), reverse=True)
    return {"items": items[:40], "total_scanned": len(items)}


def state_payload() -> dict[str, object]:
    try:
        data = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {"status": "ERROR", "error": str(exc), "goals": {}, "sessions": [], "tasks": []}
    sessions = data.get("sessions", [])
    tasks = data.get("tasks", [])
    return {
        "status": "OK",
        "updated_at": data.get("updated_at"),
        "goals": data.get("goals", {}),
        "sessions": sessions,
        "tasks": tasks,
        "open_tasks": sum(1 for task in tasks if task.get("status") not in {"done", "complete"}),
    }


def blockers_payload() -> dict[str, object]:
    blockers = [
        {
            "severity": "VERIFY",
            "title": "Re-establish the IJFW cross-chat canary",
            "detail": "The current verify.ps1 run reaches the IJFW server but does not recall the setup-time canary. Transport is present; continuity proof needs repair or a refreshed canary.",
            "source": "/freebuff-memory/scripts/verify.ps1",
        },
        {
            "severity": "OPEN DECISION",
            "title": "AnythingLLM memory write is blocked",
            "detail": "The UI is reachable, but the fresh canary chat failed before writing memory because OPENAI_API_KEY is missing. No marker row was created; the fresh retrieval step was not run.",
            "source": "/ANYTHINGLLM-MEMORY-TEST-RECEIPT-2026-08-19.md",
        },
        {
            "severity": "OPEN DECISION",
            "title": "Choose the Unsloth operating mode",
            "detail": "Decide whether the healthy native D-backed server remains the path or moves into the official Docker image after a GPU test.",
            "source": "/ai-system-explainer/03-current-state-and-gaps.md",
        },
        {
            "severity": "OPEN DECISION",
            "title": "Decide whether ComfyUI belongs in the service room",
            "detail": "Image generation is not currently part of the seven-service Compose stack.",
            "source": "/ai-system-explainer/03-current-state-and-gaps.md",
        },
        {
            "severity": "SAFETY",
            "title": "Keep access local unless an authenticated gateway is added",
            "detail": "The current bindings are localhost-only. LAN access should wait for an authenticated gateway.",
            "source": "/ai-system-explainer/03-current-state-and-gaps.md",
        },
    ]
    return {"items": blockers, "source": file_href(GAPS)}


def snapshot() -> dict[str, object]:
    health = health_payload()
    threads = load_threads()
    state = state_payload()
    artifacts = artifacts_payload()
    return {
        "generated_at": now_iso(),
        "health": health,
        "threads": threads,
        "handoff": handoff_payload(),
        "artifacts": artifacts,
        "state": state,
        "blockers": blockers_payload(),
        "links": {
            "cheatsheet": "/HARNESS_CHEATSHEET.html",
            "explainer": "/HARNESS_EXPLAINER.md",
            "slides": "/HARNESS_SYSTEM_SLIDES.html",
            "executive_handoff": "/EXECUTIVE_HANDOFF.md",
            "static_dashboard": "/.state/dash.html",
            "kiss_deck": "/.state/kiss/index.html",
            "bridge_health": "http://127.0.0.1:8765/health",
        },
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "HarnessHome/1.0"

    def log_message(self, format: str, *args: object) -> None:
        print(f"[{self.log_date_time_string()}] {format % args}")

    def send_bytes(self, payload: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802
        route = urlparse(self.path).path
        if route == "/api/snapshot":
            try:
                self.send_bytes(safe_json(snapshot()).encode("utf-8"), "application/json; charset=utf-8")
            except Exception as exc:
                self.send_bytes(safe_json({"error": str(exc)}).encode("utf-8"), "application/json; charset=utf-8", 500)
            return
        if route == "/api/health":
            self.send_bytes(safe_json(health_payload()).encode("utf-8"), "application/json; charset=utf-8")
            return
        if route == "/api/threads":
            self.send_bytes(safe_json(load_threads()).encode("utf-8"), "application/json; charset=utf-8")
            return
        if route in {"/", "/harness-home", "/harness-home/"}:
            self.serve_path(PAGE)
            return
        relative = unquote(route.lstrip("/"))
        candidate = (ROOT / relative).resolve()
        if not self.within_root(candidate):
            self.send_error(HTTPStatus.FORBIDDEN, "Path outside harness root")
            return
        self.serve_path(candidate)

    def within_root(self, path: Path) -> bool:
        try:
            path.relative_to(ROOT)
            return True
        except ValueError:
            return False

    def serve_path(self, path: Path) -> None:
        if not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return
        try:
            payload = path.read_bytes()
        except OSError as exc:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))
            return
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if path.suffix.lower() in {".md", ".txt", ".json", ".py", ".ps1", ".yaml", ".yml"}:
            content_type = "text/plain; charset=utf-8"
        self.send_bytes(payload, content_type)


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the local Harness Home dashboard")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Harness Home: http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
