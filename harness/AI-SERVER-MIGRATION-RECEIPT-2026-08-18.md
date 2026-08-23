# AI server migration receipt — 2026-08-18

## Result

The active AI path is now server-first and D-backed:

- Docker Compose owns Ollama, LiteLLM, Open WebUI, AnythingLLM, n8n, ChromaDB, and Dolt.
- Ollama models are consolidated into `D:\Docker\volumes\ollama`.
- LiteLLM routes `local-qwen` to the compose Ollama at `http://ollama:11434`.
- The native Ollama process was stopped; only the Docker Ollama owns port 11434.
- Unsloth runs from the migrated D install as a localhost server at `http://127.0.0.1:8888`.
- Unsloth health returned 200 and detected `AMD Radeon 780M Graphics` through ROCm/HIP.
- The official `unsloth/unsloth` Docker image was configured as an opt-in profile, but its pull timed out before an image was produced. The native D server is the current working fallback.

## Verification

- `docker compose config --quiet`: passed.
- All seven normal Compose services running after port hardening.
- Docker endpoints: Ollama, Open WebUI, AnythingLLM, LiteLLM, n8n, ChromaDB, and Dolt bound to `127.0.0.1`.
- LiteLLM health: HTTP 200.
- LiteLLM real inference: returned `SERVER_STACK_OK` through `local-qwen`.
- Unsloth `/api/health`: HTTP 200, `chat_only=false`, warm-up completed.
- Native Ollama process: not running.
- The previous C: AI/Docker migration left no active AI data under C:; the C: rollback copies remain preserved on D:.

## Deliberate follow-up

`D:\AI\data\Ollama` is an inactive retained copy of the former native model store.
It is not currently used by the Docker server. Do not delete it until the Docker
model list and any rollback need have been accepted; it is the next safe cleanup
candidate and is approximately 27.7 GB.

## Post-restart recovery — 2026-08-19

- Docker Desktop was started again after the Freebuff restart.
- The seven-service Compose stack was started again with localhost-only ports.
- Open WebUI, Ollama, AnythingLLM, LiteLLM, and Unsloth health checks returned
  HTTP 200.
- A real LiteLLM request returned `CURRENT_STACK_OK` through Docker Ollama.
- The D-backed native Unsloth server was restarted on `127.0.0.1:8888`.
