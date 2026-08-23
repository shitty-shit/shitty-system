# Claude Code Entry Instructions

## Shared Workspace Context
- Read `C:\Users\idfk\Desktop\harness\dotmd\AGENTS.md` and `.state\state.json` before beginning tasks.
- The canonical central memory & artifact store is `D:\SHITTYSHIT`.

## Universal Session Intake / Chat Dump Protocol
When finishing a task, milestone, or whenever the user asks to "dump chat", "save session", or "sync memory":
1. Run the universal intake tool:
   ```bash
   python "D:\SHITTYSHIT\00_MASTER\conversations\chat_intake.py" --agent claude-code --topic "<Brief Topic>" --platform cli
   ```
2. Or use clipboard intake if user copied the conversation:
   ```bash
   python "D:\SHITTYSHIT\00_MASTER\conversations\chat_intake.py" --clipboard --agent claude-code
   ```
This immediately deposits the raw conversation into `00_MASTER\conversations\inbox\` for the System Manager / Synthesizer Agent to index and update the central wiki.
