# Architectural White Paper — The Machine Sections Pattern

> Scalable, modular web development derived from 1980s Navy sonar hardware.
> Fourth canon document alongside `PRD.md`, `MASTER_SYNTHESIS.md`, `JOURNEY.md`.

## 1. Genesis: from tactical hardware to software architecture

Sonar panels on Los Angeles–class submarines: large tactile pads under remappable film
faceplates, remapped *in an instant* without rewiring. The four tenets:

- **Clarity Over Clutter** — only the tools required for the current vertical slice.
- **Tactical Remapping** — instant reconfiguration without mutating the architecture.
- **User-Defined Meaning** — under-defined primitives; the user establishes meaning.
- **Modular Isolation** — zero-dependency boundaries; no monolithic decay.

## 2. The Photo Studio Workflow metaphor

| Section | Technical purpose | Studio analogy |
|---|---|---|
| UI Layer | three-panel grid + interaction | lighting / composition |
| State Manager | live positions, sizes, labels | shot list clipboard |
| Persistence | cloud sync + history | negative storage / archive |
| Sharing | tokens + faceplates | contact sheets / proofs |
| Agent | AI orchestration + API hooks | retoucher / studio assistant |
| Community | marketplace + P2P | agency / gallery network |

### The Three-Panel Interface (future plates: content, image pipeline, etc.)

1. **Sources (left):** metadata previews of raw materials — original data untouched.
2. **Operations (middle):** staging where templates reorganize/classify content.
3. **Output / Preview (right):** visual diff of the target structure before execution.

The Lightroom model of non-destructive state management:
**Reference ≠ Representation** — moving a cube changes only the representation; the
binding (underlying system connection) mutates only on an explicit **Commit** command.

### The Blank-Canvas Principle

Cubes are intentionally under-defined flexible handles; the community builds
specialized "decks of judgment."

## 3. Technical stack — BaaS blueprint

- **Frontend:** Next.js 14+ App Router, React 18, TypeScript strict; Tailwind;
  Zustand stores for cube positions/layout.
- **BaaS:** Firebase (Firestore/Auth/Storage) + **Emulator Suite** for local-first,
  portable, offline-first development (strict local-first Git/emulator discipline).
- **Data model** (canonical contracts):

```ts
interface Cube {
  id: string; position: { x: number, y: number };
  dimensions: { width: number, height: number };
  label: string;
  type: 'basic' | 'ai' | 'app' | 'workflow';
  config: Record<string, any>;
  createdAt: Date; updatedAt: Date;
}
interface AICube extends Cube {
  type: 'ai';
  provider: 'openai' | 'anthropic' | 'google' | 'custom';
  config: { model: string; temperature: number; systemPrompt: string };
  subCubes: Cube[];          // dynamic model-selection sub-grid
}
interface Layout { id: string; userId: string; name: string;
  cubes: (Cube|AICube)[]; isPublic: boolean; shareToken?: string;
  createdAt: Date; updatedAt: Date; }
interface User { id: string; email: string;
  preferences: { gridSize: number; defaultLayout: string; theme: 'minimal'|'dark' }; }
```

- **Performance KPIs:** LCP < 2.5 s, interaction latency < 100 ms, virtualized grid
  rendering for large decks, debounced 1-second writes.

## 4. A2A handoff — orchestrating AI workflows

DeepSeek = **Architectural Validator** (advisory lead; validates module boundaries,
prevents monolithic creep). ChatGPT = **Engineering Orchestration** (primary engineer).

Five-step linear protocol: **Plan** → **Scaffold** → **Review** → **Commit** →
**Test/Run** (local emulators + preview envs). Every module independently testable;
each station debuggable station-by-station.

## 5. Value ecosystem — community, monetization, marketplace

Phases: **(1) The App** — core grid + STFU+WRITE vertical → **(2) Sharing & AI** —
share tokens, mobile sync, AI parent nodes → **(3) The Marketplace** — P2P faceplates
and monetization. Camera-bag psychology → "packaged judgment" → installed audiences;
affiliate links, premium decks, blockchain P2P.

## 6. Strategic guardrails

- **Minimalism as a strategy** — capability may be complex; the persistent interface
  stays light. Brand guardrail: *capability hidden until explicitly summoned.*
- Risk mitigations: monolithic creep → machine-sections file structure + modular
  stores; vendor lock-in → local-first emulator + portable data models; opaque AI →
  validator + human gates; performance drag → virtualized grid + debounced writes;
  feature bloat → hidden-until-summoned guardrails.
- **Technical manifesto (the core rule):**

> *Move representations first; commit changes to underlying systems only when
> explicitly requested.*

---

*Prototype mapping: `MACHINE_SECTIONS.md` stages this paper against the running
`.state/kiss/` code. The Commit gate (toolbar ▸ deck file, `bridge.py /deck`) is the
first implementation of the manifesto rule.*