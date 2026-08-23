#!/usr/bin/env python3
"""KISS DECK data builder.

Reads the OKF project ledger (same scanner as gen_projects_dash.py) plus
.state/state.json and injects the data into .state/kiss/kiss.html (which
contains a `__KISS_DATA__` placeholder) to emit .state/kiss/index.html —
a self-contained, zero-dependency cube dashboard prototype.

Usage:  python .state/kiss/gen_kiss.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(HERE, "..", "state.json")
OUT = os.path.join(HERE, "index.html")
TPL = os.path.join(HERE, "kiss.html")

sys.path.insert(0, os.path.dirname(HERE))
from gen_projects_dash import LEDGER, read, load_project  # noqa: E402


def clean(s):
    """Collapse any literal newlines/whitespace inside a text field so JSON stays valid."""
    return re.sub(r"\s+", " ", str(s)).strip()


def next_items(proj, limit=6):
    """Bullet items under the first heading of NEXT_ACTION.md, excluding the
    frontmatter `sources:` block; fall back to the section body."""
    t = read(os.path.join(proj["path"], "NEXT_ACTION.md"))
    # strip frontmatter (everything up to the closing ---) so YAML-ish bullets like
    # `- id: master-card` under `sources:` never leak into the sprite list
    if t.startswith("---"):
        end = t.find("\n---", 3)
        if end > 0:
            t = t[end + 4:]
    items = []
    for ln in t.splitlines():
        m = re.match(r"^\s*[-*]\s+(.*)$", ln)
        if m:
            s = m.group(1).strip()
            if s and not s.startswith("["):  # skip checkbox rows, keep plain bullets
                items.append(s)
        if len(items) >= limit:
            break
    if not items and proj["next_action"]:
        items = [proj["next_action"]]
    return items[:limit]


ROOT = os.path.dirname(os.path.dirname(HERE))  # workspace root (parent of .state/)


def parse_links():
    """Feed recipe: every `- [title](url) — desc` bullet in feeds/links.md
    becomes a link cube. {{ROOT}} expands to this workspace's file:// root."""
    t = read(os.path.join(HERE, "feeds", "links.md"))
    root_url = "file:///" + ROOT.replace("\\", "/")
    links = []
    for ln in t.splitlines():
        m = re.match(r"^\s*-\s+\[([^\]]+)\]\(([^)]+)\)\s*(?:[-—–]\s*(.*))?$", ln)
        if m:
            links.append({
                "title": clean(m.group(1)),
                "url": m.group(2).strip().replace("{{ROOT}}", root_url),
                "desc": clean(m.group(3) or ""),
            })
    return links


def load_state():
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except OSError:
        return {}


def main():
    if not os.path.isdir(LEDGER):
        print(f"ledger not present at {LEDGER} — skipping kiss data")
        return 1

    projects = []
    for folder in sorted(os.listdir(LEDGER)):
        d = os.path.join(LEDGER, folder)
        if not os.path.isdir(d):
            continue
        p = load_project(folder)
        projects.append({
            "folder": p["folder"],
            "title": p["title"],
            "lane": p["lane"],
            "priority": p["priority"],
            "tags": p["tags"],
            "revenue": bool(p["revenue"]),
            "status": clean(p["status"]),
            "nextAction": clean(p["next_action"]),
            "nextItems": [clean(i) for i in next_items(p)],
            "openQuestions": [clean(q) for _, q in p["open_questions"]][:4],
            "sessionLog": [clean(f"{r[0]} | {r[1]}") for r in p["session_log"]],
            "pageHref": f"../projects/pages/{folder}.html",
        })

    st = load_state()
    sessions = st.get("sessions", [])
    last_session = None
    for s in sessions:
        if last_session is None or str(s.get("last_update", "")) > str(last_session.get("last_update", "")):
            last_session = s
    freebuff_chat = ("session: " + last_session["task"]) if last_session and last_session.get("task") else "no chats yet"

    # the AI CODER PLATE — the first function plate of the KISS MVP
    # AICube fields (white paper data model): provider + model per agent
    agents = [
        {"id": "freebuff", "name": "Freebuff", "type": "CLI agent · this workspace",
         "provider": "custom", "model": "deepseek-v4 (Freebuff)",
         "status": "active", "lastSeen": "just now", "chatLoc": freebuff_chat},
        {"id": "goose", "name": "Goose", "type": "CLI agent · Block",
         "provider": "custom", "model": "goose cli (config)",
         "status": "unknown", "lastSeen": "—", "chatLoc": "no recent chats"},
        {"id": "aionui", "name": "Aionui", "type": "CLI agent",
         "provider": "custom", "model": "—",
         "status": "unknown", "lastSeen": "—", "chatLoc": "no recent chats"},
        {"id": "cochat", "name": "Cochat", "type": "CLI agent",
         "provider": "custom", "model": "—",
         "status": "unknown", "lastSeen": "—", "chatLoc": "no recent chats"},
        {"id": "codex", "name": "Codex", "type": "CLI agent · OpenAI",
         "provider": "openai", "model": "codex cli",
         "status": "active", "lastSeen": "last ijfw audit", "chatLoc": "ijfw Trident audits on this machine"},
    ]

    data = {
        "generated": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "projects": projects,
        "agents": agents,
        "links": parse_links(),
        "sessions": sessions,
    }

    with open(TPL, encoding="utf-8") as f:
        tpl = f.read()
    blob = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    if "__KISS_DATA__" not in tpl:
        print(f"ERROR: {TPL} has no __KISS_DATA__ placeholder")
        return 1
    html = tpl.replace("__KISS_DATA__", blob)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"kiss deck: {len(projects)} projects, {len(agents)} agents -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
