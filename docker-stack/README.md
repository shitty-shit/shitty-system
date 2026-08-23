# LACES_CASES Docker Stack (Railroad Tracks)

Grounded in `Desktop/dotmd/toolstack.md` v2.2 + Strategic Deployment Blueprint
Phase 1. All data on the 500GB SSD.

## Services

| Service | Port | Role | Data |
|---|---|---|---|
| n8n | 5678 | Workflow orchestrator (Inference Gate) | `D:\Docker\volumes\n8n` |
| Dolt | 3307 | Versioned SQL registry (git-like) | `D:\Docker\volumes\dolt` |
| ChromaDB | 8000 | Vector store (context/RAG) | `D:\Docker\volumes\chroma` |
| AnythingLLM | 3001 | Workspace hub, agents, MCP | `D:\Docker\volumes\anythingllm` |
| LiteLLM | 4000 | Unified model proxy | `D:\Docker\volumes\litellm` |

Note: AnythingLLM is on 3001 because 3000 is taken (PID 1384).

## Manage

```bash
docker compose up -d     # start
docker compose down      # stop
docker compose logs -f n8n
docker compose ps
```

## Native (NOT in this stack)

- **llama.cpp** — Blueprint lock: native build, Qwen2.5-3B Q4_K_M, AMD 780M iGPU, Vulkan, port 8080.
- **Ollama** — run native for GPU access; LiteLLM reaches it at `host.docker.internal:11434`.

## Roadmap

- Tier 2: self-hosted Supabase (pgvector) as OB1/Open Brain memory substrate.
- Add real keys to `.env` for cloud models.
