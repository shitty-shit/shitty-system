# Shitty System

**The operating system for a local-first AI agent stack.**

This repo is the front door to a 500GB AI workbench built on Windows: Docker services, local models, agent memory, knowledge graphs, and multi-agent coordination — all running on one machine, all under your control.

---

## What is this?

A control room for AI agents. Not a cloud platform. Not a SaaS product. A local system where:

- **Freebuff** chat agents do the work
- **Docker** runs 7 services (Ollama, LiteLLM, AnythingLLM, n8n, ChromaDB, Dolt, Open WebUI)
- **IJFW** memory keeps conversations alive across sessions
- **One Store** (`D:\SHITTYSHIT`) is the canonical knowledge base
- **KISS Deck** is the visual agent dashboard
- **D:** is the 500GB SSD that holds everything that matters

---

## System at a glance

```
┌─────────────────────────────────────────────────────┐
│                    KEVIN / USER                      │
└──────────────────────┬──────────────────────────────┘
                       │
              ┌────────▼────────┐
              │   FREEBUFF      │  Chat windows (agents do work here)
              │   CHATS         │
              └───┬────────┬────┘
                  │        │
         ┌────────▼──┐  ┌──▼──────────┐
         │ RAW DB    │  │ IJFW        │  Memory across sessions
         │ (SQLite)  │  │ (handoff,   │
         │           │  │  knowledge) │
         └─────┬─────┘  └──────┬──────┘
               │               │
         ┌─────▼───────────────▼──────┐
         │        .STATE              │  Dashboards, tasks, sessions
         │  (dash.html, KISS deck)    │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │     DOCKER SERVICES       │  Local AI service room
         │  Ollama · LiteLLM · n8n   │
         │  AnythingLLM · ChromaDB   │
         │  Dolt · Open WebUI        │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │    D: DRIVE (500GB SSD)   │  Models, data, volumes
         │  Docker · AI · repos      │
         └───────────────────────────┘
```

---

## Docs

| Document | What it covers |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Full system diagram, layer explanations, how everything connects |
| [GETTING_STARTED.md](GETTING_STARTED.md) | "I just cloned this — what do I do first?" |
| [REPOS.md](REPOS.md) | Catalog of all 30+ repos in the system |
| [SERVICES.md](SERVICES.md) | Docker service map, ports, health checks, management |
| [MEMORY.md](MEMORY.md) | How memory and continuity work across sessions |

---

## The D: drive layout

```
D:\
├── SHITTYSHIT/          # One Store — canonical knowledge base (github.com/shitty-shit/shittyshit)
├── SHITTY_GIT/          # 28 cloned repos — tools, skills, frameworks
├── Docker/
│   ├── stack/           # Compose + config (github.com/shitty-shit/docker-stack)
│   ├── volumes/         # Service data (Ollama models, n8n workflows, etc.)
│   └── wsl-data/        # WSL2 backing image
├── AI/
│   ├── apps/            # Installs (Ollama, AnythingLLM, ComfyUI, LM Studio)
│   ├── data/            # Model data, caches
│   ├── config/          # App configs
│   ├── cache/           # HuggingFace, pip, etc.
│   └── rollback/        # Backup copies from C:→D: migration
└── KISS_STFU_WRITE_GSD_MASTER.md  # Master spec for the KISS deck
```

---

## Key repos

| Repo | What it is | Link |
|---|---|---|
| **shitty-system** (this repo) | The map — docs, harness code, Docker config | [shitty-shit/shitty-system](https://github.com/shitty-shit/shitty-system) |
| **shittyshit** | One Store — memory, wiki, conversations, registry | [shitty-shit/shittyshit](https://github.com/shitty-shit/shittyshit) |
| **docker-stack** | Service room config (compose, litellm, env) | [shitty-shit/docker-stack](https://github.com/shitty-shit/docker-stack) |

See [REPOS.md](REPOS.md) for the full catalog of 30+ repos.

---

## Quick start

```powershell
# 1. Clone this repo
git clone https://github.com/shitty-shit/shitty-system.git
cd shitty-system

# 2. Start the Docker services
cd docker-stack
docker compose up -d
docker compose ps

# 3. Open the harness docs
Start-Process ../harness/HARNESS_CHEATSHEET.html

# 4. Check service health
curl http://127.0.0.1:11434/api/tags     # Ollama
curl http://127.0.0.1:4000/health         # LiteLLM
curl http://127.0.0.1:3001/api/v1/system  # AnythingLLM
```

See [GETTING_STARTED.md](GETTING_STARTED.md) for the full orientation.

---

## Status

This system is real and running. It has:

- ✅ Working Docker service room (7 services on localhost)
- ✅ Agent memory bridge (Freebuff → IJFW → One Store)
- ✅ KISS Deck agent dashboard with drag-and-drop cubes
- ✅ Writer mode (STFU+WRITE) for drafting and critique
- ✅ Knowledge graphs from documentation
- ✅ Project boards, dashboards, session tracking
- ✅ 28 cloned tool repos under the shitty-shit org

What's still open:

- ⚠️ AnythingLLM memory round-trip not fully proven
- ⚠️ Obsidian sync not confirmed
- ⚠️ Need to prove Docker services survive restarts

---

## License

This is Kevin's system. Use it, learn from it, fork it. Just don't push secrets to GitHub.
