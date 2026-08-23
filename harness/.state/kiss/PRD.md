# KISS Dashboard — Product Requirements Document (PRD)

> Canonical working spec. `id: kiss.prd.master` · `status: canonical-working-spec`
> · `phase: 1.3 (GetShitDone Master Build)` · `updated: 2026-08-17`
>
> The Social Ecosystem & Sharing Site

## 1. Product Vision & Core Philosophy

The KISS Dashboard is a modular, touch-sensitive, universal middle-layer designed
to sit between a user, their devices, their apps, and their AI agents. It functions
as a customizable cube-based control surface for complex systems, workflows, and
media contexts.

### 1.1 Origin & Design Inspiration

The foundational design idea is rooted in 1980s Navy submarine sonar control systems:

- **Clear Remappable Controls:** Large, tactile pads with translucent film faceplates.
- **Instant Context Switching:** Pushing one button mechanically/electronically remaps
  the entire "faceplate" without rewiring the system.
- **Minimal Clutter & High Adaptability:** Maximum usability with zero visual noise.

### 1.2 "The Middle Way" Interface

KISS translates the sonar philosophy into a digital cube interface:

- **The Blank Canvas:** The interface relies on a plain framework of white or minimalist
  blocks and text-forward labels. No heavy system graphics, forced icons, or borders.
- **Guided Defaults:** The dashboard launches with onboarding aids (e.g., a default "AI"
  cube that, when clicked, repopulates the board with starter nodes like "Claude" or "Gemini").
- **Total Modularity:** Everything about cube layout, artwork, and function is completely
  driven by user preference and community remixing. *Holding a cube opens a contextual
  menu ("Make this cube a...").*

### 1.3 Bypassing the Grind (Time = Money)

The platform solves the historical bottleneck in tech and creative fields: time wasted
figuring out which tools actually work together. Instead of spending months trial-and-erroring
a tech stack, newcomers can instantly adopt the proven digital workspaces of industry veterans.

## 2. Target Audience & The Symbiotic Loop

The platform thrives on an ecosystem consisting of two distinct user types:

### 2.1 The Master (Creator)

- **Profile:** High-earning professionals (3-digit million NYC commercial real estate brokers,
  verified crypto traders, senior full-stack developers, master photographers).
- **Motivation:** The "Look at My Rig" ego-flex — packaging precise workflows, app stacks, and
  AI prompts into a shareable KISS Dashboard.
- **Value Proposition:** Lead generation — a downloaded dashboard makes the consumer a captive
  audience for the Master's consulting, services, or premium courses.

### 2.2 The "Wannabe" (Consumer)

- **Profile:** Newcomers, aspiring creators, professionals looking to optimize their workflow.
- **Motivation:** Buying their way into a professional's headspace.
- **Value Proposition:** A pre-configured toolkit that strips away overhyped "snake oil" tools
  in favor of battle-tested production workflows.

## 3. Core Product Features & Mechanics

### 3.1 The Mothership & Contextual Hot-Swapping

- **The Mothership Hardware:** A master desktop computer or local server acting as a docking
  station, managing massive repositories of customized cubes.
- **Contextual Faceplates:** Plug in / connect via WiFi → instantly hot-swap the entire
  interface based on context.
- **Binge Mode:** A faceplate strictly for video streaming, media, and social feeds.
- **Deep Work Mode:** Strips away distractions — coding environments, web UI creation, local
  LLM interfaces, direct taps into VM compute/cloud GPUs.
- **Bug-Out Safe:** Ongoing project states are highly portable.

### 3.2 Edge AI & Offline-First Capability

- **On-Device Models:** Run offline with lightweight on-device AI (Google Gemma, IBM Granite)
  on phones or in browsers.
- **Resilience:** The dashboard stays intelligent and functional without a cloud connection.

### 3.3 The Anonymized Wisdom Database

- **Behavioral Telemetry:** As users dock, update, add, and delete cubes, the system quietly
  builds an anonymized global database of toolsets categorized by profession.
- **Real-Time Intelligence:** If the top 10% of developers suddenly drop a UI tool, the KISS
  database registers the shift instantly, surfacing the best tools organically.

## 4. Community, Marketplace & Monetization

### 4.1 P2P Marketplace

- **Selling the Stack:** Users publish, share, or sell custom dashboards (faceplates, cube
  logic, visual overlays) in the P2P KISS Marketplace.
- **Blockchain/NFT Integration:** Ownership, monetization, and frictionless P2P trading of
  unique dashboard setups via blockchain infrastructure.

### 4.2 The Affiliate Engine

- **Embedded Revenue:** Creators embed affiliate links, premium access, or course upsells
  directly into their cubes.
- **Automated Funnel:** Installing an "AI Video Editor" stack immediately funnels into the
  necessary SaaS trials and activations — passive income for creator and platform.

### 4.3 Subscription Tiers

- **FREE Kisses Channel:** An official, curated cube-set, free — high-value localized resources
  (free AI inference links, local grants, food resources, Craigslist/FB Marketplace blends).
- **Freemium Tier:** Basic ad-supported access with community elements and starter dashboards.
- **Paid Tiers:** $3/month up to $10+ for premium community features, advanced integrations,
  and exclusive master stacks.

## 5. Technical Implementation Specification

**Architectural Philosophy — "Machine Sections" Discipline:** UI Layer, State Manager,
Persistence Layer, Sharing Layer, Agent Layer, Community Layer.

### 5.1 Tech Stack

- Core: **Next.js 14+** (App Router), **TypeScript strict**
- UI/Styling: **React 18+** functional components, **Tailwind CSS** (minimalist, text-only),
  **React DnD Kit** (drag-and-drop grid management)
- State: **Zustand** (cube positions, dimensions, labels, layout persistence, session state)
- Backend/DB: **Firebase** (Firestore real-time + offline persistence, Firebase Auth, Firebase
  Storage for community assets)

### 5.2 Data Model Specification (MVP)

```ts
interface Cube {
  id: string;
  position: { x: number, y: number };
  dimensions: { width: number, height: number };
  label: string;
  type: 'basic' | 'ai' | 'app' | 'workflow';
  config: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

interface Layout {
  id: string;
  userId: string;
  name: string;
  cubes: Cube[];
  isPublic: boolean;
  shareToken?: string;
  createdAt: Date;
  updatedAt: Date;
}

interface User {
  id: string;
  email: string;
  preferences: {
    gridSize: number;
    defaultLayout: string;
    theme: 'minimal' | 'dark';
  };
  createdAt: Date;
}
```

## 6. Project Phases & Roadmap

### Phase 1: MVP — Core Dashboard & App (Weeks 1-4)

- **Dynamic Cube Grid:** Drag-and-drop repositioning, resizing (1x1, 2x1, 2x2), grid snapping.
  Pure minimalist design (white background, black text).
- **Cube Management:** Double-click text editing, right-click context menus, dynamic
  color-coded borders by type.
- **Layout Persistence:** Debounced auto-save to Firestore, offline capability,
  layout version history.

### Phase 2: Sharing, Mobile, & Edge AI (Weeks 5-8)

- **Share System:** Unique share tokens, read-only modes, QR codes for mobile sharing.
- **Mobile Experience ("Mini Me"):** Touch-optimized grid, swipe gestures, offline-first
  operation, sync/dock protocols with the Desktop Mothership.
- **AI Cube Integration:** Dynamic AI model selection, context-aware sub-cube generation,
  Edge AI (Gemma/Granite) local integration.

### Phase 3: Community & Marketplace (Weeks 9-12+)

- **Marketplace Infrastructure:** Faceplate sharing, creator monetization, affiliate
  integration framework.
- **Advanced Capabilities:** P2P cube trading, real-time collaboration, Blockchain/NFT
  integration, Anonymized Wisdom Database.
