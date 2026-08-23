# Agent Memory Loop — Entry Spec

Version: 1.0 | Architecture: LACES_CASES | Storage: AnythingLLM + LanceDB

## What This Is

Every agent interaction with the memory loop produces a **memory entry** — a markdown file
uploaded to the `Agent Memory Loop` workspace in AnythingLLM. LanceDB indexes each entry
for semantic retrieval. Agents read context by querying the workspace; they write knowledge
back by uploading new entries.

## Entry Format

Every entry is a markdown file with YAML frontmatter. The frontmatter carries structured
metadata for filtering and routing; the body carries the human/agent-readable content.

```markdown
---
type: observation | decision | question | fact | handoff | correction
agent: freebuff-cli
model: deepseek-v4-pro
session: 2026-08-10-memory-loop-build
timestamp: 2026-08-10T22:15:00-04:00
confidence: EXTRACTED | INFERRED | AMBIGUOUS
tags:
  - memory-loop
  - anythingllm
  - architecture
source_file: memory-loop/SETUP.md
related_nodes:
  - agent_mesh
  - laces_cases
  - toolstack_md
priority: P0 | P1 | P2 | P3
---

# [One-line summary of what was observed or decided]

[Full context. What happened, what was discovered, what decision was made,
 and why. Enough detail that a future agent reading this cold understands
 the reasoning without re-reading the source files.]

## Action Taken
- [What the agent did with this knowledge]

## Next
- [What should happen next, if anything]
```

## Field Reference

| Field | Required | Values | Purpose |
|---|---|---|---|
| `type` | Yes | `observation`, `decision`, `question`, `fact`, `handoff`, `correction` | What kind of memory this is |
| `agent` | Yes | `freebuff-cli`, `claude-code`, `codex`, `cuey`, `hermes`, `skales`, `cochat` | Which agent wrote it |
| `model` | No | model name | Which model the agent was running |
| `session` | No | `YYYY-MM-DD-brief-slug` | Groups entries from the same session |
| `timestamp` | Yes | ISO 8601 | When this was observed |
| `confidence` | Yes | `EXTRACTED`, `INFERRED`, `AMBIGUOUS` | Same taxonomy as graphify |
| `tags` | No | list of strings | For filtering and category routing |
| `source_file` | No | relative path | What file this knowledge came from |
| `related_nodes` | No | list of graph node IDs | Links to graphify knowledge graph |
| `priority` | No | `P0`, `P1`, `P2`, `P3` | How important this is for next agents to see |

## Entry Types

### observation
Something the agent noticed while working. "Discovered that the toolstack routes
all coding work to Codex and Claude Code." Not a decision — just a fact the agent
encountered.

### decision
A choice the agent made. "Decided to use FastAPI over Flask because AnythingLLM's
API already uses a similar pattern." Must include the reasoning so future agents
can revisit if circumstances change.

### question
Something the agent couldn't answer and wants a future agent (or human) to resolve.
"Unsure whether Dolt should be the primary store or just the audit log. Need Kevin's
decision."

### fact
A ground-truth statement about the system. "The Mothership runs AnythingLLM on port 3001.
The MINISFORUM is the execution node." Facts should have confidence EXTRACTED.

### handoff
Context passed from one agent to the next at session boundaries. "Freebuff built the
memory loop client. Claude Code should now wire it into the code-review workflow."

### correction
A previous memory entry was wrong. Must reference the entry being corrected and explain
what changed. "Correction to entry 2026-08-10-agent-routing: Codex is not the only
coding agent; Claude Code handles long-context refactors."

## Naming Convention

Files are named: `YYYY-MM-DD-HHMMSS-{type}-{short-slug}.md`

Example: `2026-08-10-221500-observation-toolstack-routing.md`

This sorts chronologically in the filesystem and AnythingLLM's document list.

## What Makes a Good Entry

1. **Self-contained.** A future agent reading this cold should understand it without
   re-reading the source files.
2. **Actionable.** It should tell the next agent what to do with this knowledge.
3. **Honest about confidence.** Never mark an inference as EXTRACTED. Use the same
   confidence taxonomy as graphify.
4. **Linked.** Reference related nodes from the knowledge graph so the memory loop
   and graph stay connected.
5. **Not a diary.** Don't narrate every step. Write entries when you learn something
   another agent needs to know.

## Anti-Patterns

- **Regurgitating source files.** Don't copy toolstack.md into a memory entry. Reference
  it and add what you *learned from applying it*.
- **Vague entries.** "Worked on the thing." → useless. "Discovered that Dolt table X
  has no index on column Y, causing slow queries." → useful.
- **No next step.** Every entry should give the next agent something to act on, even if
  it's just "no action needed."
- **Unmarked corrections.** If you realize a previous entry was wrong, write a correction
  entry. Don't silently overwrite. Dolt has the history; be honest about it.
