# Graph Report - C:\Users\idfk\Desktop\harness\ai-system-explainer  (2026-08-19)

## Corpus Check
- 7 files · ~2,165 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 22 nodes · 30 edges · 4 communities detected
- Extraction: 87% EXTRACTED · 10% INFERRED · 3% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Shared AI Services|Shared AI Services]]
- [[_COMMUNITY_D-Drive Storage|D-Drive Storage]]
- [[_COMMUNITY_Clients and Interfaces|Clients and Interfaces]]
- [[_COMMUNITY_Runtime Gaps|Runtime Gaps]]

## God Nodes (most connected - your core abstractions)
1. `Docker Desktop` - 10 edges
2. `LiteLLM model gateway` - 5 edges
3. `D: AI and Docker drive` - 5 edges
4. `Ollama model server` - 4 edges
5. `AnythingLLM workspace` - 4 edges
6. `Unsloth training server` - 4 edges
7. `Windows clients` - 3 edges
8. `Open WebUI chat` - 3 edges
9. `n8n automation` - 3 edges
10. `Ollama model files` - 2 edges

## Surprising Connections (you probably didn't know these)
- `Localhost-only boundary` --implements--> `Docker Desktop`  [EXTRACTED]
  04-operations-and-safety.md → 02-how-the-services-connect.md
- `Post-restart runtime state` --conceptually_related_to--> `Docker Desktop`  [EXTRACTED]
  03-current-state-and-gaps.md → 02-how-the-services-connect.md
- `AnythingLLM workspace` --conceptually_related_to--> `Freebuff canonical memory`  [AMBIGUOUS]
  02-how-the-services-connect.md → 03-current-state-and-gaps.md
- `Unsloth training server` --shares_data_with--> `D: AI and Docker drive`  [EXTRACTED]
  02-how-the-services-connect.md → 01-what-was-moved.md
- `ComfyUI` --shares_data_with--> `D: AI and Docker drive`  [EXTRACTED]
  03-current-state-and-gaps.md → 01-what-was-moved.md

## Hyperedges (group relationships)
- **Shared local AI service room** — docker_desktop, ollama, litellm, open_webui, n8n, anythingllm [EXTRACTED 1.00]
- **D-backed AI storage** — d_drive, ollama_models, unsloth, comfyui, lm_studio, rollback_copies [EXTRACTED 1.00]

## Communities

### Community 0 - "Shared AI Services"
Cohesion: 0.47
Nodes (6): LiteLLM model gateway, n8n automation, Ollama model server, Ollama model files, Open WebUI chat, Windows clients

### Community 1 - "D-Drive Storage"
Cohesion: 0.4
Nodes (6): AnythingLLM workspace, ChromaDB vector store, Docker Compose recipe, Docker Desktop, Dolt versioned SQL, Freebuff canonical memory

### Community 2 - "Clients and Interfaces"
Cohesion: 0.4
Nodes (5): AMD Radeon 780M, llama.cpp native path, Localhost-only boundary, Post-restart runtime state, Unsloth training server

### Community 3 - "Runtime Gaps"
Cohesion: 0.4
Nodes (5): C: to D: migration, ComfyUI, D: AI and Docker drive, LM Studio, Rollback copies

## Ambiguous Edges - Review These
- `AnythingLLM workspace` → `Freebuff canonical memory`  [AMBIGUOUS]
  03-current-state-and-gaps.md · relation: conceptually_related_to

## Knowledge Gaps
- **7 isolated node(s):** `Docker Compose recipe`, `Dolt versioned SQL`, `llama.cpp native path`, `ComfyUI`, `LM Studio` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `AnythingLLM workspace` and `Freebuff canonical memory`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Docker Desktop` connect `D-Drive Storage` to `Shared AI Services`, `Clients and Interfaces`?**
  _High betweenness centrality (0.513) - this node is a cross-community bridge._
- **Why does `D: AI and Docker drive` connect `Runtime Gaps` to `Shared AI Services`, `Clients and Interfaces`?**
  _High betweenness centrality (0.371) - this node is a cross-community bridge._
- **Why does `Unsloth training server` connect `Clients and Interfaces` to `Runtime Gaps`?**
  _High betweenness centrality (0.335) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `LiteLLM model gateway` (e.g. with `AnythingLLM workspace` and `n8n automation`) actually correct?**
  _`LiteLLM model gateway` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `AnythingLLM workspace` (e.g. with `LiteLLM model gateway` and `ChromaDB vector store`) actually correct?**
  _`AnythingLLM workspace` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Docker Compose recipe`, `Dolt versioned SQL`, `llama.cpp native path` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._