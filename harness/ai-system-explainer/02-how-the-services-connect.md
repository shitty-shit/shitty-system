# How the pieces connect

## The normal request path

```text
Person or local app
        |
        v
Open WebUI :8080  ---->  Ollama :11434  ---->  local model files on D:
        |
        v
LiteLLM :4000  ---->  Ollama, optional cloud model routes, or future backends

n8n :5678  ---->  workflows that call the shared APIs
AnythingLLM :3001  ---->  workspace/RAG interface
ChromaDB :8000  ---->  vector search storage
Dolt :3307  ---->  versioned SQL registry

Unsloth :8888  ---->  training/fine-tuning and model-workbench service
```

## What each service does

| Service | Plain-language job | Current evidence |
|---|---|---|
| Docker Desktop | Runs isolated Linux-style services on Windows | `VERIFIED` running with seven localhost-bound Compose services on 2026-08-19 |
| Docker Compose | The repeatable recipe for the services | `VERIFIED` configuration file; validation passed previously |
| Ollama | Serves local language models over HTTP | `VERIFIED` HTTP 200 and model list returned on 2026-08-19 |
| LiteLLM | Presents one OpenAI-style API and routes model names | `VERIFIED` liveliness HTTP 200; current explainer records a real inference pass |
| Open WebUI | Browser chat interface | `VERIFIED` HTTP 200 on 2026-08-19 |
| AnythingLLM | Workspace and retrieval interface | `VERIFIED` page health; canonical memory integration is still unproven |
| n8n | Visual workflow automation | `VERIFIED` HTTP 200 on 2026-08-19 |
| ChromaDB | Stores vectors for similarity search | `VERIFIED` heartbeat HTTP 200 on 2026-08-19 |
| Dolt | Versioned SQL data store, similar to a database with Git-like history | `VERIFIED` container running; SQL query not rechecked |
| Unsloth | Training, inference, export, and model-workbench UI | `VERIFIED` D-backed native health before restart; Docker image pull remains open |
| llama.cpp | Separate native inference path for the AMD/Vulkan experiment | `CONFIGURED`; intentionally not in the normal Compose stack |
| ComfyUI / LM Studio | Desktop AI tools and data preserved on D: | `OPEN`; not currently serverized |

## Why LiteLLM matters

Without a gateway, every application needs to know where every model lives. With
LiteLLM, an application can ask for `local-qwen`, while LiteLLM knows that this
means the Ollama service on the Compose network. That is the switchboard idea.

## Why some data is not a server

ChromaDB and Dolt are services in this setup. LanceDB and DuckDB are intentionally
embedded engines used by memory-chain code; they are libraries/storage files,
not additional servers that need a port.
