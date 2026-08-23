#!/usr/bin/env python3
"""Project Next-Steps Board generator.

Reads the OKF project ledger on D: (one folder per project, each with
PROJECT.md + NEXT_ACTION.md / STATUS.md / TASKS.md / OPEN_QUESTIONS.md / SESSION_LOG.md)
and renders, inside this workspace:

  .state/projects/index.html                       — every project's next move in one
                                                     filterable, taggable, color-coded list
  .state/projects/pages/<folder>.html              — one overview page per project
  .state/projects/pages/<folder>/<file>.html       — EVERY .md file in the project folder
                                                     rendered as a browsable page with a
                                                     folder sidebar (mirrors a local md viewer)

Pure Python stdlib (mini markdown renderer included). The ledger is read-only; output
lands in the workspace so it works with the Freebuff preview and the .state/ family.

Usage:  python .state/gen_projects_dash.py
"""
import html
import os
import re
from datetime import datetime
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = r"D:\SHITTYSHIT\01_SCHEMA\projects"
OUT = os.path.join(HERE, "projects")
PAGES = os.path.join(OUT, "pages")

LANE_ORDER = ["ACTIVE", "MUDROOM", "WORKING", "SYSTEM", "INTAKE", "REGISTERED", "PARKED"]
LANE_COLORS = {
    "ACTIVE": ("#143a28", "#4ade80"),
    "MUDROOM": ("#3a2f14", "#fbbf24"),
    "WORKING": ("#143a3a", "#2dd4bf"),
    "SYSTEM": ("#1e3a5f", "#60a5fa"),
    "INTAKE": ("#3a1e3a", "#c084fc"),
    "REGISTERED": ("#2f2f3a", "#a5b4fc"),
    "PARKED": ("#262c37", "#8a93a3"),
}
PRIORITY_COLORS = {
    "1": ("#3a1414", "#f87171"),
    "2": ("#3a2f14", "#fbbf24"),
    "3": ("#1e3a5f", "#60a5fa"),
}
DEFAULT_BADGE = ("#262c37", "#8a93a3")
REVENUE_COLOR = ("#3a3414", "#fde047")

SECTION_RE = re.compile(r"^#{1,4}\s+(.*)$")


def esc(v):
    return html.escape(str(v))


def badge(label, color, title=""):
    bg, fg = color
    t = f' title="{esc(title)}"' if title else ""
    return f'<span class="badge"{t} style="background:{bg};color:{fg}">{esc(label)}</span>'


def lane_badge(lane):
    return badge(lane or "?", LANE_COLORS.get((lane or "").upper(), DEFAULT_BADGE))


def pri_badge(pri):
    p = str(pri or "")
    if not p:
        return ""
    return badge(f"P{p}", PRIORITY_COLORS.get(p, DEFAULT_BADGE), "priority")


def rev_badge(rev):
    if str(rev or "").upper() == "YES":
        return badge("$ revenue", REVENUE_COLOR)
    return ""


def parse_frontmatter(text):
    fm = {}
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end < 0:
        return fm
    for line in text[3:end].splitlines():
        line = line.strip()
        if not line or ":" not in line or line.startswith(("#", "-", "{")):
            continue
        k, _, v = line.partition(":")
        k = k.strip().lower()
        if k == "sources":
            break  # everything after `sources:` belongs to the sources block, not card fields
        v = v.strip().strip('"')
        fm[k] = v
    tags = fm.get("tags", "")
    fm["tags"] = [t.strip().lstrip("#") for t in tags.strip("[]").split(",") if t.strip()]
    return fm


def section(text, names, limit=600):
    """Body of the first header matching any name (case-insensitive), whitespace-collapsed."""
    cur = None
    buf = []
    for ln in text.splitlines():
        m = SECTION_RE.match(ln)
        if m:
            if cur is not None:
                break
            if m.group(1).strip().lower() in names:
                cur = m.group(1).strip()
                continue
        if cur is not None:
            buf.append(ln)
    body = re.sub(r"^>\s?", "", "\n".join(buf).strip(), flags=re.M)
    body = " ".join(body.split())
    return body[:limit] or None


def checkboxes(text, names):
    """Checkbox items under the first matching section: list of (checked, item)."""
    in_sec = False
    out = []
    for ln in text.splitlines():
        m = SECTION_RE.match(ln)
        if m:
            if in_sec:
                break
            if m.group(1).strip().lower() in names:
                in_sec = True
                continue
        if in_sec:
            cm = re.match(r"^\s*[-*]\s*\[([ xX])\]\s*(.*)$", ln)
            if cm:
                out.append((cm.group(1).lower() == "x", cm.group(2).strip()))
    return out


def read(path):
    try:
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def session_rows(text, n=5):
    rows = []
    for ln in text.splitlines():
        ln = ln.strip()
        if ln.startswith("|") and "Date" not in ln and "---" not in ln:
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if len(cells) >= 3:
                rows.append(cells[:3])
    return rows[-n:]


def load_project(folder):
    d = os.path.join(LEDGER, folder)
    proj_path = os.path.join(d, "PROJECT.md")
    text = read(proj_path)
    fm = parse_frontmatter(text)
    codename = fm.get("codename") or folder

    next_file = os.path.join(d, "NEXT_ACTION.md")
    status_file = os.path.join(d, "STATUS.md")
    tasks_file = os.path.join(d, "TASKS.md")
    oq_file = os.path.join(d, "OPEN_QUESTIONS.md")
    log_file = os.path.join(d, "SESSION_LOG.md")

    next_action = (
        section(read(next_file), ["single next move"]) or
        section(read(status_file), ["current next action"]) or
        section(text, ["next action"]) or
        ""
    )
    status = (
        section(read(status_file), ["current status"]) or
        fm.get("master_status", "")
    )
    tasks = {
        "now": checkboxes(read(tasks_file), ["now"]),
        "later": checkboxes(read(tasks_file), ["later"]),
        "done": checkboxes(read(tasks_file), ["done"]),
    }
    oq = checkboxes(read(oq_file), ["open questions"]) or checkboxes(text, ["open questions"])
    sess = session_rows(read(log_file))

    md_files = sorted(
        f for f in os.listdir(d)
        if f.lower().endswith(".md") and os.path.isfile(os.path.join(d, f))
    )

    return {
        "folder": folder,
        "codename": codename,
        "title": fm.get("title") or folder,
        "description": fm.get("description") or "",
        "tags": fm.get("tags", []),
        "lane": fm.get("lane") or "?",
        "master_status": fm.get("master_status") or "",
        "revenue": fm.get("revenue") or "",
        "priority": fm.get("priority") or "",
        "next_action": next_action,
        "status": status,
        "tasks": tasks,
        "open_questions": oq,
        "session_log": sess,
        "md_files": md_files,
        "path": d,
    }


def slug(folder):
    return re.sub(r"[^a-z0-9_-]+", "-", folder.lower()).strip("-") or "project"


# ---------------------------------------------------------------------------
# Mini markdown renderer (pure stdlib)
# ---------------------------------------------------------------------------

def md_inline(text, siblings=None):
    t = escape(text)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)

    def linkify(m):
        label, url = m.group(1), m.group(2).strip()
        if siblings and re.search(r"\.md$", url, re.I):
            base = os.path.basename(url).lower()
            if base in siblings:
                url = base[:-3] + ".html"
        return f'<a href="{escape(url)}">{label}</a>'

    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", linkify, t)
    t = re.sub(r"(?<![\">])(https?://[^\s<]+)", r'<a href="\1">\1</a>', t)
    return t


def split_frontmatter(text):
    """Return (meta_dict, body)."""
    lines = text.splitlines()
    meta = {}
    i = 0
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                for ln in lines[1:j]:
                    if ln.strip().lower().startswith("sources:"):
                        break
                    if ":" in ln and not ln.strip().startswith(("-", "#", "{")):
                        k, _, v = ln.partition(":")
                        meta[k.strip()] = v.strip().strip('"')
                i = j + 1
                break
    return meta, "\n".join(lines[i:])


def md_to_html(text, siblings=None):
    meta, body = split_frontmatter(text)
    lines = body.splitlines()
    out = []
    para = []
    i, n = 0, len(lines)

    def flush():
        if para:
            out.append("<p>" + " ".join(md_inline(p, siblings) for p in para) + "</p>")
            para.clear()

    while i < n:
        s = lines[i].strip()
        if not s:
            flush()
            i += 1
            continue
        if s.startswith("```"):
            flush()
            buf = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>" + escape("\n".join(buf)) + "</code></pre>")
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{md_inline(m.group(2), siblings)}</h{lvl}>")
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,})$", s):
            flush()
            out.append("<hr>")
            i += 1
            continue
        if s.startswith(">"):
            flush()
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            out.append("<blockquote>" + "<br>".join(md_inline(b, siblings) for b in buf) + "</blockquote>")
            continue
        if re.match(r"^[-*+]\s", s):
            flush()
            out.append("<ul>")
            while i < n:
                ls = lines[i].strip()
                if not ls:
                    i += 1
                    break
                if not re.match(r"^[-*+]\s", ls):
                    break
                cm = re.match(r"^[-*+]\s*\[([ xX])\]\s*(.*)$", ls)
                if cm:
                    cls = " class='done'" if cm.group(1).lower() == "x" else ""
                    out.append(f"<li{cls}>{md_inline(cm.group(2), siblings)}</li>")
                else:
                    out.append(f"<li>{md_inline(re.sub(r'^[-*+]\s', '', ls), siblings)}</li>")
                i += 1
            out.append("</ul>")
            continue
        if re.match(r"^\d+\.\s", s):
            flush()
            out.append("<ol>")
            while i < n and re.match(r"^\d+\.\s", lines[i].strip()):
                out.append(f"<li>{md_inline(re.sub(r'^\\d+\\.\\s', '', lines[i].strip()), siblings)}</li>")
                i += 1
            out.append("</ol>")
            continue
        if s.startswith("|"):
            flush()
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            if rows:
                head = rows[0]
                body_rows = [r for r in rows[1:]
                             if not all(re.match(r"^:?-+:?$", c) for c in r)]
                out.append("<table><thead><tr>"
                           + "".join(f"<th>{md_inline(c, siblings)}</th>" for c in head)
                           + "</tr></thead><tbody>")
                for r in body_rows:
                    out.append("<tr>" + "".join(f"<td>{md_inline(c, siblings)}</td>" for c in r) + "</tr>")
                out.append("</tbody></table>")
            continue
        para.append(ln := lines[i].strip())
        i += 1
    flush()

    meta_html = ""
    if meta:
        bits = []
        for k in ("type", "title", "description", "tags", "status", "lane", "priority",
                  "revenue", "codename", "generated"):
            if k in meta:
                bits.append(f"<span class='mk'>{escape(k)}:</span> {escape(meta[k])}")
        if bits:
            meta_html = '<div class="metabox">' + " &middot; ".join(bits) + "</div>"

    return meta_html + "\n".join(out)


# ---------------------------------------------------------------------------
# Page templates
# ---------------------------------------------------------------------------

CSS = """
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body { margin: 0; font: 14px/1.55 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
         background: #0f1115; color: #e6e6e6; padding: 28px 20px 60px; }
  .wrap { max-width: 1100px; margin: 0 auto; }
  h1 { font-size: 22px; margin: 0 0 4px; }
  h2 { font-size: 20px; margin: 22px 0 8px; }
  h3 { font-size: 16px; margin: 18px 0 6px; }
  .sub { color: #8a93a3; margin-bottom: 18px; }
  .sub a, a { color: #60a5fa; text-decoration: none; }
  a:hover { text-decoration: underline; }
  .badge { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: .06em;
           padding: 2px 8px; border-radius: 999px; text-transform: uppercase; margin: 0 3px 3px 0; }
  .controls { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 14px; }
  input[type=text], select { background: #161a21; border: 1px solid #262c37; color: #e6e6e6;
           border-radius: 8px; padding: 7px 10px; font-size: 13px; }
  label.chip { background: #161a21; border: 1px solid #262c37; color: #c9d1d9; border-radius: 999px;
           padding: 5px 12px; font-size: 12px; cursor: pointer; user-select: none; }
  label.chip.active { border-color: #60a5fa; color: #60a5fa; }
  label.chip input { display: none; }
  .prow { background: #161a21; border: 1px solid #262c37; border-radius: 10px; padding: 12px 14px; margin-bottom: 10px; }
  .row-head { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
  .row-head .t { font-weight: 700; font-size: 14px; margin-right: 4px; }
  .next { margin: 6px 0 4px; font-size: 14px; }
  .tags { color: #6b7280; font-size: 12px; }
  .tags span { margin-right: 8px; }
  .card { background: #161a21; border: 1px solid #262c37; border-radius: 10px; padding: 16px; margin-bottom: 12px; }
  .card h3 { margin: 0 0 8px; font-size: 15px; }
  .muted { color: #6b7280; }
  ul { margin: 6px 0; padding-left: 18px; }
  li { margin-bottom: 3px; }
  li.done { color: #6b7280; text-decoration: line-through; }
  .nextbox { background: #12203a; border: 1px solid #2b4a7a; border-radius: 10px; padding: 14px 16px; font-size: 16px; margin-bottom: 12px; }
  table { width: 100%; border-collapse: collapse; background: #161a21; border: 1px solid #262c37; border-radius: 10px; overflow: hidden; }
  th, td { text-align: left; padding: 7px 12px; border-bottom: 1px solid #222834; font-size: 13px; }
  th { font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: #8a93a3; }
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  @media (max-width: 720px) { .grid2 { grid-template-columns: 1fr; } }
  code { background: #1c212b; padding: 1px 5px; border-radius: 4px; font-size: 12px; color: #c9d1d9; }
  pre { background: #10141b; border: 1px solid #262c37; border-radius: 8px; padding: 12px; overflow-x: auto; }
  pre code { background: none; padding: 0; }
  footer { margin-top: 30px; color: #6b7280; font-size: 12px; }
  /* doc view */
  .doc { display: flex; gap: 20px; align-items: flex-start; }
  .side { width: 230px; flex-shrink: 0; position: sticky; top: 20px; background: #161a21;
          border: 1px solid #262c37; border-radius: 10px; padding: 10px; font-size: 12px; }
  .side a { display: block; padding: 3px 8px; border-radius: 6px; color: #c9d1d9; margin-bottom: 2px;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .side a.on { background: #1e3a5f; color: #60a5fa; }
  .side .g { color: #6b7280; text-transform: uppercase; letter-spacing: .06em; font-size: 10px;
             margin: 8px 4px 4px; }
  .docbody { flex: 1; min-width: 0; background: #161a21; border: 1px solid #262c37; border-radius: 10px;
             padding: 20px 24px; }
  .docbody h1 { font-size: 20px; }
  .docbody h2 { border-bottom: 1px solid #222834; padding-bottom: 4px; }
  .metabox { background: #10141b; border: 1px solid #262c37; border-radius: 8px; padding: 8px 12px;
             color: #8a93a3; font-size: 12px; margin-bottom: 16px; }
  .metabox .mk { color: #60a5fa; }
  .pager { display: flex; justify-content: space-between; margin-top: 16px; font-size: 13px; }
  @media (max-width: 720px) { .doc { flex-direction: column; } .side { position: static; width: 100%; } }
"""


def build_index(projects):
    lanes = [l for l in LANE_ORDER if any(p["lane"].upper() == l for p in projects)]
    lanes += sorted({p["lane"].upper() for p in projects if p["lane"].upper() not in LANE_ORDER})
    tag_counts = {}
    for p in projects:
        for t in p["tags"]:
            tag_counts[t.lower()] = tag_counts.get(t.lower(), 0) + 1
    top_tags = sorted(tag_counts, key=lambda t: (-tag_counts[t], t))[:24]

    rows = []
    for p in sorted(
        projects,
        key=lambda p: (
            LANE_ORDER.index(p["lane"].upper()) if p["lane"].upper() in LANE_ORDER else 99,
            int(p["priority"]) if str(p["priority"]).isdigit() else 99,
            p["title"].lower(),
        ),
    ):
        tags_attr = ",".join(t.lower() for t in p["tags"])
        rows.append(f"""
      <div class="prow" data-title="{esc(p['title'].lower())}" data-next="{esc(p['next_action'].lower())}"
           data-tags="{esc(tags_attr)}" data-lane="{esc(p['lane'].upper())}"
           data-pri="{esc(p['priority'])}" data-rev="{esc(p['revenue'].upper())}">
        <div class="row-head">
          <a class="t" href="pages/{slug(p['folder'])}.html">{esc(p['title'])}</a>
          {lane_badge(p['lane'])}
          {pri_badge(p['priority'])}
          {rev_badge(p['revenue'])}
        </div>
        <div class="next">{esc(p['next_action']) or '<span class="muted">(no next action recorded)</span>'}</div>
        <div class="tags">{''.join(f'<span>#{esc(t)}</span>' for t in p['tags'])}</div>
      </div>""")

    chips = "".join(
        f'<label class="chip"><input type="checkbox" value="{esc(t)}" onchange="toggleTag(this)">#{esc(t)}</label>'
        for t in top_tags
    )
    lane_opts = "".join(f'<option value="{esc(l)}">{esc(l)}</option>' for l in lanes)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Project Next-Steps Board</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <h1>Project Next-Steps Board</h1>
  <div class="sub">{len(projects)} projects &middot; ledger <code>D:\\SHITTYSHIT\\01_SCHEMA\\projects</code> &middot;
    <a href="../dash.html">agent work dashboard</a></div>

  <div class="controls">
    <input type="text" id="q" placeholder="Search title or next move…" oninput="apply()">
    <select id="lane" onchange="apply()">
      <option value="">All lanes</option>{lane_opts}
    </select>
    <select id="pri" onchange="apply()">
      <option value="">All priorities</option>
      <option value="1">P1</option><option value="2">P2</option><option value="3">P3</option>
      <option value="other">P4+</option>
    </select>
    <label class="chip"><input type="checkbox" id="rev" onchange="apply()">$ revenue only</label>
    <span class="muted" id="count"></span>
  </div>
  <div class="controls" id="chips">{chips}</div>

  <div id="board">{''.join(rows)}</div>

  <footer>Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} &middot; regenerate with
    <code>python .state/gen_projects_dash.py</code> &middot; source of truth is the ledger .md files</footer>
</div>
<script>
let activeTags = new Set();
function toggleTag(cb) {{
  if (cb.checked) activeTags.add(cb.value); else activeTags.delete(cb.value);
  cb.closest('label').classList.toggle('active', cb.checked);
  apply();
}}
function apply() {{
  const q = document.getElementById('q').value.trim().toLowerCase();
  const lane = document.getElementById('lane').value;
  const pri = document.getElementById('pri').value;
  const rev = document.getElementById('rev').checked;
  let n = 0;
  document.querySelectorAll('.prow').forEach(row => {{
    let ok = true;
    if (q && !(row.dataset.title.includes(q) || row.dataset.next.includes(q))) ok = false;
    if (lane && row.dataset.lane !== lane) ok = false;
    if (pri === 'other') {{ if (['1','2','3'].includes(row.dataset.pri)) ok = false; }}
    else if (pri && row.dataset.pri !== pri) ok = false;
    if (rev && row.dataset.rev !== 'YES') ok = false;
    if (activeTags.size) {{
      const tags = row.dataset.tags.split(',');
      if (![...activeTags].every(t => tags.includes(t))) ok = false;
    }}
    row.style.display = ok ? '' : 'none';
    if (ok) n++;
  }});
  document.getElementById('count').textContent = n + ' of {len(projects)} shown';
}}
apply();
</script>
</body>
</html>"""


def render_task_list(items, done=False):
    if not items:
        return '<li class="muted">none</li>'
    lis = []
    for checked, item in items:
        cls = "done" if checked or done else ""
        lis.append(f'<li class="{cls}">{esc(item)}</li>')
    return "".join(lis)


def build_page(p):
    tasks = p["tasks"]
    s = slug(p["folder"])
    md_links = "".join(
        f"<li><a href='{esc(s)}/{esc(f[:-3] + '.html')}'>{esc(f)}</a>"
        f" <span class='muted'>&middot; {esc(os.path.join(p['path'], f))}</span></li>"
        for f in p["md_files"]
    )
    sess_rows = "".join(
        f"<tr><td>{esc(r[0])}</td><td>{esc(r[1])}</td><td>{esc(r[2])}</td></tr>" for r in p["session_log"]
    ) or '<tr><td colspan="3" class="muted">no session log yet</td></tr>'
    oq = "".join(
        f'<li>{"[x] " if c else "[ ] "}{esc(i)}</li>' for c, i in p["open_questions"]
    ) or '<li class="muted">none recorded</li>'

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{esc(p['title'])} — Next Steps</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="sub"><a href="../index.html">&larr; all projects</a> &middot; <a href="../../dash.html">agent dashboard</a></div>
  <h1>{esc(p['title'])}</h1>
  <div class="sub">{esc(p['codename'])} &middot; {esc(p['folder'])}</div>
  <p>{lane_badge(p['lane'])} {pri_badge(p['priority'])} {rev_badge(p['revenue'])}</p>
  <p class="muted">{esc(p['description'])}</p>

  <h2>Next move</h2>
  <div class="nextbox">{esc(p['next_action']) or '<span class="muted">(no next action recorded)</span>'}</div>

  <h2>Current status</h2>
  <div class="card">{esc(p['status']) or '<span class="muted">(none recorded)</span>'}</div>

  <h2>Tasks</h2>
  <div class="grid2">
    <div class="card"><h3>Now</h3><ul>{render_task_list(tasks['now'])}</ul></div>
    <div class="card"><h3>Later</h3><ul>{render_task_list(tasks['later'])}</ul></div>
    <div class="card"><h3>Done</h3><ul>{render_task_list(tasks['done'], done=True)}</ul></div>
    <div class="card"><h3>Open questions</h3><ul>{oq}</ul></div>
  </div>

  <h2>Session log</h2>
  <table><thead><tr><th>Date</th><th>Agent</th><th>Summary</th></tr></thead>
  <tbody>{sess_rows}</tbody></table>

  <h2>Project files</h2>
  <ul>{md_links}</ul>

  <footer>Folder: <code>{esc(p['path'])}</code> &middot; regenerated by
    <code>python .state/gen_projects_dash.py</code></footer>
</div>
</body>
</html>"""


def build_file_page(p, fname, body_html, files, idx):
    s = slug(p["folder"])
    siblings = {f.lower(): f[:-3] + ".html" for f in files}
    nav = []
    for f in files:
        cls = "on" if f == fname else ""
        nav.append(f'<a class="{cls}" href="{esc(f[:-3] + ".html")}">{esc(f)}</a>')
    prev = files[idx - 1] if idx > 0 else None
    nxt = files[idx + 1] if idx < len(files) - 1 else None
    pager = (
        f'<a href="{esc(prev[:-3] + ".html")}">&larr; {esc(prev)}</a>' if prev else "<span></span>"
    ) + (
        f'<a href="{esc(nxt[:-3] + ".html")}">{esc(nxt)} &rarr;</a>' if nxt else "<span></span>"
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{esc(fname)} — {esc(p['title'])}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="sub">
    <a href="../index.html">all projects</a> &middot;
    <a href="../{esc(s)}.html">{esc(p['title'])}</a> &middot;
    <a href="../../dash.html">agent dashboard</a>
  </div>
  <div class="doc">
    <div class="side">
      <div class="g">{esc(p['title'])}</div>
      {''.join(nav)}
      <div class="g">folder</div>
      <a href="../{esc(s)}.html">↑ project overview</a>
    </div>
    <div class="docbody">
      <div class="muted" style="font-size:12px">{esc(fname)} &middot; {esc(os.path.join(p['path'], fname))}</div>
      {body_html}
      <div class="pager">{pager}</div>
    </div>
  </div>
</div>
</body>
</html>"""


def main():
    os.makedirs(PAGES, exist_ok=True)
    projects = []
    total_files = 0
    for folder in sorted(os.listdir(LEDGER)):
        if not os.path.isdir(os.path.join(LEDGER, folder)):
            continue
        p = load_project(folder)
        if p is None:
            continue
        projects.append(p)
        s = slug(folder)
        # overview page
        with open(os.path.join(PAGES, s + ".html"), "w", encoding="utf-8") as f:
            f.write(build_page(p))
        # one rendered page per .md file
        sub = os.path.join(PAGES, s)
        os.makedirs(sub, exist_ok=True)
        siblings = {f.lower() for f in p["md_files"]}
        for idx, fname in enumerate(p["md_files"]):
            body = md_to_html(read(os.path.join(p["path"], fname)), siblings=siblings)
            with open(os.path.join(sub, fname[:-3] + ".html"), "w", encoding="utf-8") as f:
                f.write(build_file_page(p, fname, body, p["md_files"], idx))
            total_files += 1

    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index(projects))

    missing = [p["title"] for p in projects if not p["next_action"]]
    print(f"Projects board: {len(projects)} projects, {total_files} rendered .md pages")
    print(f"  index.html + overviews + pages written to {OUT}")
    if missing:
        print(f"  WARNING: {len(missing)} projects have no recorded next action (first 8: {', '.join(missing[:8])})")


if __name__ == "__main__":
    main()
