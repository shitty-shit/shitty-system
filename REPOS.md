# Repos

Every repo in the shitty system — what it is, where it lives, and whether it's original work or a fork.

All repos live under the **shitty-shit** GitHub organization: `github.com/shitty-shit/`

---

## Core System

These are the repos that make the system run.

| Repo | What it is | Commits | Status |
|---|---|---|---|
| **[shitty-system](https://github.com/shitty-shit/shitty-system)** | This repo — the map, docs, harness code, Docker config | — | Active |
| **[shittyshit](https://github.com/shitty-shit/shittyshit)** | One Store — canonical memory, wiki, conversations, registry | 9 | Active |
| **[docker-stack](https://github.com/shitty-shit/docker-stack)** | Docker Compose config for 7 AI services | 2 | Active |

### The Harness (in this repo)

The harness code lives in `harness/` within this repo. It includes:
- **freebuff-memory/** — IJFW memory engine, read-only bridge, tests
- **.state/** — Dashboards, KISS deck, project board, session tracking
- **ai-system-explainer/** — Knowledge graphs, plain-language docs
- **dotmd/** — LiteLLM setup, memory-loop prototype, skills reference

---

## AI Models and Infrastructure

Tools for running, serving, and fine-tuning local models.

| Repo | What it is | Commits | Type |
|---|---|---|---|
| **[litellm](https://github.com/shitty-shit/litellm)** | Unified LLM proxy — one API for all models | 36,196 | Fork |
| **[llama.cpp](https://github.com/shitty-shit/llama.cpp)** | C++ inference engine for local models | 8,826 | Fork |
| **[unsloth](https://github.com/shitty-shit/unsloth)** | Fine-tuning and model training | 4,890 | Fork |
| **[langchain](https://github.com/shitty-shit/langchain)** | LLM application framework | 15,694 | Fork |
| **[langgraph](https://github.com/shitty-shit/langgraph)** | Agent orchestration graphs | 6,719 | Fork |

---

## Agent Frameworks

Tools for building and coordinating AI agents.

| Repo | What it is | Commits | Type |
|---|---|---|---|
| **[agentic-stack](https://github.com/shitty-shit/agentic-stack)** | Agent platform with antigravity adapter + episodic logging | 54 | Original |
| **[get-shit-done](https://github.com/shitty-shit/get-shit-done)** | Agent task execution framework — phases, state, transitions | 1,077 | Original |
| **[hermes-agent](https://github.com/shitty-shit/hermes-agent)** | Hermes agent implementation | 3,612 | Original |
| **[hermes-agent-orange-book](https://github.com/shitty-shit/hermes-agent-orange-book)** | Hermes agent documentation and comparisons | 9 | Original |
| **[multica](https://github.com/shitty-shit/multica)** | Multi-agent coordination | 2,082 | Original |

---

## Skills and Tools

Reusable capabilities that agents can load.

| Repo | What it is | Commits | Type |
|---|---|---|---|
| **[graphify](https://github.com/shitty-shit/graphify)** | Turns documentation into navigable knowledge graphs | 137 | Original |
| **[caveman](https://github.com/shitty-shit/caveman)** | Multi-mode agent skill with intensity levels | 111 | Original |
| **[superpowers](https://github.com/shitty-shit/superpowers)** | Agent delegation and brainstorm skills | 355 | Original |
| **[last30days-skill](https://github.com/shitty-shit/last30days-skill)** | Content aggregation (YouTube, Reddit, Bluesky, etc.) | 265 | Original |
| **[obsidian-skills](https://github.com/shitty-shit/obsidian-skills)** | Obsidian integration skills | 35 | Fork |
| **[firecrawl](https://github.com/shitty-shit/firecrawl)** | Web scraping and crawling | 5,090 | Fork |
| **[n8n-mcp](https://github.com/shitty-shit/n8n-mcp)** | n8n MCP server integration | 926 | Fork |
| **[git-skill](https://github.com/shitty-shit/git-skill)** | Git operations skill | — | Original |

---

## Applications

Built applications and user-facing tools.

| Repo | What it is | Commits | Type |
|---|---|---|---|
| **[OpenJarvis](https://github.com/shitty-shit/OpenJarvis)** | Self-hosted AI assistant | 112 | Original |
| **[DeepTutor](https://github.com/shitty-shit/DeepTutor)** | AI tutoring system | 477 | Original |
| **[OpenDocs](https://github.com/shitty-shit/OpenDocs)** | Codebase analyzer + documentation generator | 29 | Original |
| **[VoxCPM](https://github.com/shitty-shit/VoxCPM)** | Voice synthesis | 117 | Original |
| **[nodepad](https://github.com/shitty-shit/nodepad)** | Web app with source citations | 61 | Fork |
| **[turboquant_plus](https://github.com/shitty-shit/turboquant_plus)** | Quant/trading tooling | 225 | Original |

---

## Reference and Learning

Cloned repos kept for reference, learning, and skill development.

| Repo | What it is | Commits | Type |
|---|---|---|---|
| **[andrej-karpathy-skills](https://github.com/shitty-shit/andrej-karpathy-skills)** | Karpathy's skill patterns | 27 | Fork |
| **[API-mega-list](https://github.com/shitty-shit/API-mega-list)** | Comprehensive API directory | 31 | Fork |
| **[SYSBuild](https://github.com/shitty-shit/SYSBuild)** | Shared agent brain architecture | 3 | Original |
| **[self-hosted](https://github.com/shitty-shit/self-hosted)** | Self-hosted services reference | 100 | Fork |
| **[Windows-MCP](https://github.com/shitty-shit/Windows-MCP)** | Windows MCP server | 456 | Fork |

---

## Repo statistics

- **Total repos:** 30 (including this one)
- **Original repos:** 18
- **Forks:** 12
- **Total commits across all repos:** ~90,000+

---

## How repos relate to the system

```
shitty-system (this repo)
├── harness/          → Agent workbench, memory, dashboards
├── docker-stack/     → Service room config
└── docs/             → Architecture, getting started, service map

shittyshit            → One Store (canonical knowledge base)
docker-stack          → Docker Compose (service config)

SHITTY_GIT/           → 28 cloned repos (tools, skills, frameworks)
├── agentic-stack     → Agent platform
├── graphify          → Knowledge graph builder
├── get-shit-done     → Task execution
├── hermes-agent      → Agent implementation
├── litellm           → Model gateway
├── llama.cpp         → Local inference
└── ...               → 22 more repos
```

---

## Adding new repos

When you clone or create a new repo:

1. Clone it to `D:\SHITTY_GIT\<repo-name>`
2. Set the remote to `https://github.com/shitty-shit/<repo-name>.git`
3. Add a one-liner to this file
4. If it's a core system component, also update `README.md`
