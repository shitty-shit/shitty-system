# AI system explainer — slide-ready outline

Audience: a technically curious person who did not install the system.

Communication job: by the end, the audience should understand what runs where,
how a prompt travels through the system, what moved to D:, and what still needs a
decision.

## Slide 1 — This computer is becoming a local AI server

The big idea: model files and AI services live on D:, while Windows apps act as
clients.

## Slide 2 — Why the move mattered

C: was carrying Docker data, model files, AI caches, and desktop runtimes. The
migration created roughly 200 GB of breathing room on C: and preserved rollback
copies on D:.

## Slide 3 — The service room

Docker Desktop runs the repeatable Compose recipe. Ollama serves models; LiteLLM
routes requests; Open WebUI is the chat front end; n8n, ChromaDB, Dolt, and
AnythingLLM provide workflow, retrieval, versioning, and workspace functions.

## Slide 4 — What happens when someone sends a prompt

Person or app → Open WebUI or LiteLLM → Docker Ollama → model files on D: →
response. The same shared API can be called by workflows and scripts.

## Slide 5 — Where Unsloth fits

Unsloth is the training and fine-tuning workshop. The current working path is a
D-backed native server on localhost:8888; the Docker profile is configured but
its official image pull still needs to succeed.

## Slide 6 — What is verified versus unfinished

Verified: storage migration, Docker stack, model listing, health checks, and real
inference. Open: Dockerized Unsloth, ComfyUI serverization, duplicate cleanup,
AnythingLLM memory round trip, and authenticated LAN access.

## Slide 7 — How to operate it

Start Docker Desktop, run `docker compose up -d`, check `docker compose ps`, open
Open WebUI, and perform one real model request. Keep ports localhost-only unless
authentication and firewall policy are deliberately added.

## Slide 8 — The architecture decision still ahead

Choose whether this machine is the permanent local server or one node in a larger
server pool. That decision controls GPU strategy, LAN access, ComfyUI placement,
and whether Unsloth belongs in Docker or on a dedicated GPU host.
