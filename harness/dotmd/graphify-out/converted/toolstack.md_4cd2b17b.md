<!-- converted from toolstack.md.docx -->

ShittyShit / LACES_CASES — toolstack.md
Canonical tool, platform, model, protocol, and routing layer
. This file is not a hype list. It is the operational map for what tools exist, what they do, how they should be routed, and what must not be allowed to become the brain
. Sibling files: me.md, projectstack.md, biz.md, agent.md
.
File: toolstack.md
Version: 2.2
Date: 2026-06-16
Owner: Kevin Kane
Architecture: LACES_CASES
0. TOOLSTACK LAW
No single tool is the system
. The system is the routing layer
. Use each tool for what it is best at
. Do not ask one model, app, database, agent, automation platform, or note system to do everything
.
Core rule: Markdown governs. Dolt versions. LanceDB retrieves. Local tools process. Cloud models reason. Agents execute. GSD structures real work. Receipts prove
.
1. STACK PRINCIPLES
TOKENS = MONEY.
Cloud models are for high-value reasoning
.
Local models are for privacy, repetition, and cost control
.
Markdown is the canonical human/agent source
.
Dolt stores structured truth and versioned records
.
LanceDB / Chroma store semantic/vector-searchable chunks
.
Obsidian is the local graph/navigation layer
.
GitHub is durable repo/version control
.
Google Drive / Workspace is synced storage and source packaging
.
Supabase / Firebase are product/app data layers
.
Cuey is prompt/command staging before automation
.
DoppelBrain retrieves and scouts memory; it does not govern
.
NotebookLM is source-grounded synthesis
.
n8n and Node-RED execute workflows after the workflow is clear
.
MCP connects agents to tools
.
ShittyChunk compresses and routes messy input before ingestion
.
GSD makes real project/job work spec-driven, verifiable, and resumable
.
Do not automate confusion
.
Do not create subscription sprawl
.
Do not confuse “new tool excitement” with architecture
.
The toolstack exists to ship work, save tokens, and create sellable systems
.
2. DEFAULT ROUTING MODEL
Use this routing tree
.
Private, repetitive, local-file-heavy, cheap classification
Route to: local model, local script, Ollama, llama.cpp, Hermes, Skales, AnythingLLM, Python, SQLite / Dolt / LanceDB
.
High-reasoning, strategic, architectural, final synthesis
Route to: ChatGPT, Claude, Gemini, Perplexity, top-tier model panel, Opus-class final vetter
.
Code, repo, scaffold, executable build work
Route to: Codex, Claude Code, Gemini CLI, Cursor, Cline, Agent Zero, terminal, GitHub / Git
. Rule: No coding agent gets loose access without scope, target files, dry-run mindset, verification path, and receipt.
Current web research, citations, market scouting, pricing
Route to: Perplexity, ChatGPT browsing, Gemini / Google search, source-grounded web tools
.
Long document digestion or source-grounded synthesis
Route to: NotebookLM, Gemini, MarkItDown, ShittyChunk, local markdown conversion tools
.
Prompt reuse, command storage, model-panel prompting
Route to: Cuey
.
Scattered memory lookup / artifact graveyard search
Route to: DoppelBrain, external memory layer, semantic recall, LanceDB / Chroma
.
Workflow automation
Route to: n8n, Node-RED, Make, Zapier, Latenode, Buildship
. Rule: Use automation only after the workflow shape is understood.
Canonical truth, status, decisions, structured ledgers
Route to: Markdown, Dolt, GitHub, receipts, decision logs
.
Semantic retrieval / chunk recall
Route to: LanceDB, Chroma, AnythingLLM, vector store
.
Product/app data
Route to: Supabase, Firebase
.
Visual production
Route to: Adobe Creative Cloud, Lightroom Classic, Photoshop, ComfyUI, image/video AI tools
.
Public website wrapper
Route to: WordPress, Codex Sites, Vercel, Netlify, Firebase/Supabase-backed apps
.
3. PRIMARY REQUIRED WORKFLOW: GSD-IN-THE-LOOP
GSD / Get Shit Done is a primary workflow doctrine and must be incorporated into every real project/job folder
. GSD exists to fight context rot: the decay that happens when one AI thread accumulates too much blueprint, code, feedback, and unresolved history
.
GSD rule: Serious project/job work must use specs, isolated execution context, atomic tasks, verification, summaries, and receipts
.
Required GSD docs:
PROJECT.md — project/job purpose, owner, scope, durable context
.
REQUIREMENTS.md — what must be true when done
.
ROADMAP.md — phases, milestones, ordering
.
PLAN.md — phase-level work plan
.
TASKS.xml — atomic machine-readable task plan
.
SUMMARY.md — what was done, what changed, next handoff
.
STATUS.md — current state
.
RECEIPTS/ — proof of work
.
DECISIONS/ — durable decisions and tradeoffs
.
GSD roles:
Researcher — Investigates source, domain, repo, constraints, dependencies
.
Planner — Turns goal backward into atomic tasks
.
Executor — Performs one scoped task with fresh context
.
Checker — Verifies against requirements and acceptance criteria
.
LACES_CASES adaptation: GSD does not replace LACES_CASES. GSD becomes the folder-level execution discipline inside LACES_CASES. LACES_CASES decides routing. GSD structures the work
.
4. TIER 0 — LOCAL CORE / SOVEREIGN OWNED STACK
Tool / Service
Role
Status
Cost / Account
Hermes
Local foundational reasoning, LACES-native
Core
Free / aishitty
Skales
Local foundational reasoning, pipelines, heavy local compute
Core
Free / aishitty
SIM
Helicopter / aerial orchestration layer
Registered
Free / aishitty
Mothership Desktop
Sovereign archive, Obsidian vault, canon, local models
Primary
Owned / aishitty
MINISFORUM
Execution node: Proxy-Sweep, RAW storage, SQLite
Active
Owned / aishitty
AnythingLLM
Workspace hub, agents, Builder flows, MCP
Daily
Free / aishitty
Obsidian
Canonical vault: .md, stems, configs, graph
Daily
Free / aishitty
Ollama
Local model runner
Active
Free / aishitty
LiteLLM
Unified local/API interface layer
Active
Free / aishitty
Dolt
Versioned SQL database for memory/state
Core
Free / aishitty
Chroma DB
Vector store for workspaces
Active
Free / aishitty
LanceDB
Vector store / semantic retrieval
Active
Free / aishitty
SQLite
Lightweight local state, cache, Proxy-Sweep ledger
Active
Free / aishitty
ComfyUI
Self-hosted image generation, ControlNet, LoRA
Active
Free / aishitty
Python
Pipeline automation, scripts, glue logic
Daily
Free / aishitty
AutoHotkey / AHK
OS-level clipboard/window automation
Daily
Free / aishitty
PowerShell / Bash
Shell execution and local admin
Daily
Free / aishitty
(Source:
)
5. TIER 1 — CLOUD AI / POWERHOUSE FREE + SURGICAL PAY
Tool / Service
Role
Status
Cost / Account
ChatGPT Pro
Reasoning, writing, architecture, coding, canvas/operator-style work
Active
Pro / aishitty
Claude Pro
Primary reasoning, coding, long-context, polished specs
Active / watch billing
Pro / reachkane
Claude Code
Coding agent and repo/spec execution
Active
Pro / reachkane or aishitty
Gemini Pro
Long context, video, NotebookLM/Google ecosystem
Active
Pro / aishitty
Gemini Educational
Extended limits through education lane
Active
Low/Free / aishitty
Perplexity Pro
Research, citations, current web, market scouting
Active
Pro / aishitty
MiniMax / Hailuo
Video/audio generation
Active
Pro / aishitty
Cuey
Command shelf: YANK, EXTRACT, COMPRESS, ROUTE
Active
~$10/mo / aishitty
DoppelBrain
Cloud scout/memory: SCOUT, MAP, REPORT
Active
~$10/mo / aishitty
NotebookLM
Source-grounded synthesis and source packs
Active
Google ecosystem
DeepSeek
Reasoning/coding model for comparison and low-cost work
Per-use / local/cloud
aishitty
Qwen
Local/cloud model family, coding and structured extraction
Active
Free/per-use
OpenRouter
Multi-model routing and testing
Per-use
aishitty
Featherless AI
Free OpenAI-compatible endpoint for open models
New
Free / aishitty
RunPod
GPU cloud compute
Per-use
aishitty
Together AI
Model/API/GPU-style compute
Per-use/credits
aishitty
Baseten
GPU/H100 credits and model hosting experiments
Testing
Credits / aishitty
OpenAI API
API access for app/script integration
Controlled
API spend
Anthropic API
API access for Claude workflows if needed
Controlled
API spend
Google AI Studio / Vertex
Gemini/model tooling and experiments
Active
Google ecosystem
(Source:
)
6. TIER 2 — DEV & ORCHESTRATION
Tool / Service
Role
Status
VS Code
Main IDE
Daily
Cursor
AI IDE
Active
Cline
Local AI-assisted IDE interface
Active
Docker
Containerization
Daily
Docker Compose
Multi-container local services
Daily
Git
Version control
Daily
GitHub
Repos, org, canon, issue tracking
Daily
GitHub Actions
CI/CD and automations
Active
n8n
Workflow automation, once shape is clear
Running / paused strategically
Node-RED
Local flow wiring and event routing
Available
Make
Visual automation and bridge workflows
Active
Zapier
Bridge automation
Available / limit use
Latenode
Automation experiments
Available
Buildship
App/workflow build experiments
Available
Agent Zero
Local execution hands
In AnythingLLM
MCP Servers
Protocol tool layer
Wired / active
Open WebUI
Reception-desk API interface for models/agents
Available
Hermes WebUI
Control-room native interface for Hermes-style agents
Available / evaluate
Codex
Coding/scaffold/build agent
Active
Gemini CLI
CLI coding/model workflow
Active / evaluate
OpenCode
Free coding-assistant alternative
Evaluate
Warp Agents
Terminal/agent workflow
Watchlist
Linear
Issue tracking / product management
Active
Figma
UI/design collaboration and mockups
Free/access
(Source:
)
7. DATABASE / MEMORY / KNOWLEDGE
Tool / Service
Role
Canon Rule
Markdown
Canonical portable source
Governs
Obsidian
Human graph and local navigation
UI over markdown
Dolt
Versioned structured truth
Stores rows/history
LanceDB
Vector retrieval
Finds context
Chroma DB
Vector retrieval
Workspace RAG
SQLite
Embedded state/caches
Local ledger
Supabase
Product database/auth/backend
App data
Firebase
Rapid prototypes, dashboards, lightweight apps
App/backend
Google Drive / Workspace
Source packaging and sync
Storage, not canon
GitHub
Repo and versioned source
Durable code/spec store
Notion
Dashboard/template/client surface
Not brain
OB1 / Open Brain
Personal AI memory infrastructure using Supabase/pgvector/MCP-style access
Evaluate for LACES_CASES
pgvector
Postgres vector extension
App/memory layer
Supabase Edge Functions
AI gateway / MCP-like endpoint layer
App/memory routing
(Source:
)
8. INGESTION / EXTRACTION / CONTEXT ENGINEERING
Tool / Protocol
Role
ShittyChunk
Extract, compress, route messy long input
Mudroom
Dirty staging area before canon
Great Ingest
Archive rescue and memory construction
YANK
Identity-boundary protocol: You Are Not Kevin
STEM
Portable identity/context files
Jaceon
JSON Context Engineered payload compression
Context Engineering
Ruthless optimization of context before model use
GSD Framework
Spec-driven context isolation and verification loop
MarkItDown
Convert files/docs to Markdown
Bookmarks to CSV
Export browser bookmarks/history into structured files
Whisper
Transcription
WhisperFlow / Wispr Flow
Voice to text / dictation
ExifTool
Photo metadata extraction/writing
Pillow
Python imaging library for thumbnailing/processing
Graphify
Folder/concept mapping
OpenSandbox
Secure runtime cage for agent-generated code
(Source:
)
9. CREATIVE / PHOTOGRAPHY / MEDIA
Tool / Service
Role
Status
Lightroom Classic
RAW processing, catalogs, archive work
Primary
Photoshop
Retouching, compositing, image correction
Primary
Adobe Creative Cloud
Creative production suite
Primary
Capture One
Tethered shooting / studio workflow
Studio
Pixieset
Client delivery
Active
Pic-Time
Client delivery
Active
Canva Pro
Design and quick assets
Active
Figma
UI and design systems
Active/free
Runway
AI video generation
Pay-go
Kling
AI video generation
Pay-go
Luma
AI video generation
Pay-go
Veo
AI video generation
Active/Google ecosystem
HeyGen
Avatar/video generation
Available
Hailuo
Video/audio generation
Active
OpenArt
Image generation
Active
Imagine.art
Image generation
Active
Seedance / Seedream
Video/image AI
Active
ElevenLabs
TTS and voice cloning
Active
Speechify
Voice/listening
Available
Suno
Music generation
Pay-go
Udio
Music generation
Pay-go
(Source:
)
10. BUSINESS / SALES / STORAGE
Tool / Service
Role
Status
Google Workspace — aishitty.com
Primary email, Drive, Calendar
Primary
Google Workspace — programmingnyc
Legacy account / cleanup
Consolidating
reachkane Gmail
Personal/billing account
Active
Hostinger
Hosting/site builder
Active
IONOS
Hosting/domains
Active
Mosaic
Site builder/hosting
Active
WordPress
Main site wrapper / publishing
Active
Cloudflare
DNS/CDN/security
Active
Vercel
Deploy/hosting
Active/free tier
Netlify
Deploy/hosting
Active/free tier
Railway
Deploy/hosting
Active/free tier
Dropbox
Large file transfer/backup
Active / review limit
Backblaze B2
Cold storage/offsite backup
Active
HoneyBook
CRM/contracts/invoicing
Evaluating
Dubsado
CRM/contracts/invoicing
Evaluating
HighLevel
CRM/automation
Trial/evaluate
WHOP
Community/product sales
Evaluate
Skool
Community/courses
Evaluate
Gumroad
Digital product sales
Active target
Shopify
Merch/ecommerce
Active target
Etsy
Merch/photo/product sales
Active target
HubSpot
CRM/marketing
Evaluate
SEMrush
SEO research
Available/evaluate
(Source:
)
11. SOCIAL / PLATFORMS / COMMUNITIES
Platform / Group
Role
YouTube
Tutorials, tool reviews, channel content
TikTok
Short-form content
Instagram
Photography, portfolio, short content
X / Twitter
AI/tech discourse
LinkedIn
Professional network and B2B credibility
Facebook
Social, groups, recovery, local
BlueSky
Social presence
Reddit
Community research
Discord
Dev communities, AI communities
GitHub — shitty-shit org
Code repos and canon
Behance
Photo/design portfolio
500px
Photo portfolio/backup
Flickr
Photo backup/archive
Medium
Long-form writing
Substack
Newsletter
Patreon
Membership/tips, inactive
Ko-fi
Tips, inactive
Buy Me Coffee
Tips, inactive
DEV Community
Developer digest/community
Kimchi Team
MiniMax/Kimchi coding lane
Babel Audio
Audio AI / collection
DataForce
Paid speech collection projects
User Interviews
Research study opportunities
Focus Group
Paid study opportunities
Model Mayhem
Photography/model network
AWS events
Cloud learning/networking
Coinbase / Base
Web3 experiments/watch
Firstrade / Moomoo
Trading/investing learning/watch
TurboVote
Voting reminders
Bloomberg / NewsBreak / The Essential
News/alerts
(Source:
)
12. EDUCATION / LEARNING
Resource
Focus
Status
KodeKloud
Kubernetes, DevOps, Linux
Decide/use if valuable
Anaconda / Pave
Python data science platform
Verify/use as needed
Baseten H100 credits
GPU compute for Proxy-Sweep tests
Test
Coursera
Online courses
Available
edX
Online courses
Available
Udemy
Courses
Available
Pluralsight
Tech skills
Inactive/evaluate
Frontend Masters
Tech skills
Inactive/evaluate
Think Scale AI
Claude AI resources
Paid/evaluate
YouTube technical content
Tutorials/research
Daily
AI research papers/docs
LLMs, agents, architecture
Daily
Perplexity CE brief
Intelligence digest
Daily
Ecoversity
Herbalism/health learning
Active/personal
DataCamp
AI/coding skills
Available
Khan Academy
K-12/math/practice
Available if needed
(Source:
)
13. REVIEW / CANCEL / WATCHLIST
These are not core until proven. | Tool / Service | Role | Action | | :--- | :--- | :--- | | Disney+ | Streaming | Fix/cancel later | | Firecrawl | Web scraping | Reply/archive/evaluate | | Atlassian / Confluence / Jira | Wiki/project management | Trial only if useful | | NinjaTools Expert | AI bundle | Review inactive annual | | Genspark | AI research platform | Payment/watch | | Google One | Storage expansion | Payment/watch | | Voice Recorder Pro | Mobile recording | Payment/watch | | Venice.ai | AI platform | Watchlist | | Neurapix | AI photo workflow | Watchlist | | EntryKeyID | Auth/security | Watchlist | | Dezyred | VR/social? | Watchlist | (Source:
)
14. DEFAULT AGENT LOADOUTS
Executive Strategy Agent
Load: me.md, projectstack.md, biz.md, latest decisions, relevant project stems
Use for: priorities, monetization, strategy, offers, sequencing
Tool Routing Agent
Load: me.md, toolstack.md, relevant tool cards, active stack snapshot
Use for: choose tools, reduce token cost, assign tasks, recommend automation, prevent subscription sprawl
Ingestion Agent
Load: me.md, toolstack.md, ShittyChunk spec, Mudroom rules, project stems
Use for: parse raw input, detect projects, route chunks, create receipts, produce canon update candidates
Coding / Repo Agent
Load: me.md, toolstack.md, project spec, .planning/, file tree, current issue/task
Use for: code, scaffold, scripts, schemas, receipts
Rule: Coding agents must report what changed
PRD Panel Agent
Load: me.md, toolstack.md, projectstack.md, target project section, latest related notes
Use for: PRDs, critique, implementation plans, schema proposals, monetization paths
Panel roles:
Model A = structure
Model B = critique
Model C = compression
Model D = monetization
Model E = technical architecture
Model F = content/product strategy
Model G = risk / cleanup / anti-bloat
15. TOOLSTACK UPDATE RULE
Update toolstack.md only when:
a tool becomes active
a tool is retired
routing logic changes
a new database/harness becomes canonical
a workflow becomes real enough to automate
a cost rule changes
a tool becomes part of a sellable product or service
Do not update for every random tool Kevin sees. Random tools go to: tool inbox, harness watchlist, affiliate watchlist, content idea list, parked research note
.
16. TOOL RECEIPT FORMAT
(Header reference mapped but empty structurally in the source)
17. STACK MOTTO
The stack is not the apps. The stack is the routing logic that turns chaos into shipped work
.
Saved responses are view only
NotebookLM can be inaccurate; please double check its responses.