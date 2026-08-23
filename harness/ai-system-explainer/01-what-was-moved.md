# What was moved from C: to D:

## Storage layout

| Kind of data | New home | Why it exists |
|---|---|---|
| Docker user data | `D:\Docker\user\.docker` | Docker CLI settings, credentials/configuration, and model-related blobs |
| Docker service data | `D:\Docker\volumes\<service>` | Persistent data for Ollama, Open WebUI, LiteLLM, AnythingLLM, n8n, ChromaDB, and Dolt |
| AI applications | `D:\AI\apps` | Ollama, AnythingLLM, LM Studio, ComfyUI, and Anaconda installations |
| AI model/config data | `D:\AI\data` | Ollama, AnythingLLM, LM Studio, ComfyUI, and Unsloth state |
| AI caches | `D:\AI\cache` | Hugging Face and related downloaded artifacts |
| Rollback copies | `D:\AI\rollback\20260818-193645` | Reversible copies retained after the move |

## The migration method

The affected user folders were copied with verification, then their original C:
locations were replaced with Windows junctions. A junction is a transparent sign
that says “the real folder is over there.” Existing applications can continue to
use their familiar C: path while the bytes live on D:.

The work preserved rollback copies instead of deleting the originals. That is
why D: still contains some duplicate data: recovery safety was prioritized over
immediate maximum free space.

## The biggest storage results

- C: free space increased from roughly 45.9 GB to roughly 206.8 GB during the
  migration; the latest post-restart check showed approximately 200 GB free.
- The migrated payload was approximately 145 GB.
- The inactive former native Ollama store is still retained on D: and is roughly
  27.7 GB. It is a later cleanup candidate, not active Docker data.

## What was intentionally not moved

Windows system files, Windows-managed application registration, active project
repositories, and temporary files were not treated as AI storage. Temporary
files remain a separate cleanup job because deleting them without inspection can
remove useful in-progress work.
