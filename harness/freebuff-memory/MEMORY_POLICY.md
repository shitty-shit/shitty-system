# Memory Policy

## Store

- Decisions and their rationale.
- Stable user preferences and terminology.
- Verified system facts and important discoveries.
- Files changed, tests run, and operational receipts.
- Open questions, blockers, and the next concrete action.

## Do not store

- API keys, tokens, passwords, cookies, or credentials.
- Full chat transcripts or large tool outputs.
- Speculation presented as fact.
- Repeated status noise that does not help another chat resume.

## Memory types

- `decision` — a durable choice with `summary`, `why`, and `how_to_apply`.
- `preference` — a stable Kevin/Freebuff working preference.
- `observation` — a verified fact or discovery.
- `pattern` — a reusable workflow or engineering pattern.
- `handoff` — the compact current state for the next chat.

## Token discipline

- Use `summary` prelude by default; request more detail only when needed.
- Keep handoffs below roughly 300 words.
- Store pointers to canonical files instead of copying their contents.
- Correct stale memory explicitly; do not silently add conflicting facts.

## Layer boundaries

- Freebuff SQLite is raw evidence. Read it in place and fingerprint it; do not
  bulk-copy transcripts into IJFW or canon.
- IJFW stores compressed working context and the latest session handoff.
- Central handoffs and dev-log receipts may mirror sanitized IJFW output to
  `D:\SHITTYSHIT`; claims still enter canonical files through the memory loop's
  proposal and explicit-approval gate.
