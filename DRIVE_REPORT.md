# D: Drive Report — 500GB System Drive Audit

> Generated: 2026-09-01 · Scripts in `scripts/drive-report*.ps1`

---

## Headline Numbers

| Metric | Value |
|---|---|
| **Total capacity** | 476.9 GB |
| **Used** | 404.5 GB (84.8%) |
| **Free** | 72.4 GB |
| **Easily reclaimable** | **~168 GB** (rollback snapshot + duplicate models + caches) |

---

## Where the 404 GB Lives

| Directory | Size | What it is |
|---|---|---|
| **D:\AI** | **284.4 GB** | Models, app data, one giant rollback snapshot |
| **D:\Docker** | **110.5 GB** | Docker Desktop + WSL disk + all service volumes |
| D:\SHITTY_GIT | 4.9 GB | 28 repos |
| D:\SHITTYSHIT | 1.8 GB | The One Store knowledge base |
| D:\.pnpm-store | 0.7 GB | Package cache |
| D:\Downloads | 0.6 GB | 1 file |
| D:\SHITTY_SYSTEM | 0.01 GB | This repo |
| D:\ox-alpha | ~0 GB | Agent workspace (code only) |
| D:\Antgravity_500 | ~0 GB | Agent workspace (code only) |

`D:\AI` + `D:\Docker` = **395 GB (98%)** of everything on the drive.

---

## 🔴 #1 Finding: The Rollback Snapshot — 144.8 GB (36% of the drive)

`D:\AI\rollback\20260818-193645\` is a single full backup taken **August 18** of every AI app's data directory:

| Inside the snapshot | Size |
|---|---|
| AnythingLLM desktop data (incl. Ollama model copies) | ~46 GB |
| .docker (Model Runner models) | ~7 GB |
| .lmstudio (GGUF models) | ~15 GB |
| User-ComfyUI (SD checkpoints, text encoders) | ~13 GB |
| .ollama (native Ollama models) | ~12 GB |
| Everything else | remainder |

**It is a 2-week-old point-in-time copy of data that still exists in its original location.** Every large model in it is duplicated from `D:\AI\data\` or `D:\Docker\volumes\ollama\`.

**Recommendation:** Delete it, or compress and offload it to cold storage (external drive / cloud) if you want the safety net. This single action frees **~145 GB** and takes the drive from 85% → ~55% utilization.

---

## 🟠 #2 Finding: Models Stored 3–5 Times Over

The same model weights exist in multiple runtimes' stores. Examples from the largest-file scan:

| Model | Copies | Total wasted |
|---|---|---|
| qwen3.6:27b (15.7 GB blob) | Docker Ollama only | — (single copy, fine) |
| llama3.1/3.2-8B-class blobs (6.9–8.4 GB each) | `D:\AI\data\AnythingLLM\storage\models\ollama\` **+** `D:\AI\rollback\...\anythingllm...` | ~7 GB dup in rollback |
| gemma-4-12B QAT (6.5 GB) | LM Studio **+** rollback copy | 6.5 GB dup |
| RealVisXL_V5 + umt5_xxl (12.7 GB) | ComfyUI **+** rollback copy | 12.7 GB dup |
| gemma-4-E4B (5.0 GB) | LM Studio **+** rollback copy | 5.0 GB dup |
| 4.87 GB blob (hermes/qwen-class) | **4 copies**: Docker Ollama, native Ollama (`D:\AI\data\Ollama`), AnythingLLM storage, rollback | ~14.6 GB wasted |

### The five model stores on this machine

| Store | Size | Runtime |
|---|---|---|
| `D:\Docker\volumes\ollama` | 44.6 GB | **Docker Ollama** (canonical per stack README) |
| `D:\AI\data\Ollama` | 29.4 GB | Native Windows Ollama |
| `D:\AI\data\AnythingLLM\storage\models\ollama` | ~45 GB | AnythingLLM's **internal** Ollama copy |
| `D:\AI\data\LM Studio` | 15.1 GB | LM Studio GGUFs |
| Docker Model Runner (`D:\Docker\user\.docker\models`) | ~7 GB | gemma3-qat, gemma4, granite-docling |
| `D:\AI\data\ComfyUI` | 15.8 GB | SD checkpoints (unique, no dup outside rollback) |

**Recommendation:** Pick one canonical LLM server — the stack README already says **Docker Ollama** is canonical — and point everything at `127.0.0.1:11434`. Native Ollama's 29 GB and AnythingLLM's internal ~45 GB store are the prime dedup targets: anything pulled there is re-downloadable with one `ollama pull` / one click. Potential recovery: **~60–75 GB** without losing any capability.

---

## 🟡 #3 Finding: Docker's 110 GB Breaks Down As

| Component | Size | Notes |
|---|---|---|
| `wsl-data\disk\docker_data.vhdx` | **50.5 GB** | The WSL2 virtual disk. Grows but never shrinks automatically. |
| `volumes\ollama` | 44.6 GB | Docker Ollama models (canonical store) |
| `user\.docker` | 10.9 GB | Docker CLI data + Model Runner models (~7 GB) |
| Docker Desktop app | 3.4 GB | The application itself |
| Other service volumes | ~1 GB | n8n, dolt, chroma, anythingllm, open-webui, duckdb |

**Note on the 50.5 GB vhdx:** this holds images + build cache + container layers. The stack's 7 images account for maybe 10–15 GB; the rest is likely dangling layers and build cache. `docker system prune -a --volumes` (careful — read what it deletes first) plus `Optimize-VHD`/compact can reclaim a large chunk without touching your bind-mounted volumes (those live on `D:\Docker\volumes\`, outside the vhdx — safe).

---

## 🟢 What's Healthy

- **Docker service volumes are tiny** — n8n/dolt/chroma/litellm data is <50 MB each. The heavy data lives in bind mounts, exactly as designed.
- **Code is cheap** — all 28 repos + both agent workspaces + the One Store = under 7 GB. The 500 GB story is models and one backup, not code.
- **SHITTY_SYSTEM repo is 9 MB** — the front door costs nothing.
- **Docker installed on D:** — the 3.4 GB app itself correctly lives off C:.
- **Only one rollback snapshot exists** — the rollback system ran once, not continuously. No accumulation problem (yet).

---

## Reclaim Plan (Biggest First)

| # | Action | Frees | Risk |
|---|---|---|---|
| 1 | Delete or offload `D:\AI\rollback\20260818-193645` | **~145 GB** | None if originals verified (they're all present in `D:\AI\data` / Docker volumes) |
| 2 | Point AnythingLLM at Docker Ollama instead of its internal model store; clear `D:\AI\data\AnythingLLM\storage\models\ollama` | **~45 GB** | Low — reconfigure one URL, re-embed if needed |
| 3 | Retire native Windows Ollama (or vice versa); remove `D:\AI\data\Ollama` | **~29 GB** | Low — one runtime stays |
| 4 | `docker system prune` + compact the 50 GB vhdx | **~20–35 GB** | Medium — removes unused images/containers; volumes are safe |
| 5 | Clear `D:\AI\cache\huggingface` (7.9 GB) if models are already local | ~8 GB | Low — HF cache re-downloads |
| 6 | LM Studio models you don't use | up to 15 GB | Low |

**Total potential: ~260 GB recovered, drive goes from 85% → ~30% full.**

Actions 1–3 alone need no re-downloads except anything you later want back, and get you to ~55% full in under an hour.

---

## Method Notes

Sizes measured with PowerShell `Get-ChildItem -Recurse` over every file (`scripts/drive-report.ps1`, `drive-report-deep.ps1`, `drive-report-ai.ps1` — kept in the repo for re-runs). Largest-file scan covered `D:\AI` and `D:\Docker` only; small dirs were inventoried in SYSTEM_INVENTORY.md.
