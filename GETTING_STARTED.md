# Getting Started

"I just cloned this repo. What do I do?"

---

## Prerequisites

- Windows 10/11
- Docker Desktop installed and running
- Python 3.x installed
- Git installed
- 500GB SSD mounted as D:

---

## Step 1: Clone and orient

```powershell
git clone https://github.com/shitty-shit/shitty-system.git
cd shitty-system
```

Read these in order:
1. **README.md** — the 60-second overview
2. **ARCHITECTURE.md** — how everything connects
3. **This file** — what to do right now

---

## Step 2: Start the Docker services

```powershell
cd docker-stack

# Copy the example env file and fill in any needed keys
cp .env.example .env
# Edit .env if you need cloud model API keys

# Start everything
docker compose up -d

# Verify all 7 services are running
docker compose ps
```

You should see:
| Container | Status | Port |
|---|---|---|
| shitty-ollama | running | 11434 |
| shitty-litellm | running | 4000 |
| shitty-anythingllm | running | 3001 |
| shitty-n8n | running | 5678 |
| shitty-chroma | running | 8000 |
| shitty-dolt | running | 3307 |
| shitty-openwebui | running | 8080 |

---

## Step 3: Health check

Run these quick checks to verify services are alive:

```powershell
# Ollama — should list models
curl http://127.0.0.1:11434/api/tags

# LiteLLM — should return healthy
curl http://127.0.0.1:4000/health

# AnythingLLM — should return system info
curl http://127.0.0.1:3001/api/v1/system

# n8n — should return the web UI
curl -o /dev/null -s -w "%{http_code}" http://127.0.0.1:5678

# ChromaDB — should return heartbeat
curl http://127.0.0.1:8000/api/v1/heartbeat

# Open WebUI — should return the web UI
curl -o /dev/null -s -w "%{http_code}" http://127.0.0.1:8080
```

**Important:** A green container list is not enough. You need at least one real model request to prove inference works. Try:

```powershell
# Test Ollama inference
curl http://127.0.0.1:11434/api/generate -d '{"model":"qwen2.5:3b","prompt":"Say hello","stream":false}'

# Test LiteLLM gateway (if configured)
curl http://127.0.0.1:4000/v1/chat/completions -d '{"model":"local-qwen","messages":[{"role":"user","content":"Hello"}]}'
```

---

## Step 4: Explore the harness

The harness is the agent workbench — scripts, dashboards, memory, and documentation.

```powershell
cd ../harness

# Open the clickable cheat sheet
Start-Process HARNESS_CHEATSHEET.html

# Open the system slides
Start-Process HARNESS_SYSTEM_SLIDES.html

# Read the executive handoff (the complete index)
cat EXECUTIVE_HANDOFF.md
```

---

## Step 5: Check memory and continuity

```powershell
# List all Freebuff chat threads
python freebuff-memory/scripts/freebuff_bridge.py threads

# Run the memory verification script
powershell -ExecutionPolicy Bypass -File freebuff-memory/scripts/verify.ps1

# Run the bridge tests
cd freebuff-memory
python -m pytest tests/ -v
```

---

## Step 6: Explore the One Store

If you have access to the D: drive:

```powershell
# Browse the canonical knowledge base
cd D:\SHITTYSHIT

# Read the agent entry contract
cat AGENTS.md

# See what's in the registry
cat 00_MASTER/REGISTRY.md

# Browse the wiki
cat 00_MASTER/wiki/index.md

# Check conversation threads
cat 00_MASTER/conversations/INDEX.md
```

---

## What to read next

| If you want to... | Read |
|---|---|
| Understand the full architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Know what all the repos do | [REPOS.md](REPOS.md) |
| Manage Docker services | [SERVICES.md](SERVICES.md) |
| Understand how memory works | [MEMORY.md](MEMORY.md) |
| Get the complete system index | `harness/EXECUTIVE_HANDOFF.md` |
| See the visual overview | `harness/HARNESS_SYSTEM_SLIDES.html` |
| Get the clickable cheat sheet | `harness/HARNESS_CHEATSHEET.html` |

---

## Common tasks

### Refresh the dashboard
```powershell
cd harness/.state
python gen_dash.py
python gen_projects_dash.py
Start-Process dash.html
```

### Restart Docker services
```powershell
cd D:\Docker\stack
docker compose down
docker compose up -d
docker compose ps
# Then test one real inference request
```

### Export a chat thread
```powershell
cd harness
python freebuff-memory/scripts/freebuff_bridge.py transcript --thread-id <uuid> --output export.md
```

### Build a knowledge graph
```powershell
cd harness/ai-system-explainer
python build_graph.py
# Output: graphify-out/graph.html
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Docker services won't start | Make sure Docker Desktop is running. Check `docker compose ps` |
| Ollama returns nothing | Check if Ollama is running natively AND in Docker — they can't both use port 11434 |
| LiteLLM can't reach Ollama | LiteLLM uses `host.docker.internal:11434` for native Ollama |
| Bridge tests fail | Make sure the Freebuff SQLite database exists at the expected path |
| Dashboard is stale | Run `python gen_dash.py` to regenerate |
| AnythingLLM memory not working | This is a known open item — the memory round-trip isn't fully proven yet |
