# Community: Agent Platform Hosting

A knowledge graph community in the ShittyShit / LACES_CASES ecosystem.
3 nodes, auto-detected by graphify community clustering.

## Members

### IJFW Agent Framework
- Node ID: `ijfw_framework`
- Type: document
- Source: `AGENTS.md`
- Connections: 2
- Internal edges:
  - configures -> AGENTS.md (IJFW Configuration) (EXTRACTED)
  - hosted_by -> Freebuff Desktop (INFERRED)

### AGENTS.md (IJFW Configuration)
- Node ID: `agents_md_file`
- Type: document
- Source: `AGENTS.md`
- Connections: 1
- Internal edges:
  - configures -> IJFW Agent Framework (EXTRACTED)

### Freebuff Desktop
- Node ID: `freebuff_desktop`
- Type: document
- Source: `CLAUDE.md`
- Connections: 1
- Internal edges:
  - hosted_by -> IJFW Agent Framework (INFERRED)
