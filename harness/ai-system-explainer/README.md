# LACES_CASES AI system explainer

For the complete operator index, start with the [executive handoff](../EXECUTIVE_HANDOFF.md) or the [AI system cheat sheet](../AI-SYSTEM-CHEAT-SHEET-2026-08-19.md). The [browser slide deck](../HARNESS_SYSTEM_SLIDES.html) is the visual introduction.

This folder explains the AI and Docker system in plain language for someone who
did not perform the installation.

Read in this order:

1. `00-plain-language-overview.md` — what the system is for.
2. `01-what-was-moved.md` — what left C: and where it lives on D:.
3. `02-how-the-services-connect.md` — the information flow.
4. `03-current-state-and-gaps.md` — what is verified now, after the restart, and what is not finished.
5. `04-operations-and-safety.md` — how to start, stop, and use it safely.
6. `05-what-we-did.md` — the timeline of the migration and server work.

The generated visual graph lives beside this folder in `graphify-out/`.
The interactive graph is the visual explainer for this pass. A PowerPoint export
was not created because the restarted session does not have the presentation
artifact runtime dependencies exposed; the source content is ready for a deck.

The graph was built from the curated system facts in `AI-SYSTEM-EXTRACTION.json`
using `build_graph.py`, not from an unrestricted C: scan.

Evidence rule: `VERIFIED` means directly observed in a command or health check;
`CONFIGURED` means present in a file but not necessarily running; `INFERRED`
means a reasonable explanation of how pieces relate; `OPEN` means work remains.
