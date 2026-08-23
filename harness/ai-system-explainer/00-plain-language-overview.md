# What this system is

## The short version

This computer now has a local AI server room. The large model files, Docker
data, AI caches, and training workspace were moved off the Windows system drive
and onto the second internal drive, D:. The goal is that people and applications
use shared services instead of each launching their own copy of an AI program.

Think of it like this:

- Windows is the front desk and browser.
- Docker is the building that keeps services separated and repeatable.
- Ollama is the local model engine.
- LiteLLM is the switchboard that gives different applications one API.
- Open WebUI is the human chat window.
- n8n is the automation worker.
- ChromaDB and Dolt are storage shelves for search and versioned records.
- Unsloth is the model-training and fine-tuning workshop.

The system is local-first: the local services can run without sending a prompt
to a cloud provider. Cloud models are present as optional LiteLLM routes, but
their credentials are kept in the private `.env` file and were not printed.

## What “server-first” means here

The desktop applications are no longer supposed to be the authority for models.
A browser, script, workflow, or another local client should call the server.
This avoids duplicate model downloads, inconsistent settings, and “which app is
actually answering?” confusion.

## The important distinction

Moving files to D: solved storage pressure. Running services centrally solves
availability and repeatability. Those are related but different jobs:

1. Storage migration: get AI data off C:.
2. Runtime migration: make Docker or a D-backed server own the AI process.
3. Access design: make clients use one clear local endpoint.
4. Verification: prove the endpoint answers before calling the system working.
