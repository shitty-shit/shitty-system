# Provider ledger — every API key and budget in one place

The business: assess → sign up → test → make content about AI providers.
This ledger is the single record of which providers are live in the gateway,
what key each one uses, and what budget/credit sits on it. Markdown governs,
receipts prove: the spend numbers in this table come from the Admin UI.

## The two-key mental model (the thing that used to make LiteLLM confusing)

- **Provider key** — the real key the provider gives you. Your credit card at
  that provider. Entered **once**, in `.env` (this stack) or via the Admin UI.
  Never handed to apps.
- **Virtual key** — a budget-capped key you mint from the master key:
  `python keys.py create <alias> <usd>`. This is what apps/tests/content get.
  Each one gets its own row in the Admin UI spend log.
- **Budget** — set on the virtual key. When it's spent, the key auto-returns
  429: the provider can never bleed you silently again.

Rule: **one virtual key per experiment, one budget per virtual key, spend log
= the receipt.** That is the entire system.

## The ledger

| Provider | LiteLLM name | Key lives in | Budget cap | Spent | Stranded credit | Pipeline |
|---|---|---|---|---|---|---|
| OpenRouter | `openrouter/*` | `.env` → OPENROUTER_API_KEY | | | | ☐ assess ☐ key ☐ test ☐ content |
| Google Gemini | `gemini/*` | `.env` → GEMINI_API_KEY | | | | ☐ assess ☐ key ☐ test ☐ content |
| Alibaba DashScope | `dashscope/*` | `.env` → DASHSCOPE_API_KEY | | | | ☐ assess ☐ key ☐ test ☐ content |
| bynara (custom endpoint) | `bynara/*` | `.env` → BYNARA_API_KEY + BYNARA_API_BASE | | | | ☐ assess ☐ key ☐ test ☐ content |
| | | | | | | |

Columns: **Budget cap** = what you're willing to spend on this provider.
**Spent** = what LiteLLM has actually charged (Admin UI → **Logs**).
**Stranded credit** = free/prepaid credit sitting at the provider — burn it
deliberately with a dedicated virtual key, log what you drained it with.

## When a new provider comes in (the loop)

1. **Assess** — sign up, grab the API key, note any free/stranded credit.
2. **Key it** — add the key either way:
   - `.env` → add `PROVIDER_API_KEY=...`, then `docker compose up -d`; or
   - Admin UI → **Models + Endpoints** → **Add Model** tab → paste the key
     (or `os.environ/NAME` to
     reference one already in `.env`).
   - Not a stock LiteLLM provider (like bynara)? Add `api_base` too — see
     `litellm_config.yaml` for the pattern.
3. **Test** — Admin UI Playground, or mint a scratch virtual key and curl:
   `python keys.py create <alias>-test 5`, then hit `/v1/chat/completions`.
4. **Log it** — add the row above; update Budget cap / Spent / Stranded.
5. **Content** — write it up with real numbers from the spend log.

## Daily commands (from this folder)

| Do this | Command |
|---|---|
| See every key + budget + what's left | `python keys.py list` |
| Mint a budget-capped key | `python keys.py create <alias> <usd>` |
| Stop a key right now | `python keys.py block <sk-...>` |
| Last spend rows | `python keys.py spend 20` |
| One key's detail | `python keys.py info <sk-...>` |

Windows: `keys list`, `keys create ...` work the same. Everything also lives
in the Admin UI at http://localhost:4000/ui (login `admin` / your
`LITELLM_MASTER_KEY` from `.env`).
