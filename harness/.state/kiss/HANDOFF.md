# KISS DASHBOARD — EXECUTIVE HANDOFF & CHEAT SHEET

> **Who this is for:** anyone (or any agent) picking up this workspace with little or no
> context. Read §1, skim §2, and use §3–§8 as reference. Every file name is a link.
> Last updated 2026-08-19. Companion pieces: `slides.html` (the explainer deck) and
> `diagrams/system-map.svg` (the one-picture map).

---

## 1. The sixty-second story

We built a **cube-based dashboard** — think a blank grid of white tiles you can drag,
stack, rename, resize, and remap — and proved it on the web with two working "plates"
(function decks): one for **AI coding agents**, one for **writing**. Everything is
**local-first**: files, not cloud. The whole system runs on Python's standard library
and one zero-dependency HTML file.

The idea (from the canon docs): 1980s submarine sonar panels — big tactile pads whose
whole faceplate could be *remapped instantly* without rewiring. The digital version:
cubes whose meaning is defined entirely by the user. The one governing rule:
**move representations first; commit to files only when explicitly requested**
(the "Commit gate").

What actually works today, end-to-end, verified live:

- **Coders plate** — cubes for Freebuff / Goose / Aionui / Cochat / Codex. Type a task
  in a cube, press **➤ send** → a real `.md` brief lands in that agent's `inbox/`
  folder → the deck shows `inbox: N briefs` → the agent works it and claims it.
- **Writer plate (STFU+WRITE)** — a quiet writing surface bound to real `.md` drafts.
  Typing touches **no file**; **Ctrl+S** commits to `drafts/`, **Ctrl+E** exports.
  Phase 4 critique loop: ship a finished draft to an agent as a critique brief
  (summarize / structure / key phrases), and the returned critique lands back on the
  deck as a note cube.
- **The frame** underneath both — grid, snapping, stacking, history, themes, menus,
  persistence, and a **live machine-sections tracer** that lights up the actual
  data-flow diagram in the corner of the screen as you drag.

---

## 2. The one-picture map

```
diagrams/system-map.svg   ← open this. Every box is a real file, every arrow a real command.
```

(Also embedded as slide 3 of `slides.html`, and the two canonical data-flow figures
live in `diagrams/` — see §6.)

---

## 3. Run it — the cheat sheet

All commands run from this workspace root (`...\SHITTYSHIT`).

| What you want | Command |
|---|---|
| **The deck** (main thing to look at) | `python .state/kiss/gen_kiss.py` then open `.state/kiss/index.html` (or serve the folder) |
| **The bridge** (needed for briefs/drafts/decks) | `python .state/kiss/bridge.py` → lives at `http://127.0.0.1:8765` (`/health` to check) |
| **The state dashboard** | `python .state/gen_dash.py` → open `.state/dash.html` |
| **The projects board** (110 projects, 839 pages) | `python .state/gen_projects_dash.py` → open `.state/projects/index.html` |
| **End-of-day butler** | `python .state/butler.py --eod` — or just double-click `.state/CLOSE-DAY.bat` |
| **Butler watch mode** | `python .state/butler.py --watch` (regenerates dash on every state change) |
| **Regenerate everything** | the butler's EOD pass already does deck + board + dash |
| **Mini Me (phone view)** | open the deck with `?mini` (or any window ≤ 820px wide) |
| **Point a phone at the bridge** | open the deck with `?bridge=192.168.x.x:8765` (LAN IP of the Mothership) |
| **IJFW audits** | `ijfw cross audit <file>` — see `.ijfw/` and `dotmd/ijfw/` |

**Where things live on disk**

| Thing | Path |
|---|---|
| Deck template (the frame, all logic) | `.state/kiss/kiss.html` |
| Deck build (generated, open this) | `.state/kiss/index.html` |
| Bridge server | `.state/kiss/bridge.py` |
| Deck data builder | `.state/kiss/gen_kiss.py` |
| Agent inbox (real briefs) | `.state/kiss/inbox/<agent>/` |
| Writer drafts | `.state/kiss/drafts/` (`export/` for exports) |
| Returned critiques | `.state/kiss/critiques/` |
| Committed deck files | `.state/kiss/decks/` |
| Kind feeds (recipe + link feed) | `.state/kiss/feeds/` |
| PWA / Android assets | `.state/kiss/manifest.json`, `sw.js`, `icon.svg`, `icon-192.png`, `icon-512.png` |
| Android build guide | `.state/kiss/ANDROID_BUILD.md` |
| State memory | `.state/state.json` (source of truth), `.state/dash.html` (view) |
| State protocol | `.state/README.md` |
| Butler | `.state/butler.py`, `.state/CLOSE-DAY.bat` |
| Projects board generator | `.state/gen_projects_dash.py` |
| The agent handshake | `AGENTS.md` at workspace root (and `dotmd/AGENTS.md`) |

**The bridge API** (all JSON, `127.0.0.1:8765`, CORS open):

| Route | Method | What it does |
|---|---|---|
| `/health` | GET | `{ok, inbox, briefs, decks}` — is it up? |
| `/briefs` · `/decks` · `/drafts` · `/critiques` | GET | list each store |
| `/brief` | POST | write `inbox/<agent>/<ts>-<task>.md` — the only disk touch on dispatch |
| `/critique` | POST | write a critique brief for an agent (draft + tasks + return path) |
| `/draft` | GET/POST | read / commit a writer draft |
| `/export` | POST | write `.md` + `.txt` to `drafts/export/` |
| `/deck` | GET/POST | load / commit a deck file (the Commit gate) |
| `/critique` | GET | read a returned critique |
| `/brief?path=…` | DELETE | claim a brief (agent deletes its file) |

---

## 4. What was built — the full inventory

### The frame — `kiss.html` (one file, zero dependencies)
The entire cube engine. Kinds, grid + snapping (1×1 / 2×1 / 2×2), drag / resize /
collapse / stack, double-click rename, right-click / touch-hold "make this cube a…"
menu, type borders (`basic | ai | app | workflow`), ⚡ behavior chips, minimal + dark
themes, 12-version layout history, debounced autosave, the **Commit gate**, and the
live machine-sections tracer. **Rendering is always a pure function of the `deck`
object** — that single rule is why new kinds plug in without touching the engine.

### The bridge — `bridge.py` (port 8765)
The local stand-in for Firestore and the **Agent Layer binding**. It is the *only*
component that writes files: inbox briefs, deck commits, drafts, exports, critiques.
Atomic writes, sanitized names, CORS open so a phone can dock to it.

### The generators
- `gen_kiss.py` — injects the ledger (110 projects), `state.json` sessions, and feeds
  into `kiss.html` → `index.html`, with `{{ROOT}}` expansion.
- `gen_dash.py` — `state.json` → `dash.html` (the "what's happening" dashboard).
- `gen_projects_dash.py` — the D: ledger → `projects/index.html` + per-project pages +
  every `.md` rendered as a browsable page (839 pages total).
- `butler.py` — end-of-day automation: state snapshot, activity scan, day brief
  (`archive/YYYY-MM-DD_brief.md` + `LATEST_BRIEF.md`), regenerates all surfaces.
  `CLOSE-DAY.bat` runs it and opens the dashboard.

### The plates (function decks on the frame)
- **Coders** — Freebuff / Goose / Aionui / Cochat / Codex cubes; status + last-chat
  toggles; assign-task queues; real `.md` inbox per agent; claim deletes the file.
- **Writer (STFU+WRITE Phases 2 + 4)** — WRITE surface bound to `drafts/*.md`;
  PROJECT manager; SOURCE / VOICE / OUTPUT stubs; EDIT·CRITIQUE critique loop; five
  modes (FLOW / FREEWRITE / EDIT / REFERENCE / OUTPUT, Ctrl+1–5); Ctrl+S commit,
  Ctrl+E export; non-destructive verified.
- **Link cubes** — the recipe proof: `feeds/links.md` bullets become app-type cubes
  that open / copy URLs. Any future kind is a feed + a renderer, never a frame change.

### Mini Me — the Android web app (Phase 2 seed)
`?mini` (or ≤ 820px viewport) boots the Coders plate and reflows it into a
thumb-reachable column. Touch: 550 ms long-press menu, drag, 28 px corner resize,
canvas scroll. PWA assets (manifest / service worker / icons) make it installable and
offline-first. `?bridge=<LAN ip>:8765` docks the phone to the Mothership bridge.
`ANDROID_BUILD.md` documents the Capacitor wrap → APK.

---

## 5. The canon — the docs that drive everything

| Doc | What it is |
|---|---|
| [`PRD.md`](PRD.md) | The canonical product spec: vision, data model, Phase 1–3 roadmap |
| [`MASTER_SYNTHESIS.md`](MASTER_SYNTHESIS.md) | Vision narrative: blank canvas, masters/wannabes, marketplace |
| [`JOURNEY.md`](JOURNEY.md) | History + validated build path (Prototype Zero → Writer → replicate) |
| [`WHITE_PAPER.md`](WHITE_PAPER.md) | The Machine Sections pattern + "Reference ≠ Representation" + A2A protocol |
| [`STFU_WRITE.md`](STFU_WRITE.md) | The first vertical: quiet surface, six cubes, five modes, Phases 2–5 |
| [`MACHINE_SECTIONS.md`](MACHINE_SECTIONS.md) | The six sections mapped onto the **running code** (function by function) |
| [`STATE.md`](STATE.md) | State of the frame: canon → build → gap sheet → verified receipts → next |
| [`CANON_RECONCILIATION.md`](CANON_RECONCILIATION.md) | Provenance chain of all source docs + the reconciliation verdict |
| [`ANDROID_BUILD.md`](ANDROID_BUILD.md) | Capacitor wrap steps for the Mini Me → APK build |

**Source documents** (absorbed originals + text extractions) in [`sources/`](sources/):
the A2A Handoff Artifact (Oct 2025 — the origin of Machine Sections and the
data-flow diagram), the Scaffolding Spec (a second vertical: file-ops plate, Phase 4),
PRD v1.0 (the consolidating PRD that deprecated the rest), plus the Ecosystem
Governance Charter and Strategic Framework.

---

## 6. The diagrams

| Figure | File | Shows |
|---|---|---|
| System map | [`diagrams/system-map.svg`](diagrams/system-map.svg) | Everything: inputs → builders → surfaces → bridge → gaps |
| Machine sections flow | [`diagrams/machine-sections-flow.png`](diagrams/machine-sections-flow.png) | Canonical cube-drag data flow (figure 1) |
| Brief dispatch flow | [`diagrams/brief-dispatch-flow.svg`](diagrams/brief-dispatch-flow.svg) (+ `.png`) | The one guarded write the philosophy permits (figure 2) |

The **live tracer** at the bottom of the deck renders figure 1's stations inline and
lights them in real time as you use the deck (drag → USER/UI/STATE, save → PERSIST,
commit → SHARE, brief → AGENT).

---

## 7. Status — honest, verified, and not-yet

**Verified live (proven end-to-end, receipts in `STATE.md` §4):**
Coders brief loop · the Commit gate (drag never writes; commit does) · Writer
non-destructive drafts + export · the Phase 4 critique loop (draft → brief → agent →
`critiques/` → note cube) · 6 kinds through one frame · the live tracer · Mini Me
touch interactions · IJFW audits return real findings.

**Stubbed by design (hidden-until-summoned, per the philosophy):**
Writer Phase 3/5 (engine primitives, STEM-Lite context), share tokens / QR / live
mirror, marketplace / P2P / wisdom DB, A2A pipeline stages in briefs, AI adapters.

**Also in this workspace (other threads, not KISS):**
`PRD_now/` (IDFKAI web PRD package), the AI-server migration to D: Docker
(`AI-SERVER-MIGRATION-RECEIPT-2026-08-18.md`, `C-DRIVE-AI-DOCKER-MIGRATION-PLAN…`,
`relocate-ai-docker.ps1`, `move-ai-rollback-to-d.ps1`), `dotmd/` (memory-loop,
litellm-stack, docs), `.ijfw/` + `dotmd/ijfw/` (IJFW memory/audit tooling).

**Next moves (ranked by the canon's own roadmap):**
1. Writer Phase 5 (STEM-Lite context folders) — 2. A2A protocol into briefs —
3. Android APK via Capacitor — 4. AI adapters (route critiques through a live model).

---

## 8. Glossary (for the newcomer)

| Term | Meaning |
|---|---|
| **Frame** | The kind-agnostic engine (grid, persistence, menus) — never changes per feature |
| **Cube** | A tile on the grid; its meaning is whatever you assign (`basic / ai / app / workflow`) |
| **Plate** | A function deck built on the frame (Coders, Writer, …) |
| **Kind** | A cube recipe: renderer + behaviors + interactions + type + feed |
| **Bridge** | The local server (8765) that is the *only* writer of files |
| **Brief** | A task dispatched to an agent as a `.md` file in its `inbox/` folder |
| **Binding vs representation** | Representation = deck state (safe to move); binding = files (changed only on explicit commit) |
| **Commit gate** | The rule + button: nothing touches disk until you say so |
| **Machine Sections** | The six isolated layers (UI / State / Persistence / Sharing / Agent / Community) |
| **Mothership / Mini Me** | Desktop = Mothership; the phone web app = Mini Me, docking via `?bridge=` |
| **Butler** | The end-of-day automation that archives, briefs, and regenerates everything |
| **Canon** | The doc set in §5 — the source of truth for what this project *is* |

---

*End of handoff. If an agent is reading this: read `STATE.md` next, then `AGENTS.md`
at the workspace root, then check your inbox folder — `.state/kiss/inbox/<you>/`.*
