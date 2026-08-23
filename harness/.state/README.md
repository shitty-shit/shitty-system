# .state/ — Shared Agent State Layer

The single source of truth for **what is actually going on** across every agent instance
(Freebuff tabs, claude, codex, gemini) and across days. Any agent can read it in one file,
any agent can update it, and it survives end-of-day.

## Why this exists

Multiple agent instances (e.g., two Freebuff tabs) do **not** share conversation memory. They
DO share this filesystem. So the shared memory is a file — `state.json` — plus the dashboard
rendered from it. When a new agent starts (or a new tab opens), `AGENTS.md` at the workspace
root points it here, and it is instantly onboarded to every open session, task, and goal.

## Files

| File | Purpose |
|---|---|
| `state.json` | THE source of truth: goals, sessions, tasks |
| `README.md` | This protocol |
| `gen_dash.py` | Pure-stdlib generator: `state.json` → `dash.html`. Run with `python .state/gen_dash.py` |
| `dash.html` | The web dashboard (open in any browser; regenerated, not live) |

## Two-layer memory strategy

- **Operational layer (this — works now, zero dependencies):** `state.json` holds sessions,
  tasks, and goals. Every agent reads it at start and writes at milestones. This is what
  "without missing a beat" actually runs on.
- **Semantic recall layer (later):** `dotmd/memory-loop/` (AnythingLLM) once proven —
  long-term recall and auto-generated briefs. `dotmd/.ijfw/memory/` is empty and
  `graphify-out/` is a static artifact; treat both as future inputs, not current state.

## Checkpoint rhythm (mandatory for every agent)

1. **On start** — read `state.json`; find your session by `id`, or create one
   (`status: "open"`, `task`, `tab`, timestamps). If another instance already created it,
   adopt it — do not duplicate.
2. **At each milestone** — append to your session's `accomplished`, refresh `next_steps`,
   set `last_update`, and flip statuses in `tasks[]` that you changed.
3. **Before ending a turn** — same as #2, then run `python3 .state/gen_dash.py`.

## Cross-tab rules

- Only edit **your own** session entry. Never rewrite another session's history.
- Always re-read `state.json` before acting — the other tab may have moved since you last looked.
- If a session is `done`, leave it; start a new entry for new work.
- `last_update` is the heartbeat: if it is > 1 day old and status is `open`, the dashboard
  flags the session **FROM A PREVIOUS DAY — READY TO CONTINUE**.

## End-of-day ritual (human, ~1 minute)

1. Tell the current agent to update its session + tasks (or edit `state.json` yourself).
2. Run `python .state/gen_dash.py` (or `py .state/gen_dash.py` if `python` is a dead alias).
3. Open `.state/dash.html` (or keep the Freebuff preview open). Leave it in a browser tab.
4. Next day: open a new Freebuff tab in this workspace → root `AGENTS.md` auto-loads → the
   agent reads `state.json` and resumes the open sessions. Same for claude/codex/gemini if
   they read the root `AGENTS.md` or `dotmd/AGENTS.md`.

## Automation — the data butler (no remembering required)

The whole EOD job is scripted. You never have to remember the ritual:

| Trigger | What happens |
|---|---|
| `python .state/butler.py` (or `--eod`) | Archive a state snapshot, scan today's file activity, summarize today's audits, write the day brief (`archive/YYYY-MM-DD_brief.md` + `LATEST_BRIEF.md`), regenerate `dash.html` |
| Double-click `CLOSE-DAY.bat` | Runs the EOD butler, then opens the dashboard in your browser — for the exhausted-human case |
| Windows Task Scheduler (once registered) | Runs the same EOD pass automatically every day at 23:45 — for the "I forgot everything" case |
| `python .state/butler.py --watch` | While you work: polls `state.json` and regenerates the dashboard whenever it changes |

The butler **never edits** `state.json` sessions or tasks — it only reads state and writes
archive artifacts, the brief, and the dashboard. What agents wrote stays authoritative; the
activity scan is labeled machine-detected so nobody confuses it with real progress notes.

**Next-morning resume loop:** the scheduled butler (or last night's double-click) wrote
`LATEST_BRIEF.md` → a new Freebuff tab loads `AGENTS.md` → the agent reads `state.json`
+ the brief → it resumes the open sessions. Nothing to remember.

## Project Next-Steps Board

The D: project ledger (110 project folders, each with `PROJECT.md` + `NEXT_ACTION.md` /
`TASKS.md` / `STATUS.md` / `OPEN_QUESTIONS.md`) renders to a web board:

- `python .state/gen_projects_dash.py` → `.state/projects/index.html` — every project's
  next move in one list, searchable, filterable by lane / priority / tag / revenue,
  color-coded (lane, P1–P3, revenue) — plus `.state/projects/pages/<folder>.html` — one
  overview page per project (next move, status, tasks now/later/done, open questions,
  session log) — plus `.state/projects/pages/<folder>/<file>.html` — **every .md file**
  in the folder rendered as a browsable page with a folder sidebar + prev/next pager
  (a browser-native replacement for a local markdown viewer; 839 pages for 110 projects).
- The butler's EOD pass regenerates this board automatically along with `dash.html`.
- The ledger .md files remain the source of truth; the board is a read-only view.
  Regenerate after the ledger changes. Open `index.html` from disk for full navigation
  (the Freebuff preview serves one file at a time).

## KISS Deck — AI Coders plate (web MVP)

Scope per direction: ONE working function plate first — the AI coders — before any
mothership / marketplace / community work. That plate is proven on web:

- `python .state/kiss/gen_kiss.py` → `.state/kiss/index.html` — runnable deck
  (template `kiss.html`; data injected from the ledger + `state.json`).
- **Coders plate:** cubes for Freebuff / Goose / Aionui / Cochat / Codex — per-cube
  display toggles (status / last-chat location / queue) and an assign-task input.
- **The .md repo (real dispatch):** `python .state/kiss/bridge.py` starts a local
  server (127.0.0.1:8765). The ➤ send button writes a brief as
  `.state/kiss/inbox/<agent>/<ts>-<task>.md`; the deck lists pending briefs back
  (`inbox: N briefs`), and ✓ claim deletes the file. Root `AGENTS.md` tells every
  agent to check its inbox folder — that's the "distribute to agents" loop.
- **Open cubes for project folders:** `＋ cube` menu — AI-coders starter set,
  searchable project-from-ledger picker (110 projects), or a blank cube.
- **PRD Phase-1 mechanics:** grid snapping (1x1/2x1/2x2), color-coded type borders
  (`basic | ai | app | workflow`), double-click rename, right-click / touch-hold
  "make this cube a…" menu, minimal (white) + dark themes, layout version history
  (last 12 auto-saved snapshots, restorable from the toolbar).
- **Writer plate (STFU+WRITE Phase 2 — Writer Without AI):** `Writer` preset —
  the six functional cubes (WRITE / PROJECT / SOURCE / VOICE / EDIT / OUTPUT) and
  five modes (FLOW / FREEWRITE / EDIT / REFERENCE / OUTPUT, Ctrl+1..5) that remap
  the grid. The WRITE cube is a silent monospace surface bound to real `.md`
  drafts via the bridge (`/draft`): typing is representation-only, Ctrl+S commits
  to `drafts/`, Ctrl+E exports `.md` + `.txt` to `drafts/export/` — the
  non-destructive Lightroom rule, verified. Phase 4/5 (AI critique, STEM-Lite)
  are stubbed as hidden-until-summoned cubes.
- Docs: `kiss/PRD.md` (canonical spec) + `kiss/MASTER_SYNTHESIS.md` (vision) + `kiss/JOURNEY.md` (history) + `kiss/MACHINE_SECTIONS.md` (six sections mapped to the running code, with the cube-drag flow).
- **The frame:** the deck is a kind-agnostic frame — grids, persistence, menus and the
  bridge never change; new kinds plug in via `kiss/feeds/README.md` (renderer, behaviors,
  interactions, type, feed). Proven by adding **link cubes**: `feeds/links.md` bullets
  (with `{{ROOT}}` expansion) become app-type cubes that open/copy URLs.
- The butler's EOD pass regenerates the deck with the board and dashboard.


## Notes

- Both tabs must open the **same workspace root** — that is what makes the file shared.
- If the workspace root ever becomes a git repo, add `.state/` (or at least `dash.html`)
  to `.gitignore` — `state.json` changes constantly.
- `dash.html` is static: it reloads every 5 minutes, but only shows new data after you
  re-run `gen_dash.py`.
