#!/usr/bin/env python3
"""KISS inbox bridge — tiny local server for the AI-Coders plate.

Lets the KISS deck (running in a browser) write/read/claim task briefs as
plain markdown files in `.state/kiss/inbox/<agent>/`. Any agent — a Freebuff
tab, cline, goose, codex, aionui, cochat, … — can pick up its folder and work
the briefs. This is the ".md repo to distribute to agents" of the MVP.

Usage:  python .state/kiss/bridge.py [port]      (default 127.0.0.1:8765)

API (CORS-enabled for the deck page):
  GET    /health               -> {"ok": true, "inbox": "<path>", "briefs": n}
  GET    /briefs               -> {"briefs": [{agent, path, task, ts}]}
  POST   /brief                -> body {"agent","name","task","status","chatLoc"}
                                -> {"ok": true, "path": "<abs path of written .md>"}
  DELETE /brief?path=<abs>     -> removes that brief (agent claimed it)

Pure stdlib. No deps. """
import json
import os
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
INBOX = os.path.join(HERE, "inbox")
DECKS = os.path.join(HERE, "decks")
DRAFTS = os.path.join(HERE, "drafts")
CRITIQUES = os.path.join(HERE, "critiques")


def slug(s, n=48):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:n] or "brief"


def brief_path(agent, task):
    d = os.path.join(INBOX, agent)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, time.strftime("%Y%m%d-%H%M%S") + "-" + slug(task) + ".md")


def write_brief(agent, name, task, extra):
    path = brief_path(agent, task)
    body = "\n".join([
        f"# ASSIGN TO {name}",
        f"- agent: {agent}",
        f"- status: {extra.get('status', '')}",
        f"- last chat: {extra.get('chatLoc', '')}",
        f"- created: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## TASK",
        task,
        "",
        "_(Assigned from the KISS deck. Read this brief, do the task, then mark "
        "done + reply via your session log so the dash stays current.)_",
    ])
    with open(path, "w", encoding="utf-8") as f:
        f.write(body + "\n")
    return path


def first_task(p):
    try:
        with open(p, encoding="utf-8") as f:
            t = f.read()
        m = re.search(r"## TASK\s*\n(.*)", t, re.S)
        if m:
            return m.group(1).strip().splitlines()[0].strip() or None
    except OSError:
        pass
    return None


def list_briefs():
    out = []
    if not os.path.isdir(INBOX):
        return out
    for agent in sorted(os.listdir(INBOX)):
        d = os.path.join(INBOX, agent)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(d, fn)
            if fn == "README.md":
                continue
            out.append({"agent": agent, "path": p,
                        "task": first_task(p) or fn[:-3], "ts": fn[:15]})
    return out


def write_critique_brief(agent, draft, draft_text, tasks):
    """Outbound half of Writer Phase 4: a critique brief in the agent's inbox
    carrying the full draft text + the requested analyses, plus the exact file
    the agent should write its response back to (critiques/<slug>.md)."""
    d = os.path.join(INBOX, agent)
    os.makedirs(d, exist_ok=True)
    slugd = slug(draft)
    brief = os.path.join(d, time.strftime("%Y%m%d-%H%M%S") + "-critique-" + slugd + ".md")
    ret = os.path.join(CRITIQUES, slugd + ".md")
    os.makedirs(CRITIQUES, exist_ok=True)
    task_lines = "\n".join("- " + t for t in tasks) if tasks else "- summarize"
    body = "\n".join([
        "# CRITIQUE BRIEF — " + draft,
        "- agent: " + agent,
        "- draft: " + draft,
        "- created: " + time.strftime("%Y-%m-%d %H:%M:%S"),
        "",
        "## REQUESTED",
        task_lines,
        "",
        "## DRAFT TEXT",
        draft_text.strip() or "_(empty draft)_",
        "",
        "## INSTRUCTIONS",
        "Critique the draft above on ONLY the requested items. Be specific and actionable;",
        "quote the text you are critiquing. Then write your critique (plain markdown,",
        "one `##` heading per requested item) to this exact file, then delete this brief:",
        "",
        ret,
    ])
    with open(brief, "w", encoding="utf-8") as f:
        f.write(body + "\n")
    return brief, ret


def critique_file(name):
    n = name if name.lower().endswith(".md") else name + ".md"
    n = re.sub(r"[^A-Za-z0-9 ._-]+", "", n).strip() or "critique.md"
    return os.path.join(CRITIQUES, n)


def list_critiques():
    out = []
    if not os.path.isdir(CRITIQUES):
        return out
    for fn in sorted(os.listdir(CRITIQUES)):
        if fn.endswith(".md") and fn != "README.md":
            p = os.path.join(CRITIQUES, fn)
            try:
                txt = open(p, encoding="utf-8").read()
            except OSError:
                txt = ""
            lines = [l for l in txt.strip().splitlines() if l.strip()]
            preview = lines[0] if lines else "(empty)"
            if len(preview) > 90:
                preview = preview[:90] + "…"
            out.append({"name": fn[:-3], "path": p, "preview": preview,
                        "mtime": time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(p)))})
    return out


class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self._send(200, {})

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/health":
            briefs = list_briefs()
            self._send(200, {"ok": True, "inbox": INBOX, "briefs": len(briefs), "decks": DECKS})
        elif u.path == "/briefs":
            self._send(200, {"briefs": list_briefs()})
        elif u.path == "/decks":
            self._send(200, {"decks": list_decks()})
        elif u.path == "/deck":
            q = parse_qs(u.query)
            name = (q.get("name") or [""])[0]
            p = deck_file(name)
            try:
                with open(p, encoding="utf-8") as f:
                    self._send(200, json.load(f))
            except OSError:
                self._send(404, {"error": "no such deck"})
        elif u.path == "/drafts":
            self._send(200, {"drafts": list_drafts()})
        elif u.path == "/critiques":
            self._send(200, {"critiques": list_critiques()})
        elif u.path == "/critique":
            q = parse_qs(u.query)
            name = (q.get("name") or [""])[0]
            p = critique_file(name)
            try:
                with open(p, encoding="utf-8") as f:
                    self._send(200, {"name": name, "content": f.read()})
            except OSError:
                self._send(404, {"error": "no such critique"})
        elif u.path == "/draft":
            q = parse_qs(u.query)
            name = (q.get("name") or [""])[0]
            p = draft_file(name)
            try:
                with open(p, encoding="utf-8") as f:
                    self._send(200, {"name": name, "content": f.read()})
            except OSError:
                self._send(404, {"error": "no such draft"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        u = urlparse(self.path)
        if u.path not in ("/brief", "/deck", "/draft", "/export", "/critique"):
            return self._send(404, {"error": "not found"})
        try:
            n = int(self.headers.get("Content-Length", 0))
            d = json.loads(self.rfile.read(n) or b"{}")
        except Exception as e:
            return self._send(400, {"error": f"bad body: {e}"})
        if u.path == "/deck":
            name = str(d.get("name") or "")
            if not re.fullmatch(r"[A-Za-z0-9._-]+", name):
                return self._send(400, {"error": "bad deck name (letters/digits/._-)"})
            p = deck_file(name)
            os.makedirs(DECKS, exist_ok=True)
            snap = d.get("snap") or {}
            with _atomic_write(p) as f:
                json.dump({"committed": time.strftime("%Y-%m-%d %H:%M:%S"), "snap": snap},
                          f, indent=2, ensure_ascii=False)
            return self._send(200, {"ok": True, "path": p})
        if u.path in ("/draft", "/export"):
            name = str(d.get("name") or "untitled")
            content = str(d.get("content") or "")
            os.makedirs(DRAFTS, exist_ok=True)
            if u.path == "/export":
                exp = os.path.join(DRAFTS, "export")
                os.makedirs(exp, exist_ok=True)
                base = re.sub(r"[^A-Za-z0-9 _-]+", "", name).strip() or "draft"
                paths = []
                for ext in (".md", ".txt"):
                    p = os.path.join(exp, base + ext)
                    with _atomic_write(p) as f:
                        f.write(content)
                    paths.append(p)
                return self._send(200, {"ok": True, "paths": paths})
            p = draft_file(name)
            with _atomic_write(p) as f:
                f.write(content)
            return self._send(200, {"ok": True, "path": p})
        if u.path == "/critique":
            agent = str(d.get("agent") or "codex").replace("/", "_").replace("\\", "_")
            draft = str(d.get("draft") or "untitled").strip() or "untitled"
            draft_text = str(d.get("draftText") or "")
            tasks = [str(t).strip() for t in (d.get("tasks") or []) if str(t).strip()]
            if not draft_text.strip():
                return self._send(400, {"error": "empty draft text"})
            brief, ret = write_critique_brief(agent, draft, draft_text, tasks)
            return self._send(200, {"ok": True, "brief": brief, "return": ret})
        agent = str(d.get("agent") or "agent").replace("/", "_").replace("\\", "_")
        task = (d.get("task") or "").strip()
        if not task:
            return self._send(400, {"error": "empty task"})
        p = write_brief(agent, d.get("name") or agent, task, d)
        self._send(200, {"ok": True, "path": p})

    def do_DELETE(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        p = (q.get("path") or [""])[0]
        try:
            if p and os.path.isfile(p) and os.path.abspath(p).startswith(os.path.abspath(INBOX)):
                os.remove(p)
                self._send(200, {"ok": True})
            else:
                self._send(400, {"error": "bad path"})
        except OSError as e:
            self._send(500, {"error": str(e)})

    def log_message(self, *a):
        pass


def draft_file(name):
    n = name if name.lower().endswith(".md") else name + ".md"
    n = re.sub(r"[^A-Za-z0-9 ._-]+", "", n).strip() or "untitled.md"  # keep the .md ext
    return os.path.join(DRAFTS, n)


def list_drafts():
    out = []
    if not os.path.isdir(DRAFTS):
        return out
    for fn in sorted(os.listdir(DRAFTS)):
        if fn.endswith(".md") and fn != "README.md":
            p = os.path.join(DRAFTS, fn)
            try:
                words = len(open(p, encoding="utf-8").read().split())
            except OSError:
                words = 0
            out.append({"name": fn[:-3], "words": words,
                        "mtime": time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(p)))})
    return out


def deck_file(name):
    return os.path.join(DECKS, name if name.lower().endswith(".json") else name + ".json")


def list_decks():
    out = []
    if not os.path.isdir(DECKS):
        return out
    for fn in sorted(os.listdir(DECKS)):
        if fn.endswith(".json"):
            p = os.path.join(DECKS, fn)
            mtime = os.path.getmtime(p)
            out.append({"name": fn[:-5], "path": p,
                        "ts": time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))})
    return out


class _atomic_write:
    """Write then rename, so a mid-write crash never leaves a torn deck file."""
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        self.tmp = self.path + ".tmp"
        self.f = open(self.tmp, "w", encoding="utf-8")
        return self.f
    def __exit__(self, *a):
        self.f.close()
        os.replace(self.tmp, self.path)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    os.makedirs(INBOX, exist_ok=True)
    os.makedirs(DECKS, exist_ok=True)
    os.makedirs(DRAFTS, exist_ok=True)
    os.makedirs(os.path.join(DRAFTS, "export"), exist_ok=True)
    os.makedirs(CRITIQUES, exist_ok=True)
    drafts_readme = os.path.join(DRAFTS, "README.md")
    if not os.path.exists(drafts_readme):
        with open(drafts_readme, "w", encoding="utf-8") as f:
            f.write("# Drafts (STFU+WRITE)\n\n"
                    "Source drafts are immutable until you explicitly save from the WRITE "
                    "cube (Ctrl+S / 💾). Exports land in `export/` as .md + .txt. "
                    "The KISS frame never overwrites these silently.\n")
    deck_readme = os.path.join(DECKS, "README.md")
    if not os.path.exists(deck_readme):
        with open(deck_readme, "w", encoding="utf-8") as f:
            f.write("# KISS deck files\n\n"
                    "Committed layouts (the Sharing section of the Machine Sections "
                    "pattern). Each `.json` is one portable deck — move it, share it, "
                    "or load it from the deck toolbar. Representation lives here only "
                    "when you explicitly commit it.\n")
    crit_readme = os.path.join(CRITIQUES, "README.md")
    if not os.path.exists(crit_readme):
        with open(crit_readme, "w", encoding="utf-8") as f:
            f.write("# KISS critiques — returned agent feedback\n\n"
                    "Agents write their critique responses here (one .md per draft), then the\n"
                    "Writer's EDIT · CRITIQUE cube lands them back on the deck as note cubes.\n")
    readme = os.path.join(INBOX, "README.md")
    if not os.path.exists(readme):
        with open(readme, "w", encoding="utf-8") as f:
            f.write("# KISS inbox — briefs for agents\n\n"
                    "Each subfolder is one agent. Each `.md` file is one assigned task.\n\n"
                    "**Protocol:** read your folder → work the brief → update the project's\n"
                    "SESSION_LOG.md with what you did → delete the brief when done (claim).\n\n"
                    "**Critique briefs** (a `CRITIQUE BRIEF` file) ask you to critique a draft:\n"
                    "write your critique (one `##` heading per requested item) to the\n"
                    "`critiques/` file named in the brief's INSTRUCTIONS, then delete the brief.\n"
                    "Agents that read AGENTS.md get pointed here automatically.\n")
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    print(f"kiss bridge on http://127.0.0.1:{port}  (inbox: {INBOX})")
    srv.serve_forever()


if __name__ == "__main__":
    main()