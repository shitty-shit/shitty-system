# Server-first AI layout

The canonical runtime is the Docker Compose project in this directory. Windows
desktop applications are optional clients; they are not the model authority.

## Shared endpoints

| Service | URL | Purpose |
|---|---|---|
| Open WebUI | http://localhost:8080 | Human chat client for the compose Ollama |
| Ollama | http://localhost:11434 | Shared local model API |
| AnythingLLM | http://localhost:3001 | Workspace/RAG client |
| LiteLLM | http://localhost:4000 | Unified model gateway |
| n8n | http://localhost:5678 | Workflow/orchestration client |
| ChromaDB | http://localhost:8000 | Vector store |
| Unsloth Studio (native D: fallback) | http://127.0.0.1:8888 | Current training/data server |
| Unsloth Docker profile | http://127.0.0.1:8888 / :8800 | Optional container server after image pull |

All persistent service data is on D:. Ollama models are canonical at
`D:\Docker\volumes\ollama`. Unsloth work, exports, runs, and Hugging Face cache
are on D: under `D:\AI`.

The current native Unsloth server is bound to localhost and uses the migrated
D-backed install. It detected the AMD Radeon 780M through ROCm/HIP. The official
Docker image pull timed out before producing an image, so the Docker profile is
configured but not yet running.

Start or stop the current native fallback:

```powershell
$u = 'D:\AI\data\Unsloth\studio\bin\unsloth.exe'
Start-Process $u -ArgumentList 'studio','-H','127.0.0.1','-p','8888' -WorkingDirectory 'D:\AI\data\Unsloth\studio'
& $u studio stop
```

The native fallback and the Docker profile must not run at the same time because
both use port 8888.

## Start the normal shared stack

```powershell
Set-Location D:\Docker\stack
docker compose up -d
docker compose ps
```

## Start Unsloth

Set a real local password in the process environment before starting it:

```powershell
$env:UNSLOTH_JUPYTER_PASSWORD = 'replace-with-a-local-secret'
docker compose --profile unsloth up -d unsloth
docker compose logs --tail=100 unsloth
```

The official image documents `--gpus all` for GPU training. This compose service
does not claim GPU access on this AMD 780M/Docker Desktop host. CPU chat/data
workflows may start, but training/export must be validated on the actual host
before treating them as available.

## Ownership rules

- Use Open WebUI, AnythingLLM, LiteLLM, or API clients against the shared services.
- Do not start a second native Ollama on port 11434.
- Keep model/data caches on D:; do not redirect them back into `%USERPROFILE%`.
- Compose ports are bound to `127.0.0.1` for local clients only. Do not change them
  to wildcard/LAN bindings until authentication and Windows Firewall policy have
  been reviewed.
- AnythingLLM remains an application workspace, not the canonical Freebuff memory
  backend, until its API/RAG round-trip is separately verified.
