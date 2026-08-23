# LiteLLM stack — one gateway, all providers

> **Not a coder? Start with [START-HERE.md](START-HERE.md)** — a plain-language
> guide that takes you from double-click to your first budget card. This file
> is the full technical manual; that one is the everyday version.

Two containers on day one (gateway + Postgres). Redis is the third, gated
behind a compose overlay for when you register duplicate keys per provider.

| Container  | Image                          | Why                                      |
|------------|--------------------------------|------------------------------------------|
| LiteLLM    | ghcr.io/berriai/litellm        | One OpenAI-compatible endpoint           |
| PostgreSQL | postgres:16                    | Admin UI, virtual keys, spend tracking   |
| Redis      | redis:7 (day two, optional)    | Rate-limit-aware load balancing + cache  |

## If LiteLLM confused you before — read this (30 seconds)

There are only **two kinds of keys**, and mixing them up is the whole game:

- **Provider keys** are your credit cards. Each provider gives you one; you
  enter it once (`.env` or Admin UI) and never touch it again.
- **Virtual keys** are per-project budget cards. You mint them from the master
  key, give one to each app/agent/experiment, and set a dollar budget on it.
  When a virtual key spends its budget, it **stops working (429)** — the
  provider physically cannot bleed you silently.

The Admin UI (http://localhost:4000/ui) is where everything is visible: models,
keys, and the spend log — a receipt for every single request. **You never have
to edit config files to do daily work**; the config file in this folder just
pre-loads your four providers so they exist from minute one.

## One-command setup

**Windows: double-click `setup.cmd`.** Mac/Linux/WSL: `bash setup.sh`.

It checks Docker, creates `.env` with fresh random master + salt keys (keeps
an existing `.env` untouched), starts the stack, waits for the gateway, prints
your login, and opens the Admin UI. That's the whole install.

Manual alternative: `cp .env.example .env` (fill keys) → `docker compose up -d`.

- Gateway: http://localhost:4000  (OpenAI-compatible, `/v1/chat/completions`)
- Admin UI: http://localhost:4000/ui — login `admin` / your `LITELLM_MASTER_KEY`

Smoke test (master key works here; use it only to test):

```bash
curl http://localhost:4000/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "openrouter/anthropic/claude-sonnet-4", "messages": [{"role": "user", "content": "ping"}]}'
```

Models are pre-wired in `litellm_config.yaml` as wildcards, so call any model
under these namespaces: `openrouter/<model>`, `gemini/<model>`,
`dashscope/<model>`, `bynara/<model>`.

## Daily operations — keys and budgets from the terminal

```bash
python keys.py list                        # every key: budget, spent, left
python keys.py create content-test 5       # mint a $5 budget-capped key
python keys.py spend 20                    # last 20 spend-log rows
python keys.py block sk-xxx                # hard-stop a key right now
python keys.py delete sk-xxx               # delete a key
```

Windows: `keys list`, `keys create content-test 5`, etc. Master key is read
from `.env` automatically. Everything these show is also in the Admin UI.

## Virtual keys + spend = the burn-down tool

Never hand out the master key. Create a **virtual key** per app/agent/
experiment with a budget, and the Admin UI's spend ledger shows exactly where
tokens went — that's how you find and deliberately burn down stranded
balances. Budget caps auto-harden: LiteLLM returns 429 once a key hits its
budget, so stranded credit gets burned deliberately, not by accident.

Key with a per-provider scope and budget, via API:

```bash
curl http://localhost:4000/key/generate \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"models": ["dashscope/*"], "max_budget": 10.0, "metadata": {"name": "dashscope-burn"}}'
```

## The provider ledger

`providers.md` tracks every provider: which key it uses, budget cap, spend,
stranded credit, and where it is in your assess → key → test → content
pipeline. New provider? Follow the loop at the bottom of that file.

## Adding provider keys

1. **Env vars (recommended here)** — edit `.env`, `docker compose up -d` to
   reload. Keys are already referenced from `litellm_config.yaml`.
2. **Admin UI** — Models + Endpoints → Add Model tab → paste the key, or enter
   `os.environ/OPENROUTER_API_KEY` (the env var name) to reference one already
   in `.env`. Models added in the UI persist to Postgres.

## Day two: Redis (duplicate keys per provider)

When you register a second key for a provider, enable rate-limit-aware routing:

```bash
docker compose -f docker-compose.yml -f docker-compose.redis.yml up -d
```

This wires `REDIS_HOST`/`REDIS_PORT`/`REDIS_PASSWORD` into the router, so
cooldowns and usage-based routing track across all keys instead of one
process's memory. Then switch `litellm_config.yaml` to
`routing_strategy: usage-based-routing-v2` (see the comment there — v2
*requires* Redis; day one uses the in-memory v1, which is why it starts
without Redis). For Redis-backed caching, swap the `cache:` line in
`litellm_config.yaml` per the comment there, then
`docker compose -f ... -f docker-compose.redis.yml restart litellm`.

## Notes

- **Security**: `setup.cmd` generates real master + salt keys for you. Never
  change the salt after first run. `.env` holds secrets — keep it out of any
  repo. Don't expose port 4000 publicly without auth on top.
- **Pinning**: `main-latest` tracks nightly builds; pin a release tag
  (`ghcr.io/berriai/litellm:main-v1.xx.x`) once the stack is proven.
- **Logs / down**: `docker compose logs -f litellm` · `docker compose down`
  (data persists in the `postgres_data` volume).
- **Update**: `docker compose pull && docker compose up -d`.
