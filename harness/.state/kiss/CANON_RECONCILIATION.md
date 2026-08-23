# Canon Resolution & Reconciliation

The three sources cited on `diagrams/machine-sections-flow.png` are **found and absorbed**
into `.state/kiss/sources/` (2026-08-17). This file resolves them and reconciles deltas
against `PRD.md` (the working canon) and the prototype.

## 1. Source resolution

| Cited on diagram | Actual file | Found at | In the repo |
|---|---|---|---|
| `A2A_HANDOFF_ARTIFACT.pdf` | `🧩 A2A HANDOFF ARTIFACT.pdf` (2025-10-20, Kevin → DeepSeek) | `kiss docs/` repo + Desktop/prd_mudroom | `sources/a2a_artifact.txt` |
| `kiss_dashboard_scaffolding_spec.pdf` | `kiss_dashboard_scaffolding_spec.pdf` (2025-10) | `kiss docs/` repo + D: ledger `kiss_dashboard/assets/` | `sources/scaffolding_spec.txt` |
| `KISS_DASHBOARD_PRD_WORKING.md` | `PRD_KISS_Dashboard_v1.0.md` (DRAFT, 2026-06-13 — the consolidated "working" PRD) | Desktop/prd_mudroom | `sources/KISS_DASHBOARD_PRD_WORKING_v1.0.md` |

**Bonus canon also absorbed:** `KISS Dashboard Ecosystem Governance Charter.md`,
`The KISS Dashboard Strategic Framework.md` (prd_mudroom), and the project's real home:
the git repo **`kiss docs/`** (`00_SHITTYSHIT_MASTER/.PROJECTS_SHITTYSHIT/kiss docs`,
commits b952dce…9c35629) with `WHAT_WE_HAVE.md` (base inventory, 2026-08-09) and the
asset list (11_KISS_DASHBOARD.md, Complete Narrative, etc.).

## 2. Provenance chain (how everything fits)

```
2025-10-20  A2A HANDOFF ARTIFACT      → machine sections, 5-step A2A loop, data-flow diagram (the PNG!)
2025-10     scaffolding spec          → three-panel UI, Lightroom commit model, templates, sweep
2025-12     social ecosystem doc      → masters/wannabes, marketplace, camera-bag
2026-06-13  PRD v1.0                  → DEPRECATES all of the above ("this PRD is the gate");
                                        scaffolding spec explicitly = Phase 4 feature
2026-08     PRD.md (our canon)        → later iteration, "canonical-working-spec phase 1.3"
2026-08-17  .state/kiss/index.html    → the prototype of PRD Phase 1 (Prototype Zero)
```

## 3. Delta: v1.0 PRD vs working PRD.md (both are authoritative; v1.0 = depth)

- **v1.0 adds:** functional requirements (§4 Mothership/AI cube/persistence/PWA/onboarding/
  performance), PWA spec (§4.4 — our deck *is* a local-first PWA surrogate), performance
  budget (§4.6: LCP < 2.5s, input < 100ms — same as WHITE_PAPER), **machine-gun
  directory structure (§6.4)**, GitHub-Flow + CI §7 (for the product repo), **UI/UX
  spec §8**: 6×4 grid (we use 9-col; responsive: 6→4→2-3 columns; our prototype is
  desktop-9, mobile future), **cube states §8.2** (default/hover/dragging/editing with
  visual treatments — prototype has these as CSS classes), **context menu §8.3**
  (Edit label / Resize 1×1,1×2,2×1,2×2 / Duplicate / Delete — prototype matches 1:1
  plus Collapse, Sub-2×2, type menu), **testing §9** (Vitest/Playwright targets map
  to our store functions `cubeStore`≈`deck`, `sync.ts`≈debounce+history), **risks §10**
  (R-03: scaffold creep gate — "this PRD is the gate"), phases §11 (4-6 weeks MVP).
- **Our PRD.md adds:** AICube data model with subCubes, colors-by-type, the FREE place
  Kis-Channel, marketplace mechanics, phases 1-3 with the marketplace as 3.
- **Net:** no contradictions; our PRD.md is the trim, v1.0 is the spec-depth version.
  Adopt v1.0's §5-§9 as the product-side engineering spec when we repo the product.

## 4. Concept deltas absorbed

1. **AI Cube = dynamic parent node** (A2A §7, Governance §2, Strategic §2): "positioned
   at top of the default dashboard"; clicking repopulates with starter sub-cubes
   (Claude/Gemini/Perplexity/ChatGPT); non-permanent starting aids. → Our Coders plate
   is the working rendition (toolbar `＋` menu + presets); the sub-cube expansion UI is
   our future stack interaction.
2. **The scaffolding spec = Phase 4 vertical** (v1.0 confirmed): SOURCES/OPERATIONS/
   OUTPUT-PREVIEW three-pane, Lightroom non-destructive COMMIT (keep/move/archive), dry
   run, rollback manifests, template engine ("railroad tracks" + type extensions +
   distribution + _SYSTEM ops), system-wide sweep ("`sweep status all`"). → NOT in the
   prototype (correct — it's Phase 4 per the gate; our Commit-gate is the same
   discipline at layout grain).
3. **Layered-architecture rule** (Governance §3): community drives style/logic/bundles
   as *layers*; core never modified. → prototype accepts this: types/behaviors/kinds are
   all data, community-remixable; core is the frame.
4. **Governance principles** (A2A §9): transparency of AI contributions, human in the
   loop, "if a feature needs onboarding/documentation, question its necessity",
   composable future. → capture in the product's DoD later; the inbox A2A stages were
   already planned from this doc family.
5. **v1.0 §8.4 responsive columns** (6/4/2-3) vs our CELL=124 9-col: adopt mobile break
   points when the Android plate ships.

## 5. Prototype status vs v1.0 Phase 1 checklist (#: item → prototype)

| Phase-1 item (v1.0 §11) | Status in frame |
|---|---|
| grid + cubes + drag/resize/edit/add/delete | ✅ all built |
| persistence + auth (Firebase) | 1/2 — persistence built (localStorage + deck files); auth is architectural (N/A single-user-frame) until Firebase swap |
| onboarding tutorial | 🔲 Guided Defaults exist (presets, ＋ menus); tour not built |
| PWA shell / service worker | 🔲 future (offline default is simpler) |
| AI cube with live API | 🟡 inbox bridge is the local-first API loop |

**Bottom line:** the three-mystery documents were real, local, and their doctrine is
already implemented in phased form; the only things they add that the prototype
doesn't already honor are the UI-spec depth (states/menu/responsive), testing strategy,
parent-node AI expansion, and the Phase-4 scaffolding plate — all correctly gated
behind the roadmap.