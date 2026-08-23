# C: AI and Docker relocation plan

Status: DRY-RUN ONLY — no files moved or deleted.

Destination volumes verified on 2026-08-18:

- `C:`: internal NVMe, 45.9 GB free.
- `D:`: internal NVMe labeled `DockerData`, 423.9 GB free, healthy.
- Existing Docker data at `D:\Docker`: approximately 47.2 GB.
- Planned new roots: `D:\AI` and `D:\Docker\user\.docker`.

## Relocation candidates

| Source | Destination | Approx. size | Method |
|---|---:|---:|---|
| `C:\Users\idfk\.docker` | `D:\Docker\user\.docker` | 12.0 GB | verified copy, then junction or `DOCKER_CONFIG` |
| `C:\Users\idfk\AppData\Local\Programs\Ollama` | `D:\AI\apps\Ollama` | 3.0 GB | verified copy, junction |
| `C:\Users\idfk\.ollama` | `D:\AI\data\Ollama` | 27.7 GB | stop Ollama, verified copy, junction/config |
| `C:\Users\idfk\AppData\Local\Ollama` | `D:\AI\data\Ollama-local` | 1.5 GB | verified copy, junction if required |
| `C:\Users\idfk\AppData\Local\Programs\AnythingLLM` | `D:\AI\apps\AnythingLLM` | 1.5 GB | verified copy, junction |
| `C:\Users\idfk\AppData\Roaming\anythingllm-desktop` | `D:\AI\data\AnythingLLM` | 45.0 GB | verified copy, junction/config |
| `C:\Users\idfk\AppData\Local\Programs\LM Studio` | `D:\AI\apps\LM Studio` | 0.8 GB | verified copy, junction |
| `C:\Users\idfk\.lmstudio` | `D:\AI\data\LM Studio` | 15.1 GB | verified copy, junction/config |
| `C:\Users\idfk\AppData\Local\Programs\ComfyUI` | `D:\AI\apps\ComfyUI` | 0.6 GB | verified copy, junction |
| `C:\Users\idfk\ComfyUI` | `D:\AI\data\ComfyUI` | 15.8 GB | verified copy, junction/model-path config |
| `C:\Users\idfk\.unsloth` | `D:\AI\data\Unsloth` | 7.6 GB | verified copy, junction |
| `C:\Users\idfk\anaconda3` | `D:\AI\apps\Anaconda3` | 11.3 GB | verify no active process, verified copy, junction |
| `C:\Users\idfk\.cache\huggingface` | `D:\AI\cache\huggingface` | 3.0 GB | verified copy, environment/config |

Estimated relocation payload: approximately 145 GB including application binaries.

## Deliberately excluded from relocation

- Windows system files and Windows-managed application registration.
- Docker's existing `D:\Docker` engine/data tree; it is already on the target drive.
- Active source repositories and project data unless separately classified as AI model storage.
- `C:\Users\idfk\AppData\Local\Temp`; this is a cleanup candidate, not a migration target.

## Execution gates

1. Stop Ollama and any AI desktop apps using the affected paths.
2. Copy with retry limits and preserve timestamps/attributes.
3. Compare source and destination file counts and byte totals.
4. Keep the original source directories renamed as rollback backups until validation passes.
5. Reopen Docker and AI apps and verify model discovery/inference.
6. Only after validation, remove rollback copies with explicit approval.

## Execution receipt

Completed 2026-08-18:

- All 15 planned C: AI/Docker paths were copied, byte-count verified, and replaced with junctions targeting `D:\AI` or `D:\Docker\user\.docker`.
- Ollama was relaunched from `D:\AI\apps\Ollama\ollama.exe`; `ollama list` successfully discovered the models on D:.
- Rollback copies were moved to `D:\AI\rollback\20260818-193645`; no `.c-backup-*` directories remain on C:.
- C: free space increased from approximately 45.9 GB to 206.8 GB.
- D: free space is approximately 131.9 GB while the rollback copies are retained.
- Docker CLI is on D: and reports version 29.7.2. Docker Desktop was started from `D:\Docker\Docker\Docker Desktop.exe`; daemon validation passed with 9 containers visible and the expected Docker data tree on D:.
