# What the migration work actually did

## 1. Swept the system drive

The first pass was read-only. It identified large AI and Docker areas under the
`idfk` Windows profile, including Docker blobs, Ollama models, AnythingLLM data,
LM Studio, ComfyUI, Unsloth, Anaconda, and the Hugging Face cache. It also checked
that D: was the intended internal `DockerData` drive with enough free space.

## 2. Moved the data without destroying the old paths

Fifteen C: paths were copied to D: with Robocopy, file and byte totals were
checked, and the original locations were replaced with junctions. This preserved
application compatibility while moving the actual bytes. Rollback copies were
kept on D: instead of deleting them.

## 3. Consolidated the model authority

There were two Ollama runtimes: a native Windows process and a Docker service.
The native model store was copied into the Docker Ollama store, LiteLLM was
changed from the host-native address to the Compose-network address, and the
native Ollama process was stopped. This made Docker Ollama the single model
authority.

## 4. Added a server-first Unsloth path

The official Unsloth Docker profile was added with D-backed work, export, run,
and Hugging Face cache mounts. Its image pull timed out, so the already-migrated
Unsloth installation was launched as a localhost server instead. That server
passed its health check and detected the AMD Radeon 780M through ROCm/HIP.

## 5. Reduced accidental exposure

The Compose ports were changed from wildcard bindings to `127.0.0.1`. That means
local browsers and applications can use the services, but another device on the
LAN cannot reach them by accident. LAN access remains a separate authenticated
gateway decision.

## 6. Recovered after the Freebuff restart

The restart stopped Docker Desktop and Unsloth. The files were still present, so
Docker Desktop and the Compose stack were started again, followed by Unsloth.
Every key endpoint returned HTTP 200, and LiteLLM produced the test response
`CURRENT_STACK_OK` through the Docker Ollama.

## 7. What I deliberately did not claim

I did not claim that the official Unsloth Docker image is working, that ComfyUI
is a shared server, or that AnythingLLM is the canonical Freebuff memory backend.
Those are separate verification tasks, not assumptions hidden inside the final
diagram.
