# AI system cheat sheet

**For:** Kevin or a new operator  
**Status snapshot:** 2026-08-19  
**Canonical overview:** [EXECUTIVE_HANDOFF.md](EXECUTIVE_HANDOFF.md)

## One-sentence explanation

This is a local-first AI control room: Freebuff is the operator/chat layer, IJFW is compact working memory, Docker hosts the shared AI services, D: stores the heavy AI/Docker data, and receipts/graphs/dashboards make the work inspectable.

## Open these first

1. [Executive handoff](EXECUTIVE_HANDOFF.md) — complete human and operator orientation.
2. [Clickable HTML cheat sheet](HARNESS_CHEATSHEET.html) — quick navigation.
3. [Browser slide deck](HARNESS_SYSTEM_SLIDES.html) — visual explanation.
4. [AI/Docker interactive graph](ai-system-explainer/graphify-out/graph.html) — relationships and evidence tags.
5. [Main harness dashboard](.state/dash.html) — sessions, goals, and tasks.
6. [Latest IJFW handoff](freebuff-memory/ijfw/memory/handoff.md) — what the next chat should know.

## What to use for what

| If you want to… | Open/use | Plain-language meaning |
|---|---|---|
| Chat with a local model | [Open WebUI](http://127.0.0.1:8080) | Browser front end for the shared Ollama server |
| Call a model from code | [LiteLLM](http://127.0.0.1:4000) | One API gateway that routes requests to local or cloud models |
| Browse a workspace or RAG collection | [AnythingLLM](http://127.0.0.1:3001) | Document/workspace interface; full memory round trip is still open |
| Build automations | [n8n](http://127.0.0.1:5678) | Visual workflow runner |
| Train or prepare models | [Unsloth Studio](http://127.0.0.1:8888) | D-backed training/data server; currently native fallback, localhost only |
| Inspect the model API | [Ollama API](http://127.0.0.1:11434) | Shared local model server used by LiteLLM and Open WebUI |
| Inspect vector storage | [ChromaDB](http://127.0.0.1:8000) | Vector-search service; no human dashboard is assumed |
| Inspect versioned SQL data | `127.0.0.1:3307` | Dolt SQL server; connect with a SQL client |
| Continue another agent’s work | [IJFW handoff](freebuff-memory/ijfw/memory/handoff.md) | Compact cross-chat context |

All service links are local to this computer. The Compose ports are bound to `127.0.0.1`; they are not LAN-accessible by default.

## Current verified state

As of this snapshot:

- Docker Desktop is running from `D:\Docker\Docker\Docker Desktop.exe`.
- The seven normal Compose services are running: n8n, Dolt, ChromaDB, AnythingLLM, LiteLLM, Ollama, and Open WebUI.
- Open WebUI, Ollama, LiteLLM, and AnythingLLM returned HTTP 200.
- Ollama listed models from the D-backed Docker store.
- A real LiteLLM request through `local-qwen` returned `FINAL_DOC_CHECK`.
- Native D-backed Unsloth is healthy at `127.0.0.1:8888`.
- The official Docker Unsloth profile is configured but is not the current Unsloth runtime; do not start it while native Unsloth owns port 8888.

The current status is “running and verified now,” not “guaranteed after every reboot.” Re-run the health commands below after a restart.

## Start and verify

Start the normal server room:

```powershell
Start-Process 'D:\Docker\Docker\Docker Desktop.exe'
Set-Location D:\Docker\stack
docker compose up -d
docker compose ps
```

Check the main endpoints:

```powershell
Invoke-WebRequest http://127.0.0.1:8080
Invoke-WebRequest http://127.0.0.1:11434/api/tags
Invoke-WebRequest http://127.0.0.1:4000/health/liveliness
Invoke-WebRequest http://127.0.0.1:3001
Invoke-WebRequest http://127.0.0.1:8888/api/health
```

Start the current native Unsloth fallback only if it is not already running:

```powershell
$u = 'D:\AI\data\Unsloth\studio\bin\unsloth.exe'
Start-Process $u -ArgumentList 'studio','-H','127.0.0.1','-p','8888' -WorkingDirectory 'D:\AI\data\Unsloth\studio'
```

Stop it with:

```powershell
& 'D:\AI\data\Unsloth\studio\bin\unsloth.exe' studio stop
```

Do not run native Unsloth and the Docker Unsloth profile at the same time. They both claim port 8888.

## Where the heavy data lives

| Category | Canonical/current location | Notes |
|---|---|---|
| Docker Compose project | [D:\Docker\stack](D:/Docker/stack) | Runtime authority; live `docker-compose.yml` is private/ignored |
| Docker volumes | [D:\Docker\volumes](D:/Docker/volumes) | Persistent service data and canonical Ollama models |
| AI applications | [D:\AI\apps](D:/AI/apps) | Ollama, AnythingLLM, LM Studio, ComfyUI, Anaconda3 |
| AI data | [D:\AI\data](D:/AI/data) | App data, model stores, Unsloth work, and retained native stores |
| AI cache | [D:\AI\cache](D:/AI/cache) | Hugging Face and related caches |
| Rollback copies | [D:\AI\rollback\20260818-193645](D:/AI/rollback/20260818-193645) | Retained until the new runtime is accepted |

The inactive `D:\AI\data\Ollama` copy is retained for rollback and is not the active Docker model store. It is a later cleanup candidate, not something to delete casually.

## Runtime code and configuration

### Current D-backed Compose stack

- [Live Compose file](D:/Docker/stack/docker-compose.yml) — seven normal services plus opt-in Unsloth profile. Do not publish its private `.env` companion.
- [Safe Compose example](D:/Docker/stack/docker-compose.example.yml) — shareable template.
- [LiteLLM routing](D:/Docker/stack/litellm-config.yaml) — local Qwen route and configured provider routes.
- [Server-first operating guide](D:/Docker/stack/SERVER-FIRST-AI.md) — start/stop, endpoints, ownership, and safety rules.
- [Unsloth environment template](D:/Docker/stack/unsloth.env.example) — safe variable names only.
- [Dolt schema](D:/Docker/stack/dolt/memory_schema.sql) — versioned SQL memory schema.
- [n8n memory workflow](D:/Docker/stack/n8n/memory-loop-ingest.workflow.json) — workflow artifact.
- [Stack README](D:/Docker/stack/README.md) — background/reference; prefer the server-first guide for current runtime behavior.

### Migration and rollback code

- [relocate-ai-docker.ps1](relocate-ai-docker.ps1) — dry-run/execute migration with verified copies and junctions.
- [move-ai-rollback-to-d.ps1](move-ai-rollback-to-d.ps1) — moves retained rollback material to D:.
- [move-remaining-ai-rollback-to-d.ps1](move-remaining-ai-rollback-to-d.ps1) — completes rollback relocation.
- [Migration receipt](AI-SERVER-MIGRATION-RECEIPT-2026-08-18.md) — what moved, what was verified, and what remains retained.
- [C: to D: migration plan](C-DRIVE-AI-DOCKER-MIGRATION-PLAN-2026-08-18.md) — source/destination map and execution gates.

### Harness, memory, and continuity code

- [Freebuff bridge](freebuff-memory/scripts/freebuff_bridge.py) — list threads, inspect a thread, render explicit transcripts, publish sanitized handoffs.
- [IJFW verifier](freebuff-memory/scripts/verify.ps1) — transport and canary checks.
- [Bridge tests](freebuff-memory/tests/test_freebuff_bridge.py) — automated bridge coverage; last verified 3/3.
- [Memory policy](freebuff-memory/MEMORY_POLICY.md) — what belongs in durable memory.
- [Memory README](freebuff-memory/README.md) — setup and operating contract.
- [Memory-loop CLI](dotmd/memory-loop/memory.py) — semantic-memory prototype.
- [Memory MCP server](dotmd/memory-loop/mcp_server.py) — prototype MCP interface.
- [Memory specification](dotmd/memory-loop/MEMORY_SPEC.md) — entry format.
- [Memory setup notes](dotmd/memory-loop/SETUP.md) — prototype setup.

### Dashboards, graphs, and generators

- [Dashboard generator](.state/gen_dash.py) → [main dashboard](.state/dash.html).
- [Project board generator](.state/gen_projects_dash.py) → [project board](.state/projects/index.html).
- [KISS generator](.state/kiss/gen_kiss.py) → [KISS surface](.state/kiss/index.html) and [slides](.state/kiss/slides.html).
- [KISS bridge](.state/kiss/bridge.py) — queues, drafts, and commits bridge.
- [AI graph builder](ai-system-explainer/build_graph.py) → [interactive graph](ai-system-explainer/graphify-out/graph.html) and [graph report](ai-system-explainer/graphify-out/GRAPH_REPORT.md).
- [Graph facts](ai-system-explainer/AI-SYSTEM-EXTRACTION.json) — curated facts and explicitly tagged relationships.
- [Broad harness graph](dotmd/graphify-out/graph.html) — wider ecosystem map.

## What was done in this work

1. Inspected the existing harness instead of treating previous plans as proof.
2. Separated raw chat evidence, IJFW memory, `.state` operations, Docker services, and project outputs.
3. Migrated the major AI/Docker payload from C: to D: with verified copies, junctions, and rollback retention.
4. Made Docker Ollama the server authority and routed LiteLLM/Open WebUI through it.
5. Kept Unsloth available as a D-backed localhost server while the Docker GPU path remains unproven.
6. Restarted the server room after the Freebuff restart and re-ran endpoint and real-inference checks.
7. Built a curated graph and beginner documentation with `VERIFIED`, `CONFIGURED`, `INFERRED`, and `OPEN` labels.
8. Produced this handoff, the HTML cheat sheet, the visual slide deck, and the detailed explainer set.

## Known gaps and safe next decisions

- AnythingLLM’s full document → embedding → retrieval → answer round trip is not yet proven as the canonical memory backend.
- ComfyUI is on D: but is not yet a shared server endpoint.
- The duplicate native Ollama store remains retained until rollback is explicitly accepted.
- Dockerized Unsloth needs a successful image pull and host-specific GPU validation before replacing native Unsloth.
- All endpoints are localhost-only. LAN access requires authentication and firewall review.
- There is no single live “Harness Home” page combining health, current threads, latest handoff, receipts, and blockers.

## Glossary

- **Container:** a packaged service process managed by Docker.
- **Compose:** the recipe that starts the related containers together.
- **Model server:** a process such as Ollama that loads and serves models.
- **Gateway:** LiteLLM; callers use one API while it chooses the backend.
- **RAG:** retrieval-augmented generation; a system finds relevant documents before asking a model to answer.
- **Junction:** a Windows filesystem link that lets software keep its old C: path while the data physically lives on D:.
- **Receipt:** a dated record of actions and verification, including what was not proven.

## If something is broken

Start with `docker compose ps`, then check the endpoint table. If Docker is unavailable, open Docker Desktop and wait for the daemon before changing files. If Unsloth is unavailable, check whether another process owns port 8888. Do not delete rollback data, model stores, or `.env` files as a first troubleshooting step.

