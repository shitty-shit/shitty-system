# System Inventory — Complete Machine Audit

> Generated: 2026-09-01 by Buffy

---

## 🐳 DOCKER DIAGNOSTIC: Gordon / Docker AI

### Status: ✅ WORKING (with one cosmetic warning)

**Docker Desktop 4.88.1 (237512)** — installed on **D:\Docker\Docker\** (not C: drive).

### The "Gordon failing" issue

Gordon (`docker ai`) is **functional right now**. The recurring `[W] Backend installation failed for: not implemented` in the inference log is **expected** — it's the **vLLM backend** which is Linux-only/GPU-only and simply doesn't exist on Windows. It's a cosmetic warning, not a failure.

**Evidence it works:**
- `docker ai` starts and makes tool calls (tested live)
- Docker Model Runner responds on `http://127.0.0.1:12434`
- Models list successfully: `gemma3-qat` (3.88B), `gemma4`, `granite-docling:258M-Q8_0`
- The llama.cpp backend (`com.docker.llama-server.exe`) is installed at `D:\Docker\Docker\resources\model-runner\bin\`

### What actually happens on startup

Every Docker Desktop restart triggers this sequence in `inference.log`:
1. `Successfully initialized store` ✅
2. `3 backends available` ✅ (llama.cpp, vllm, and OpenAI-compatible)
3. `Backend installation failed for: not implemented` ⚠️ (vllm — expected on Windows)
4. Models list successfully ✅

### How to use Gordon

```bash
# Interactive — opens a REPL
docker ai

# Pipe a question (auto-approves tool calls)
echo "list running containers" | docker ai

# If it asks for confirmation, type: a (for "all" auto-approve)
```

### Docker Settings (key flags)
- `EnableDockerAI: true`
- `EnableInference: true`
- `enableInferenceTCPPort: 12434`
- `enableInferenceGPUVariant: false` (CPU only — correct for AMD 780M iGPU)
- `wslEngineEnabled: true`

### WSL Distros
| Distro | State |
|---|---|
| Ubuntu | Stopped |
| docker-desktop | Running |
| podman-machine-default | Running |
| superagent | Running |

---

## 🖥️ C: DRIVE — Installed Programs

### Program Files (notable)
| Category | Apps |
|---|---|
| **AI/ML** | Docker, Dolt, Qwen, LM Studio, BLACKBOXAI, Locally Uncensored, Neo, Perplexity, Voicebox, EchoWrite |
| **IDEs/Editors** | JetBrains, Sublime Text, Sublime Merge, Alacritty, DB Browser for SQLite, TablePlus |
| **Dev Tools** | Git, GitHub CLI, Go, CMake, MSBuild, .NET, Visual Studio, nodejs |
| **Productivity** | Obsidian, LibreOffice, Dropbox, IrfanView, Brave, Firefox, Thunderbird, Notion, Linear |
| **Creative** | Adobe, darktable, Scribus 1.6.6, AionUi |
| **Security/Network** | Tailscale, OnionShare, Malwarebytes, UrbanVPN, TAP-Windows |
| **Communication** | Ace, Meta Horizon, DingTalklite |
| **Automation** | UiPath Platform, RUXIM |
| **System** | Rainmeter, LocalSend, HP drivers, AMD, Intel, Logi Options+ |

### AppData/Local/Programs (user-level installs)
| App | Type |
|---|---|
| **@codebufffreebuff-desktop** | Freebuff — the agent interface |
| **@openworkdesktop** | OpenWork |
| **@freestyleelectron** | Freestyle |
| **@granolaelectron** | Granola |
| **@multicadesktop** | Multica |
| **@accomplishdesktop** | Accomplish |
| **@runabledesktop** | Runable |
| **Antigravity / Antigravity IDE** | Custom dev tools |
| **AnythingLLM** | Desktop client for AnythingLLM Docker |
| **Cherry Studio** | AI chat studio |
| **ComfyUI** | Stable Diffusion workflow UI |
| **Devin** | AI coding agent |
| **Kiro** | AI IDE |
| **LM Studio** | Local model runner |
| **Ollama** | Local model runner (native, also in Docker) |
| **OpenCode** | Code editor |
| **Warp** | Terminal |
| **Zed** | Editor |
| **Podman / Podman Desktop** | Alternative container runtime |
| **a0-launcher** | Agent Zero Launcher |
| **anytype** | Note-taking / knowledge base |
| **Bionic** | Custom app |
| **Bloome** | Custom app |
| **Gamut** | Custom app |
| **HulyDesktop** | Project management |
| **Nimbalyst** | Custom app |
| **Verdent** | Custom app |
| **ZCode** | Custom app |
| **Python 3.12** | Python runtime |

### Startup Programs
- Google Drive File Stream
- AMD Noise Suppression
- Ollama (auto-start)
- Pieces for Developers
- Rainmeter
- Figma Agent
- Discord
- Notion
- Perplexity
- Ace
- OneDrive

---

## 💾 D: DRIVE — The 500GB System

### Top-Level Layout
```
D:\
├── AI/                  # AI app data, models, caches
│   ├── apps/            # Anaconda3, AnythingLLM, ComfyUI, LM Studio, Ollama
│   ├── cache/
│   ├── config/
│   ├── data/
│   └── rollback/
├── Antgravity_500/      # Antigravity agent workspace
├── Docker/              # Docker Desktop install + all service volumes
│   ├── Docker/          # Docker Desktop binary install
│   ├── stack/           # docker-compose.yml + configs
│   ├── volumes/         # Persistent data for all services
│   └── wsl-data/        # WSL VM data
├── DockerWSL/           # WSL Docker storage
├── Downloads/
├── ox-alpha/            # Ox agent workspace (with .agent, .memory, skills)
├── SHITTY_GIT/          # 28 git repos (clones/forks under shitty-shit org)
├── SHITTYSHIT/          # The One Store (knowledge base)
└── SHITTY_SYSTEM/       # This repo — the system front door
```

### Docker Services (all running)
| Service | Container | Port | Image | Health |
|---|---|---|---|---|
| **n8n** (orchestrator) | shitty-n8n | 5678 | n8nio/n8n:latest | ✅ Up 5h |
| **Dolt** (versioned SQL) | shitty-dolt | 3307 | dolthub/dolt-sql-server:latest | ✅ Up 5h |
| **ChromaDB** (vector store) | shitty-chroma | 8000 | chromadb/chroma:latest | ✅ Up 5h |
| **AnythingLLM** (workspace hub) | shitty-anythingllm | 3001 | mintplexlabs/anythingllm:latest | ✅ Healthy |
| **LiteLLM** (model proxy) | shitty-litellm | 4000 | ghcr.io/berriai/litellm:main-stable | ✅ Up 5h |
| **Ollama** (model server) | shitty-ollama | 11434 | ollama/ollama:latest | ✅ Up 5h |
| **Open WebUI** (chat UI) | shitty-openwebui | 8080 | ghcr.io/open-webui/open-webui:main | ✅ Healthy |

### Docker Model Runner Models
| Model | Parameters | Size |
|---|---|---|
| gemma3-qat | 3.88B (Q4_K_M) | 2.36 GiB |
| gemma4 | — | — |
| granite-docling:258M-Q8_0 | 164M (Q8_0) | 166.28 MiB |

### Ollama Models (Docker)
| Model | Size | Type |
|---|---|---|
| qwen3.6:27b | 17 GB | Local |
| deepseek-r1:8b | 5.2 GB | Local |
| hermes-3-llama-3.1-8B-Q4_K_M | 4.9 GB | Local |
| mistral:latest | 4.4 GB | Local |
| gemma-3-4b-it-abliterated-Q4_K_M | 3.3 GB | Local |
| qwen3-abliterated:4b | 2.5 GB | Local |
| hermes-3-llama-3.2-3B-Q4_K_M | 2.0 GB | Local |
| llama3.2:latest | 2.0 GB | Local |
| qwen3-8B-abliterated-Q4_K_M | 5.0 GB | Local |
| nomic-embed-text:latest | 274 MB | Embeddings |
| qwen2.5:0.5b | 397 MB | Local |
| kimi-k2.7-code:cloud | — | Cloud |
| kimi-k2.6:cloud | — | Cloud |
| deepseek-v4-pro:cloud | — | Cloud |
| deepseek-v4-flash:cloud | — | Cloud |

### LiteLLM Configured Models
- `local-qwen` → Ollama
- `local-llamacpp` → llama.cpp
- `claude-sonnet` → API proxy
- `gpt-4o` → API proxy

---

## 📦 D: SHITTY_GIT — 28 Repos

All repos are cloned under `shitty-shit` GitHub org. Split into **original work** and **forked upstream**.

### Original Work (your repos)
| Repo | Purpose |
|---|---|
| **agentic-stack** | Core agentic framework |
| **API-mega-list** | Curated API list |
| **caveman** | Custom project |
| **DeepTutor** | AI tutoring system |
| **get-shit-done** | Task management |
| **graphify** | Knowledge graphs + visualizations |
| **hermes-agent** | Hermes AI agent |
| **hermes-agent-orange-book** | Hermes docs/guide |
| **ijfw** | IJFW memory system |
| **multica** | Multi-agent system |
| **n8n-mcp** | n8n MCP integration |
| **nodepad** | Note-taking tool |
| **OpenDocs** | Documentation system |
| **OpenJarvis** | Jarvis-style AI assistant |
| **obsidian-skills** | Obsidian integration skills |
| **self-hosted** | Self-hosting configs |
| **superpowers** | Extended capabilities |
| **SYSBuild** | System building tools |
| **turboquant_plus** | Quantitative analysis |
| **VoxCPM** | Voice synthesis |
| **Windows-MCP** | Windows MCP integration |

### Forked Upstream
| Repo | Origin |
|---|---|
| **andrej-karpathy-skills** | Fork of Karpathy's skills |
| **firecrawl** | Fork of Firecrawl |
| **langchain** | Fork of LangChain |
| **langgraph** | Fork of LangGraph |
| **last30days-skill** | Skill package |
| **litellm** | Fork of LiteLLM |
| **llama.cpp** | Fork of llama.cpp |
| **unsloth** | Fork of Unsloth |

---

## 🧠 Agent Workspaces on D:

### Antgravity_500 (`D:\Antgravity_500\`)
An agent workspace with:
- `core/` — Core logic
- `web/` — Web interface
- `bin/` — Scripts/executables
- `workflows/` — Automation workflows
- `writing_vault/` — Content storage
- Has its own `config.json` and `AGENTS.md`

### Ox-Alpha (`D:\ox-alpha\`)
Another agent workspace with:
- `.agent/` — Agent config
- `.memory/` — Memory persistence
- `skills/` — Installed skills
- `scripts/` — Automation
- `stack/` — Service configs
- `web/` — Web interface
- `yanks/` — Clipboard/snippet storage
- `docs/` — Documentation

---

## 🧠 The One Store (`D:\SHITTYSHIT\`)

The master knowledge base:
```
SHITTYSHIT/
├── 00_MASTER/     # Master index and cross-references
├── 01_SCHEMA/     # Data schemas and structures
├── 02_WORLD/      # World models and ontologies
├── AGENTS.md      # Agent instructions
└── index.md       # Entry point
```

---

## 🔌 Port Map

| Port | Service | Protocol |
|---|---|---|
| 2323 | Something (PID 4) | TCP |
| 3001 | AnythingLLM | HTTP |
| 3307 | Dolt SQL | MySQL |
| 4000 | LiteLLM | HTTP |
| 5678 | n8n | HTTP |
| 8000 | ChromaDB | HTTP |
| 8080 | Open WebUI | HTTP |
| 11434 | Ollama | HTTP |
| 12434 | Docker Model Runner | HTTP |

---

## 📊 Key Findings

1. **Docker is healthy** — all 7 services running, Model Runner active
2. **Gordon/Docker AI works** — the "vllm not implemented" warning is cosmetic
3. **Massive duplication** — Ollama runs both natively (C:) and in Docker (D:), plus LM Studio is installed too
4. **Two alternative runtimes** — Podman Desktop is also installed alongside Docker
5. **The system is sophisticated** — 28 repos, 7 Docker services, 3 WSL distros, 3 agent workspaces, and a full knowledge base
6. **Docker install is on D:** — at `D:\Docker\Docker\`, not the default C: location (saves C: drive space)
7. **WSL data on D:** — Docker WSL data is at `D:\Docker\wsl-data` (good — keeps the 500GB drive useful)
