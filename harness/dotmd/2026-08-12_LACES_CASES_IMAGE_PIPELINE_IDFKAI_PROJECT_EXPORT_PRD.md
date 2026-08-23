# Project Export & PRD — LACES_CASES / Image Pipeline / IDFKAI

> **Source:** Cuey shared comparison — https://cuey.io/share/dZr2TTItD3
> **Exported:** 2026-08-12
> **Prompt:** "I've been talking to you in this conversation for a long time and you're going to start
> getting context rot soon. So why don't you export as complete a project summary as you can for the
> different projects we talked about in here. And if you can do any PRD work on any one of them, do it."
> **Models compared:** Claude Sonnet 5 Think · Claude Opus 5 Think · ChatGPT
> **Note:** The body below is the most complete of the three answers (ChatGPT). The Sonnet and Opus
> variants remain retrievable from the share link above and can be folded in when LACES_CASES
> ingestion exists. This file is the seed document the LACES_CASES v0.7 acceptance test says to ingest first.

---

# LACES_CASES / Image Pipeline / IDFKAI — Project Export and PRD Snapshot

**Purpose:** Preserve the current project state before context rot and provide a clean handoff for future conversations, agents, project files, or local ingestion.

**Core operating rule:** Build the **70% version** that works, persists, and can be demonstrated. Do not delay deployment while designing the perfect future system.

**Portfolio objective:** Create something that remembers Kevin and somewhere public to discuss what is being built.

## 1. Executive Summary

Three equal-priority projects are moving in parallel. They intersect, but they should not be allowed to collapse into one giant, unbuildable project.

1. **LACES_CASES:** A persistent, dynamic AI memory system in which agents—not Kevin—perform the clerical organization work.

2. **Image Pipeline:** A large-scale system for identifying, analyzing, deduplicating, tagging, and organizing hundreds of thousands or potentially millions of photographs. Its structured outputs will eventually feed LACES_CASES.

3. **IDFKAI:** The public website, publishing surface, brand, and content system used to discuss the projects, evaluate emerging AI harnesses, attract feedback, and advocate for the underlying ideas.

The immediate win condition is not perfection. It is:

- **LACES_CASES 0.7 works and survives a reboot.**
- **IDFKAI 0.7 is publicly accessible and can publish content.**
- **The build-and-publish feedback loop begins.**

## 2. Shared Strategy: The 70% Rule

The projects currently need **proof of existence**, not architectural perfection.

### Build Now

- Persistent memory that works across sessions.
- A dedicated internal drive holding the data and application state.
- Basic document ingestion and retrieval.
- Access to the same memory from more than one agent or model.
- A public website with enough structure to publish.
- Initial social platforms for distributing ideas and build reports.
- Documentation showing what works, what failed, and what is still experimental.

### Do Not Wait For

- A perfect knowledge graph.
- Fully autonomous agents.
- A final OKF schema.
- Complete image-archive ingestion.
- Elaborate permissions and multi-user administration.
- A polished dashboard for every service.
- A perfect brand, website, or content strategy.
- Every possible cloud/local integration.

### Working Loop

```text
BUILD SOMETHING
      ↓
DOCUMENT WHAT HAPPENED
      ↓
LACES_CASES RETAINS IT
      ↓
TURN THE EXPERIENCE INTO CONTENT
      ↓
IDFKAI PUBLISHES IT
      ↓
SOCIAL PLATFORMS DISTRIBUTE IT
      ↓
FEEDBACK / COLLABORATORS / USERS
      ↓
IMPROVE THE BUILD
```

The loop is more valuable now than another month of speculative architecture.

## 3. Portfolio Boundaries

### Track 1 — LACES_CASES

- Persistent dynamic memory.
- Canonical knowledge.
- Document ingestion and retrieval.
- Agent clerical work.
- Markdown and structured metadata.
- Semantic indexing.
- Cloud/local harness architecture.
- Infrastructure required to operate the memory system.

### Track 2 — Image Pipeline

- Image repository inventory.
- File identity and hashing.
- Duplicate and similarity detection.
- EXIF/IPTC and other metadata.
- Visual tagging and embeddings.
- People, places, events, clients, licensing, and provenance.
- Structured output that eventually enters LACES_CASES.

### Track 3 — IDFKAI

- Relume-assisted site architecture.
- Website implementation and staging.
- Branding and positioning.
- Publishing and content operations.
- Social-platform presence.
- AI harness reviews, comparisons, and "smackdowns."
- Public discussion of persistent memory, agent systems, and the build process.

**Boundary rule:** When working inside one track, record dependencies on the others without trying to solve all three simultaneously.

# Project 1: LACES_CASES

## 4. LACES_CASES Project Summary

LACES_CASES is an internal harness architecture designed as a middle path between local AI sovereignty and cloud AI reasoning power.

Its working architectural description is:

> **A command-governed, tool-connected, sandboxed harness system operating across cloud and local environments as a cost-aware agent operating system.**

The immediate project is narrower than that full vision: **establish persistent cross-agent document memory on the Linux machine and dedicated internal drive.**

The user experience should be simple: Kevin tells the system something once, and the system can find, update, connect, and use it later. Kevin should not become the permanent librarian.

## 5. LACES_CASES Product Thesis

### Problem

AI conversations, generated documents, tool outputs, and decisions are scattered across many online platforms, hundreds of chats, and numerous local and cloud applications. Attempts to organize them manually often create an even larger artifact graveyard.

AI agents also lose context between sessions, forcing Kevin to repeatedly reconstruct projects and explain prior decisions.

### Thesis

A useful AI memory system does not need to understand everything perfectly. It needs to retain information durably, preserve provenance, make the information retrievable, and allow agents to maintain the filing structure.

### Hegelian Design Principle

LACES_CASES follows Kevin's thesis-antithesis-synthesis methodology:

- **Thesis:** Fully local systems provide sovereignty, privacy, and direct ownership.
- **Antithesis:** Cloud systems provide stronger reasoning, broader knowledge, and fewer local hardware constraints.
- **Synthesis:** A governed harness uses cloud and local systems for the work each performs best while maintaining local canonical memory and cost awareness.

## 6. LACES_CASES 0.7 PRD

### Product Goal

Deliver a working persistent-memory system that stores canonical knowledge on the dedicated internal drive, indexes it for retrieval, and makes the same knowledge available to multiple agents or models.

### Primary User

- **Kevin:** Technical communicator, project owner, content creator, and nontraditional system builder who needs the architecture to remain understandable without requiring formal software-engineering training.

### Supporting Actors

- Claude, Codex, Qwen, and other AI agents or models.
- AnythingLLM or another retrieval interface.
- n8n workflows.
- Cuey as a command and prompt staging shelf.
- DoppelBrain as a cloud-side retrieval and synthesis scout.
- Future MCP, API, or harness clients.

### Primary User Story

Kevin supplies a document, conversation export, decision, or project note once. The system preserves the original source, creates a normalized knowledge record, indexes it, and allows different agents to retrieve the same information later—even after services or the host machine restart.

## 7. LACES_CASES 0.7 Scope

### Required for Version 0.7

- Data and application state reside on the dedicated internal drive.
- Docker services retain their state across container and host restarts.
- A document can be ingested without manually rebuilding it inside every AI application.
- The original source or a reliable reference to it is retained.
- Canonical knowledge remains inspectable in a portable format.
- Basic metadata and provenance are attached.
- The document is indexed in LanceDB or the selected semantic store.
- At least two different agents or models can retrieve the same seeded information.
- Updated information can replace or supersede an earlier record.
- A minimal backup can be created.
- The complete memory survives a reboot and remains queryable.

### Preferred but Not Blocking

- Automated folder creation.
- Automatic project classification.
- Basic duplicate detection.
- Basic stale-document detection.
- Automatic index or table-of-contents generation.
- n8n-assisted ingestion.
- LiteLLM token and model accounting.
- Obsidian-compatible links and front matter.

## 8. Proposed LACES_CASES 0.7 Architecture

```text
KEVIN
  │
  │ conversations / exports / documents / decisions
  ▼
INGESTION
  │
  ├── preserve source
  ├── normalize text
  ├── create stable identity
  ├── extract basic metadata
  ├── classify project/type
  ├── add provenance
  └── check obvious duplicates
          │
          ▼
CANONICAL KNOWLEDGE
Markdown + structured metadata + source references
          │
          ├─────────────────────┐
          ▼                     ▼
Agent-maintained files       LanceDB
and project indexes          semantic retrieval
          │                     │
          └──────────┬──────────┘
                     ▼
             SHARED MEMORY LAYER
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Claude      Codex      Qwen/etc.
```

The main tradeoff is that Markdown plus a vector index is less sophisticated than a full knowledge graph, but it is easier to inspect, repair, export, and get running. That makes it the best 70% default.

## 9. Infrastructure Plan

### Existing Foundation

- Linux installation is available.
- Docker is installed.
- A dedicated extra internal drive is available for project data.
- n8n is installed or available but has not yet been put into active use.

### Minimum Service Stack

- **Portainer:** Basic Docker/container administration.
- **AnythingLLM:** Initial document interface, workspace, and retrieval environment.
- **LanceDB:** Persistent semantic/vector index.
- **n8n:** Ingestion and workflow orchestration.
- **LiteLLM:** Common model gateway and token/cost accounting.

### Secondary Services

- **Caddy:** Reverse proxy and HTTPS when a service needs network or public access.
- **Homepage:** Optional service dashboard.
- **MkDocs or another internal wiki:** Human-readable browsing layer.
- **Gitea:** Optional versioning and local repository hosting.
- **Website staging services:** Added when IDFKAI deployment requires them.

Secondary services must not delay the persistent-memory proof.

## 10. Recommended Drive Layout

The exact mount point remains to be chosen. The following is a proposed understandable layout, not an existing confirmed directory structure.

```text
/mnt/laces_cases/
├── canonical/
│   ├── projects/
│   ├── people/
│   ├── decisions/
│   ├── references/
│   └── indexes/
├── sources/
│   ├── chat_exports/
│   ├── documents/
│   ├── web_exports/
│   └── media/
├── databases/
│   └── lancedb/
├── appdata/
│   ├── anythingllm/
│   ├── n8n/
│   ├── litellm/
│   └── portainer/
├── processing/
│   ├── inbox/
│   ├── staged/
│   ├── failed/
│   └── completed/
├── exports/
├── logs/
└── backups/
```

This layout separates original sources, canonical knowledge, databases, application state, and backups. The separation makes failures easier to understand and reduces application lock-in.

## 11. Functional Requirements

- **FR-1 — Ingest:** The system shall accept at least Markdown, plain text, PDF, and copied chat content.
- **FR-2 — Preserve:** The system shall retain the original file or a durable source reference.
- **FR-3 — Identify:** Every canonical item shall receive a stable identifier.
- **FR-4 — Normalize:** The system shall produce readable normalized text suitable for indexing.
- **FR-5 — Describe:** The system shall attach basic metadata and provenance.
- **FR-6 — Classify:** The system shall assign a project and document type when confidence is sufficient.
- **FR-7 — Index:** Canonical content shall be indexed in the shared retrieval store.
- **FR-8 — Retrieve:** Multiple agents shall be able to retrieve the same stored knowledge.
- **FR-9 — Update:** Newer information shall be able to supersede an old assertion without silently destroying history.
- **FR-10 — Persist:** Records and indexes shall survive service and host restarts.
- **FR-11 — Inspect:** Kevin shall be able to inspect the canonical files without a proprietary application.
- **FR-12 — Export:** Canonical knowledge shall remain portable to another retrieval system.
- **FR-13 — Back Up:** The system shall support a basic backup of canonical data and required database state.
- **FR-14 — Log Failures:** Failed ingestion shall not silently disappear.

## 12. Minimum Knowledge Record

The exact Google OKF schema and terminology still require verification. Version 0.7 should use a minimal internal record that can later be mapped to OKF rather than blocking deployment on schema perfection.

```yaml
id: stable-record-id
title: Human-readable title
project: LACES_CASES
type: decision | note | source | summary | requirement
status: active | superseded | archived
created_at: ISO-8601 timestamp
updated_at: ISO-8601 timestamp
source_type: chat | file | web | agent | manual
source_reference: original file, URL, or conversation reference
provenance:
  author: Kevin or originating agent/source
  ingested_by: workflow or agent
tags:
  - persistent-memory
  - infrastructure
relationships:
  - type: relates_to
    target: another-record-id
supersedes: optional-record-id
confidence: confirmed | inferred | proposed
```

The important fields for the first version are **identity, project, type, provenance, status, timestamps, and source reference**. Complex ontology work can follow later.

## 13. Agent Clerk Responsibilities

The agents are intended to perform the clerical work. Kevin should not have to spend his time manually moving Markdown files around.

### Version 0.7 Clerk Duties

- Create a canonical record from an incoming source.
- Suggest a title, project, document type, and tags.
- Retain provenance.
- Place the record in a predictable location.
- Update a project index.
- Flag obvious duplicates or contradictions.
- Submit the record for semantic indexing.
- Report failures for human review.

### Later Clerk Duties

- Reconcile competing versions.
- Detect stale project summaries.
- Generate relationship links.
- Maintain tables of contents.
- Propose archival actions.
- Extract structured decisions and requirements from long conversations.
- Route records into Dolt, LanceDB, Obsidian-compatible files, or other canonical stores.

## 14. Obsidian Position

Obsidian is not intended to become Kevin's required working environment.

An Obsidian-compatible vault can be generated because Markdown, front matter, and links are portable and useful. However, Obsidian should remain an **optional compatibility and browsing layer**, not a foundational dependency.

If Obsidian is replaced later, the canonical Markdown and metadata should survive unchanged.

## 15. Cuey and DoppelBrain Roles

### Cuey

Cuey serves as the command shelf for repeatable verbs and prompts such as **YANK, EXTRACT, and COMPRESS**.

The key emerging use case is to store extraction prompts in Cuey, use them against many cloud agents and platforms, and process the exported results before local ingestion.

### DoppelBrain

DoppelBrain acts as a cloud memory scout for retrieval, comparison, and synthesis across online artifacts.

### Canonical Boundary

Neither Cuey nor DoppelBrain is the permanent canonical store. Their job is to identify, retrieve, synthesize, compress, and route useful material toward durable project memory.

```text
ONLINE ARTIFACT GRAVEYARD
          ↓
Cuey commands / YANK prompts
          ↓
DoppelBrain retrieval and synthesis
          ↓
ShittyChunk or other parsing/compression
          ↓
LACES_CASES ingestion
          ↓
LOCAL CANONICAL MEMORY
```

This cloud-side pre-local processing stage prevents the local computer from having to ingest every raw artifact before deciding what matters.

## 16. LACES_CASES 0.7 Acceptance Test

The first milestone is complete when the following test passes:

1. Create a small test document containing a unique project fact and phrase.
2. Place it in the ingestion inbox.
3. Preserve the original source.
4. Produce a canonical Markdown record with basic metadata.
5. Index it in the shared semantic store.
6. Retrieve the correct fact through Agent or Model A.
7. Retrieve the same fact through Agent or Model B.
8. Shut down and restart the containers.
9. Restart the host machine.
10. Retrieve the fact again.
11. Update or supersede the record.
12. Reindex it and retrieve the updated fact.
13. Inspect the canonical file directly on the internal drive.
14. Create a basic backup of the canonical data and retrieval state.

If this passes, LACES_CASES has crossed from an idea into a demonstrable persistent-memory system.

## 17. LACES_CASES Non-Goals for Version 0.7

- Solving the complete image archive.
- Building a universal ontology.
- Creating a perfect Google OKF implementation.
- Fully autonomous knowledge reconciliation.
- Supporting every AI agent and harness.
- Building the final user interface.
- Ingesting every historical chat immediately.
- Creating a production SaaS platform.
- Making Obsidian mandatory.
- Building an elaborate knowledge graph before basic retrieval works.

## 18. LACES_CASES Risks and Controls

- **Scope expansion:** Every service and metadata idea can become a subproject. **Control:** Only install what the acceptance test requires.
- **False shared memory:** Different AnythingLLM workspaces may use isolated collections. **Control:** Explicitly verify that both test agents query the same collection or retrieval endpoint.
- **Container persistence errors:** Data may accidentally remain inside disposable containers. **Control:** Bind all important volumes to the dedicated internal drive and verify paths.
- **Vector database treated as canon:** Embeddings are indexes, not the authoritative records. **Control:** Keep canonical source and normalized files separately.
- **Automation before understanding:** n8n can hide a badly understood workflow. **Control:** Prove one ingestion manually before automating it.
- **Schema paralysis:** OKF work could delay deployment. **Control:** Begin with the minimum record and map it later.
- **Artifact flood:** Importing everything could recreate the graveyard locally. **Control:** Stage, synthesize, classify, and selectively promote artifacts into canon.
- **No recovery path:** A single-drive system can fail. **Control:** Establish a second backup target after the first persistence proof.

# Project 2: Image Pipeline

## 19. Image Pipeline Project Summary

The Image Pipeline addresses Kevin's very large professional photography archive. The archive may include hundreds of thousands or potentially millions of image records accumulated across a long photography career.

The project needs to determine what files exist, identify duplicates and related versions, extract existing metadata, create useful visual metadata, and establish relationships among people, places, events, clients, licensing information, and provenance.

The image-specific technical decisions belong in the dedicated Image Pipeline project or conversation. LACES_CASES only needs to guarantee that the resulting structured knowledge has somewhere durable and queryable to go.

## 20. Image Pipeline Mini-PRD

### Product Goal

Create a scalable and restartable pipeline that inventories the archive, establishes file identity, extracts metadata, detects duplicates or similarities, and emits records suitable for LACES_CASES ingestion.

### Initial Functional Scope

- Enumerate storage locations and files.
- Record file paths, sizes, dates, formats, and basic integrity information.
- Generate cryptographic hashes for exact identity.
- Evaluate perceptual hashes or embeddings for visual similarity.
- Extract EXIF, IPTC, XMP, and available sidecar metadata.
- Preserve original file locations and provenance.
- Identify exact duplicates without deleting anything automatically.
- Group likely derivatives, edits, exports, or resized copies.
- Add visual tags where useful.
- Produce structured records that can feed the shared knowledge system.
- Resume processing after interruption without starting over.

### Proposed Data Flow

```text
IMAGE REPOSITORIES
        ↓
Inventory and file identity
        ↓
Metadata extraction
        ↓
Exact duplicate detection
        ↓
Visual similarity / derivative grouping
        ↓
Optional AI tagging and embeddings
        ↓
Structured image records
        ↓
LACES_CASES / OKF-compatible knowledge
        ↓
Shared persistent retrieval
```

### Image Pipeline 0.7 Acceptance Condition

A representative pilot folder can be scanned repeatedly without corrupting data, exact duplicates can be identified, metadata is extracted, processing can resume after interruption, and structured results can be imported into LACES_CASES.

### Image Pipeline Non-Goals for the Pilot

- Processing the entire archive before validating the approach.
- Automatically deleting duplicate images.
- Perfect face, event, or location recognition.
- Reorganizing all original files immediately.
- Solving licensing and rights records in one pass.
- Requiring the LACES_CASES document MVP to solve image-specific engineering.

# Project 3: IDFKAI

## 21. IDFKAI Project Summary

IDFKAI is the public platform for discussing the work, publishing experiments, comparing emerging AI harnesses, developing the brand, and attracting feedback or collaborators.

Its immediate purpose is not to look like a finished company. Its purpose is to provide Kevin with a public place to stand while the systems are being built.

The build itself is content. LACES_CASES does not need to be finished before discussing the problem, design decisions, failures, and working demonstrations.

## 22. IDFKAI 0.7 Mini-PRD

### Product Goal

Launch a credible but lightweight public website and distribution presence that can publish build logs, ideas, demonstrations, and AI harness comparisons.

### Core Audience

- People frustrated by AI memory loss and fragmented conversations.
- Builders evaluating local and cloud AI harnesses.
- Nontraditional technical users trying to assemble understandable systems.
- AI creators, tool developers, and potential collaborators.
- Photographers and archive owners interested in AI-assisted knowledge systems.

### Minimum Website Structure

- **Home:** Clear statement of what IDFKAI is exploring.
- **Projects:** LACES_CASES, Image Pipeline, and related experiments.
- **Build Log:** Short posts documenting progress, failures, and decisions.
- **Harness Smackdowns:** Comparisons of Hermes, AionUi, OpenHuman, Skales, and emerging alternatives.
- **About:** Kevin's relevant background and perspective.
- **Contact or Follow:** Clear path to social channels, email, or newsletter.

### Minimum Publishing Requirements

- Public URL with HTTPS.
- Mobile-readable layout.
- Simple publishing workflow Kevin can actually use.
- At least one published build-log article.
- A project page for LACES_CASES.
- A method for sharing posts to social platforms.
- Basic analytics or another way to observe whether anyone is finding the work.

### Role of Relume

Relume is being used or considered for information architecture, sitemap generation, wireframing, and initial website structure. It should accelerate the site launch rather than turn the site into another long design project.

### IDFKAI 0.7 Acceptance Condition

The site is publicly reachable, explains the project direction, contains at least one real project page and one real article, and gives Kevin a repeatable way to publish the next update.

## 23. Initial Content Pillars

- **Persistent AI Memory:** Why repeating yourself to agents is unacceptable.
- **Build in Public:** What worked, what failed, and what turned out to be bullshit.
- **Harness Smackdowns:** Direct comparisons of new agent harnesses.
- **Local vs. Cloud:** The false binary and the LACES_CASES middle path.
- **Artifact Graveyard:** Why AI outputs accumulate faster than people can organize them.
- **Agents as Clerks:** Why humans should not spend their lives filing Markdown for machines.
- **TOKENS=$:** Prompt hygiene, input/output compression, and AI cost reduction.
- **Image Archive:** Applying AI memory architecture to a massive professional photography archive.
- **Nonprogrammer System Building:** Creating understandable AI infrastructure without pretending to be a traditional software engineer.
- **Serious Tool, Stupid Name:** The ShittyShit contradiction as an intentional brand dialectic.

## 24. Seed Post Ideas

- "I'm tired of explaining myself repeatedly to AI, so I'm building a persistent memory layer."
- "Why should humans organize Markdown files for AI agents?"
- "The AI artifact graveyard: hundreds of conversations and nowhere canonical to put them."
- "The 70% rule: persistent memory does not need to be perfect to become useful."
- "Local versus cloud AI is the wrong argument."
- "We installed Docker. That is not the accomplishment."
- "Can two different AI agents remember the same fact after a server reboot?"
- "Why Obsidian is an output format, not my new full-time job."
- "Testing the newest AI harnesses so you don't have to pretend every launch is revolutionary."
- "Documents are the test. Two million photographs are the real problem."

# Cross-Project System

## 25. How the Three Projects Intersect

```text
LACES_CASES
Persistent memory and canonical knowledge
        ▲
        │ structured records
        │
IMAGE PIPELINE
Large-scale image analysis and metadata
        │
        │ build reports / discoveries
        ▼
IDFKAI
Publishing, demonstrations, harness reviews,
social distribution, and community feedback
        │
        │ feedback / tools / collaborators
        └──────────────────────────────► LACES_CASES
```

LACES_CASES stores and retrieves project knowledge. The Image Pipeline supplies a difficult real-world data problem. IDFKAI turns the work into public material and brings external feedback into the next development cycle.

## 26. Confirmed Strategic Decisions

- The **70% version** is the current target.
- Persistent memory is the first LACES_CASES proof.
- The dedicated internal drive will hold the important data and persistent application state.
- Agents should perform the filing and maintenance work.
- Canonical knowledge must remain portable and inspectable.
- Obsidian is optional compatibility, not the foundation.
- LanceDB is an index and retrieval component, not the only canonical record.
- Documents are the initial proving ground.
- The Image Pipeline remains a separate technical track.
- IDFKAI must launch before every project is finished.
- Building and publishing should proceed in parallel.
- LACES_CASES remains an internal harness architecture rather than being forced to act as the public vehicle for everything.
- Public content should include practical testing of emerging harnesses.
- Cuey and DoppelBrain are processing and retrieval layers, not final canonical storage.
- Cost awareness and token reduction remain architectural concerns through TOKENS=$.

## 27. Open Decisions

These are unresolved questions, not blockers for defining the projects.

### LACES_CASES

- Exact device, filesystem, mount point, and capacity of the dedicated internal drive.
- Backup destination and schedule.
- Whether AnythingLLM provides the cleanest shared-memory interface or is only an initial test harness.
- Exact shared-collection design for cross-agent retrieval.
- Which models or agent clients will perform the first two-agent acceptance test.
- Exact Google OKF specification and the minimum useful mapping.
- Whether canonical records remain file-first or later move into Dolt with Markdown exports.
- How agents authenticate to the memory layer.
- Which ingestion step is manual before n8n automation begins.

### Image Pipeline

- Number, location, format, and condition of source repositories.
- Pilot dataset size.
- Hashing, perceptual similarity, and embedding tools.
- Database used for file and relationship records.
- Policy for derivatives, sidecars, RAW/JPEG pairs, and exported edits.
- Compute and storage requirements for full-scale processing.

### IDFKAI

- Final domain and brand relationship among IDFKAI, AISHITTY, and ShittyShit.
- Final website stack and hosting location.
- CMS or file-based publishing workflow.
- Initial social platforms and account names.
- Newsletter or email-capture tool.
- Whether the site is hosted on the local server, externally, or through a hybrid staging/deployment workflow.

## 28. Immediate Execution Plan

### Workstream A — LACES_CASES 0.7

1. Identify and mount the dedicated internal drive.
2. Create the persistent directory structure.
3. Confirm Docker can read and write to it.
4. Deploy the minimum memory services with persistent volumes.
5. Manually ingest one representative document before automating anything.
6. Confirm the canonical source and normalized record are inspectable.
7. Index the document.
8. Connect two different agents or models to the shared collection.
9. Run the reboot and update acceptance test.
10. Create a basic backup.
11. Capture screenshots, architecture notes, failures, and results for publication.
12. Declare Version 0.7 complete instead of immediately redesigning it.

### Workstream B — IDFKAI 0.7

1. Use Relume to settle the minimum sitemap and page hierarchy.
2. Choose the fastest maintainable website stack.
3. Create the Home, Projects, Build Log, About, and Follow/Contact pages.
4. Publish the LACES_CASES project page.
5. Publish the first build-log post.
6. Establish the first social distribution account or accounts.
7. Share the working persistent-memory demonstration.
8. Continue improving the site in public.

### Workstream C — Image Pipeline Pilot

1. Select a representative but disposable or safely copied pilot folder.
2. Inventory the files without modifying them.
3. Extract basic metadata and exact hashes.
4. Test duplicate and similarity methods.
5. Define the minimum image record that LACES_CASES can accept.
6. Send a small result set into the shared memory system.
7. Use the pilot results to define the full Image Pipeline PRD.

## 29. Definition of the First Combined Win

The first combined milestone is achieved when:

- LACES_CASES remembers and retrieves a real project fact after a reboot.
- Two agents can retrieve that fact from shared memory.
- The underlying source and canonical record remain visible on the internal drive.
- IDFKAI is publicly online.
- A post explains or demonstrates what was built.
- The post can be distributed through at least one social platform.

At that point, Kevin no longer has only an idea. He has **a working artifact, a demonstration, a public platform, and a feedback loop**.

## 30. Continuity Prompt for the Next Agent or Conversation

```text
We are continuing three connected but separately managed projects:

1. LACES_CASES 0.7
Build a 70% persistent cross-agent memory system on a Linux/Docker
machine using a dedicated internal drive. Canonical knowledge should
remain portable and inspectable. LanceDB is an index, not the sole
canon. Agents are the clerks. Obsidian is optional compatibility.
The immediate acceptance test is ingest → retrieve through two agents
→ reboot → retrieve again → update → retrieve updated knowledge.

2. Image Pipeline
Develop a restartable system for inventorying, hashing, deduplicating,
extracting metadata from, and eventually tagging a very large
photography archive. Keep image-specific engineering separate from
the LACES_CASES document MVP. The structured output will eventually
feed LACES_CASES.

3. IDFKAI
Launch the public website and publishing system now, without waiting
for the other projects to be finished. Use it for build logs,
persistent-memory ideas, artifact-graveyard discussions, and practical
comparisons of emerging AI harnesses.

Operating rule:
Do not chase perfection. Use the 70% rule. The immediate objective is
something that remembers Kevin and somewhere public to talk about it.

When proposing next steps, identify which track each task belongs to,
state the primary tradeoff, and prevent scope from one track from
blocking the others.
```

## 31. Suggested Export Filename

`2026-08-12_LACES_CASES_IMAGE_PIPELINE_IDFKAI_PROJECT_EXPORT_PRD.md`
