<!-- ijfw-schema: v1 -->
# Knowledge Base
---
type: decision
summary: One repo for Freebuff cross-chat memory
stored: 2026-08-17T02:28:56.298Z
hash: d1173822c02c
tags: [freebuff, ijfw, shared-memory, architecture]
---
<!-- hash:d1173822c02c -->
Freebuff chats working in C:\Users\idfk\Desktop\harness use the dedicated freebuff-memory repository through IJFW MCP. IJFW_PROJECT_DIR is pinned to that repo so the store does not depend on chat working directory. The AnythingLLM memory prototype is deferred.

**Why:** A fixed local repo prevents split memory and gives Kevin inspectable, versionable handoffs without requiring other IDEs or cloud services.

**How to apply:** At chat start call ijfw_memory_prelude. Store durable decisions as they happen and a compact handoff after substantive work.
---
type: decision
summary: Adopt three-layer Freebuff-to-canon memory architecture
stored: 2026-08-17T02:50:12.676Z
hash: cc5d8e3af25c
tags: [freebuff, ijfw, memory-loop, architecture]
---
<!-- hash:cc5d8e3af25c -->
Freebuff shared memory uses three layers: Freebuff desktop-v2.db is authoritative raw conversation evidence; IJFW in Desktop/harness/freebuff-memory is the compact cross-chat hot cache; D:/SHITTYSHIT handoffs plus the guarded laces_cases memory loop are the all-local-agent handoff and canonical layers. Raw transcripts are read in place and fingerprinted, never bulk-copied into memory. Canonical claims still use proposal plus explicit Kevin approval.

**Why:** Preserves raw conversations, provides fast cross-chat continuity, and integrates with the existing local canonical system without creating a competing source of truth.

**How to apply:** Use freebuff_bridge.py for read-only thread discovery/fingerprints and publish IJFW handoffs to D:/SHITTYSHIT/00_MASTER/handoffs/freebuff.
