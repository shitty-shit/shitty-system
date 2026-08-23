# KISS Dashboard — Product Requirements Document (PRD)

**Document Version:** 1.0  
**Status:** DRAFT — Ready for Review  
**Date:** 2026-06-13  
**Author:** Kevin Kane  
**Classification:** Internal / Development Team

---

## 1. Document Control

### 1.1 Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2025-10-20 | Kevin Kane | Initial concept, A2A handoff artifact |
| 0.2 | 2025-10 | Kevin Kane | Scaffolding spec, social ecosystem doc |
| 0.3 | 2025-12 | Kevin Kane | Consolidated spec, project narrative |
| 1.0 | 2026-06-13 | Kevin Kane | Unified PRD — synthesizing all docs into single SDD-facing spec |

### 1.2 Source Documents (Consolidated Into This PRD)

The following documents are **deprecated** by this PRD. All requirements, decisions, and specifications previously contained in them are now consolidated here:

1. `kiss-dashboard-spec.md` — Original consolidated specification
2. `KISS Dashboard – Complete Project Narrative and Specification.docx` — Project origin story and platform structure
3. `KISS Dashboard Social Ecosystem & Sharing Site.docx` — Community, monetization, marketplace
4. `kiss_dashboard_scaffolding_spec.pdf` — Project scaffolding & file management (Phase 4 feature)
5. `🧩 A2A HANDOFF ARTIFACT.pdf` — AI-to-AI collaboration workflow and technical brief
6. `kiss_dashboard_v1.html` — Early prototype (reference only)

### 1.3 Review & Approval

| Role | Name | Status | Date |
|------|------|--------|------|
| Product Owner | Kevin Kane | Draft | 2026-06-13 |
| Technical Lead | TBD | Pending | |
| QA Lead | TBD | Pending | |

---

## 2. Executive Summary

### 2.1 The Product

KISS Dashboard is a **minimalist, modular workspace** built around a grid of text-only "cubes." Users arrange, resize, and label these cubes to create personalized control panels for their tools, AI agents, workflows, and projects. It is a canvas — the platform provides the structure, but the meaning comes from the user.

### 2.2 The Origin Story

This product draws from real-world experience: Navy sonar control panels on a Los Angeles-class submarine in the 1980s. Each sonar button was a large, backlit pad with a translucent film faceplate. Push one button, and the entire faceplate would remap — changing the meaning and function of every button simultaneously. This enabled infinite reconfiguration with zero clutter. KISS Dashboard translates that physical metaphor into a digital workspace.

### 2.3 Guiding Philosophy

> **"The dashboard, like great art, is a timeless canvas — users and community members give meaning to each block, ascribing their own roles, workflows, and creative logic to the interface."**

**Core tenets:**
- **Blank canvases, not prefilled widgets.** White blocks. Bold text. Zero preset iconography. The platform provides the grid; the user provides the meaning.
- **Never enforce rigid design.** Every cube is modifiable, replaceable, and remixable.
- **Station-by-station debugging.** The "Machine Sections" architecture ensures each layer (UI, state, persistence, sharing) is independently inspectable and replaceable.
- **Simplicity first.** If a feature requires onboarding documentation, question its necessity.
- **Composable future.** Every layer, every feature, every integration slot is designed to evolve independently.

### 2.4 Scope of This PRD

This document covers **Phase 1 (MVP)** in full detail. Phases 2-4 are defined at a high level for architectural planning purposes but are **explicitly out of scope** for the current development cycle.

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | Core dashboard — grid, cubes, drag-and-drop, persistence, auth, PWA | **IN SCOPE — This PRD** |
| Phase 2 | Sharing, mobile companion, AI cube integration | Out of scope |
| Phase 3 | Community marketplace, monetization, NFT/blockchain | Out of scope |
| Phase 4 | Project scaffolding, file management, real-time collaboration | Out of scope |

---

## 3. Personas & Use Cases

### 3.1 Primary Personas

#### Persona A: "Power User Kevin" (You)
- **Profile:** Creator with 23+ active projects. Needs a single surface to access AI tools, project files, workflows, and media tools without clicking through nested menus.
- **Needs:** Instant access. Custom layouts per project type. Cross-device sync. Offline note-taking on phone.
- **Pain point:** Current workflow requires too many context switches between apps, tabs, and folders.

#### Persona B: "New Creator"
- **Profile:** Just starting out. Overwhelmed by tool choice. Needs a gentle on-ramp that doesn't lock them into someone else's system.
- **Needs:** Guided defaults (e.g., "AI" cube that populates with Claude, ChatGPT, Gemini). Ability to modify everything. No decision fatigue.
- **Pain point:** Most tools impose their structure; this user needs a blank slate that doesn't feel empty.

#### Persona C: "Pro Curator"
- **Profile:** Expert in a domain (video editing, coding, photography) who wants to package their setup for others.
- **Needs:** Save faceplates. Share configurations. Eventually monetize curated stacks.
- **Pain point:** No clean way to package and distribute their workflow configurations.

### 3.2 Use Cases (Phase 1)

| ID | Actor | Action | Expected Result | Priority |
|----|-------|--------|-----------------|----------|
| UC-01 | Any user | Open dashboard for first time | See default grid with "AI" cube and guided onboarding | Must |
| UC-02 | Any user | Drag a cube to new position | Cube snaps to grid, position persists after refresh | Must |
| UC-03 | Any user | Double-click a cube label | Enter edit mode, type new label, press Enter to save | Must |
| UC-04 | Any user | Right-click a cube | Context menu: Edit, Resize, Duplicate, Delete | Must |
| UC-05 | Any user | Click empty grid area | Option to add new cube at that position | Must |
| UC-06 | Any user | Resize cube (1x1 → 1x2, 2x1, 2x2) | Cube expands, adjacent cubes reflow | Must |
| UC-07 | Any user | Click "AI" cube | Dashboard repopulates with AI model sub-cubes (Claude, ChatGPT, Gemini, Perplexity) | Must |
| UC-08 | Any user | Use dashboard offline | Changes queue locally, sync on reconnect | Must |
| UC-09 | New user | Complete onboarding | Understand drag/drop, editing, and layout saving | Must |
| UC-10 | Any user | Close and reopen browser | Layout restores exactly as last saved | Must |
| UC-11 | Any user | Log in from different device | Same layout loads (Firebase sync) | Should |
| UC-12 | Any user | Share layout via token | Another user can view (read-only) the layout | Should |

---

## 4. Functional Requirements

### 4.1 Core Dashboard ("Mothership")

#### REQ-01: Grid System
- **Description:** A responsive grid of configurable cube cells.
- **Acceptance Criteria:**
  - Grid is configurable in columns and rows (default: 6 columns × 4 rows)
  - Grid cells are visible as subtle background guides (not heavy borders)
  - Grid adapts responsively to viewport size
  - Minimum cell size: 120px × 120px
  - Grid background: light gray (#f5f5f5) or off-white (#fafafa)

#### REQ-02: Cube — Visual Design
- **Description:** Text-only white blocks on the grid.
- **Acceptance Criteria:**
  - Cube fill: pure white (#ffffff)
  - Cube text: black, bold, sans-serif, centered horizontally and vertically
  - No icons, no images, no borders (except on hover/focus)
  - On hover: subtle shadow (0 2px 8px rgba(0,0,0,0.08)), 1px border (#e0e0e0)
  - On focus/active: slightly darker border (#bdbdbd), stronger shadow
  - Text scales with cube size (min 12px, max 24px)
  - Text wraps if longer than cube width; truncates with ellipsis if still overflowing

#### REQ-03: Cube — Drag-and-Drop
- **Description:** Users can reposition any cube by dragging.
- **Acceptance Criteria:**
  - Drag initiated by click-and-hold (300ms threshold or movement threshold of 5px)
  - During drag: cube lifts with elevated shadow, slight scale (1.02)
  - Grid highlights valid drop zones as ghost outlines
  - On drop: cube snaps to nearest valid grid cell
  - If drop zone occupied: cubes push/swap (not overlap)
  - If drop invalid: cube returns to original position with smooth animation
  - Operation completes in < 100ms perceived latency

#### REQ-04: Cube — Resizing
- **Description:** Users can resize cubes to occupy 1×1, 1×2, 2×1, or 2×2 grid cells.
- **Acceptance Criteria:**
  - Resize handle visible on hover (bottom-right corner, 12px touch target)
  - Drag handle to expand/contract to allowed dimensions
  - Only allowed if target cells are empty or can be displaced
  - On resize: adjacent cubes reflow to accommodate
  - Minimum size: 1×1; Maximum size: 2×2 (Phase 1)

#### REQ-05: Cube — Text Editing
- **Description:** In-place editing of cube labels.
- **Acceptance Criteria:**
  - Double-click or "Edit" from context menu enters edit mode
  - Text field autofocused with current text selected
  - Save on Enter key or blur (click outside)
  - Cancel on Escape key
  - Max label length: 50 characters
  - Empty labels not allowed (revert to previous or show placeholder)

#### REQ-06: Cube — Context Menu
- **Description:** Right-click menu for cube actions.
- **Acceptance Criteria:**
  - Appears adjacent to clicked cube (not off-screen)
  - Options: Edit, Duplicate, Resize → (1×1, 1×2, 2×1, 2×2), Delete
  - Click outside menu dismisses it
  - Keyboard navigable (↑↓ to select, Enter to confirm, Esc to dismiss)

#### REQ-07: Cube — Add/Remove
- **Description:** Create new cubes and delete existing ones.
- **Acceptance Criteria:**
  - Add: Click empty grid cell → option to add cube; or toolbar "Add Cube" button
  - New cubes default label: "New Cube" (selected for immediate renaming)
  - Delete: Context menu "Delete" with confirmation toast (undo available for 5s)
  - Duplicate: Creates copy offset by 1 cell right (or next available cell)

#### REQ-08: Cube — Types (Phase 1)
- **Description:** Different cube types with minimal visual distinction.
- **Acceptance Criteria:**
  - Types: `basic` (default), `ai` (special "AI" parent cube), `folder` (container for sub-cubes)
  - Visual distinction is TEXT-ONLY — e.g., `ai` cubes have prefix label "🤖" (wait — **no icons**. Use subtle background tint: AI cubes get #f8f9fa tint, folder cubes get slightly different tint)
  - Actually, re-reading the spec: **NO icons, NO visual flourishes.** Use text-only cues. AI cubes have label "AI — " prefix. Folder cubes have label "📁"... no, no emojis.
  - **Decision:** Use subtle text prefix for type indication. "AI:" prefix for AI cubes. "/" suffix for folders. This is the only type indicator.

### 4.2 The "AI" Cube — Guided Defaults

#### REQ-09: AI Parent Cube
- **Description:** A special cube that, when clicked, repopulates the grid with AI model sub-cubes.
- **Acceptance Criteria:**
  - Appears as default cube in top-left on first launch
  - Label: "AI" (without prefix, as it's already understood)
  - On click: dashboard transitions to "AI mode" — grid repopulates with: "Claude", "ChatGPT", "Gemini", "Perplexity"
  - Each sub-cube is a regular cube that can be edited, moved, deleted
  - "Back" button or clicking a "← Dashboard" cube returns to main layout
  - AI mode is a separate saved layout (not destructive to main layout)

#### REQ-10: Sub-Cube Behavior
- **Description:** Sub-cubes spawned from AI parent behave like regular cubes.
- **Acceptance Criteria:**
  - Can be dragged, resized, edited, deleted independently
  - Persist in the AI layout
  - Can be promoted to main dashboard via drag to "Back" area
  - On click: for Phase 1, simply show a toast "Opens [Model Name]" (actual integration is Phase 2)

### 4.3 Persistence & Sync

#### REQ-11: Firebase Integration
- **Description:** All cube data persists to Firebase Firestore.
- **Acceptance Criteria:**
  - Firestore collection: `users/{userId}/layouts/{layoutId}`
  - Auto-save on every meaningful change (debounced 1 second)
  - Offline support: Firestore persistence enabled, sync on reconnect
  - Optimistic UI: local state updates immediately, Firestore syncs in background

#### REQ-12: Data Model

```typescript
// types/index.ts

interface Cube {
  id: string;           // UUID v4
  x: number;            // Grid column (0-indexed)
  y: number;            // Grid row (0-indexed)
  w: number;            // Width in cells (1 or 2)
  h: number;            // Height in cells (1 or 2)
  label: string;        // Display text (max 50 chars)
  type: 'basic' | 'ai' | 'folder';
  createdAt: Timestamp;
  updatedAt: Timestamp;
}

interface Layout {
  id: string;           // UUID v4
  name: string;         // e.g., "Main", "AI", "Video Editing"
  cubes: Cube[];
  isDefault: boolean;   // True for the main dashboard layout
  createdAt: Timestamp;
  updatedAt: Timestamp;
}

interface UserProfile {
  uid: string;
  email: string | null;
  displayName: string | null;
  preferences: {
    gridCols: number;     // Default: 6
    gridRows: number;     // Default: 4
    defaultLayoutId: string;
  };
  createdAt: Timestamp;
  updatedAt: Timestamp;
}
```

#### REQ-13: Authentication
- **Description:** Multiple auth methods supported via Firebase Auth.
- **Acceptance Criteria:**
  - Email/password (signup + login)
  - Google OAuth
  - GitHub OAuth
  - Anonymous auth (allow usage without account, prompt to create later)
  - Auth state persists across sessions
  - Logged-in state visible in UI (subtle, not prominent)

### 4.4 Progressive Web App (PWA)

#### REQ-14: PWA Requirements
- **Description:** Dashboard is installable as a PWA.
- **Acceptance Criteria:**
  - Web App Manifest with app name, icons, theme colors
  - Service Worker with basic offline caching
  - Works offline: grid displays, cubes editable, changes queued for sync
  - Responsive: functional on tablet and desktop browsers
  - Mobile browser: usable but not fully optimized (full mobile app is Phase 2)

### 4.5 Onboarding

#### REQ-15: First-Time User Experience
- **Description:** Guided walkthrough for new users.
- **Acceptance Criteria:**
  - On first visit (anonymous or new account): show onboarding overlay
  - Step 1: "This is your canvas" — highlight the grid
  - Step 2: "Drag to rearrange" — demo drag one cube
  - Step 3: "Double-click to rename" — demo edit
  - Step 4: "Right-click for more options" — show context menu
  - Step 5: "Click AI to explore AI tools" — highlight AI cube
  - Each step: user must perform the action to proceed (learn-by-doing)
  - "Skip" button available at all times
  - Onboarding state saved to localStorage (don't show again)

### 4.6 Performance Requirements

#### REQ-16: Core Web Vitals
| Metric | Target | Measurement |
|--------|--------|-------------|
| Largest Contentful Paint (LCP) | < 2.5s | PageSpeed Insights |
| First Input Delay (FID) | < 100ms | PageSpeed Insights |
| Cumulative Layout Shift (CLS) | < 0.1 | PageSpeed Insights |
| Time to Interactive (TTI) | < 3.5s | Lighthouse |

#### REQ-17: Runtime Performance
- **Description:** Dashboard must feel instantaneous.
- **Acceptance Criteria:**
  - Drag-and-drop: 60fps, no dropped frames
  - Cube edit save: < 50ms perceived latency
  - Layout restore from Firebase: < 500ms after auth
  - Grid renders 100+ cubes without virtualization (Phase 1 scope is < 50 cubes)
  - Debounced Firestore writes: 1000ms delay after last change

---

## 5. Non-Functional Requirements

### 5.1 Design & UX

- **Visual identity:** Extreme minimalism. The grid IS the interface. No chrome, no sidebars, no persistent toolbars (toolbar appears on interaction).
- **Color palette:** White (#ffffff) cubes, light gray (#f5f5f5) grid background, black (#000000) text, subtle grays for hover/focus states.
- **Typography:** System sans-serif stack (Inter or -apple-system, BlinkMacSystemFont, 'Segoe UI'). Bold weight for cube labels. Size scales with cube dimensions.
- **Animation:** Subtle, functional only. Snap-to-grid animation (150ms ease-out). Hover transitions (100ms). No decorative animations.
- **Accessibility:** WCAG 2.1 AA minimum. Keyboard navigation for all actions. Screen reader compatible (aria-labels on cubes). Focus indicators visible.

### 5.2 Security

- **Firebase Security Rules:**
  - Users can only read/write their own `users/{userId}` document and subcollections
  - Public read access only for layouts explicitly marked `isPublic: true` (Phase 2)
  - Input sanitization on all text fields (prevent XSS)
- **Authentication:** Secure token handling via Firebase SDK. No custom auth logic.
- **Data validation:** Client-side and server-side (Firestore rules) validation of all writes.

### 5.3 Scalability

- **Phase 1 target:** Support 1,000 active users, 10 layouts per user, 50 cubes per layout.
- **Firestore limits:** Designed to stay well within Firebase Spark/Blaze free tier for Phase 1.
- **Code architecture:** Module boundaries designed to support future backend migration (e.g., Supabase) without UI changes.

---

## 6. Architecture & Technical Design

### 6.1 Machine Sections Architecture

The codebase is organized into **six independent sections** — each can be developed, tested, debugged, and potentially replaced without touching the others.

```
┌─────────────────────────────────────────────────────┐
│                    UI LAYER                          │
│  Cube.tsx | CubeGrid.tsx | ContextMenu.tsx          │
│  Toolbar.tsx | Onboarding.tsx                        │
├─────────────────────────────────────────────────────┤
│                  STATE MANAGER                       │
│  cubeStore.ts | layoutStore.ts | userStore.ts       │
│  (Zustand — one store per concern)                   │
├─────────────────────────────────────────────────────┤
│                PERSISTENCE LAYER                     │
│  firebase.ts | sync.ts | offlineQueue.ts            │
│  (Firebase Auth + Firestore)                         │
├─────────────────────────────────────────────────────┤
│                 SHARING LAYER                        │
│  share.ts | tokens.ts                                │
│  (Phase 2 — stubbed interfaces in Phase 1)           │
├─────────────────────────────────────────────────────┤
│                  AGENT LAYER                         │
│  aiCube.ts | apiHooks.ts                             │
│  (Phase 2 — stubbed interfaces in Phase 1)           │
├─────────────────────────────────────────────────────┤
│                COMMUNITY LAYER                       │
│  marketplace.ts | nft.ts | affiliates.ts            │
│  (Phase 3+ — not implemented)                        │
└─────────────────────────────────────────────────────┘
```

### 6.2 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Framework | Next.js | 14+ (App Router) | React framework, SSR, API routes, PWA |
| Language | TypeScript | 5.x | Type safety, strict mode |
| Styling | Tailwind CSS | 3.4+ | Utility-first, minimal CSS footprint |
| UI Components | shadcn/ui | latest | Accessible primitives (dialog, tooltip, dropdown) |
| State | Zustand | 4.5+ | Lightweight state management |
| Drag & Drop | @dnd-kit/core | 7.x | Modern, accessible, performant DnD |
| Backend | Firebase | 10.x | Auth, Firestore, Storage |
| Icons | Lucide React | latest | Minimal — only for UI chrome (NOT cubes) |
| Testing | Vitest + Testing Library | latest | Unit/integration tests |
| E2E Testing | Playwright | latest | End-to-end tests |
| Linting | ESLint + Prettier | latest | Code quality |
| Deployment | Vercel | — | Hosting, preview deployments |

### 6.3 Data Flow

```
User Action (drag/rename/resize)
    │
    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  UI Layer    │────▶│  Zustand     │────▶│  Firebase    │
│  Components  │◀────│  Store       │◀────│  Firestore   │
└──────────────┘     └──────────────┘     └──────────────┘
                            │                      │
                            ▼                      ▼
                     Local state            Cloud persistence
                     (instant)              (debounced 1s)
                            │                      │
                            └──────────┬───────────┘
                                       ▼
                            ┌──────────────────┐
                            │  Optimistic UI   │
                            │  + Offline Queue │
                            └──────────────────┘
```

Every cube interaction triggers:
1. **Local update** → UI reflects change immediately (optimistic)
2. **Zustand store update** → State synchronized across components
3. **Firestore sync** → Debounced write (1000ms after last change)

On page load:
1. Auth state resolves (Firebase Auth)
2. Layout fetched from Firestore (or local cache if offline)
3. Grid renders with cubes in saved positions

### 6.4 Directory Structure

```
kiss-dashboard/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout (providers, metadata)
│   ├── page.tsx                 # Main dashboard page
│   ├── globals.css              # Tailwind directives + global styles
│   ├── sections/                # Machine Sections
│   │   ├── ui/
│   │   │   ├── Cube.tsx
│   │   │   ├── CubeGrid.tsx
│   │   │   ├── ContextMenu.tsx
│   │   │   ├── Toolbar.tsx
│   │   │   └── Onboarding.tsx
│   │   ├── state/
│   │   │   ├── cubeStore.ts
│   │   │   ├── layoutStore.ts
│   │   │   └── userStore.ts
│   │   ├── persistence/
│   │   │   ├── firebase.ts
│   │   │   ├── sync.ts
│   │   │   └── offlineQueue.ts
│   │   ├── sharing/
│   │   │   └── README.md        # Phase 2 stub
│   │   └── agent/
│   │       └── README.md        # Phase 2 stub
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useCubes.ts
│   │   ├── useLayout.ts
│   │   └── useDragAndDrop.ts
│   ├── lib/
│   │   ├── utils.ts             # cn() helper, general utilities
│   │   └── constants.ts         # Grid defaults, limits, etc.
│   └── types/
│       └── index.ts             # All TypeScript interfaces
├── components/
│   └── ui/                      # shadcn/ui components (auto-generated)
├── public/
│   ├── manifest.json            # PWA manifest
│   └── icons/                   # PWA icons (192x192, 512x512)
├── tests/
│   ├── unit/                    # Vitest tests (mirror app structure)
│   └── e2e/                     # Playwright tests
├── firebase.json                # Firebase config
├── firestore.rules              # Security rules
├── firestore.indexes.json       # Composite indexes
├── next.config.js               # Next.js config (PWA setup)
├── tailwind.config.ts           # Tailwind theme config
├── vitest.config.ts             # Test config
├── playwright.config.ts         # E2E test config
├── .eslintrc.json               # Linting rules
├── .prettierrc                  # Formatting rules
├── tsconfig.json
└── package.json
```

---

## 7. Development Workflow & Git Strategy

### 7.1 Branching Strategy: GitHub Flow (Simplified)

We use **GitHub Flow** — lightweight, appropriate for a solo/small team. No complex Git Flow needed.

```
main (protected, always deployable)
  │
  ├── feature/cube-drag-drop    ──▶ PR ──▶ merge
  ├── feature/firebase-sync     ──▶ PR ──▶ merge
  ├── feature/auth-flow         ──▶ PR ──▶ merge
  ├── feature/pwa-shell         ──▶ PR ──▶ merge
  ├── feature/onboarding        ──▶ PR ──▶ merge
  │
  └── hotfix/offline-sync-bug   ──▶ PR ──▶ merge (fast-track)
```

**Branch naming conventions:**
- `feature/<short-description>` — New features
- `fix/<short-description>` — Bug fixes
- `chore/<short-description>` — Maintenance, config, deps
- `docs/<short-description>` — Documentation updates

**Commit message convention (Conventional Commits):**
```
feat: add cube drag-and-drop with grid snapping
fix: resolve offline sync queue race condition
chore: update firebase to v10.12
 docs: add machine sections architecture diagram
 test: add unit tests for cubeStore
refactor: extract drag logic into useDragAndDrop hook
```

### 7.2 Development Lifecycle

```
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Plan   │───▶│  Develop │───▶│  Review │───▶│  Test   │───▶│  Deploy │
│ (Issue) │    │ (Branch) │    │  (PR)   │    │ (CI/CD) │    │(Vercel) │
└─────────┘    └──────────┘    └─────────┘    └─────────┘    └─────────┘
```

**1. Plan:** Every piece of work starts as a GitHub Issue. Issues are tagged:
- `phase-1` / `phase-2` / `phase-3` / `phase-4`
- `must-have` / `should-have` / `nice-to-have`
- `section: ui` / `section: state` / `section: persistence` / `section: sharing`

**2. Develop:** Create feature branch from `main`. Work locally. Use Firebase emulator for local development (no live Firebase needed).

**3. Review:** Open PR when ready. Self-review checklist (see Section 10). Merge only after CI passes.

**4. Test:** CI runs lint, type-check, unit tests, and build on every PR.

**5. Deploy:** Vercel auto-deploys `main` to production. Preview deployments on every PR.

### 7.3 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  lint-and-typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run test:unit
      - run: npm run build
```

**Vercel config:** Auto-deploy `main` branch to production. Every PR gets a preview URL.

### 7.4 Environments

| Environment | URL | Firebase | Purpose |
|-------------|-----|----------|---------|
| **Local** | localhost:3000 | Firebase Emulator | Daily development |
| **Preview** | vercel-preview-xxx.vercel.app | Staging project | PR reviews |
| **Production** | kiss-dashboard.vercel.app | Production project | Live app |

**Firebase projects:** Create 3 separate Firebase projects (local-emulator, staging, production). Use environment variables to switch between them.

### 7.5 Definition of Done

A feature is **Done** when ALL of the following are true:

- [ ] Code is written and follows project conventions (lint, format, types)
- [ ] Unit tests cover core logic (minimum 70% coverage for new code)
- [ ] Feature works in the Firebase emulator environment
- [ ] Manual testing checklist completed (see Section 10)
- [ ] PR is opened with clear description and screenshots/GIFs
- [ ] CI passes (lint, typecheck, tests, build)
- [ ] No console errors or warnings in dev build
- [ ] Code reviewed (self-review minimum; peer review when team grows)
- [ ] Merged to `main` and deployed to preview
- [ ] Issue closed with implementation notes

---

## 8. UI/UX Specification

### 8.1 Dashboard Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  kiss-dashboard                              [User ▼]               │  ← Header (minimal)
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │
│  │   AI   │  │ Claude │  │ChatGPT │  │ Gemini │  │Perplex │        │
│  └────────┘  └────────┘  └────────┘  └────────┘  └────────┘        │
│                                                                      │
│  ┌────────────────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │
│  │   Video Editing    │  │ Notes  │  │ Todo   │  │ Calendar│        │
│  │                    │  └────────┘  └────────┘  └────────┘        │
│  └────────────────────┘                                              │
│                                                                      │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐                    │
│  │ Scripts│  │ Assets │  │ Export │  │ Settings│                   │
│  └────────┘  └────────┘  └────────┘  └────────┘                    │
│                                                                      │
│                          [+ Add Cube]                                │  ← Floating action (appears on hover near bottom)
├──────────────────────────────────────────────────────────────────────┤
│  Grid: 6×4                      Layout: Main           Sync: ✓       │  ← Footer (subtle status bar)
└──────────────────────────────────────────────────────────────────────┘
```

### 8.2 Cube States

```
DEFAULT          HOVER              DRAGGING           EDITING
┌────────┐      ┌────────┐        ┌────────┐        ┌──────────────┐
│        │      │        │        │        │        │              │
│ Claude │  →   │ Claude │   →    │ Claude │   →    │ [Claude    ] │  ← editable text field
│        │      │        │        │        │        │              │
└────────┘      └────────┘        └────────┘        └──────────────┘
  white bg      light border      elevated shadow   blue outline (focus)
  black text    subtle shadow     slight scale      text selected
```

### 8.3 Context Menu

```
┌──────────────────┐
│  ✏️  Edit Label  │
├──────────────────┤
│  📐 Resize       │
│    ├─ 1 × 1      │
│    ├─ 1 × 2      │
│    ├─ 2 × 1      │
│    └─ 2 × 2      │
├──────────────────┤
│  📋 Duplicate    │
├──────────────────┤
│  🗑️  Delete      │   ← Red text, confirmation on click
└──────────────────┘

Note: Icons in menu are OK (UI chrome). Cubes remain text-only.
```

### 8.4 Responsive Behavior

| Breakpoint | Grid Columns | Cube Size | Notes |
|------------|-------------|-----------|-------|
| Desktop (≥1024px) | 6 | 120-180px | Full layout |
| Tablet (768-1023px) | 4 | 100-140px | Slightly compressed |
| Mobile landscape | 4 | 80-100px | Functional but not optimized |
| Mobile portrait | 2-3 | 80-120px | Minimum viable |

---

## 9. Testing Strategy

### 9.1 Unit Tests (Vitest)

Test every store, utility function, and hook. Mirror the app directory structure in `tests/unit/`.

**Priority test targets:**
- `cubeStore` — CRUD operations, position updates, resize logic
- `layoutStore` — layout switching, persistence integration
- `useDragAndDrop` — collision detection, snap-to-grid, boundary checks
- `sync.ts` — debounced writes, offline queue, conflict resolution

### 9.2 E2E Tests (Playwright)

Cover the critical user journeys:

1. **Onboarding flow** — New user sees tutorial, completes steps, layout persists
2. **Cube CRUD** — Add, edit, resize, move, delete a cube
3. **Drag and drop** — Drag cube from A to B, verify new position persists after refresh
4. **AI cube** — Click AI cube, see sub-cubes, click back
5. **Auth flow** — Sign up, create cubes, log out, log in, verify cubes restored
6. **Offline mode** — Disconnect, make changes, reconnect, verify sync

### 9.3 Manual Testing Checklist

**For every PR, verify:**
- [ ] Feature works in Chrome, Firefox, Safari (latest 2 versions)
- [ ] Feature works on mobile browser (iOS Safari, Android Chrome)
- [ ] Feature works with Firebase emulator (offline)
- [ ] Feature works against staging Firebase (online)
- [ ] No visual regressions at all breakpoints
- [ ] Keyboard navigation works (Tab, Enter, Escape, arrow keys)
- [ ] Screen reader announces state changes correctly

---

## 10. Risks & Mitigations

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|----|------|------------|--------|------------|-------|
| R-01 | Drag-and-drop performance degrades with 50+ cubes | Medium | High | Virtualize rendering if needed; optimize with React.memo; profile early | Tech Lead |
| R-02 | Firebase offline sync has edge cases (conflicts, large queues) | Medium | High | Extensive testing with emulator; implement conflict resolution strategy; consider custom queue | Tech Lead |
| R-03 | Scope creep from scaffolding spec (Phase 4 features leaking in) | High | High | **This PRD is the gate.** Refer all feature requests to PRD. Scaffold spec is explicitly Phase 4. | Product Owner |
| R-04 | Mobile browser experience is poor (not a native app) | Medium | Medium | Set expectations: mobile browser is "usable," full mobile app is Phase 2 | Product Owner |
| R-05 | Firebase costs exceed budget at scale | Low | Medium | Monitor usage; design abstraction layer for future backend migration; stay within Spark tier limits for Phase 1 | Tech Lead |
| R-06 | @dnd-kit doesn't meet custom grid-snapping needs | Low | High | Evaluate dnd-kit grid support early (spike: 1 day); fallback to react-grid-layout if needed | Tech Lead |
| R-07 | PWA offline functionality is unreliable | Medium | Medium | Use Workbox for service worker; test extensively with Lighthouse; graceful degradation | Tech Lead |

---

## 11. Phased Roadmap (High-Level)

### Phase 1: Core Dashboard (MVP) — 4-6 Weeks
**Goal:** Prove the cube interface works in a live web environment.
**Deliverables:** Browser dashboard with grid, cubes, drag-and-drop, persistence, auth, PWA.

| Week | Focus | Key Deliverables |
|------|-------|-----------------|
| 1 | Project setup, architecture | Repo, CI/CD, Firebase config, Machine Sections structure, base grid rendering |
| 2 | Core cube mechanics | Drag-and-drop, resize, edit, add, delete — all local state only |
| 3 | Persistence & auth | Firebase integration, offline sync, auth flows, data model |
| 4 | Polish & PWA | Onboarding, PWA shell, responsive breakpoints, performance optimization |
| 5-6 | Buffer & testing | E2E tests, bug fixes, performance tuning, soft launch to test users |

### Phase 2: Sharing & Mobile — 4 Weeks (TBD)
- Share tokens + QR codes + read-only views
- "Mini Me" mobile app (PWA → native)
- Desktop-mobile docking and sync
- AI cube with live API integration (OpenAI, Anthropic)

### Phase 3: Community & Marketplace — 6 Weeks (TBD)
- Faceplate sharing marketplace
- P2P cube stack trading
- Creator monetization + affiliate links
- NFT/blockchain integration (optional)

### Phase 4: Advanced Features — 8 Weeks (TBD)
- Project scaffolding & file management (three-panel interface from scaffolding spec)
- Real-time collaboration
- System-wide sweep across projects
- Professional template marketplace

---

## 12. Open Questions & Decisions Needed

The following items need **your decision** before development begins. These are the discussion points we should resolve together:

### Decision Required: Product

| # | Question | Options | My Recommendation |
|---|----------|---------|-------------------|
| D-01 | **Product name** | "KISS Dashboard" (working title) vs. rebrand | Keep "KISS Dashboard" for MVP; rebrand before public launch if desired |
| D-02 | **Anonymous auth** | Allow usage without account? | Yes — lower friction, prompt to save account later |
| D-03 | **Default grid size** | How many columns × rows? | 6 × 4 on desktop, responsive down to 2 columns on mobile |
| D-04 | **Cube count limit** | Max cubes per layout? | 50 for Phase 1 (prevents abuse, covers 99% of use cases) |

### Decision Required: Technical

| # | Question | Options | My Recommendation |
|---|----------|---------|-------------------|
| D-05 | **Next.js rendering** | Server Components vs. Client Components for grid? | Client Components for the grid (needs interactivity); SC for auth/layout shell |
| D-06 | **Drag library** | @dnd-kit vs. react-grid-layout vs. custom? | @dnd-kit — modern, accessible, performant; spike in Week 1 to validate |
| D-07 | **State shape** | One Zustand store or multiple? | Multiple stores (cubeStore, layoutStore, userStore) — matches Machine Sections |
| D-08 | **Testing threshold** | Minimum code coverage? | 70% for stores/utils; E2E for all critical paths; no coverage gate in CI (quality over numbers) |

### Decision Required: Workflow

| # | Question | Options | My Recommendation |
|---|----------|---------|-------------------|
| D-09 | **Repo setup** | Monorepo vs. single repo? | Single repo for Phase 1; monorepo if mobile app splits in Phase 2 |
| D-10 | **Issue tracking** | GitHub Issues vs. external tool? | GitHub Issues — simple, integrated, close to code |
| D-11 | **Documentation** | Where does the "source of truth" live? | **This PRD** + README.md in repo for setup instructions; update PRD as specs evolve |

---

## 13. Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Cube** | A white, text-only block on the grid. The fundamental UI element. |
| **Faceplate** | A saved dashboard layout (collection of cubes with positions and labels). Named after the sonar film faceplates. |
| **Machine Sections** | The six-layer architecture (UI, State, Persistence, Sharing, Agent, Community). Each layer is independent. |
| **Mothership** | The desktop/browser version of the dashboard. |
| **Mini Me** | The mobile companion app (Phase 2). |
| **Railroad tracks** | The standard base folder structure applied to all scaffolded projects (Phase 4). |
| **Scaffolding** | The project/file management system for creating and organizing project folders (Phase 4). |
| **Sweep** | Cross-project query capability — pull data from all projects simultaneously (Phase 4). |

### Appendix B: Reference Links

- Next.js App Router: https://nextjs.org/docs/app
- Zustand: https://docs.pmndrs.com/zustand/
- @dnd-kit: https://dndkit.com/
- Firebase Web: https://firebase.google.com/docs/web/setup
- shadcn/ui: https://ui.shadcn.com/

### Appendix C: Prior Art & Inspiration

- **Navy sonar panels:** Physical metaphor — tactile, remappable, zero clutter.
- **NotebookLM:** Three-panel source/operation/output pattern (scaffolding spec).
- **Adobe Lightroom:** Non-destructive editing model — sandbox before commit (scaffolding spec).
- **Notion:** Blank-canvas flexibility with block-based editing.
- **Figma:** Infinite canvas with modular components.

---

**END OF DOCUMENT**

*This PRD supersedes all previous project documents. For questions, clarifications, or change requests, open a GitHub Issue referencing the relevant section number.*
