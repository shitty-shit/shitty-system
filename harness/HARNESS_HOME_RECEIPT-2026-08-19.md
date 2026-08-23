# Harness Home build receipt — 2026-08-19

## Result

Built and launched a local read-only operations console at:

`http://127.0.0.1:8788/`

Port 8787 was already occupied by an existing static server, so it was left unchanged.

## What the page combines

- Live HTTP probes for Open WebUI, AnythingLLM, n8n, LiteLLM, Chroma, and Ollama.
- Docker container status for the seven normal Compose services, including Dolt.
- Freebuff thread inventory through the existing read-only SQLite bridge.
- The current IJFW `handoff.md` excerpt and source link.
- Recent workspace artifacts with direct file links.
- Current open decisions and safety blockers from the system gap register.
- Links to the cheat sheet, executive handoff, slides, static dashboard, and KISS deck.

## Changed files

- `harness_home.py` — same-origin read-only API and static file server.
- `.state/harness-home/index.html` — responsive accessible live dashboard.
- `EXECUTIVE_HANDOFF.md` — Harness Home is now the first operational entry point.
- `HARNESS_CHEATSHEET.html` — live Home and server code links added.

## Verification

- `python -m py_compile .\harness_home.py` — passed.
- `GET /` — HTTP 200.
- `GET /api/health` — HTTP 200; 7/7 services healthy at build time.
- `GET /api/snapshot` — HTTP 200; 12 Freebuff threads, 40 recent artifacts, 4 blockers, current handoff.
- `GET /.state/dash.html` — HTTP 200 through the new server.
- Freebuff bridge unit tests pass 3/3. The broader `verify.ps1` run reaches IJFW but fails its setup-time cross-chat canary assertion; Harness Home records that as an open verification blocker.

## Start / stop

From `C:\Users\idfk\Desktop\harness`:

```powershell
python .\harness_home.py --port 8788
```

The current background process was started from this workspace with PID 31312. Closing that process stops only Harness Home; it does not stop Docker, Freebuff, IJFW, or the existing 8787 server.
