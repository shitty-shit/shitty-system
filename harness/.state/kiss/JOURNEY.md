# KISS Dashboard — The Journey

> The evolution: 1980s Navy sonar → digital cubes → a disciplined, AI-orchestrated
> commercial software pipeline. Canonical narrative alongside `PRD.md` and
> `MASTER_SYNTHESIS.md`.

## 1. The Tactical Origin: 1980s Navy Sonar

The foundational architecture is rooted in the physical design of Navy sonar control
panels on Los Angeles–class submarines (1980s).

- **The Sonarman's Panel:** maximum clarity, rapid operator response, zero clutter.
  Large tactile pads with translucent film "faceplates", backlit.
- **Remapping Without Rewiring:** one control button could instantly remap the meaning
  of every other pad on the panel — infinite reconfigurability, no nested menus.
- **The "KISS" Philosophy:** *Keep It Simple, Stupid* — only the exact controls for the
  current scenario; adapt as context shifts.

## 2. The Digital Translation: Cubes & "Machine Sections"

- **Under-Designed Blank Canvases:** white, text-only cubes on a flexible grid; no icons,
  heavy borders, or decorative graphics. Cubes are generic fluid entry points — portals
  to apps, AI agents, data sources, custom scripts — defined by the user or community.
- **Desktop "Mothership" & Mobile "Mini Me":** a rich browser dashboard docks and syncs
  with an offline-first companion mobile app.
- **The "Machine Sections" Metaphor** (modeled on a photographic studio — see
  `MACHINE_SECTIONS.md` for the mapping onto the working prototype):
  - **UI Layer** — grid + drag-and-drop (lighting/composition)
  - **State Manager** — local stores: cube positions, labels, sizes (shot list)
  - **Persistence Layer** — real-time, debounced cloud sync (negative storage)
  - **Sharing Layer** — share tokens for read-only layout mirroring (contact sheets)
  - **Agent Layer (future)** — dynamic AI sub-cubes, model configs (retoucher assistant)
  - **Community Layer (future)** — P2P marketplace for faceplates/layouts (agency network)

## 3. The Strategic Build Path: Disciplined Focus

*"Don't build the city before the first house works."*

1. **Prototype Zero (KISS-PM):** a spatial project-tracking canvas to test drag-and-drop,
   resizing, snapping, and local state persistence — no heavy backend.
   *(This is exactly what `.state/kiss/index.html` is: the frame, proven.)*
2. **The Commercial Proving Ground (STFU+WRITE / KISS Writer):** the first vertical.
   "Loud name. Quiet software." Default interface fully silent; formatting, research
   cubes, and AI models only appear when summoned.
3. **Ecosystem Replication:** once cubes, decks, remapping, and state persistence are
   proven by Writer, replicate to KISS Photo, KISS Code, KISS Video.

## 4. The Creator Ecosystem: "Camera-Bag Psychology"

- Rejects crowded app-store models in favor of human connection. A beginner wants to
  know: *what does a working professional in my field actually use?*
- **Packaged Judgment:** a shared deck = years of selection and trial-and-error packaged
  into one loadable environment.
- **Creator/User Flywheel:** users and creators are one and the same — the community
  builds the long-tail inventory, templates, and dialects; the core team isn't the
  content factory.

## 5. Technical Stabilization & Modern Governance (2025–2026)

- **The Standardized Stack:** Next.js (App Router) + React + TypeScript; Tailwind CSS;
  Zustand; Firebase (Auth/Firestore/Storage) with local emulators.
- **Agent-to-Agent (A2A) Handoff:** Creative/Engineering Orchestrator (ChatGPT) ↔
  Technical Workflow Validator (DeepSeek). Inspectable loop:
  **Plan → Scaffold → Review → Commit → Test**.
- **The "Bug-Out" Repository:** local-first, portable, structured around an Obsidian
  Map of Content + Git — the whole spec, PRD, and codebase survives platform breakages
  and account lockouts. *(This workspace — root dump + `dotmd/` git repo + `.state/` —
  is the living version of that principle.)*

**Throughline:** a quiet, simple surface housing deep, serious capability.
