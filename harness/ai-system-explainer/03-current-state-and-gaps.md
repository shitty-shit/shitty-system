# Current state after the restart and recovery

## What is current and verified

- The documentation, migration receipts, Compose recipe, and LiteLLM routing
  configuration still exist on disk.
- C: has approximately 200 GB free in the latest check.
- D: contains the Docker volumes, AI applications, model data, caches, and
  rollback copies.
- The first post-restart inspection found the Docker daemon unavailable and no
  service listeners on the normal ports. This was expected because the restart
  stopped background processes; it was not evidence that the configuration was
  lost.
- Docker Desktop and the normal Compose stack have now been restarted.
- The current verification found all seven Compose services running on
  localhost, Unsloth healthy on D:, and a real LiteLLM request returning
  `CURRENT_STACK_OK`.

## What was verified before the restart

- Seven normal Compose services started successfully.
- Ollama listed the consolidated models from the D-backed Docker store.
- LiteLLM health returned HTTP 200.
- A real LiteLLM request returned `SERVER_STACK_OK` through the Docker Ollama.
- Unsloth health returned HTTP 200, completed warm-up, and detected the AMD
  Radeon 780M through ROCm/HIP.
- All normal service ports were changed to localhost-only bindings.

## Current service map

| Endpoint | Current result |
|---|---|
| Open WebUI `127.0.0.1:8080` | HTTP 200 |
| Ollama `127.0.0.1:11434` | HTTP 200 and models listed |
| LiteLLM `127.0.0.1:4000` | health HTTP 200 and real inference passed |
| AnythingLLM `127.0.0.1:3001` | HTTP 200 |
| Unsloth `127.0.0.1:8888` | API health HTTP 200 |
| n8n, ChromaDB, Dolt | Compose containers running |

## What remains open

1. Decide whether Unsloth should remain the native D-backed server or move into
   the official Docker image after a successful image pull and GPU test.
2. Containerize or serverize ComfyUI if image generation belongs in the shared
   service room.
3. Remove the duplicate native Ollama store only after the Docker model list and
   rollback decision are accepted.
4. Verify AnythingLLM with a complete API/RAG round trip before calling it the
   system's memory backend.
5. Add an authenticated gateway if access from other devices on the LAN is
   needed. The current default is local-machine access only.

## Honest status language

Do not say “everything is running” after a restart until `docker compose ps`,
endpoint health checks, and one real model request pass again. The durable claim
is: “the server-first configuration and migration are installed; the runtime
needs to be started after reboot.”
