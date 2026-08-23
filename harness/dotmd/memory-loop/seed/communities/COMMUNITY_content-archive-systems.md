# Community: Content & Archive Systems

A knowledge graph community in the ShittyShit / LACES_CASES ecosystem.
6 nodes, auto-detected by graphify community clustering.

## Connected To
- Brand Filter & Turtle Flip
- Monetization & Token Economics

## Members

### ShittyChunk Compression
- Node ID: `shittyshit_chunk`
- Type: document
- Source: `graphify-out/converted/Kevin Kane â€” me.md_5702cd27.md`
- Connections: 3
- Internal edges:
  - uses -> Great Ingest Pipeline (EXTRACTED)
  - conceptually_related_to -> Content Machine Pipeline (INFERRED)
- Cross-community edges:
  - serves -> TOKENS = MONEY Doctrine (EXTRACTED) [crosses to Monetization & Token Economics]

### Great Ingest Pipeline
- Node ID: `great_ingest`
- Type: document
- Source: `graphify-out/converted/Kevin Kane â€” me.md_5702cd27.md`
- Connections: 3
- Internal edges:
  - uses -> ShittyChunk Compression (EXTRACTED)
  - feeds_into -> Mudroom Staging Area (EXTRACTED)
  - conceptually_related_to -> Good Book of Ghosts (INFERRED)

### Content Machine Pipeline
- Node ID: `content_machine`
- Type: document
- Source: `graphify-out/converted/projectstack.md_4e2e08f6.md`
- Connections: 2
- Internal edges:
  - conceptually_related_to -> ShittyChunk Compression (INFERRED)
  - consumes -> Harness Smackdown Reviews (EXTRACTED)

### Harness Smackdown Reviews
- Node ID: `harness_smackdown`
- Type: document
- Source: `graphify-out/converted/projectstack.md_4e2e08f6.md`
- Connections: 2
- Internal edges:
  - consumes -> Content Machine Pipeline (EXTRACTED)
- Cross-community edges:
  - publishes -> AIShitty.com (EXTRACTED) [crosses to Brand Filter & Turtle Flip]

### Mudroom Staging Area
- Node ID: `mudroom`
- Type: document
- Source: `graphify-out/converted/Kevin Kane â€” me.md_5702cd27.md`
- Connections: 1
- Internal edges:
  - feeds_into -> Great Ingest Pipeline (EXTRACTED)

### Good Book of Ghosts
- Node ID: `good_book_ghosts`
- Type: document
- Source: `graphify-out/converted/projectstack.md_4e2e08f6.md`
- Connections: 1
- Internal edges:
  - conceptually_related_to -> Great Ingest Pipeline (INFERRED)
