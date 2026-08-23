# KISS deck feeds — the frame's content ports

The deck is a **frame**: cubes, grid, persistence, menus, and the bridge are
kind-agnostic. Every *kind* of content plugs in through the same five steps,
and every *feed* is one markdown file here.

## Add a new kind (recipe — e.g. a `link` cube took these five edits)

1. **Feed** — a `.md` file in `feeds/` + a parser in `gen_kiss.py`
   (`parse_links()` is the template); result lands in `KISS_DATA.*`.
2. **Renderer** — `body<Kind>(c)` in `kiss.html`, registered in the `bodyHtml` map.
3. **Behaviors** — a `BEHAVIORS.<kind>` entry (shown in the ⚡ chip menu).
4. **Interaction** — an `if (c.kind === '…')` block in `attachCube`
   (click/drag/drop rules) plus anything needed in the inspector.
5. **Type & presets** — `TYPE_BY_KIND` mapping (basic/ai/app/workflow) and
   where the kind shows up (presets, the `＋ cube` menu).

That's the whole loop: **frame stays, kinds proliferate.**

## Why it holds

- Grid, snapping, resize presets, stacking, dbl-click rename, context menu,
  theme, history, auto-save — zero kind-specific code.
- `localStorage` round-trips any cube's `data` — a new kind persists free.
- The bridge (`.md` inbox) is content-agnostic too: any kind can write/read
  files through it, not just agent tasks.