# STFU+WRITE — The Quiet Architecture of Professional Focus

> First focused, commercial vertical on the KISS frame. Fifth canon doc.
> "Loud name. Quiet software." — AI that knows when to shut up.

## 1. Core philosophy

- **Behind the Page, Not in the Way:** "We put the intelligence behind the page, not
  between you and the page." During raw freewriting the interface disappears.
- **Capability Hidden Until Summoned:** formatting, AI critique, research, media,
  publishing — all hidden until the writer intentionally summons them.

## 2. Non-destructive architecture (the "Lightroom" model)

- **Move representations first:** layouts, cards, and outline cubes are lightweight
  representations; move/swap/group/resize freely without altering underlying files.
- **Untouched source materials:** raw creative drafts are immutable source artifacts;
  changes commit to storage only when explicitly requested.

## 3. The initial Writer Deck — six functional cubes

| Cube | Purpose |
|---|---|
| WRITE | focus area for input |
| PROJECT | management of drafts and book structures |
| VOICE | style guidelines / dictation preferences |
| EDIT | revision overlays |
| SOURCE | research, character sheets, outlines |
| OUTPUT | formatting and export preparation |

**Five workspace modes** — FLOW (focused draft), FREEWRITE (uninhibited), EDIT
(revision), REFERENCE (research docked alongside), OUTPUT (finalize/export).
Opening a control cube remaps the visible grid to its specialized sub-cubes.

## 4. Phased roadmap

- **Phase 2 — Writer Without AI:** prove the minimalist writing client on its own.
  Refine FLOW, keyboard shortcuts, simple local file exports (Markdown + plain text),
  no backend network requirements. *(this is what the prototype's Writer plate builds)*
- **Phase 3 — KISS Writer Engine:** move the writing viewport onto reusable KISS
  grid primitives. *(the frame already is this)*
- **Phase 4 — AI After the Human:** targeted AI after the draft — summarization,
  critique, structural analysis, key-phrase extraction — via modular adapters
  (OpenAI / Anthropic / Gemini swappable without rewriting the core).
  *(built as the EDIT·CRITIQUE cube — ships a draft to an agent inbox as a critique
  brief and lands the return as a note cube; live model adapters still stubbed.)*
- **Phase 5 — STEM-Lite Context:** portable Markdown-backed background folders
  (style prefs, outlines, character guides, terminology dictionaries) fed to AI on
  demand — no massive chat histories.

## 5. Target audience & success metrics

Serious long-form creators: sci-fi/novelists, copywriters, technical content creators.
Success = sustained time writing, high return-session rate, frequency of returning to
FLOW, zero confusion about cube behavior. So intuitive a new user finishes a
productive session without the philosophy ever being explained.

---

*Prototype: the Writer plate (`index.html` → Writer preset) implements Phase 2 —
real `.md` drafts via `bridge.py /draft`, explicit-save-only (the Commit gate), and
the six cubes + five modes remapping the grid. Phase 4 (AI critique) is built: the
EDIT·CRITIQUE cube ships a draft to an agent inbox as a critique brief (summarize /
structure / keyphrases) and lands the returned critique as a note cube. Phase 5
(STEM-Lite context) remains stubbed as a hidden-until-summoned cube.*