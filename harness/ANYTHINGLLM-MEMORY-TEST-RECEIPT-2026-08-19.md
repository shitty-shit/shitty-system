# AnythingLLM memory test receipt — 2026-08-19

## Result

**Status: BLOCKED / WRITE FAILED.** The AnythingLLM service is reachable, but a complete canary write → fresh-query retrieval round trip could not be completed because the configured chat provider returned a missing-credential error before creating a memory.

## Test identity

- Service: `http://127.0.0.1:3001`
- AnythingLLM version observed in UI: `v1.16.0`
- Workspace: `Shittyshit` / slug `my-workspace`
- Canary marker: `HARNESS-ANYTHINGLLM-CANARY-20260819-1439`
- Source canary: [ANYTHINGLLM-CANARY-SOURCE-2026-08-19.md](freebuff-memory/receipts/ANYTHINGLLM-CANARY-SOURCE-2026-08-19.md)

## Steps performed

1. Confirmed the AnythingLLM home page responded HTTP 200.
2. Opened the authenticated local AnythingLLM UI in Chrome.
3. Started a fresh thread and submitted a write instruction containing the exact canary marker.
4. AnythingLLM returned:

   `The OPENAI_API_KEY environment variable is missing or empty.`

5. Checked the AnythingLLM SQLite database read-only after the attempt:

   - `memories` rows: `0`
   - rows containing the canary marker: `0`
   - workspace documents: `0`
6. Did not run the fresh retrieval query because the write had not succeeded. A retrieval response without a confirmed write would not prove memory continuity.

## Additional gates found

- Direct API probes for `/api/v1/auth`, `/api/v1/workspaces`, and the workspace endpoint returned HTTP 403 because no API key is configured for scripted access.
- The browser file chooser rejected automated selection of the Markdown source file; Chrome reports the ChatGPT extension needs “Allow access to file URLs” for automated uploads. The source file was not uploaded.
- No AnythingLLM database rows or service configuration were directly modified by this test. The only durable test artifact created in the harness is the source canary and this receipt.

## Next action to obtain a real PASS

Configure one of these, then rerun the same marker test:

1. Provide a valid AnythingLLM chat-provider credential for the current OpenRouter/OpenAI route; or
2. Configure the workspace to use the local Ollama service and select an available local model; and
3. Enable AnythingLLM Personalization/Memory if it is disabled.

A pass requires all three signals: a successful write acknowledgement, a memory row containing the exact marker, and a fresh query in a separate thread that returns the exact marker.
