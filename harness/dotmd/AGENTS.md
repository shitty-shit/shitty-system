---
ijfw_version: 1.3.2
ijfw_schema: 1
type: business
primary_type: business
secondary_types: []
confidence: 0.695
detected_at: 2026-08-11T01:32:04.245Z
signals:
  - kind: file_extension_ratio
    weight: 0.7
    domain: business
    ratio: 0.857
    count: 6
  - kind: file_extension_ratio
    weight: 0.7
    domain: software
    ratio: 0.143
    count: 1
---
# AGENTS.md

This file follows the open AGENTS.md spec (https://agents.md/) and is the
canonical agent-instructions surface for this project. Platform-specific
files (CLAUDE.md, GEMINI.md, WAYLAND.md, codex/AGENTS.md, .cursorrules,
.windsurfrules, copilot-instructions.md) are thin adapters that point here.

Five IJFW-managed regions live in this file. Content outside the markers is
yours -- IJFW will never touch it.

| Region | Purpose |
|---|---|
| MEMORY | Project memory recalled from `.ijfw/memory/` |
| ROUTING | Platform skill-routing rules |
| AGENTS | Registered agent roster |
| BLACKBOARD | Multi-CLI orchestration scratchpad (Pillar B) |
| DISCIPLINE | Per-domain discipline rules (code \| narrative \| business \| design \| research) |

<!-- IJFW-MEMORY-START -->
Project memory at .ijfw/memory/. Call `ijfw_memory_prelude` for full context.
<!-- IJFW-MEMORY-END -->

<!-- IJFW-ROUTING-START -->
<!-- IJFW-ROUTING-END -->

<!-- IJFW-AGENTS-START -->
No project agents yet. Run `ijfw team` to set them up.
<!-- IJFW-AGENTS-END -->

<!-- IJFW-BLACKBOARD-START -->
<!-- Reserved for Pillar B multi-CLI orchestration. Empty in alpha. -->
<!-- IJFW-BLACKBOARD-END -->

<!-- IJFW-DISCIPLINE-START -->
<!-- IJFW-DISCIPLINE-END -->

## Shared agent state (workspace-wide handoff)

This repo sits inside a multi-agent workspace. Before starting work, read `../.state/state.json`
(open sessions, tasks, goals) and follow the protocol in `../.state/README.md`. Update your
session entry at milestones and regenerate the dashboard with `python3 ../.state/gen_dash.py`.
Platform adapters (CLAUDE.md, etc.) point here, so any agent entering this repo gets the same
onboarding.

## The One Store (canonical archive)

The canonical archive for every artifact from every agent is `D:\SHITTYSHIT`
(the git repo pushed to GitHub `shitty-shit/shittyshit`). On start, also read
`D:\SHITTYSHIT\00_MASTER\REGISTRY.md` (artifact database) and
`D:\SHITTYSHIT\00_MASTER\conversations\INDEX.md`. Deposit conversations as
threads in `D:\SHITTYSHIT\00_MASTER\conversations\threads\` per its
TEMPLATE/README. Doctrine: `D:\SHITTYSHIT\00_MASTER\one-store.md`.
For answers that synthesize across sources, read the compiled wiki at
`D:\SHITTYSHIT\00_MASTER\wiki\` (index.md first); maintain pages you touch
with provenance per `wiki/SCHEMA.md` and run `wiki/lint.py` after edits.
