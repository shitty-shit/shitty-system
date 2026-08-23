# Community: Agent Coordination Layer

A knowledge graph community in the ShittyShit / LACES_CASES ecosystem.
10 nodes, auto-detected by graphify community clustering.

## Connected To
- Brand Identity & Commerce
- LACES_CASES Infrastructure

## Members

### Canonical Tetrad (me, toolstack, projectstack, biz)
- Node ID: `canonical_tetrad`
- Type: document
- Source: `graphify-out/converted/Kevin Kane â€” me.md_5702cd27.md`
- Connections: 5
- Internal edges:
  - produces -> STEM / YANK Identity System (EXTRACTED)
  - structures -> GSD (Get Shit Done) Workflow (EXTRACTED)
  - conceptually_related_to -> Project Compiler (INFERRED)
- Cross-community edges:
  - includes -> ShittyShit.co (INFERRED) [crosses to Brand Identity & Commerce]
  - includes -> toolstack.md (Tool/Capability Map) (EXTRACTED) [crosses to LACES_CASES Infrastructure]

### STEM / YANK Identity System
- Node ID: `stem_yank`
- Type: document
- Source: `graphify-out/converted/Kevin Kane â€” me.md_5702cd27.md`
- Connections: 3
- Internal edges:
  - produces -> Canonical Tetrad (me, toolstack, projectstack, biz) (EXTRACTED)
  - defines -> Agent Load Order Protocol (EXTRACTED)
  - maintained_by -> Canon Purge Notes (BlinkChange, Jenkev) (INFERRED)

### GSD (Get Shit Done) Workflow
- Node ID: `gsd_workflow`
- Type: document
- Source: `graphify-out/converted/Kevin Kane â€” me.md_5702cd27.md`
- Connections: 2
- Internal edges:
  - structures -> Canonical Tetrad (me, toolstack, projectstack, biz) (EXTRACTED)
  - implemented_by -> GSD Agent Skills (40+ commands) (EXTRACTED)

### GSD Agent Skills (40+ commands)
- Node ID: `gsd_skill_set`
- Type: document
- Source: `graphify-out/converted/skills-reference_2ea28198.md`
- Connections: 2
- Internal edges:
  - implemented_by -> GSD (Get Shit Done) Workflow (EXTRACTED)
  - generates_spreadsheet_for -> create_skills_spreadsheet.py (EXTRACTED)

### Agent Load Order Protocol
- Node ID: `agent_load_order`
- Type: document
- Source: `graphify-out/converted/Kevin Kane â€” me.md_5702cd27.md`
- Connections: 2
- Internal edges:
  - defines -> STEM / YANK Identity System (EXTRACTED)
  - follows -> Agent Mesh Coordination (EXTRACTED)

### create_skills_spreadsheet.py
- Node ID: `openpyxl_script`
- Type: code
- Source: `create_skills_spreadsheet.py`
- Connections: 2
- Internal edges:
  - generates_spreadsheet_for -> GSD Agent Skills (40+ commands) (EXTRACTED)
  - calls -> openpyxl (Excel Library) (EXTRACTED)

### Agent Mesh Coordination
- Node ID: `agent_mesh`
- Type: document
- Source: `graphify-out/converted/Kevin Kane â€” me.md_5702cd27.md`
- Connections: 1
- Internal edges:
  - follows -> Agent Load Order Protocol (EXTRACTED)

### Project Compiler
- Node ID: `project_compiler`
- Type: document
- Source: `graphify-out/converted/projectstack.md_4e2e08f6.md`
- Connections: 1
- Internal edges:
  - conceptually_related_to -> Canonical Tetrad (me, toolstack, projectstack, biz) (INFERRED)

### Canon Purge Notes (BlinkChange, Jenkev)
- Node ID: `purge_notes`
- Type: document
- Source: `graphify-out/converted/Kevin Kane â€” me.md_5702cd27.md`
- Connections: 1
- Internal edges:
  - maintained_by -> STEM / YANK Identity System (INFERRED)

### openpyxl (Excel Library)
- Node ID: `openpyxl_library`
- Type: code
- Source: `create_skills_spreadsheet.py`
- Connections: 1
- Internal edges:
  - calls -> create_skills_spreadsheet.py (EXTRACTED)
