# Community: Brand Filter & Turtle Flip

A knowledge graph community in the ShittyShit / LACES_CASES ecosystem.
5 nodes, auto-detected by graphify community clustering.

## Connected To
- Brand Identity & Commerce
- Content & Archive Systems

## Members

### IDFKAI.com
- Node ID: `idfkai_com`
- Type: document
- Source: `graphify-out/converted/Shittyshit_biz.md_dcaf3797.md`
- Connections: 3
- Internal edges:
  - utilizes -> Turtle-Flip Protocol (EXTRACTED)
  - routes_to -> Brand Filter Matrix (EXTRACTED)
- Cross-community edges:
  - owns_brand -> ShittyShit.co (EXTRACTED) [crosses to Brand Identity & Commerce]

### AIShitty.com
- Node ID: `aishitty_com`
- Type: document
- Source: `graphify-out/converted/Shittyshit_biz.md_dcaf3797.md`
- Connections: 3
- Internal edges:
  - routes_to -> Brand Filter Matrix (EXTRACTED)
- Cross-community edges:
  - owns_brand -> ShittyShit.co (EXTRACTED) [crosses to Brand Identity & Commerce]
  - publishes -> Harness Smackdown Reviews (EXTRACTED) [crosses to Content & Archive Systems]

### Brand Filter Matrix
- Node ID: `brand_filter_matrix`
- Type: document
- Source: `graphify-out/converted/shittyshit_branding.md_bd2b339c.md`
- Connections: 3
- Internal edges:
  - routes_to -> IDFKAI.com (EXTRACTED)
  - routes_to -> AIShitty.com (EXTRACTED)
- Cross-community edges:
  - routes_to -> BigShotNYC (EXTRACTED) [crosses to Brand Identity & Commerce]

### Turtle-Flip Protocol
- Node ID: `turtle_flip`
- Type: document
- Source: `graphify-out/converted/shittyshit_branding.md_bd2b339c.md`
- Connections: 2
- Internal edges:
  - utilizes -> IDFKAI.com (EXTRACTED)
  - enables -> Sanitization Rules (Private to Public) (EXTRACTED)

### Sanitization Rules (Private to Public)
- Node ID: `sanitization_rules`
- Type: document
- Source: `graphify-out/converted/Shittyshit_biz.md_dcaf3797.md`
- Connections: 1
- Internal edges:
  - enables -> Turtle-Flip Protocol (EXTRACTED)
