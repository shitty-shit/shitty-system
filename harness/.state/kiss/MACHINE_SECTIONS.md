# KISS Machine Sections — mapped onto the working prototype

The "Machine Sections" discipline (studio metaphor: lighting, shot list, negative
storage, contact sheets, retoucher, agency) applied to the **real running code** in
`.state/kiss/`. Status column = what the prototype actually has today.

| Section | Studio metaphor | In the prototype (file → function) | Status |
|---|---|---|---|
| **UI Layer** | lighting / composition | `kiss.html`: `cubeEl()`, `attachCube()`, `startDrag()`, `spawnSpriteDrag()`, `ctxMenu()`, `editLabel()`, grid consts (`CELL/GAP/PAD`), `snapX/Y/W/H`, presets, `render()` | ✅ built |
| **State Manager** | shot list | `deck` object (`cubes/order/z/seq/preset`) + `makeCube()`, `serialize()`/`pick()`, `render()` | ✅ built (plain module state; PRD target: Zustand) |
| **Persistence Layer** | negative storage | `localStorage` `kiss.deck.v1` + history `kiss.deck.history` (last 12) + theme; file side: `gen_kiss.py` → `index.html`, butler EOD regen | ✅ built (local-first; PRD target: Firestore) |
| **Sharing Layer** | contact sheets | **seeded** — Commit gate writes layouts to `.state/kiss/decks/<name>.json` via the bridge (portable, loadable); share tokens/QR still future | 🟡 deck files; tokens future |
| **Agent Layer** | retoucher assistant | agent cubes now carry `AICube` fields (provider/model — white paper §3) + `bridge.py` inbox repo (`.md` briefs) + `AGENTS.md` protocol + `state.json` sessions | 🟡 working MVP |
| **Community Layer** | agency network | none — docs only (`PRD.md` §4, `MASTER_SYNTHESIS.md` §3) | 🔲 future (marketplace, faceplates) |

## A cube-drag, walked through all sections that exist

```
 USER drags a cube
     │
     ▼
UI Layer ─── pointerdown on .cube-head → attachCube() → startDrag()
     │      pointermove > 4px → snapX/Y() → c.x/c.y/z mutated
     ▼
State Layer   deck.cubes[id] updated (single source of truth)
     │
     ├──► UI Layer re-renders from state (render() rebuilds cubes; render is a pure
     │        function of deck — this is the loop that keeps drag, stack, rename,
     │        theme and history all consistent)
     │
     ├──► pointerup → handleDrop() → stack/join-list/dock (state mutation only)
     │
     ▼
Persistence Layer  saveSoon() → 400ms debounce → save()
     → localStorage kiss.deck.v1   (layout survives reload)
     → pushHistory()               (version history, restorable from toolbar)
     │
     ▼
Agent Layer (only when the drop is a task ➤ brief)
     bridge.py POST /brief → writes .md file in inbox/<agent>/ → deck shows
     "inbox: N briefs" → claim (DELETE) removes it
```

**The rule that makes the sections work:** *UI never mutates state directly — it always
goes through the `deck` object, and rendering is always a pure function of `deck`.*
That single discipline is what lets the frame accept new kinds (per `feeds/README.md`)
without touching the sections.

**The Commit gate (white paper §6 manifesto):** dragging, stacking, renaming only move
the *representation* (deck state + localStorage). The *bindings* — ledger .md files,
inbox briefs, deck files — change only on explicit actions: the ➤ brief send, or the
Commit ▾ button (writes `serialize()` out to `.state/kiss/decks/<name>.json` via the
bridge, atomic write, reloadable from the same menu). Verified: move a cube → load a
committed deck → position restores from the commit, not from the working state.

## Prototype-now vs product-later

- The prototype's Persistence+Sharing is *one localStorage key*; the product gets
  Firestore + share tokens. The port is honest: `serialize()` already emits the
  `Cube[]` shape the PRD data model spells out (`id/position/dimensions/label/type/
  config`), so the Zustand/Firestore migration is a serialization swap, not a redesign.
- The prototype's Agent Layer (`.md` inbox) is *stronger on purpose* for this user's
  world: every agent in this workspace (Freebuff, codex, goose, …) already reads
  markdown files. Cloud sync can come later; local-first is the bug-out doctrine.

See also: `PRD.md` (§5 architecture, §5.1 stack), `feeds/README.md` (kind recipe).

## Canonical data-flow diagram

`diagrams/machine-sections-flow.png` — KISS DASHBOARD: "MACHINE SECTIONS" SYSTEM
DATA FLOW (visual tracking of data propagation during a cube-drag across the
decoupled stations).

The diagram shows the **product** stack (React DnD Kit / Zustand / Firestore /
share tokens). Every station already exists in the prototype with different
bindings — files instead of cloud:

| Diagram step | Product stack | Prototype implementation (this frame) |
|---|---|---|
| User drags cube | operator gesture | `pointerdown` → `attachCube()` → `startDrag()` |
| Drag event | React DnD Kit CUBEGRID/CUBE.TSX — capture drag-end, compute coords, snap, collision | `pointermove` → `snapX/Y()` + overlap checks; `pointerup` → `handleDrop()` (stack / join-list / dock) |
| Dispatch store update | dispatch store update | direct mutation of the `deck` object + `render()` (pure function of state — same zero-lag guarantee) |
| **State Manager** | Zustand `useCubeStore.ts` (instant local update, re-render <100ms, 1s debounced sync) | `deck.cubes[id]` mutation + `render()`; **400 ms debounced** `save()` → localStorage + `pushHistory()` (the 1s flush, tuned) |
| **Persistence** | Firestore `layouts/{layoutId}` (commit write, offline store, reconnect sync) | `localStorage` `kiss.deck.v1` + `kiss.deck.history`; deck files via Commit ▾ → `bridge.py /deck` (atomic write, loadable); offline is the default, not a fallback |
| **Sharing** | share token / read-only live mirror (<30s cross-device) | seeded: deck `.json` files are portable; live mirror = loading the same file (token/QR mirror still future) |
| Agent / Community | — | agent cubes + inbox `.md` briefs (working); marketplace (future) |

The footer philosophy — *move representations first, commit only when requested* —
is enforced by the Commit gate: drags mutate representation only; the `➤` inbox
brief and `Commit ▾` deck file are the only binding writes.

Sources cited on the diagram: `kiss_dashboard_scaffolding_spec.pdf`,
`A2A_HANDOFF_ARTIFACT.pdf`, `KISS_DASHBOARD_PRD_WORKING.md` — resolved 2026-08-17:
all three found locally and absorbed into `sources/` (see `CANON_RECONCILIATION.md`).

## Canonical brief-dispatch flow (figure 2)

`diagrams/brief-dispatch-flow.svg` (+ rendered `.png`) — KISS DASHBOARD: "BRIEF
DISPATCH" SYSTEM DATA FLOW (the assign-task → .md inbox → claim cycle). Same
six-station grammar as figure 1, with the bridge as the Agent Layer's binding.

| Diagram step | Real implementation (this frame) |
|---|---|
| User types task, hits Enter | agent cube input → `keydown` → queue item, `queued · not sent` badge — **representation only, no file** |
| ➤ send pressed | `sendBrief(id)` → `POST /api/brief {agent, task}` to `bridge.py` (127.0.0.1:8765) |
| queue item `sent=true` | `deck` mutation → `render()` → `in inbox` badge + `loadBriefs()` poll |
| debounced save | `saveSoon()` → 400 ms → `localStorage` `kiss.deck.v1` + `pushHistory()` — still the *representation* |
| bridge write | `POST /brief` handler: sanitize agent + task → atomic write `inbox/<agent>/<ts>-<slug>.md` → `{ok, path}` — **the only disk touch in the whole flow** |
| agent workflow | agent reads its folder (`AGENTS.md` protocol) → works the brief → claim → `DELETE /brief` → bridge deletes file → deck `loadBriefs()` clears the count |

The rule made explicit on the figure: *the .md file is the binding; the deck's
localStorage state is the representation — typing and queueing never touch disk;
only the explicit ➤ send writes a brief file.* Same Commit-gate discipline as
figure 1 (cube drag), now proven at the agent-dispatch grain.

Figure 1 = representation movement (drag). Figure 2 = the one deliberate,
guarded write the philosophy permits (dispatch). Together they are the full
machine flow: move freely, commit exactly when you mean it.
