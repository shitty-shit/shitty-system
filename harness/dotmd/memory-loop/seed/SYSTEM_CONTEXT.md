# Agent Memory Loop — System Context

This workspace is the **persistent memory spine** for the ShittyShit / LACES_CASES
agent ecosystem. Every agent that works inside this ecosystem reads from and writes
to this loop.

## What This Is

A LanceDB-backed vector memory store (via AnythingLLM) that gives agents:

1. **Cross-session memory** — What one agent learns, the next agent knows.
2. **Semantic search** — Ask "what tools handle code review?" and find relevant
   past observations, even if they don't use those exact words.
3. **Decision history** — Why was a particular choice made? The reasoning is here.
4. **Handoff context** — When one agent finishes and another starts, the baton
   passes through this workspace.

## How Agents Use This

### On Start
Query the loop for current state:
```
"current priorities, recent decisions, open questions, system state"
```

### During Work
Search for relevant past knowledge:
```
"how does the LACES_CASES routing work for coding tasks?"
```

### On Finish
Write a handoff entry summarizing what was done, what was decided, what's next.

## Entry Types

| Type | Meaning |
|---|---|
| observation | Something discovered while working |
| decision | A choice made, with reasoning |
| question | Something that needs answering later |
| fact | Ground truth about the system |
| handoff | Context passed between agents at session boundaries |
| correction | A previous entry was wrong; here's the fix |

## Confidence Tags

Same taxonomy as graphify:
- **EXTRACTED** — directly from source files, verifiable
- **INFERRED** — reasonable conclusion, but could be wrong
- **AMBIGUOUS** — uncertain, flagged for review

## Connecting to the Graph

Every memory entry can link to nodes in the graphify knowledge graph via the
`related_nodes` frontmatter field. The graph provides the static structure;
the memory loop provides the living context on top of it.

## Rules

1. Write self-contained entries. A future agent should understand without re-reading sources.
2. Be honest about confidence. Never mark inference as EXTRACTED.
3. Link to the graph when possible.
4. Always include a next step, even if it's "no action needed."
5. Don't use this as a diary. Write when you learn something another agent needs.

---

*This document is the reference card for the memory loop. It should not be modified
by agents — it's the map, not the territory.*
