# KISS — The State of the Frame

Consolidated index of everything: canon → build → status. Written 2026-08-17
after Kevin handed over the **complete** canon set. Read this first, then anything
it points to.

## 1. The canon (all held in `.state/kiss/`)

| Doc | Core commitments | Implementation status |
|---|---|---|
| `PRD.md` | Product vision, data model (`Cube` / `AICube` / `Layout` / `User`), Phase 1–3 roadmap | v 1–3 implemented as Prototype Zero; data model matches `serialize()` |
| `MASTER_SYNTHESIS.md` | Vision narrative: blank canvas, masters/wannabes, marketplace | vision only (Phase 3) |
| `JOURNEY.md` | History + validated build path: Prototype Zero → Writer vertical → ecosystem replication | Prototype Zero = this frame; Writer = built (Phase 2) |
| `WHITE_PAPER.md` | Six Machine Sections, Reference ≠ Representation (+Commit gate), A2A five-step protocol, KISS on the stack | Sections mapped + Commit gate built; A2A stages not yet in inbox |
| `STFU_WRITE.md` | First vertical: quiet surface, non-destructive, six cubes, five modes, Phases 2–5 | Phases 2 & 4 built & verified; 3/5 stubbed |
| `diagrams/machine-sections-flow.png` | Canonical cube-drag data flow (product stack) | annotated against real code in `MACHINE_SECTIONS.md`; also the original is §6 of the A2A artifact in `sources/a2a_artifact.txt` |
| `diagrams/brief-dispatch-flow.svg` (+ `.png`) | Figure 2 — canonical brief-dispatch flow (queue → ➤ → bridge write → inbox → claim) | same six-station grammar; annotated against real code in `MACHINE_SECTIONS.md` |
| `HANDOFF.md` + `slides.html` + `diagrams/system-map.svg` (+ `.png`) | **The handoff kit** (2026-08-19): executive cheat sheet with links to every file/command/dashboard; a 12-slide zero-dependency newcomer deck (keyboard nav); the one-picture system map (inputs → builders → surfaces → bridge → gaps) | every box in the map is a real file; the map is embedded as slide 3 of the deck |

**Resolved 2026-08-17:** all three diagram-cited sources were found locally and absorbed
into `sources/` (text-extracted via pdftotext) — see `CANON_RECONCILIATION.md` for the
full provenance chain (A2A artifact 2025-10 → scaffolding spec → PRD v1.0 2026-06
[deprecates all prior] → our PRD.md → prototype), the v1.0 depth-deltas, and the
Phase-4 scaffolding verdict. Bonus canon also in `sources/`: Ecosystem Governance
Charter, Strategic Framework. The real project home lives in the git repo
`kiss docs/` (WHAT_WE_HAVE.md base inventory) + D: ledger `kiss_dashboard/`.

## 2. What exists (the build)

- **The frame** — `kiss.html` (single-file, zero-dependency): kinds, grid + snapping
  (1x1/2x1/2x2), drag/resize/collapse/stack, dbl-click rename, right-click / touch-hold
  "make this cube a…", type borders (basic/ai/app/workflow), ⚡ behavior chips, minimal +
  dark themes, layout history (12), autosave, Export/Import-level Commit gate.
- **The bridge** — `bridge.py` (127.0.0.1:8765): inbox briefs (`.md`), deck commits,
  drafts + export. The local-first stand-in for Firestore, and the Agent Layer binding.
- **`gen_kiss.py`** — injects ledger (110 projects), agents, feeds into the deck;
  `{{ROOT}}` expansion; the butler EOD pass regenerates deck + board + dashboard.
- **Plates (function decks):**
  - **Coders** — Freebuff / Goose / Aionui / Cochat / Codex; status + last-chat toggles;
    assign-task queues; real `.md` inbox per agent.
  - **Writer (STFU+WRITE Phase 2 + 4)** — WRITE surface bound to `drafts/*.md`;
    PROJECT; SOURCE/VOICE/OUTPUT stubs; EDIT·CRITIQUE ships a draft to an agent
    inbox as a critique brief (summarize/structure/keyphrases) and lands the return
    as a note cube; FLOW/FREEWRITE/EDIT/REFERENCE/OUTPUT modes; Ctrl+S commit,
    Ctrl+E export (.md + .txt); non-destructive verified.
  - **Focus/Full** — master next-steps list, project cubes, link cubes from feeds.
- **Feeds / kinds recipe** — `feeds/README.md` (5-step recipe; `links` proven).
- **Docs:** PRD, MASTER_SYNTHESIS, JOURNEY, WHITE_PAPER, STFU_WRITE, MACHINE_SECTIONS.
- **Handoff kit:** `HANDOFF.md` (cheat sheet: 60-second story, run commands, file inventory, bridge API, canon, diagrams, status, glossary — every entry links to its file), `slides.html` (12-slide explainer deck, zero deps, ←/→ nav), `diagrams/system-map.svg` (+ PNG) (one-picture map of the whole system).

## 3. Honest gap-sheet (everything NOT built — every one of these is roadmapped)

| Gap | Value depth | Why delayed |
|---|---|---|
| Firestore/Zustand/Next.js stack swap | — | prototype is a frame; `serialize()` already emits the product `Cube[]` shape, so it's a serialization swap |
| Share tokens / QR / live mirror | Sharing § | nothing yet; deck files are the portable binding |
| Mobile "Mini Me" / Android native build | — | web app built (PWA + touch + reflow); Capacitor wrap + dock sync remain |
| Marketplace / P2P / community / wisdom DB | — | Phase 3; not before the first house works |
| A2A pipeline (Plan → Scaffold → Review → Commit → Test) | — | protocol not yet modeled into briefs |
| Writer Phase 3 (engine primitives) | — | the writer already lives ON the frame — 1.2 done implicitly |
| Writer Phase 5 (STEM-Lite) | — | stubbed; Phase 4 critique loop built |
| IJFW auth gaps (gemini login; claude key; 18 MCP servers) | — | needs user |
| Scheduled butler task (23:45) | — | needs approval |

## 4. The verified receipts (each claim was proven end-to-end in the preview)

- IJFW Trident audits return real findings (Windows spawn + codex override patched).
- Coders: brief → `inbox/<agent>/*.md` → deck shows `inbox: N briefs` → claim deletes file.
- Bridge: draw a bound **only on explicit commits** — the Commit gate restores committed
  positions over moved ones.
- Writer: typing creates **no file**; Ctrl+S writes `drafts/*.md`; Ctrl+E writes
  `.md` + `.txt`; PROJECT lists and reloads.
- **Writer Phase 4 critique loop:** draft → EDIT·CRITIQUE → send → bridge writes
  `inbox/<agent>/*-critique-*.md` (requested tasks + full draft + return path) →
  agent writes `critiques/<slug>.md` and deletes the brief → deck refresh shows the
  return → ▸ lands it as a note cube.
- Frame: 6 kinds (project/step/list/agent/note/link/write/drafts/stack) all pass
  through the same drag/stack/history/persistence path.
- **Live machine-sections tracer:** bottom panel renders an inline SVG of the
  actual diagram — USER → UI → STATE → PERSIST with SHARE (commit deck) and
  AGENT (brief) branching below — and lights each station in real time:
  drag start (user/ui), snap/move (state), debounced save (persist), deck
  commit (share), brief send/claim (agent). Stations light with the same
  color-coding as the two canonical figures. (The data-flow diagram now runs
  itself inside the frame.)
- **Mini Me (Android web app):** touch drag / long-press menu / corner resize all
  verified with synthetic touch pointer events; `?mini` (or ≤820px viewport) boots
  the Coders plate and reflows it into a single full-width, thumb-reachable column;
  canvas scrolls (`touch-action:none` on the header), larger touch targets,
  `?bridge=<LAN ip>:8765` override for the Mothership, and PWA assets
  (manifest.json + sw.js + icon.svg/.png) with offline-first caching — see
  ANDROID_BUILD.md for the Capacitor wrap.

## 5. Next moves, ranked by the docs' own roadmap

1. **Writer Phase 5 (STEM-Lite)** — portable markdown context folders (style, outline,
   characters, terminology) feeding critique briefs on demand.
2. **A2A protocol into briefs** (Plan → Scaffold → Review → Commit → Test stage tracking).
3. **Android native build** — wrap the Mini Me web app via Capacitor (steps in
   ANDROID_BUILD.md), then the dock/sync handshake to the Mothership.
4. **AI adapters** — route critique through a live model (cloud/local) instead of a
   human-agent round-trip; gemini/claude auth; scheduled butler task.