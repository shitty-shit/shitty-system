#!/usr/bin/env python3
"""Generate the shared agent work dashboard from state.json.

Usage:  python3 .state/gen_dash.py   ->   writes .state/dash.html
Pure Python standard library — no dependencies.
"""
import html
import json
import os
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(HERE, "state.json")
OUT_PATH = os.path.join(HERE, "dash.html")

BADGE = {
    "open": '<span class="badge badge-open">OPEN</span>',
    "done": '<span class="badge badge-done">DONE</span>',
    "in_progress": '<span class="badge badge-progress">IN PROGRESS</span>',
    "todo": '<span class="badge badge-todo">TODO</span>',
    "blocked": '<span class="badge badge-blocked">BLOCKED</span>',
    "cancelled": '<span class="badge badge-done">CANCELLED</span>',
}


def esc(value):
    return html.escape(str(value))


def fmt_iso(iso):
    try:
        return datetime.fromisoformat(iso).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(iso)


def day_of(iso):
    try:
        return datetime.fromisoformat(iso).strftime("%Y-%m-%d")
    except Exception:
        return ""


def render_sessions(sessions, today):
    if not sessions:
        return '<p class="muted">No sessions recorded yet.</p>'
    cards = []
    for s in sessions:
        status = s.get("status", "open")
        last = s.get("last_update") or s.get("created_at") or ""
        stale = bool(day_of(last)) and day_of(last) < today
        stale_html = (
            ' <span class="badge badge-stale">FROM A PREVIOUS DAY — READY TO CONTINUE</span>'
            if stale else ""
        )
        acc = "".join(f"<li>{esc(x)}</li>" for x in s.get("accomplished", []))
        if not acc:
            acc = '<li class="muted">none recorded</li>'
        nxt = "".join(f"<li>{esc(x)}</li>" for x in s.get("next_steps", []))
        if not nxt:
            nxt = '<li class="muted">none recorded</li>'
        cards.append(
            f"""
        <div class="card">
          <div class="card-head">
            <h3>{esc(s.get('task') or s.get('id') or 'Untitled session')}</h3>
            {BADGE.get(status, esc(status))}{stale_html}
          </div>
          <div class="meta">
            <span>id: {esc(s.get('id', ''))}</span> &middot;
            <span>tab: {esc(s.get('tab', ''))}</span> &middot;
            <span>agent: {esc(s.get('agent', ''))} {esc(s.get('model', ''))}</span> &middot;
            <span>last update: {fmt_iso(last)}</span>
          </div>
          <div class="cols">
            <div class="col">
              <h4>Accomplished so far</h4>
              <ul>{acc}</ul>
            </div>
            <div class="col">
              <h4>Next steps</h4>
              <ul>{nxt}</ul>
            </div>
          </div>
        </div>"""
        )
    return "\n".join(cards)


def render_tasks(tasks):
    if not tasks:
        return '<p class="muted">No tasks in the queue.</p>'
    rows = []
    for t in tasks:
        rows.append(
            "<tr>"
            + f"<td>{BADGE.get(t.get('status', 'todo'), esc(t.get('status', '')))}</td>"
            + f"<td>{esc(t.get('priority', ''))}</td>"
            + f"<td>{esc(t.get('title', ''))}</td>"
            + f"<td>{esc(t.get('session') or '&mdash;')}</td>"
            + f"<td class='muted'>{esc(t.get('notes', ''))}</td>"
            + "</tr>"
        )
    return (
        '<table><thead><tr><th>Status</th><th>Priority</th><th>Task</th>'
        "<th>Session</th><th>Notes</th></tr></thead><tbody>"
        + "\n".join(rows)
        + "</tbody></table>"
    )


def main():
    with open(STATE_PATH, encoding="utf-8") as f:
        st = json.load(f)
    today = date.today().isoformat()
    goals = st.get("goals", {})
    sessions = st.get("sessions", [])
    tasks = st.get("tasks", [])
    open_sessions = [s for s in sessions if s.get("status") == "open"]
    open_tasks = [t for t in tasks if t.get("status") not in ("done", "cancelled")]
    gen_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    brief_snippet = ""
    brief_path = os.path.join(HERE, "LATEST_BRIEF.md")
    if os.path.isfile(brief_path):
        try:
            with open(brief_path, encoding="utf-8") as f:
                brief_head = "\n".join(f.read().splitlines()[:6])
            brief_snippet = (
                '<div class="goal"><b>Latest day brief (butler)</b><br>'
                f'<pre style="white-space:pre-wrap;margin:6px 0 0;font-size:12px;color:#c9d1d9;">{esc(brief_head)}</pre>'
                '<span class="muted">full: .state/LATEST_BRIEF.md</span></div>'
            )
        except OSError:
            pass

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="300">
<title>Agent Work Dashboard</title>
<style>
  :root {{ color-scheme: dark; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font: 14px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
         background: #0f1115; color: #e6e6e6; padding: 32px 20px 60px; }}
  .wrap {{ max-width: 1000px; margin: 0 auto; }}
  h1 {{ font-size: 22px; margin: 0 0 4px; }}
  .sub {{ color: #8a93a3; margin-bottom: 20px; }}
  .sub code, footer code {{ color: #c9d1d9; background: #1c212b; padding: 1px 5px; border-radius: 4px; }}
  h2 {{ font-size: 15px; text-transform: uppercase; letter-spacing: .08em; color: #8a93a3; margin: 28px 0 10px; }}
  .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 14px; }}
  .card {{ background: #161a21; border: 1px solid #262c37; border-radius: 10px; padding: 16px; }}
  .card-head {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
  .card h3 {{ margin: 0; font-size: 15px; line-height: 1.35; }}
  .meta {{ color: #8a93a3; font-size: 12px; margin: 8px 0 12px; }}
  .cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
  @media (max-width: 640px) {{ .cols {{ grid-template-columns: 1fr; }} }}
  .col h4 {{ margin: 0 0 6px; font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: #8a93a3; }}
  ul {{ margin: 0; padding-left: 18px; }}
  li {{ margin-bottom: 4px; }}
  .badge {{ display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: .06em;
            padding: 2px 8px; border-radius: 999px; text-transform: uppercase; }}
  .badge-open {{ background: #143a28; color: #4ade80; }}
  .badge-done {{ background: #262c37; color: #8a93a3; }}
  .badge-progress {{ background: #1e3a5f; color: #60a5fa; }}
  .badge-todo {{ background: #3a2f14; color: #facc15; }}
  .badge-blocked {{ background: #3a1414; color: #f87171; }}
  .badge-stale {{ background: #3a2f14; color: #fbbf24; }}
  table {{ width: 100%; border-collapse: collapse; background: #161a21; border: 1px solid #262c37; border-radius: 10px; overflow: hidden; }}
  th, td {{ text-align: left; padding: 8px 12px; border-bottom: 1px solid #222834; vertical-align: top; }}
  th {{ font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: #8a93a3; }}
  .muted {{ color: #6b7280; }}
  .goal {{ background: #161a21; border: 1px solid #262c37; border-left: 3px solid #60a5fa; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; }}
  .goal b {{ color: #8a93a3; font-size: 11px; text-transform: uppercase; letter-spacing: .06em; }}
  footer {{ margin-top: 36px; color: #6b7280; font-size: 12px; }}
  .rollup {{ font-size: 12px; color: #8a93a3; margin-bottom: 4px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Agent Work Dashboard</h1>
  <div class="sub">LACES_CASES workspace &middot; shared state from <code>.state/state.json</code> &middot;
    <a href="projects/index.html" style="color:#60a5fa">project next-steps board</a> &middot;
    <a href="kiss/index.html" style="color:#2dd4bf">KISS deck (cube dashboard)</a></div>
  <div class="rollup">{len(open_sessions)} open session(s) &middot; {len(open_tasks)} open task(s)</div>

  {brief_snippet}

  <h2>Goals</h2>
  <div class="goal"><b>Overall</b><br>{esc(goals.get('overall', ''))}</div>
  <div class="goal"><b>Today</b><br>{esc(goals.get('today', ''))}</div>

  <h2>Open Sessions — ready to continue</h2>
  <div class="cards">{render_sessions(sessions, today)}</div>

  <h2>Task Queue</h2>
  {render_tasks(tasks)}

  <footer>Generated {gen_time} &middot; auto-reloads every 5 min &middot; refresh data with <code>python3 .state/gen_dash.py</code></footer>
</div>
</body>
</html>"""

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Wrote {OUT_PATH} ({len(doc)} bytes)")


if __name__ == "__main__":
    main()
